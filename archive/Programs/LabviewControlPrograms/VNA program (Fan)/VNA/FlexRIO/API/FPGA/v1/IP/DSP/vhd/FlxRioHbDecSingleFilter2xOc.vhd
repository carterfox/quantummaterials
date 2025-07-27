-------------------------------------------------------------------------------
--
-- File: FlxRioHbDecSingleFilter2xOc.vhd
-- Author: John Ammerman
-- Original Project: Emerald Bay
-- Date: 2 January 2014
--
-------------------------------------------------------------------------------
-- (c) 2013 Copyright National Instruments Corporation
-- All Rights Reserved
-- National Instruments Internal Information
-------------------------------------------------------------------------------
--
-- Purpose:  Creates a single halfband decimating filter with 2x overclocking.
--
--           kInputSamplesPerCycle - specifies the number of parallel samples
--                                   input on each Clk cycle.  Valid values are
--                                   1, 2, 4, 8, and 16.
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
--                             kCyclesPerInput speciifes how often new data
--                             can be pushed into the filter.  For example, if
--                             if kCyclesPerInput is set to two, then input
--                             valid can only assert every other 1x clock cycle.
--                             The number of MACs used is proportional to
--                             kCyclesPerInput.  Supported values for kCyclesPerInput
--                             are 1, 2, and 4.  Once you get to 4 only one
--                             MAC is used so there is no advantage to implement
--                             higher values.
--
--           This filter is implemented as a mac chain that is broken into
--           segments.  Each segment computes a sub-set of the coefficients.
--           The segments are connected together serially to save on resources
--           by utilizing the shift in on each segment.  Each segment gets it's
--           input data from a different input (since there are kInputSamplesPerCycle
--           inputs).  Those inputs have to be delayed to match the pipeline
--           delay of the previous segments, and that is done using inferred
--           SRLs.
--
--                         ______      ______      ______
--                        |      |    |      |    |      |
--           DataIn(x) ---| Macs |----| Macs |----| Macs |--- ...
--                        |______|   -|______|   -|______|
--                         ______   |           |
--                        |      |  |           |
--           DataIn(y) ---| SRL1 |--            |
--                        |______|              |
--                         ______               |
--                        |      |              |
--           DataIn(z) ---| SRL2 |--------------
--                        |______|
--
--           Each successive SRL is longer, to match the increased delay of
--           the macs.  DataValid is also delayed in the SRLs along with the
--           data, so that it lines up properly when inserted into the next
--           segment.
--
--           If  kInputSamplesPerCycle is greater than one, then there are
--           kInputSamplesPerCycle / 2 segements since every other coefficient is
--           zero (except the middle tap which is handled specially).  If
--           kInputSamplesPerCycle is equal to one, then there is only one
--           segement.
--
--           If  kInputSamplesPerCycle is greater than one, then each segment
--           contains kNumMacsPerFilter2xOc/kNumSegments MACs.  If
--           kInputSamplesPerCycle is equal to one, then there are
--           kNumMacsPerFilter2xOc/(2*kCyclesPerInput) MACs in the single
--           segement.
--
-------------------------------------------------------------------------------

library ieee, work;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;
  use work.FlxRioPkgNiUtilitiesDsp.all;
  use work.FlxRioPkgHbDec.all;

entity FlxRioHbDecSingleFilter2xOc is
  generic(
    kInputSamplesPerCycle : integer;
    kFilterIndex          : integer;
    kUseDsp48e1           : boolean;
    kCyclesPerInput       : integer);
  port(
    Clk           : in std_logic;
    cReset        : in boolean;
    cDataInValid  : in boolean;
    cDataIn       : in Signed18Array_t(kInputSamplesPerCycle-1 downto 0);  -- S18.1
    cDataOutValid : out boolean;
    cDataOut      : out signed(36 downto 0));  -- S37.2
end FlxRioHbDecSingleFilter2xOc;

architecture RTL of FlxRioHbDecSingleFilter2xOc is

  -- This function calculates the number of segments.
  function CalcNumOfSegments (SamplePerCycle : integer) return integer is
  begin
    if(SamplePerCycle > 1) then
      -- There are kInputSamplesPerCycle / 2 segements since every other coefficient is zero
      -- (except the middle tap which is handled specially).
       return SamplePerCycle / 2;
    else
      return 1;
    end if;
  end function CalcNumOfSegments;

  -- This function calculates which input sample to send to the forward data of
  -- each filter segment.
  function CalcForDataInDelayIndex (SegmentIndex : integer) return integer is
    variable Index : integer;
  begin
    -- Only one input sample per cycle, so just return 0.
    if(kInputSamplesPerCycle = 1) then
      return 0;
    end if;
    -- Each filter's segement(0) index is kDecimationFactor larger than the
    -- previous since we are decimating by kDecimationFactor.
    Index := kFilterIndex*kDecimationFactor;
    -- Since every other coefficient is zero, we will only do a calculation on
    -- every other data point, hence we decrement the segement data index by
    -- two for every segment.
    if(SegmentIndex /= 0) then
      for I in 1 to SegmentIndex loop
        Index := Index - 2;
        -- Wrap the segement data index if it went below zero
        if(Index < 0) then
          Index := Index + kInputSamplesPerCycle;
        end if;
      end loop;
    end if;
    return Index;
  end function CalcForDataInDelayIndex;

  -- This function calculates which input sample to send to the reverse data of
  -- each filter segment.
  function CalcRevDataInDelayIndex (SegmentIndex : integer) return integer is
    variable Index : integer;
  begin
    -- Only one input sample per cycle, so just return 0.
    if(kInputSamplesPerCycle = 1) then
      return 0;
    end if;
    -- Filter(0), Segement(0) always uses this input data index
    Index := kInputSamplesPerCycle - (kNumCoefficients-1 mod kInputSamplesPerCycle);
    -- Each filter's segement(0) index is kDecimationFactor larger than the
    -- previous since we are decimating by kDecimationFactor.
    Index :=  Index + (kFilterIndex*kDecimationFactor);
    -- Wrap the segement data index if it went above kInputSamplesPerCycle-1
    Index := Index mod kInputSamplesPerCycle;
    -- Since every other coefficient is zero, we will only do a calculation on
    -- every other data point, hence we increment the segement data index by
    -- two for every segment.
    if(SegmentIndex /= 0) then
      for I in 1 to SegmentIndex loop
        Index := Index + 2;
        -- Wrap the segement data index if it went above kInputSamplesPerCycle-1
        Index := Index mod kInputSamplesPerCycle;
      end loop;
    end if;
    return Index;
  end function CalcRevDataInDelayIndex;

  -- This function calculates which input sample to send to the middle data of
  -- each filter segment.
  function CalcMidTapDataInDelayIndex return integer is
    variable Index : integer;
  begin
    -- Only one input sample per cycle, so just return 0.
    if(kInputSamplesPerCycle = 1) then
      return 0;
    end if;
    -- If kInputSamplesPerCycle = 2, the Filter(0) uses input data index (1)
    if(kInputSamplesPerCycle = 2) then
      Index := 1;
    -- For all other kInputSamplesPerCycle values, the Filter(0) uses input data index (3)
    else
       Index := 3;
    end if;
    -- Each filter's segement(0) index is kDecimationFactor larger than the
    -- previous since we are decimating by kDecimationFactor.
    Index := Index + (kFilterIndex*kDecimationFactor);
    -- Wrap the segement data index if it went above kInputSamplesPerCycle-1
    Index := Index mod kInputSamplesPerCycle;
    return Index;
  end function CalcMidTapDataInDelayIndex;

  constant kNumCalcCycles : integer := 2**CalcCycleCountLength(kCyclesPerInput,kInputSamplesPerCycle);
  constant kNumOfMacs : integer := CalcNumOfMacs(kCyclesPerInput,kInputSamplesPerCycle);

  -- There are kInputSamplesPerCycle / 2 segements since every other coefficient is zero
  -- (except the middle tap which is handled specially).
  constant kNumSegments : integer := CalcNumOfSegments(kInputSamplesPerCycle);

  -- If kInputSamplesPerCycle > 1, then the middle tap data in should be delayed kNumCalcCycles
  -- for kNumOfMacs-1 MACs so that the data arrives at the same time as the forward
  -- and reverse data.
  constant kBaseMiddleTapDataDelay : integer := (kNumOfMacs-1)*kNumCalcCycles;
  -- If kInputSamplesPerCycle = 1, then the middle tap data in should be delayed
  -- kBaseMiddleTapDataDelay plus an additional kNumCalcCycles/2 clock cyles
  -- so that the middle tap data arrives at the same time as the forward
  -- and reverse data.  An additional kNumCalcCycles/2 cycles is required
  -- since the middle tap data comes in as an odd input.
  constant kOneSpcMiddleTapDataDelay : integer := kBaseMiddleTapDataDelay + (kNumCalcCycles/2);

  constant kDataInPipeLength : integer := kOneSpcMiddleTapDataDelay+1;

  type DataInPipe_t is array( natural range <> ) of Signed18Array_t(kDataInPipeLength-1 downto 0);

  signal cDataValidInPipe : BooleanVector(kDataInPipeLength-1 downto 0) := (others => false);
  signal cDataInPipe : DataInPipe_t(kInputSamplesPerCycle-1 downto 0) := (others => (others => (others => '0')));

  signal cForDataInArray : Signed18Array_t(kNumOfMacs downto 0);
  signal cForDataOutArray : Signed18Array_t(kNumOfMacs downto 0);
  signal cRevDataInArray : Signed18Array_t(kNumOfMacs downto 0);
  signal cRevDataOutArray : Signed18Array_t(kNumOfMacs downto 0);

  signal cPValid : BooleanVector(kNumOfMacs downto 0);
  signal cP    : Signed48Array_t(kNumOfMacs downto 0);
  signal cPcin : Signed48Array_t(kNumOfMacs downto 0);

  signal cDataValidInArray : BooleanVector(kNumOfMacs downto 0);
  signal cDataValidOutArray : BooleanVector(kNumOfMacs downto 0);

  signal cEvenInput : boolean := true;
  signal cEvenInputPipe : BooleanVector(kDataInPipeLength-1 downto 0) := (others => true);

  --vhook_sigstart
  signal cMidTapDataIn: signed(17 downto 0);
  signal cMidTapDataInValid: boolean;
  --vhook_sigend

begin

  -- cEvenInput is only used if kInputSamplesPerCycle = 1.  cEvenInput toggles every time
  -- cDataInValid asserts.  This signal is used to enable writting to the data SRLs.
  -- If cEvenInput is true, then the forward and reverse data SRLs are written with
  -- the input data.  If cEvenInput is false, then the middle data SRLs are written
  -- with the input data.  This allows onle level of SRL32s to be use for all three
  -- memories since we will only be writing to each memory every other time
  -- cDataInValid asserts.
  process(Clk)
  begin
    if rising_edge(Clk) then
      if(cReset) then
        cEvenInput <= true;
      elsif(cDataInValid) then
        cEvenInput <= not cEvenInput;
      end if;
    end if;
  end process;

  -- Create the Even Input pipeline delay.  This will be used for cMidTapDataInValid
  -- since we delay the middle tap input data so that it lines up with the MAC
  -- chain delay.
  cEvenInputPipe(0) <= cEvenInput;
  process(Clk)
  begin
    if rising_edge(Clk) then
      cEvenInputPipe(cEvenInputPipe'high downto 1) <= cEvenInputPipe(cEvenInputPipe'high-1 downto 0);
    end if;
  end process;

  -- Create the DataValid pipeline delay
  cDataValidInPipe(0) <= cDataInValid;
  process(Clk)
  begin
    if rising_edge(Clk) then
      cDataValidInPipe(cDataValidInPipe'high downto 1) <= cDataValidInPipe(cDataValidInPipe'high-1 downto 0);
    end if;
  end process;

  -- Create the Data pipeline delay
  GenDataInDelay:
  for I in 0 to kInputSamplesPerCycle-1 generate
    cDataInPipe(I)(0) <= cDataIn(I);
    process(Clk)
    begin
      if rising_edge(Clk) then
        cDataInPipe(I)(kDataInPipeLength-1 downto 1) <=
          cDataInPipe(I)(kDataInPipeLength-2 downto 0);
      end if;
    end process;
  end generate;

  -- Always send the pipelined data and datavalid to the middle tap
  cMidTapDataInValid <= cDataValidInPipe(kBaseMiddleTapDataDelay) when kInputSamplesPerCycle > 1
                   else cDataValidInPipe(kOneSpcMiddleTapDataDelay) and
                        (cReset or not cEvenInputPipe(kOneSpcMiddleTapDataDelay));
  cMidTapDataIn <= cDataInPipe(CalcMidTapDataInDelayIndex)(kBaseMiddleTapDataDelay) when kInputSamplesPerCycle > 1
              else cDataInPipe(CalcMidTapDataInDelayIndex)(kOneSpcMiddleTapDataDelay);

  -- Create the MACs and mux in the correct data to each MAC
  GenMacs:
  for I in 0 to kNumOfMacs-1 generate

    -- Mux in the correct data and data valid signal.  Choose the correct pipelined data if this MAC is the
    -- first of a new segement, otherwise choose the data from the previous MAC.
    cDataValidInArray(I) <= cDataValidOutArray(I) when ((I mod (kNumOfMacs /kNumSegments)) /= 0)
            else cDataValidInPipe(I*kOverclockingFactor) and (cEvenInput or kInputSamplesPerCycle > 1);
    cForDataInArray(I) <= cForDataOutArray(I) when ((I mod (kNumOfMacs /kNumSegments)) /= 0)
            else cDataInPipe(CalcForDataInDelayIndex(I/(kNumOfMacs /kNumSegments)))(I*kOverclockingFactor);
    cRevDataInArray(I) <= cRevDataOutArray(I) when ((I mod (kNumOfMacs /kNumSegments)) /= 0)
            else cDataInPipe(CalcRevDataInDelayIndex(I/(kNumOfMacs /kNumSegments)))(I*kOverclockingFactor);

    --vhook_e FlxRioHbDecMac2xOc
    --vhook_a kMacIndex I
    --vhook_a cDataInValid cDataValidInArray(I)
    --vhook_a cPcin cPcin(I)
    --vhook_a cDataOutValid cDataValidOutArray(I+1)
    --vhook_a cForDataIn cForDataInArray(I)
    --vhook_a cForDataOut cForDataOutArray(I+1)
    --vhook_a cRevDataIn cRevDataInArray(I)
    --vhook_a cRevDataOut cRevDataOutArray(I+1)
    --vhook_a cPcout cPcin(I+1)
    --vhook_a cP cP(I+1)
    --vhook_a cPValid cPValid(I+1)
    FlxRioHbDecMac2xOcx: entity work.FlxRioHbDecMac2xOc (RTL)
      generic map (
        kMacIndex             => I,                      --integer
        kInputSamplesPerCycle => kInputSamplesPerCycle,  --integer
        kFilterIndex          => kFilterIndex,           --integer
        kUseDsp48e1           => kUseDsp48e1,            --boolean
        kCyclesPerInput       => kCyclesPerInput)        --integer
      port map (
        Clk                => Clk,                      --in  std_logic
        cReset             => cReset,                   --in  boolean
        cDataInValid       => cDataValidInArray(I),     --in  boolean
        cForDataIn         => cForDataInArray(I),       --in  signed(17:0)
        cRevDataIn         => cRevDataInArray(I),       --in  signed(17:0)
        cMidTapDataInValid => cMidTapDataInValid,       --in  boolean
        cMidTapDataIn      => cMidTapDataIn,            --in  signed(17:0)
        cPcin              => cPcin(I),                 --in  signed(47:0)
        cDataOutValid      => cDataValidOutArray(I+1),  --out boolean
        cForDataOut        => cForDataOutArray(I+1),    --out signed(17:0)
        cRevDataOut        => cRevDataOutArray(I+1),    --out signed(17:0)
        cPValid            => cPValid(I+1),             --out boolean
        cP                 => cP(I+1),                  --out signed(47:0)
        cPcout             => cPcin(I+1));              --out signed(47:0)

  end generate GenMacs;

  cDataOutValid <= cPValid(kNumOfMacs);
  -- The sum of the absolute value of the coefficients is < 1.7, so we only need two integer bits.
  -- We can safely discard the rest of the integer bits.
  cDataOut <= cP(kNumOfMacs)(36 downto 0);  -- From S48.13 to S37.2

end RTL;
