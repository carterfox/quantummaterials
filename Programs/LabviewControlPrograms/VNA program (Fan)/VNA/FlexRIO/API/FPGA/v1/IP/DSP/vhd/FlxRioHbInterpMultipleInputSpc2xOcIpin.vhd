-------------------------------------------------------------------------------
--
-- File: FlxRioHbInterpMultipleInputSpc2xOcIpin.vhd
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

entity FlxRioHbInterpMultipleInputSpc2xOcIpin is
 generic(
    kInputSamplesPerCycle : integer range 1 to 32 := 1;
    kCyclesPerInput       : integer range 1 to 8 := 1;
    kUseDsp48e1           : boolean := true;
    kInterpolate          : boolean := false);
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
    sDataIn16    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn17    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn18    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn19    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn20    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn21    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn22    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn23    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn24    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn25    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn26    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn27    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn28    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn29    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn30    : in std_logic_vector(17 downto 0);  -- S18.1
    sDataIn31    : in std_logic_vector(17 downto 0);  -- S18.1
    sOutputValid : out std_logic;
    sDataOut0    : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut1    : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut2    : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut3    : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut4    : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut5    : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut6    : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut7    : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut8    : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut9    : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut10   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut11   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut12   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut13   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut14   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut15   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut16   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut17   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut18   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut19   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut20   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut21   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut22   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut23   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut24   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut25   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut26   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut27   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut28   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut29   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut30   : out std_logic_vector(36 downto 0);  -- S37.2
    sDataOut31   : out std_logic_vector(36 downto 0)); -- S37.2
end FlxRioHbInterpMultipleInputSpc2xOcIpin;

architecture RTL of FlxRioHbInterpMultipleInputSpc2xOcIpin is

  constant kOutputSamplesPerCycle : integer := CalcOutputSamplesPerCycle(kInputSamplesPerCycle,kCyclesPerInput,kInterpolate);

  --vhook_sigstart
  signal sOutputValidBool: boolean;
  --vhook_sigend

  signal sDataInArray: Signed18Array_t(kMaxInputSpc-1 downto 0);
  signal sDataInSpc : Signed18Array_t(kInputSamplesPerCycle-1 downto 0);

  signal sDataOutSpc: Signed37Array_t(kOutputSamplesPerCycle-1 downto 0);
  signal sDataOutArray: Signed37Array_t(kMaxOutputSpc-1 downto 0);

begin

  sDataInArray(0)  <= signed(sDataIn0);
  sDataInArray(1)  <= signed(sDataIn1);
  sDataInArray(2)  <= signed(sDataIn2);
  sDataInArray(3)  <= signed(sDataIn3);
  sDataInArray(4)  <= signed(sDataIn4);
  sDataInArray(5)  <= signed(sDataIn5);
  sDataInArray(6)  <= signed(sDataIn6);
  sDataInArray(7)  <= signed(sDataIn7);
  sDataInArray(8)  <= signed(sDataIn8);
  sDataInArray(9)  <= signed(sDataIn9);
  sDataInArray(10) <= signed(sDataIn10);
  sDataInArray(11) <= signed(sDataIn11);
  sDataInArray(12) <= signed(sDataIn12);
  sDataInArray(13) <= signed(sDataIn13);
  sDataInArray(14) <= signed(sDataIn14);
  sDataInArray(15) <= signed(sDataIn15);
  sDataInArray(16) <= signed(sDataIn16);
  sDataInArray(17) <= signed(sDataIn17);
  sDataInArray(18) <= signed(sDataIn18);
  sDataInArray(19) <= signed(sDataIn19);
  sDataInArray(20) <= signed(sDataIn20);
  sDataInArray(21) <= signed(sDataIn21);
  sDataInArray(22) <= signed(sDataIn22);
  sDataInArray(23) <= signed(sDataIn23);
  sDataInArray(24) <= signed(sDataIn24);
  sDataInArray(25) <= signed(sDataIn25);
  sDataInArray(26) <= signed(sDataIn26);
  sDataInArray(27) <= signed(sDataIn27);
  sDataInArray(28) <= signed(sDataIn28);
  sDataInArray(29) <= signed(sDataIn29);
  sDataInArray(30) <= signed(sDataIn30);
  sDataInArray(31) <= signed(sDataIn31);

  -- Reshape the inputs from LV FPGA
  sDataInSpc <= sDataInArray(kInputSamplesPerCycle-1 downto 0);

  -- Instantiate the halfband filter
  --vhook_e FlxRioHbInterpMultipleInputSpc2xOc
  --vhook_a sReset to_boolean(sReset)
  --vhook_a sEnOutputFFs to_boolean(sEnOutputFFs)
  --vhook_a sInputValid to_boolean(sInputValid)
  --vhook_a sDataIn sDataInSpc
  --vhook_a sOutputValid sOutputValidBool
  --vhook_a sDataOut sDataOutSpc
  FlxRioHbInterpMultipleInputSpc2xOcx: entity work.FlxRioHbInterpMultipleInputSpc2xOc (RTL)
    generic map (
      kInputSamplesPerCycle => kInputSamplesPerCycle,  --integer range kMaxInputSpc:kMinInputSpc
      kCyclesPerInput       => kCyclesPerInput,        --integer range kMaxCyclesPerInput:kMinCyclesPerInput
      kUseDsp48e1           => kUseDsp48e1,            --boolean:=true
      kInterpolate          => kInterpolate)           --boolean:=false
    port map (
      SampleClk    => SampleClk,                 --in  std_logic
      SampleClk2x  => SampleClk2x,               --in  std_logic
      sReset       => to_boolean(sReset),        --in  boolean
      sEnOutputFFs => to_boolean(sEnOutputFFs),  --in  boolean
      sInputValid  => to_boolean(sInputValid),   --in  boolean
      sDataIn      => sDataInSpc,                --in  Signed18Array_t(kInputSamplesPerCycle-1:0)
      sOutputValid => sOutputValidBool,          --out boolean
      sDataOut     => sDataOutSpc);              --out Signed37Array_t(CalcOutputSamplesPerCycle(kInputSamplesPerCycle,kCyclesPerInput,kInterpolate)-1:0)


  -- Reshape outputs to pass back to LV FPGA
  ReshapeDataOut:
  process(sDataOutSpc)
  begin
    sDataOutArray <= (others=>(others=>'0'));
    sDataOutArray(kOutputSamplesPerCycle-1 downto 0) <= sDataOutSpc;
  end process ReshapeDataOut;

  sOutputValid <= to_stdlogic(sOutputValidBool);

  sDataOut0   <= std_logic_vector(sDataOutArray(0));
  sDataOut1   <= std_logic_vector(sDataOutArray(1));
  sDataOut2   <= std_logic_vector(sDataOutArray(2));
  sDataOut3   <= std_logic_vector(sDataOutArray(3));
  sDataOut4   <= std_logic_vector(sDataOutArray(4));
  sDataOut5   <= std_logic_vector(sDataOutArray(5));
  sDataOut6   <= std_logic_vector(sDataOutArray(6));
  sDataOut7   <= std_logic_vector(sDataOutArray(7));
  sDataOut8   <= std_logic_vector(sDataOutArray(8));
  sDataOut9   <= std_logic_vector(sDataOutArray(9));
  sDataOut10  <= std_logic_vector(sDataOutArray(10));
  sDataOut11  <= std_logic_vector(sDataOutArray(11));
  sDataOut12  <= std_logic_vector(sDataOutArray(12));
  sDataOut13  <= std_logic_vector(sDataOutArray(13));
  sDataOut14  <= std_logic_vector(sDataOutArray(14));
  sDataOut15  <= std_logic_vector(sDataOutArray(15));
  sDataOut16  <= std_logic_vector(sDataOutArray(16));
  sDataOut17  <= std_logic_vector(sDataOutArray(17));
  sDataOut18  <= std_logic_vector(sDataOutArray(18));
  sDataOut19  <= std_logic_vector(sDataOutArray(19));
  sDataOut20  <= std_logic_vector(sDataOutArray(20));
  sDataOut21  <= std_logic_vector(sDataOutArray(21));
  sDataOut22  <= std_logic_vector(sDataOutArray(22));
  sDataOut23  <= std_logic_vector(sDataOutArray(23));
  sDataOut24  <= std_logic_vector(sDataOutArray(24));
  sDataOut25  <= std_logic_vector(sDataOutArray(25));
  sDataOut26  <= std_logic_vector(sDataOutArray(26));
  sDataOut27  <= std_logic_vector(sDataOutArray(27));
  sDataOut28  <= std_logic_vector(sDataOutArray(28));
  sDataOut29  <= std_logic_vector(sDataOutArray(29));
  sDataOut30  <= std_logic_vector(sDataOutArray(30));
  sDataOut31  <= std_logic_vector(sDataOutArray(31));

end RTL;
