-------------------------------------------------------------------------------
--
-- File: FlxRioHbInterpMac2xOc.vhd
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
-- Purpose:  Implements the MAC for the Halfband Decimator.
--
--           kMacIndex - specifies the MAC index within this filter.  This is
--                       used to select the correct coefficient and data.
--
--           kInputSamplesPerCycle - specifies the number of parallel samples input
--                             on each Clk cycle.  Valid values are 1, 2, 4, 8,
--                             and 16.
--
--           kFilterIndex - specifies which output sample this filter is
--                          calculating.
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
--                             valid can only assert every other 1x clock cycle.
--                             The number of MACs used is proportional to
--                             kCyclesPerInput.  Supported values for kCyclesPerInput
--                             are 1, 2, and 4.  Once you get to 4 only one
--                             MAC is used so there is no advantage to implement
--                             higher values.
--
--           This component uses SRLs to store the forward, middle, and reverse
--           data.  It uses DSP48Es or DSP48E1s (based on kUseDsp48e1) to
--           implement the actual MAC.
--
-------------------------------------------------------------------------------

library ieee, work;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;
  use work.FlxRioPkgNiUtilitiesDsp.all;
  use work.FlxRioPkgHbInterp.all;
  use work.FlxRioPkgHbInterpCoefficients.all;

library UNISIM;
  use UNISIM.Vcomponents.ALL;

-- synthesis translate_off
-- synthesis translate_on

entity FlxRioHbInterpMac2xOc is
  generic(
    kInputSamplesPerCycle : integer range kMaxInputSpc downto kMinInputSpc;
    kCyclesPerInput       : integer range kMaxCyclesPerInput downto kMinCyclesPerInput;
    kUseDsp48e1           : boolean := true;
    kInterpolate          : boolean := false;
    kFilterIndex          : integer := 0;
    kMacIndex             : integer := 0);
  port(
    Clk                : in std_logic;
    cReset             : in boolean;
    cDataInValid       : in boolean;
    cForDataIn         : in signed(17 downto 0);  -- S18.1
    cRevDataIn         : in signed(17 downto 0);  -- S18.1
    cMidTapDataInValid : in boolean;
    cMidTapDataIn      : in signed(17 downto 0);  -- S18.1
    cPcin              : in signed(47 downto 0);  -- S48.13
    cDataOutValid      : out boolean;
    cForDataOut        : out signed(17 downto 0);  -- S18.1
    cRevDataOut        : out signed(17 downto 0);  -- S18.1
    cPValid            : out boolean;
    cP                 : out signed(47 downto 0);  -- S48.13
    cPcout             : out signed(47 downto 0)); -- S48.13
end FlxRioHbInterpMac2xOc;

architecture RTL of FlxRioHbInterpMac2xOc is

  component dsp48e1
    generic(
      acascreg           : integer := 1;
      adreg              : integer := 1;
      alumodereg         : integer := 1;
      areg               : integer := 1;
      autoreset_patdet   : string := "MATCH";
      a_input            : string := "DIRECT";
      bcascreg           : integer := 1;
      breg               : integer := 1;
      b_input            : string := "DIRECT";
      carryinreg         : integer := 1;
      carryinselreg      : integer := 1;
      creg               : integer := 1;
      dreg               : integer := 1;
      inmodereg          : integer := 1;
      mask               : bit_vector := X"3FFFFFFFFFFF";
      mreg               : integer := 1;
      opmodereg          : integer := 1;
      pattern            : bit_vector := X"000000000000";
      preg               : integer := 1;
      sel_mask           : string := "MASK";
      sel_pattern        : string := "PATTERN";
      use_dport          : boolean;
      use_mult           : string := "MULT_S";
      use_pattern_detect : string := "NO_PATDET";
      use_simd           : string := "ONE48");
    port(
      clk            : in  std_ulogic;
      a              : in  std_logic_vector(29 downto 0);
      b              : in  std_logic_vector(17 downto 0);
      c              : in  std_logic_vector(47 downto 0);
      d              : in  std_logic_vector(24 downto 0);
      carryin        : in  std_ulogic;
      acin           : in  std_logic_vector(29 downto 0);
      bcin           : in  std_logic_vector(17 downto 0);
      pcin           : in  std_logic_vector(47 downto 0);
      carrycascin    : in  std_ulogic;
      multsignin     : in  std_ulogic;
      acout          : out  std_logic_vector(29 downto 0);
      bcout          : out std_logic_vector(17 downto 0);
      carrycascout   : out std_ulogic;
      multsignout    : out std_ulogic;
      p              : out std_logic_vector(47 downto 0);
      patternbdetect : out std_ulogic;
      patterndetect  : out std_ulogic;
      overflow       : out std_ulogic;
      underflow      : out std_ulogic;
      carryout       : out std_logic_vector(3 downto 0);
      pcout          : out std_logic_vector(47 downto 0);
      opmode         : in  std_logic_vector(6 downto 0);
      alumode        : in  std_logic_vector(3 downto 0);
      carryinsel     : in  std_logic_vector(2 downto 0);
      inmode         : in  std_logic_vector(4 downto 0);
      cea1           : in  std_ulogic;
      cea2           : in  std_ulogic;
      cealumode      : in  std_ulogic;
      ceb1           : in  std_ulogic;
      ceb2           : in  std_ulogic;
      cec            : in  std_ulogic;
      cecarryin      : in  std_ulogic;
      cem            : in  std_ulogic;
      cectrl         : in  std_ulogic;
      cep            : in  std_ulogic;
      cead           : in  std_ulogic;
      ced            : in  std_ulogic;
      ceinmode       : in  std_ulogic;
      rsta           : in  std_ulogic;
      rstalumode     : in  std_ulogic;
      rstb           : in  std_ulogic;
      rstc           : in  std_ulogic;
      rstallcarryin  : in  std_ulogic;
      rstm           : in  std_ulogic;
      rstctrl        : in  std_ulogic;
      rstp           : in  std_ulogic;
      rstd           : in  std_ulogic;
      rstinmode      : in  std_ulogic);
    end component;

  component dsp48e
    generic(
      ACASCREG           : integer := 1;
      ALUMODEREG         : integer := 1;
      AREG               : integer := 1;
      AUTORESET_PATTERN_DETECT        : boolean := FALSE;
      AUTORESET_PATTERN_DETECT_OPTINV : string := "MATCH";
      A_INPUT            : string := "DIRECT";
      BCASCREG           : integer := 1;
      BREG               : integer := 1;
      B_INPUT            : string := "DIRECT";
      CARRYINREG         : integer := 1;
      CARRYINSELREG      : integer := 1;
      CREG               : integer := 1;
      MASK               : bit_vector := X"3FFFFFFFFFFF";
      MREG               : integer := 1;
      MULTCARRYINREG     : integer := 1;
      OPMODEREG          : integer := 1;
      PATTERN            : bit_vector := X"000000000000";
      PREG               : integer := 1;
      SEL_MASK           : string := "MASK";
      SEL_PATTERN        : string := "PATTERN";
      SEL_ROUNDING_MASK  : string := "SEL_MASK";
      SIM_MODE           : string := "SAFE";
      USE_MULT           : string := "MULT_S";
      USE_PATTERN_DETECT : string := "NO_PATDET";
      USE_SIMD           : string := "ONE48");
    port(
      CLK            : in  std_ulogic;
      A              : in  std_logic_vector(29 downto 0);
      ACIN           : in  std_logic_vector(29 downto 0);
      ACOUT          : out std_logic_vector(29 downto 0);
      B              : in  std_logic_vector(17 downto 0);
      BCIN           : in  std_logic_vector(17 downto 0);
      BCOUT          : out std_logic_vector(17 downto 0);
      C              : in  std_logic_vector(47 downto 0);
      P              : out std_logic_vector(47 downto 0);
      PCIN           : in  std_logic_vector(47 downto 0);
      PCOUT          : out std_logic_vector(47 downto 0);
      CARRYIN        : in  std_ulogic;
      CARRYOUT       : out std_logic_vector(3 downto 0);
      CARRYCASCIN    : in  std_ulogic;
      CARRYCASCOUT   : out std_ulogic;
      OPMODE         : in  std_logic_vector(6 downto 0);
      ALUMODE        : in  std_logic_vector(3 downto 0);
      CARRYINSEL     : in  std_logic_vector(2 downto 0);
      MULTSIGNIN     : in std_ulogic;
      MULTSIGNOUT    : out std_ulogic;
      OVERFLOW       : out std_ulogic;
      UNDERFLOW      : out std_ulogic;
      PATTERNBDETECT : out std_ulogic;
      PATTERNDETECT  : out std_ulogic;
      CEA1           : in  std_ulogic;
      CEA2           : in  std_ulogic;
      CEALUMODE      : in  std_ulogic;
      CEB1           : in  std_ulogic;
      CEB2           : in  std_ulogic;
      CEC            : in  std_ulogic;
      CECARRYIN      : in  std_ulogic;
      CECTRL         : in  std_ulogic;
      CEM            : in  std_ulogic;
      CEMULTCARRYIN  : in  std_ulogic;
      CEP            : in  std_ulogic;
      RSTA           : in  std_ulogic;
      RSTALLCARRYIN  : in  std_ulogic;
      RSTALUMODE     : in  std_ulogic;
      RSTB           : in  std_ulogic;
      RSTC           : in  std_ulogic;
      RSTCTRL        : in  std_ulogic;
      RSTM           : in  std_ulogic;
      RSTP           : in  std_ulogic);
  end component;

  constant kNumMacs : integer := CalcNumOfMacs(kInputSamplesPerCycle,kCyclesPerInput,kInterpolate);
  constant kIsFirstMac : boolean := kMacIndex=0;
  constant kIsLastMac : boolean := kMacIndex=(kNumMacs-1);

  constant kCycleCountLength : integer := CalcCycleCountLength(kCyclesPerInput,kInputSamplesPerCycle,kInterpolate);
  constant kNumCalcCycles : integer := 2**kCycleCountLength;

  -- This function calculates the forward coefficient index used for this MAC.
  function CalcForCoeffIndex (CycleCount : integer) return integer is
      variable NumNonZeroCoeffPerSegment : integer;
      variable OffsetWithinSegment : integer;
      variable SegmentOffset : integer;
      variable ReturnVal : integer;
      variable SamplesPerCycle : integer;
  begin
      if kInterpolate then
        --When interpolating, we need to know the samples per cycle after zero stuffing
        SamplesPerCycle := kInputSamplesPerCycle*kInterpolationFactor;
      else
        SamplesPerCycle := kInputSamplesPerCycle;
      end if;

      if(SamplesPerCycle > 1) then
        -- Calculate the number of non-zero coefficients used per segment
        NumNonZeroCoeffPerSegment := (kNumMacsPerFilter2xOc*kOverclockingFactor)/SamplesPerCycle;--8*2/8=2
        -- Calculate the coefficient offset within a segment
        OffsetWithinSegment := (kMacIndex mod NumNonZeroCoeffPerSegment)*kNumCalcCycles*SamplesPerCycle;--(kMaxIndex mod 2)*2*8= (kMaxIndex mod 2)*16
        -- Calculate the offset of the segment
        SegmentOffset := (kMacIndex / NumNonZeroCoeffPerSegment)*kOverclockingFactor; --kMaxIndex/2*2
        -- Calculate the base coefficient index for cycle zero
        ReturnVal  := OffsetWithinSegment + SegmentOffset;

        -- Add SamplesPerCycle if it is cycle one
        ReturnVal := ReturnVal + (SamplesPerCycle * CycleCount);
        -- Subtract one if it is the middle tap
        if(kIsLastMac and CycleCount = (kNumCalcCycles-1)) then
          ReturnVal := ReturnVal-1;
        end if;
      else
        -- Calculate the coefficient index that is used for cycle zero of this MAC
        -- We multiply be two because we don't calculate the zero coefficients
        ReturnVal := kMacIndex * kNumCalcCycles * 2;
        -- Adjust for this particular cycle count
        -- We multiply be two because we don't calculate the zero coefficients
        ReturnVal := ReturnVal + (CycleCount * 2);
        -- Subtract one if it is the middle tap
        if(kIsLastMac and CycleCount = (kNumCalcCycles-1)) then
          ReturnVal := ReturnVal-1;
        end if;
      end if;
      return ReturnVal;
  end function CalcForCoeffIndex;

  -- This function calculates the SRL address to use to look-up the data that matches
  -- the corresponding coefficient index.  Note that this works for forward, middle,
  -- and backwards SRLs.
  function CalcSrlAddr (CoeffIndex : integer) return integer is
      variable ReturnVal : integer;
      variable SamplesPerCycle : integer;
  begin
      if kInterpolate then
        --When interpolating, we need to know the samples per cycle after zero stuffing
        SamplesPerCycle := kInputSamplesPerCycle*kInterpolationFactor;
      else
        SamplesPerCycle := kInputSamplesPerCycle;
      end if;

      if(SamplesPerCycle > 1) then
        -- Calculate the adjustment to the coefficient index based on the filter index.  This formula was derived
        -- by analyzing address patterns for each SamplesPerCycle in a spreadsheet.
        ReturnVal := CoeffIndex + (SamplesPerCycle - 1) - (kDecimationFactor * kFilterIndex);
        -- Divide by SamplesPerCycle to get the final SRL address.
        ReturnVal := ReturnVal / SamplesPerCycle;
      else
        -- Since every other input data is written into a particular data SRL, we just divide the
        -- CoeffIndex by two to get the SRL address
        ReturnVal :=  CoeffIndex / 2;
      end if;
      return ReturnVal;
  end function CalcSrlAddr;

  constant kForSrlAddrCycleZero : integer := CalcSrlAddr(CalcForCoeffIndex(0));
  constant kMidSrlAddr          : integer := CalcSrlAddr(CalcForCoeffIndex(kNumCalcCycles-1));
  constant kRevSrlAddrCycleZero : integer := CalcSrlAddr(kHbInterpCoefficients'high - CalcForCoeffIndex(0));

  signal cDataInValidPipe : BooleanVector(4 + kNumCalcCycles downto 0) := (others => false);
  signal cForDataInPipe   : Signed18Array_t(kNumCalcCycles-1 downto 0) := (others =>(others => '0'));
  signal cRevDataInPipe   : Signed18Array_t(kNumCalcCycles-1 downto 0) := (others =>(others => '0'));

  signal cForSrlAddr : unsigned(4 downto 0) := to_unsigned(kForSrlAddrCycleZero,5);
  signal cMidSrlAddr : unsigned(4 downto 0) := to_unsigned(kMidSrlAddr,5);
  signal cRevSrlAddr : unsigned(4 downto 0) := to_unsigned(kRevSrlAddrCycleZero,5);

  signal cMidTapSrlDataComb : signed(17 downto 0);
  signal cMidTapSrlDataOut  : signed(17 downto 0) := (others => '0');
  signal cForSrlDataComb    : signed(17 downto 0);
  signal cForSrlDataOut     : signed(17 downto 0) := (others => '0');
  signal cRevSrlDataComb    : signed(17 downto 0);
  signal cRevSrlDataOut     : signed(17 downto 0) := (others => '0');

  signal cCoefficient : signed(17 downto 0) := kHbInterpCoefficients(CalcForCoeffIndex(0));

  signal cPreAdderInputA : signed (17 downto 0);
  signal cPreAdderInputB : signed (17 downto 0);

  signal cOpMode : std_logic_vector(6 downto 0) := "0100101";
  signal cA : std_logic_vector(29 downto 0);
  signal cB : std_logic_vector(17 downto 0);
  signal cD : std_logic_vector(24 downto 0);

  signal cPSlv : std_logic_vector(47 downto 0);
  signal cPcoutSlv : std_logic_vector(47 downto 0);

  signal cCycleCount : unsigned(kCycleCountLength-1 downto 0) := (others => '0');

  signal cResetPipe : boolean := true;

  --Limit the fanout of the cResetPipe signal for timing
  attribute keep : string;
  attribute keep of cResetPipe: signal is "true";
  attribute max_fanout: integer;
  attribute max_fanout of cResetPipe : signal is 5;

  --vhook_sigstart
  --vhook_sigend

begin

  -- Pipeline cReset to make timing easier to meet.
  process(Clk)
  begin
    if rising_edge(Clk) then
      cResetPipe <= cReset;
    end if;
  end process;

  -- Create the counter that keeps track of how many calculation we have done since the last
  -- cDataInValid.  This signal is used to select the correct coefficient for the MAC.
  -- The CycleCountEn signal insures the counter starts up safely.
  process(Clk)
  begin
    if rising_edge(Clk) then
      if(cDataInValid or cResetPipe) then
        cCycleCount <= (others => '0');
      else
        -- only multi-CPS-implementations need more than 2 coefficients.
        if kCyclesPerInput > 1 then
          cCycleCount <= cCycleCount + 1;
        else
          -- SPC-implementations only use two counter values for 2xOC
          cCycleCount <= to_unsigned(1, cCycleCount'length);
        end if;
      end if;
    end if;
  end process;

  --Pipeline the input data to send to the next MAC
  process(Clk)
  begin
    if rising_edge(Clk) then
      cDataInValidPipe <= cDataInValidPipe(cDataInValidPipe'high-1 downto 0) & cDataInValid;
      cForDataInPipe <= cForDataInPipe(cForDataInPipe'high-1 downto 0) & cForDataIn;
      cRevDataInPipe <= cRevDataInPipe(cRevDataInPipe'high-1 downto 0) & cRevDataIn;
    end if;
  end process;

  -- Assign the outputs that will go to the next MAC
  cDataOutValid <= cDataInValidPipe(kNumCalcCycles-1);
  cForDataOut   <= cForDataInPipe(kNumCalcCycles-1);
  cRevDataOut   <= cRevDataInPipe(kNumCalcCycles-1);

  -- Create the forward and reverse addresses
  process(Clk)
  begin
    if rising_edge(Clk) then

      -- Reset to the cycle zero address when cDataInValid asserts
      if(cDataInValid or cResetPipe) then
        cForSrlAddr <= to_unsigned(kForSrlAddrCycleZero,cForSrlAddr'length);
      -- Calculate towards the middle tap each consecutive cycle
      else
        cForSrlAddr <= cForSrlAddr + 1;
      end if;

      -- Reset to the cycle zero address when cDataInValid asserts
      if(cDataInValid or cResetPipe) then
        cRevSrlAddr <= to_unsigned(kRevSrlAddrCycleZero,cRevSrlAddr'length);
      -- Calculate towards the middle tap each consecutive cycle
      else
        cRevSrlAddr <= cRevSrlAddr - 1;
      end if;
    end if;
  end process;

  cMidSrlAddr <= to_unsigned(kMidSrlAddr,cMidSrlAddr'length);

  -- Create the middle data SRL.
  GenMidTapDataSRLs:
  for I in 0 to cMidTapDataIn'length-1 generate
    --vhook_i SRLC32E  MidTapDataSrl
    --vhook_h INIT
    --vhook_h IS_CLK_INVERTED
    --vhook_a clk Clk
    --vhook_a d   cMidTapDataIn(I)
    --vhook_a ce  to_stdlogic(cMidTapDataInValid)
    --vhook_a a   std_logic_vector(cMidSrlAddr)
    --vhook_a q   cMidTapSrlDataComb(I)
    --vhook_a q31 open
    MidTapDataSrl: SRLC32E
      port map (
        Q   => cMidTapSrlDataComb(I),            --out STD_ULOGIC
        Q31 => open,                             --out STD_ULOGIC
        A   => std_logic_vector(cMidSrlAddr),    --in  STD_LOGIC_VECTOR(4:0):="00000"
        CE  => to_stdlogic(cMidTapDataInValid),  --in  STD_ULOGIC
        CLK => Clk,                              --in  STD_ULOGIC
        D   => cMidTapDataIn(I));                --in  STD_ULOGIC
  end generate;

  -- Pipeline the middle tap data SRL output to improve timing
  process(Clk)
  begin
    if rising_edge(Clk) then
      cMidTapSrlDataOut <= signed(cMidTapSrlDataComb);
    end if;
  end process;

  -- Create the forward data SRL.
  GenForDataSRLs:
  for I in 0 to cForDataIn'length-1 generate
    --vhook_i SRLC32E  ForDataSrl
    --vhook_h INIT
    --vhook_h IS_CLK_INVERTED
    --vhook_a clk Clk
    --vhook_a d   cForDataIn(I)
    --vhook_a ce  to_stdlogic(cDataInValid)
    --vhook_a a   std_logic_vector(cForSrlAddr)
    --vhook_a q   cForSrlDataComb(I)
    --vhook_a q31 open
    ForDataSrl: SRLC32E
      port map (
        Q   => cForSrlDataComb(I),             --out STD_ULOGIC
        Q31 => open,                           --out STD_ULOGIC
        A   => std_logic_vector(cForSrlAddr),  --in  STD_LOGIC_VECTOR(4:0):="00000"
        CE  => to_stdlogic(cDataInValid),      --in  STD_ULOGIC
        CLK => Clk,                            --in  STD_ULOGIC
        D   => cForDataIn(I));                 --in  STD_ULOGIC
  end generate;

  -- Pipeline the forward data SRL output to improve timing
  process(Clk)
  begin
    if rising_edge(Clk) then
      cForSrlDataOut <= signed(cForSrlDataComb);
    end if;
  end process;

  -- Create the reverse data SRL.
  GenRevDataSRLs:
  for I in 0 to cRevDataIn'length-1 generate
    --vhook_i SRLC32E  RevDataSrl
    --vhook_h INIT
    --vhook_h IS_CLK_INVERTED
    --vhook_a clk Clk
    --vhook_a d   cRevDataIn(I)
    --vhook_a ce  to_stdlogic(cDataInValid)
    --vhook_a a   std_logic_vector(cRevSrlAddr)
    --vhook_a q   cRevSrlDataComb(I)
    --vhook_a q31 open
    RevDataSrl: SRLC32E
      port map (
        Q   => cRevSrlDataComb(I),             --out STD_ULOGIC
        Q31 => open,                           --out STD_ULOGIC
        A   => std_logic_vector(cRevSrlAddr),  --in  STD_LOGIC_VECTOR(4:0):="00000"
        CE  => to_stdlogic(cDataInValid),      --in  STD_ULOGIC
        CLK => Clk,                            --in  STD_ULOGIC
        D   => cRevDataIn(I));                 --in  STD_ULOGIC
  end generate;

  -- Pipeline the reverse data SRL output to improve timing
  process(Clk)
  begin
    if rising_edge(Clk) then
      cRevSrlDataOut <= signed(cRevSrlDataComb);
    end if;
  end process;

  -- Vivado was creating this as a BRAM, and meeting timing from the BRAM is
  -- getting hard, possibly because the register is being forced to be external.
  -- regardless, the BRAM itself is wasteful with only two possible values, so
  -- hard coding the two actual cases so this gets contant folded, really is a
  -- mux
  -- Create the coefficient mux
  process(Clk)
  begin
    if rising_edge(Clk) then
      if kCyclesPerInput > 1 then
        cCoefficient <= kHbInterpCoefficients(CalcForCoeffIndex(to_integer(cCycleCount)));
      else
        if cCycleCount = to_unsigned(1, cCycleCount'length) then
          cCoefficient <= kHbInterpCoefficients(CalcForCoeffIndex(1));
        else
          cCoefficient <= kHbInterpCoefficients(CalcForCoeffIndex(0));
        end if;
      end if;
    end if;
  end process;

  -- Create the opmode for the DSP48E(1)
  process(Clk)
  begin
    if rising_edge(Clk) then
      if(kIsFirstMac) then
        if(cDataInValidPipe(2)) then
          cOpmode <= "0000101";  -- p=(a+d)*b or p=a*b
        else
          cOpmode <= "0100101";  -- p=p+((a+d)*b) or p=p+(a*b)
        end if;
      else
        if(cDataInValidPipe(2)) then
          cOpmode <= "0010101";  -- p=pcin+((a+d)*b) or p=pcin+(a+*b)
        else
          cOpmode <= "0100101";  -- p=p+((a+d)*b) or p=p+(a*b)
        end if;
      end if;
    end if;
  end process;

  -- Select the middle tap data for the first pre-adder input if we are on the last calculation cycle
  -- of the last MAC, otherwise select the normal forward data.
  cPreAdderInputA <= cMidtapSrlDataOut when (cDataInValidPipe(kNumCalcCycles) and kIsLastMac)
                else cForSrlDataOut;

  -- Select zeros for the second pre-adder input if we are on the last calculation cycle
  -- of the last MAC since there is no symmetric data for the middle tap, otherwise select the normal
  -- reverse data.
  cPreAdderInputB <= (others => '0') when (cDataInValidPipe(kNumCalcCycles) and kIsLastMac)
                else cRevSrlDataOut;

  -- Use a DSP48E1 for the MAC if kUseDsp48e1 is true.  The pre-adder is implemented
  -- in the DSP48E1.
  GenerateDsp48e1 : if kUseDsp48e1 generate
  begin

    -- Assign the first pre-adder input to the A input of the DSP48E1.
    cA <= std_logic_vector(resize(cPreAdderInputA,cA'length));
    -- Assign the second pre-adder input to the D input of the DSP48E1.
    cD <= std_logic_vector(resize(cPreAdderInputB,cD'length));
    -- Assign the coefficient to the B input of the DSP48E1
    cB <= std_logic_vector(cCoefficient);

    -- Create the DSP48E1.  Note that the pre-adder is enabled.
    dsp48e1_x : dsp48e1
      generic map(
      acascreg => 1,
      adreg => 1,
      alumodereg => 1,
      areg => 1,
      autoreset_patdet => "NO_RESET",
      a_input => "DIRECT",
      bcascreg => 1,
      breg => 2,
      b_input => "DIRECT",
      carryinreg => 1,
      carryinselreg => 1,
      creg => 1,
      dreg => 1,
      inmodereg => 1,
      mask => x"3FFFFFFFFFFF",
      mreg => 1,
      opmodereg => 1,
      pattern => x"000000000000",
      preg => 1,
      sel_mask => "MASK",
      sel_pattern => "PATTERN",
      use_dport => true,
      use_mult => "MULTIPLY",
      use_pattern_detect => "NO_PATDET",
      use_simd => "ONE48")
    port map(
      clk => Clk,
      a => cA,
      b => cB,
      c => (others => '0'),
      d => cD,
      carryin => '0',
      acin => (others => '0'),
      bcin => (others => '0'),
      pcin => std_logic_vector(cPcin),
      carrycascin => '0',
      multsignin => '0',
      acout => open,
      bcout => open,
      carrycascout => open,
      multsignout => open,
      p => cPSlv,
      patternbdetect => open,
      patterndetect => open,
      overflow => open,
      underflow => open,
      carryout => open,
      pcout => cPcoutSlv,
      opmode => cOpmode,
      alumode => (others => '0'),
      carryinsel => (others => '0'),
      inmode => "00101",
      cea1 => '1',
      cea2 => '1',
      cealumode => '1',
      ceb1 => '1',
      ceb2 => '1',
      cec => '1',
      cecarryin => '1',
      cem => '1',
      cectrl => '1',
      cep => '1',
      cead => '1',
      ced => '1',
      ceinmode => '1',
      rsta => '0',
      rstalumode => '0',
      rstb => '0',
      rstc => '0',
      rstallcarryin => '0',
      rstm => '0',
      rstctrl => '0',
      rstp => '0',
      rstd => '0',
      rstinmode => '0');
    
    end generate GenerateDsp48e1;

  -- Use a DSP48E for the MAC if kUseDsp48e1 is false.  The pre-adder is implemented in Slice logic.
  GenerateDsp48e : if not kUseDsp48e1 generate
    signal sPreAdder : signed(18 downto 0) := (others => '0');
  begin

    -- Implement the pre-adder with Slice logic;
    process(Clk)
    begin
      if rising_edge(Clk) then
        sPreAdder <= resize(cPreAdderInputA,sPreAdder'length) +
                     resize(cPreAdderInputB,sPreAdder'length);
      end if;
    end process;

    cA <= std_logic_vector(resize(sPreAdder,cA'length));
    cB <= std_logic_vector(cCoefficient);

    -- Create the DSP48E
    dsp48e_x : dsp48e
    generic map(
      acascreg => 1,
      alumodereg => 1,
      areg => 1,
      autoreset_pattern_detect => false,
      autoreset_pattern_detect_optinv => "MATCH",
      a_input => "DIRECT",
      bcascreg => 1,
      breg => 2,
      b_input => "DIRECT",
      carryinreg => 1,
      carryinselreg => 1,
      creg => 1,
      mask => x"3FFFFFFFFFFF",
      mreg => 1,
      multcarryinreg => 1,
      opmodereg => 1,
      pattern => x"000000000000",
      preg => 1,
      sel_rounding_mask => "SEL_MASK",
      sel_mask => "MASK",
      sel_pattern => "PATTERN",
      use_mult => "MULT_S",
      use_pattern_detect => "NO_PATDET",
      use_simd => "ONE48")
    port map(
      clk => Clk,
      a => cA,
      b => cB,
      c => (others => '0'),
      carryin => '0',
      acin => (others => '0'),
      bcin => (others => '0'),
      pcin => std_logic_vector(cPcin),
      carrycascin => '0',
      multsignin => '0',
      acout => open,
      bcout => open,
      carrycascout => open,
      multsignout => open,
      p => cPSlv,
      patternbdetect => open,
      patterndetect => open,
      overflow => open,
      underflow => open,
      carryout => open,
      pcout => cPcoutSlv,
      opmode => cOpmode,
      alumode => "0000",
      carryinsel => "000",
      cea1 => '1',
      cea2 => '1',
      cealumode => '1',
      ceb1 => '1',
      ceb2 => '1',
      cec => '1',
      cecarryin => '1',
      cem => '1',
      cectrl => '1',
      cep => '1',
      cemultcarryin => '1',
      rsta => '0',
      rstalumode => '0',
      rstb => '0',
      rstc => '0',
      rstallcarryin => '0',
      rstm => '0',
      rstctrl => '0',
      rstp => '0');

  end generate GenerateDsp48e;

  -- Assign the final outputs
  cPValid <= cDataInValidPipe(cDataInValidPipe'high);
  cPcout  <= signed(cPcoutSlv);
  cP      <= signed(cPSlv);

end RTL;
