
library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;

library work; 
use work.FlxRioHbInterpMultipleInputSpc2xOcIpin;

entity FlxRio00 is
  port (
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
end entity FlxRio00;

architecture RTL of FlxRio00 is

begin  -- architecture RTL

  Ipin_1: entity work.FlxRioHbInterpMultipleInputSpc2xOcIpin
    generic map (
      kInputSamplesPerCycle => 8,
      kCyclesPerInput       => 1,
      kUseDsp48e1           => true,
      kInterpolate          => true)
    port map (
      SampleClk    => SampleClk,
      SampleClk2x  => SampleClk2x,
      sReset       => sReset,
      sEnOutputFFs => sEnOutputFFs,
      sInputValid  => sInputValid,
      sDataIn0     => sDataIn0,
      sDataIn1     => sDataIn1,
      sDataIn2     => sDataIn2,
      sDataIn3     => sDataIn3,
      sDataIn4     => sDataIn4,
      sDataIn5     => sDataIn5,
      sDataIn6     => sDataIn6,
      sDataIn7     => sDataIn7,
      sDataIn8     => sDataIn8,
      sDataIn9     => sDataIn9,
      sDataIn10    => sDataIn10,
      sDataIn11    => sDataIn11,
      sDataIn12    => sDataIn12,
      sDataIn13    => sDataIn13,
      sDataIn14    => sDataIn14,
      sDataIn15    => sDataIn15,
      sDataIn16    => sDataIn16,
      sDataIn17    => sDataIn17,
      sDataIn18    => sDataIn18,
      sDataIn19    => sDataIn19,
      sDataIn20    => sDataIn20,
      sDataIn21    => sDataIn21,
      sDataIn22    => sDataIn22,
      sDataIn23    => sDataIn23,
      sDataIn24    => sDataIn24,
      sDataIn25    => sDataIn25,
      sDataIn26    => sDataIn26,
      sDataIn27    => sDataIn27,
      sDataIn28    => sDataIn28,
      sDataIn29    => sDataIn29,
      sDataIn30    => sDataIn30,
      sDataIn31    => sDataIn31,
      sOutputValid => sOutputValid,
      sDataOut0    => sDataOut0,
      sDataOut1    => sDataOut1,
      sDataOut2    => sDataOut2,
      sDataOut3    => sDataOut3,
      sDataOut4    => sDataOut4,
      sDataOut5    => sDataOut5,
      sDataOut6    => sDataOut6,
      sDataOut7    => sDataOut7,
      sDataOut8    => sDataOut8,
      sDataOut9    => sDataOut9,
      sDataOut10   => sDataOut10,
      sDataOut11   => sDataOut11,
      sDataOut12   => sDataOut12,
      sDataOut13   => sDataOut13,
      sDataOut14   => sDataOut14,
      sDataOut15   => sDataOut15,
      sDataOut16   => sDataOut16,
      sDataOut17   => sDataOut17,
      sDataOut18   => sDataOut18,
      sDataOut19   => sDataOut19,
      sDataOut20   => sDataOut20,
      sDataOut21   => sDataOut21,
      sDataOut22   => sDataOut22,
      sDataOut23   => sDataOut23,
      sDataOut24   => sDataOut24,
      sDataOut25   => sDataOut25,
      sDataOut26   => sDataOut26,
      sDataOut27   => sDataOut27,
      sDataOut28   => sDataOut28,
      sDataOut29   => sDataOut29,
      sDataOut30   => sDataOut30,
      sDataOut31   => sDataOut31);

end architecture RTL;
