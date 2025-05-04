
library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;

library work; 
use work.FlxRioHbDecMultipleInputSpc2xOcIpin;

entity FlxRio01 is
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
    sOutputValid : out std_logic;
    sDataOut0    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut1    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut2    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut3    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut4    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut5    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut6    : out std_logic_vector(36 downto 0);   -- S37.2
    sDataOut7    : out std_logic_vector(36 downto 0));  -- S37.2
end entity FlxRio01;

architecture RTL of FlxRio01 is

begin  -- architecture RTL
  FlxRioHbDecMultipleInputSpc2xOcIpin_1: entity work.FlxRioHbDecMultipleInputSpc2xOcIpin
    generic map (
      kInputSamplesPerCycle => 16,  -- note this was wrong in the DSP
                                    -- instantiation, which is super scary.
      kCyclesPerInput       => 1,
      kUseDsp48e1           => true)
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
      sOutputValid => sOutputValid,
      sDataOut0    => sDataOut0,
      sDataOut1    => sDataOut1,
      sDataOut2    => sDataOut2,
      sDataOut3    => sDataOut3,
      sDataOut4    => sDataOut4,
      sDataOut5    => sDataOut5,
      sDataOut6    => sDataOut6,
      sDataOut7    => sDataOut7);

end architecture RTL;
