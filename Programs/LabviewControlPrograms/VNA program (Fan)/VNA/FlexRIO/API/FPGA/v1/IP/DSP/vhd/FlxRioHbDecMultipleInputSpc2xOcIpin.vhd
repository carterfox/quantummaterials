-------------------------------------------------------------------------------
--
-- File: FlxRioHbDecMultipleInputSpc2xOcIpin.vhd
-- Author: John Ammerman
-- Original Project: Emerald Bay
-- Date: 12 December 2013
--
-------------------------------------------------------------------------------
-- (c) 2013 Copyright National Instruments Corporation
-- All Rights Reserved
-- National Instruments Internal Information
-------------------------------------------------------------------------------
--
-- Purpose:  Creates a Halfband decimating filter that accepts kInputSamplesPerCycle
--           input samples per SampleClk cycle.  2x overclocking is used to
--           reduce resource utilization.  Note that this is the top level VHDL file
--           that should be instantiated in the IPIN.  The valid values supported for
--           kInputSamplesPerCycle are 1, 2, 4, 8, and 16.  If kInputSamplesPerCycle
--           is set to a value less than 16, then the extra sDataIn(x) and
--           sDataOut(x) signals can be ignored and hidden in the IPIN connector
--           pane.
--
--           The filter has a passband ripple bewteen 0 and -0.01 dB up to 0.2 of the
--           input data rate.  It has a stopband rejection of -85 dB past 0.3 of the
--           input data rate.
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
--                             kCyclesPerInput speciifes how often new data
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
  use work.FlxRioPkgHbDec.all;

entity FlxRioHbDecMultipleInputSpc2xOcIpin is
 generic(
    kInputSamplesPerCycle : integer range 1 to 16 := 1;
    kCyclesPerInput : integer range 1 to 4 := 1;
    kUseDsp48e1 : boolean := true);
  port(
    SampleClk    : in std_logic;
    SampleClk2x  : in std_logic;
    sReset       : in std_logic;
    sEnOutputFFs : in std_logic;
    sInputValid  : in std_logic;
    sDataIn0     : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn1     : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn2     : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn3     : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn4     : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn5     : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn6     : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn7     : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn8     : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn9     : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn10    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn11    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn12    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn13    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn14    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn15    : in std_logic_vector(17 downto 0);  -- S18.1
    sOutputValid : out std_logic;
    sDataOut0    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut1    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut2    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut3    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut4    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut5    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut6    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut7    : out std_logic_vector(36 downto 0));  -- S37.2
end FlxRioHbDecMultipleInputSpc2xOcIpin;

architecture RTL of FlxRioHbDecMultipleInputSpc2xOcIpin is

  constant kOutputSamplesPerCycle : integer := CalcOutputSamplesPerCycle(kInputSamplesPerCycle);

  --vhook_sigstart
  signal sOutputValidBool: boolean;
  --vhook_sigend

  signal sDataInArray: Signed18Array_t(kMaxSamplesPerCycle-1 downto 0);
  signal sDataInSpc : Signed18Array_t(kInputSamplesPerCycle-1 downto 0);

  signal sDataOutSpc: Signed37Array_t(kOutputSamplesPerCycle-1 downto 0);
  signal sDataOutArray: Signed37Array_t((kMaxSamplesPerCycle / kDecimationFactor)-1 downto 0);

begin

  sDataInArray(0) <= signed(sDataIn0);
  sDataInArray(1) <= signed(sDataIn1);
  sDataInArray(2) <= signed(sDataIn2);
  sDataInArray(3) <= signed(sDataIn3);
  sDataInArray(4) <= signed(sDataIn4);
  sDataInArray(5) <= signed(sDataIn5);
  sDataInArray(6) <= signed(sDataIn6);
  sDataInArray(7) <= signed(sDataIn7);
  sDataInArray(8) <= signed(sDataIn8);
  sDataInArray(9) <= signed(sDataIn9);
  sDataInArray(10) <= signed(sDataIn10);
  sDataInArray(11) <= signed(sDataIn11);
  sDataInArray(12) <= signed(sDataIn12);
  sDataInArray(13) <= signed(sDataIn13);
  sDataInArray(14) <= signed(sDataIn14);
  sDataInArray(15) <= signed(sDataIn15);

  -- Reshape the inputs from LV FPGA
  sDataInSpc <= sDataInArray(kInputSamplesPerCycle-1 downto 0);

  -- Instantiate the halfband filter
  --vhook_e FlxRioHbDecMultipleInputSpc2xOc
  --vhook_a sReset to_boolean(sReset)
  --vhook_a sEnOutputFFs to_boolean(sEnOutputFFs)
  --vhook_a sInputValid to_boolean(sInputValid)
  --vhook_a sDataIn sDataInSpc
  --vhook_a sOutputValid sOutputValidBool
  --vhook_a sDataOut sDataOutSpc
  FlxRioHbDecMultipleInputSpc2xOcx: entity work.FlxRioHbDecMultipleInputSpc2xOc (RTL)
    generic map (
      kInputSamplesPerCycle => kInputSamplesPerCycle,  --integer range kMaxSamplesPerCycle:kMinSamplesPerCycle
      kUseDsp48e1           => kUseDsp48e1,            --boolean
      kCyclesPerInput       => kCyclesPerInput)        --integer range kMaxCyclesPerInput:kMinCyclesPerInput
    port map (
      SampleClk    => SampleClk,                 --in  std_logic
      SampleClk2x  => SampleClk2x,               --in  std_logic
      sReset       => to_boolean(sReset),        --in  boolean
      sEnOutputFFs => to_boolean(sEnOutputFFs),  --in  boolean
      sInputValid  => to_boolean(sInputValid),   --in  boolean
      sDataIn      => sDataInSpc,                --in  Signed18Array_t(kInputSamplesPerCycle-1:0)
      sOutputValid => sOutputValidBool,          --out boolean
      sDataOut     => sDataOutSpc);              --out Signed37Array_t(CalcOutputSamplesPerCycle(kInputSamplesPerCycle)-1:0)

  -- Reshape outputs to pass back to LV FPGA
  ReshapeDataOut:
  process(sDataOutSpc)
  begin
    sDataOutArray <= (others=>(others=>'0'));
    sDataOutArray(kOutputSamplesPerCycle-1 downto 0) <= sDataOutSpc;
  end process ReshapeDataOut;

  sOutputValid <= to_stdlogic(sOutputValidBool);
  sDataOut0 <= std_logic_vector(sDataOutArray(0));
  sDataOut1 <= std_logic_vector(sDataOutArray(1));
  sDataOut2 <= std_logic_vector(sDataOutArray(2));
  sDataOut3 <= std_logic_vector(sDataOutArray(3));
  sDataOut4 <= std_logic_vector(sDataOutArray(4));
  sDataOut5 <= std_logic_vector(sDataOutArray(5));
  sDataOut6 <= std_logic_vector(sDataOutArray(6));
  sDataOut7 <= std_logic_vector(sDataOutArray(7));

end RTL;
