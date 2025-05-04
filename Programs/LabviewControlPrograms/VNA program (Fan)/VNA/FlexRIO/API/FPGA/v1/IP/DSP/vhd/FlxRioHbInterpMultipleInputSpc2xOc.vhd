-------------------------------------------------------------------------------
--
-- File: FlxRioHbInterpMultipleInputSpc2xOc.vhd
-- Author: Stephen Dark
-- Original Project: VST 2.0
-- Date: 1 August 2014
--
-------------------------------------------------------------------------------
-- (c) 2014 Copyright National Instruments Corporation
-- All Rights Reserved
-- National Instruments Internal Information
-------------------------------------------------------------------------------
--
-- Purpose:  Creates a Halfband decimating filter that accepts multiple input
--           samples per clock cycle
--
--           kInputSamplesPerCycle - specifies the number of parallel samples input
--                                   on each Clk cycle.  Valid values are 1, 2, 4,
--                                   8, and 16.
--
--           kUseDsp48e1 - If kUseDsp48e1 is false, then the pre-adder is
--                         implemented in Slice logic and DSP48Es are used
--                         to implement each MAC.  If kUseDsp48e1 is true,
--                         then the pre-adder is implemented in the DSP48E1
--                         and DSP48E1s are used to implement each MAC.
--
--           kCyclesPerInput - This generic determines the "throughput" of the
--                             filter.  kCyclesPerInput must be one if
--                             kInputSamplesPerCycle is greater than one.  If
--                             kInputSamplesPerCycle is equal to one then
--                             kCyclesPerInput specifies how often new data
--                             can be pushed into the filter.  For example, if
--                             if kCyclesPerInput is set to two, then input
--                             valid can only assert every other SampleClk cycle.
--                             The number of MACs used is proportional to
--                             kCyclesPerInput.  Supported values for kCyclesPerInput
--                             are 1, 2, and 4.  Once you get to 4 only one
--                             MAC is used so there is no advantage to implement
--                             higher values.
--
--           Max Input Data Rate (samples/cycle)= kInputSamplesPerCycle / kCyclesPerInput
--
-------------------------------------------------------------------------------

library ieee, work;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;
  use work.FlxRioPkgNiUtilitiesDsp.all;
  use work.FlxRioPkgHbInterp.all;

entity FlxRioHbInterpMultipleInputSpc2xOc is
  generic(
    kInputSamplesPerCycle : integer range kMaxInputSpc downto kMinInputSpc;
    kCyclesPerInput       : integer range kMaxCyclesPerInput downto kMinCyclesPerInput;
    kUseDsp48e1           : boolean := true;
    kInterpolate          : boolean := false);
  port(
    SampleClk    : in std_logic;
    SampleClk2x  : in std_logic;
    sReset       : in boolean;
    sEnOutputFFs : in boolean;
    sInputValid  : in boolean;
    sDataIn      : in Signed18Array_t(kInputSamplesPerCycle-1 downto 0); -- S18.1
    sOutputValid : out boolean;
    sDataOut     : out Signed37Array_t(CalcOutputSamplesPerCycle(kInputSamplesPerCycle,kCyclesPerInput,kInterpolate)-1 downto 0));  -- S37.2
end FlxRioHbInterpMultipleInputSpc2xOc;

architecture RTL of FlxRioHbInterpMultipleInputSpc2xOc is

  constant kNumSingleFilters : integer := CalcNumSingleFilters(kInputSamplesPerCycle,kCyclesPerInput,kInterpolate);
  constant kOutputSpc : integer := CalcOutputSamplesPerCycle(kInputSamplesPerCycle,kCyclesPerInput,kInterpolate);

  signal ssCount: unsigned(0 downto 0);
  signal ssCycleZero : boolean;

  signal sResetPipe : boolean := true;
  signal sInputValidPipe : boolean := false;
  signal sDataInPipe : Signed18Array_t(kInputSamplesPerCycle-1 downto 0) := (others => (others => '0'));

  signal ssReset : boolean := true;
  signal ssInputValid : boolean := false;
  signal ssDataIn     : Signed18Array_t(kInputSamplesPerCycle-1 downto 0) := (others => (others => '0'));

  signal ssFilterDataOutValid : BooleanVector(kNumSingleFilters-1 downto 0);
  signal ssFilterDataOut      : Signed37Array_t(kNumSingleFilters-1 downto 0);

  signal ssDataOutValid : boolean := false;
  signal ssDataOut      : Signed37Array_t(kNumSingleFilters-1 downto 0) := (others => (others => '0'));

  constant kCenterTapPipeDelay : integer := kPipelineDelay-2; --remove two for output and input FFs
  constant kFilterDelay : integer := 14; --floor of (#filtertaps-1)/4 => floor((59-1)/4) => 14
  --replace with ceil(kCenterTap/InputSamplesPerCycle)+1 later
  constant kMaxCenterFilterDelay : integer := (kFilterDelay/kInputSamplesPerCycle) + 2;
  signal sDataValidPipeDelay : BooleanVector(kCenterTapPipeDelay downto 0) := (others => false);
  type CenterTapFilterDelay_t is array( natural range <> ) of Signed18Array_t(kMaxCenterFilterDelay-1 downto 0);
  type CenterTapPipelineDelay_t is array( natural range <> ) of Signed18Array_t(kCenterTapPipeDelay downto 0);
  signal sCenterTapPipeDelay : CenterTapPipelineDelay_t(kInputSamplesPerCycle-1 downto 0) := (others => (others => (others => '0')));
  signal sCenterTapFilterDelay : CenterTapFilterDelay_t(kInputSamplesPerCycle-1 downto 0) := (others => (others => (others => '0')));
  signal sCenterTap : Signed18Array_t(kInputSamplesPerCycle-1 downto 0);
  signal sDataOutPreExtend : Signed18Array_t(kInputSamplesPerCycle-1 downto 0);

  -- Make sure these do not get merged with other FFs into SRLs.  These need to be discrete FFs
  -- to meet timing between the SampleClk and SampleClk2x clock domains.
  attribute keep : string;
  attribute keep of sInputValidPipe: signal is "true";
  attribute keep of sDataInPipe: signal is "true";
  attribute keep of ssInputValid: signal is "true";
  attribute keep of ssDataIn: signal is "true";
  attribute keep of ssDataOutValid: signal is "true";
  attribute keep of ssDataOut: signal is "true";
  attribute keep of sDataOut: signal is "true";
  attribute keep of sOutputValid: signal is "true";

  --vhook_sigstart
  signal sOutputValidLcl: std_logic;
  --vhook_sigend

begin

  -- Create the Sync Counter
  --vhook_e FlxRioOverclockingSyncCounter
  --vhook_g kOverclockFactor kOverclockingFactor
  --vhook_g kCountMaxFanout 30
  --vhook_a aReset false
  --vhook_a BaseClk SampleClk
  --vhook_a bStart sEnOutputFFs
  --vhook_a OverClk SampleClk2x
  --vhook_a oCount ssCount
  --vhook_a oCountValid open
  --vhook_a oBaseClkEdgeNext open
  FlxRioOverclockingSyncCounterx: entity work.FlxRioOverclockingSyncCounter (RTL)
    generic map (
      kOverclockFactor => kOverclockingFactor,  --integer:=3
      kCountMaxFanout  => 30)                   --integer:=30
    port map (
      aReset           => false,         --in  boolean
      BaseClk          => SampleClk,     --in  std_logic
      bStart           => sEnOutputFFs,  --in  boolean:=true
      OverClk          => SampleClk2x,   --in  std_logic
      oCount           => ssCount,       --out unsigned(log2less1(kOverclockFactor):0):=(others=>'0')
      oCountValid      => open,          --out boolean
      oBaseClkEdgeNext => open);         --out boolean

  -- Select CycleZero
  -- Either cycle of ssCount could be used, but this cycle allows the final accumulator
  -- output to be sampled directly back to the 1x SampleClk domain
  -- If the pipeline delay in the SampleClk 2x domain changes, then this value may need
  -- to be changed.
  ssCycleZero  <= ssCount = "0";

  -- Pipeline the input data in the SampleClk domain to ensure that there is no logic
  -- between the SampleClk and SampleClk2x FFs.  This makes timing easier to meet.
  process(SampleClk)
  begin
    if rising_edge(SampleClk) then
      sResetPipe      <= sReset;
      sInputValidPipe <= sInputValid;
      sDataInPipe     <= sDataIn;
    end if;
  end process;

  -- Pipeline the input data in the SampleClk2x domain to ensure that there is no logic
  -- between the SampleClk and SampleClk2x FFs.  This makes timing easier to meet.
  -- This also acts as a double synchronizer that protects the rest of the logic in this
  -- IPIN from the asynchronous assertion of the LV FPGA diagram reset.
  process(SampleClk2x)
  begin
    if rising_edge(SampleClk2x) then
      ssReset      <= sResetPipe;
      ssInputValid <= sInputValidPipe and ssCycleZero;
      ssDataIn     <= sDataInPipe;
    end if;
  end process;


  -- Generate all of the filters
  GenSingleFilters:
  for I in 0 to kNumSingleFilters-1 generate
      --vhook_e FlxRioHbInterpSingleFilter2xOc
      --vhook_a kFilterIndex  I
      --vhook_a kInputSamplesPerCycle kInputSamplesPerCycle
      --vhook_a Clk SampleClk2x
      --vhook_a cReset ssReset
      --vhook_a cDataInValid ssInputValid
      --vhook_a cDataIn ssDataIn
      --vhook_a cDataOutValid ssFilterDataOutValid(I)
      --vhook_a cDataOut ssFilterDataOut(I)
      FlxRioHbInterpSingleFilter2xOcx: entity work.FlxRioHbInterpSingleFilter2xOc (RTL)
        generic map (
          kInputSamplesPerCycle => kInputSamplesPerCycle,  --integer range kMaxInputSpc:kMinInputSpc
          kCyclesPerInput       => kCyclesPerInput,        --integer range kMaxCyclesPerInput:kMinCyclesPerInput
          kUseDsp48e1           => kUseDsp48e1,            --boolean:=true
          kInterpolate          => kInterpolate,           --boolean:=false
          kFilterIndex          => I)                      --integer:=0
        port map (
          Clk           => SampleClk2x,              --in  std_logic
          cReset        => ssReset,                  --in  boolean
          cDataInValid  => ssInputValid,             --in  boolean
          cDataIn       => ssDataIn,                 --in  Signed18Array_t(kInputSamplesPerCycle-1:0)
          cDataOutValid => ssFilterDataOutValid(I),  --out boolean
          cDataOut      => ssFilterDataOut(I));      --out signed(36:0)
  end generate GenSingleFilters;

  -- Pipeline the output data in the SampleClk2x domain to ensure that there is no logic
  -- between the SampleClk and SampleClk2x FFs.  This makes timing easier to meet.
  process(SampleClk2x)
  begin
    if rising_edge(SampleClk2x) then
      ssDataOutValid <= ssFilterDataOutValid(0);
      ssDataOut <= ssFilterDataOut;
    end if;
  end process;

  -- Create the final FFs
  -- These FFs transfer the output data back to the SampleClk domain and prevent the data from
  -- changing in the LV FPGA diagram when the LV FPGA asynchronous reset de-asserts.

  --vhook_e FlxRioDFlopDsp OutValidFlop
  --vhook_a kResetVal '0'
  --vhook_a aReset false
  --vhook_a cEn sEnOutputFFs
  --vhook_a Clk SampleClk
  --vhook_a cD to_stdlogic(ssDataOutValid)
  --vhook_a cQ sOutputValidLcl
  OutValidFlop: entity work.FlxRioDFlopDsp (rtl)
    generic map (kResetVal => '0')  --std_logic:='0'
    port map (
      aReset => false,                        --in  boolean
      cEn    => sEnOutputFFs,                 --in  boolean
      Clk    => SampleClk,                    --in  std_logic
      cD     => to_stdlogic(ssDataOutValid),  --in  std_logic
      cQ     => sOutputValidLcl);             --out std_logic:=kResetVal

  sOutputValid <= to_boolean(sOutputValidLcl);


  --If we are interpolating and SPC is 2 or greater, we will be passing the input
  --data straight through interleaved with the filter outputs.  While we could have
  --implemented this functionality into the single filter implementation, this would
  --have used more FFs.  In the case that OutputSpc=1 or less, then we will only be
  --using the filtered outputs which is the same as the decimation use case below.
  FinalInterpolateFFs:
  if kInterpolate and kOutputSpc > 1 generate

    sDataValidPipeDelay(0) <= sInputValidPipe;
    process(SampleClk)
    begin
      if rising_edge(SampleClk) then
        sDataValidPipeDelay(kCenterTapPipeDelay downto 1) <=
          sDataValidPipeDelay(kCenterTapPipeDelay-1 downto 0);
      end if;
    end process;

    --Create the Data pipeline delay for center tap values when interpolating
    --When interpolating, half of the output samples will be from the filter outputs
    --and half will come from this pipeline of the original input data when SPC>1.
    CenterTapDelay:
    for I in 0 to kInputSamplesPerCycle-1 generate
      sCenterTapPipeDelay(I)(0) <= sDataInPipe(I);
      process(SampleClk)
      begin
        if rising_edge(SampleClk) then
          sCenterTapPipeDelay(I)(kCenterTapPipeDelay downto 1) <=
            sCenterTapPipeDelay(I)(kCenterTapPipeDelay-1 downto 0);
        end if;
      end process;

      sCenterTapFilterDelay(I)(0) <= sCenterTapPipeDelay(I)(kCenterTapPipeDelay);
      process(SampleClk)
      begin
        if rising_edge(SampleClk) then
          if sDataValidPipeDelay(kCenterTapPipeDelay) then
          sCenterTapFilterDelay(I)(kMaxCenterFilterDelay-1 downto 1) <=
            sCenterTapFilterDelay(I)(kMaxCenterFilterDelay-2 downto 0);
          end if;
        end if;
      end process;

      sCenterTap((kFilterDelay+I) mod kInputSamplesPerCycle) <= sCenterTapFilterDelay(I)
	                                      ((kFilterDelay+I)/kInputSamplesPerCycle);
    end generate CenterTapDelay;


    GenerateOutputDataFFsOuterInterp:
    for i in 0 to kNumSingleFilters-1 generate
      GenerateOutputDataFFsInnerInterpCenter:
      for j in sCenterTap(0)'range generate
        --vhook_e FlxRioDFlopDsp OutputDataFlopInterpCenter
        --vhook_a kResetVal '0'
        --vhook_a aReset false
        --vhook_a cEn sEnOutputFFs
        --vhook_a Clk SampleClk
        --vhook_a cD sCenterTap(i)(j)
        --vhook_a cQ sDataOutPreExtend(i)(j)
        OutputDataFlopInterpCenter: entity work.FlxRioDFlopDsp (rtl)
          generic map (kResetVal => '0')  --std_logic:='0'
          port map (
            aReset => false,                    --in  boolean
            cEn    => sEnOutputFFs,             --in  boolean
            Clk    => SampleClk,                --in  std_logic
            cD     => sCenterTap(i)(j),         --in  std_logic
            cQ     => sDataOutPreExtend(i)(j)); --out std_logic:=kResetVal
      end generate GenerateOutputDataFFsInnerInterpCenter;

      --!!!remember to update to be generic for output data type
      sDataOut(2*i+1) <= sDataOutPreExtend(i)(sDataOutPreExtend(0)'high) &
                         sDataOutPreExtend(i)(sDataOutPreExtend(0)'high) &
                         sDataOutPreExtend(i) & "00000000000000000";

      GenerateOutputDataFFsInnerInterpFilter:
      for j in ssDataOut(0)'range generate
        --vhook_e FlxRioDFlopDsp OutputDataFlopInterpFilter
        --vhook_a kResetVal '0'
        --vhook_a aReset false
        --vhook_a cEn sEnOutputFFs
        --vhook_a Clk SampleClk
        --vhook_a cD ssDataOut(i)(j)
        --vhook_a cQ sDataOut(2*i)(j)
        OutputDataFlopInterpFilter: entity work.FlxRioDFlopDsp (rtl)
          generic map (kResetVal => '0')  --std_logic:='0'
          port map (
            aReset => false,             --in  boolean
            cEn    => sEnOutputFFs,      --in  boolean
            Clk    => SampleClk,         --in  std_logic
            cD     => ssDataOut(i)(j),   --in  std_logic
            cQ     => sDataOut(2*i)(j)); --out std_logic:=kResetVal

      end generate GenerateOutputDataFFsInnerInterpFilter;
    end generate GenerateOutputDataFFsOuterInterp;
  end generate FinalInterpolateFFs;

  FinalDecimateFFs:
  if not kInterpolate or kOutputSpc=1 generate
    GenerateOutputDataFFsOuterDec:
    for i in 0 to kNumSingleFilters-1 generate
      GenerateOutputDataFFsInnerDec:
      for j in 0 to ssFilterDataOut(0)'high generate
        --vhook_e FlxRioDFlopDsp OutputDataFlop
        --vhook_a kResetVal '0'
        --vhook_a aReset false
        --vhook_a cEn sEnOutputFFs
        --vhook_a Clk SampleClk
        --vhook_a cD ssDataOut(i)(j)
        --vhook_a cQ sDataOut(i)(j)
        OutputDataFlop: entity work.FlxRioDFlopDsp (rtl)
          generic map (kResetVal => '0')  --std_logic:='0'
          port map (
            aReset => false,            --in  boolean
            cEn    => sEnOutputFFs,     --in  boolean
            Clk    => SampleClk,        --in  std_logic
            cD     => ssDataOut(i)(j),  --in  std_logic
            cQ     => sDataOut(i)(j));  --out std_logic:=kResetVal
      end generate GenerateOutputDataFFsInnerDec;
    end generate GenerateOutputDataFFsOuterDec;
  end generate FinalDecimateFFs;

end RTL;
