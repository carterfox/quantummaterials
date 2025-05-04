-------------------------------------------------------------------------------
--
-- File: FlxRioPkgHbDec.vhd
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
-- Purpose:  This package file constains constants and types for the halfband 
--           decimator.
--
-------------------------------------------------------------------------------

library IEEE, work;
  use IEEE.std_logic_1164.all;
  use IEEE.numeric_std.all;
  use work.FlxRioPkgHbDecCoefficients.all;
  use work.FlxRioPkgNiUtilitiesDsp.all;

Package FlxRioPkgHbDec is

  -- Only 1, 2, 4, 8, and 16 input SPC are currently supported
  constant kMinSamplesPerCycle : integer := 1;
  constant kMaxSamplesPerCycle : integer := 16;
  
  -- Only 1, 2, and 4 cycles per input is currently supported
  constant kMinCyclesPerInput : integer := 1;
  constant kMaxCyclesPerInput : integer := 4;
  
  -- Only 2x overclocking is currently supported
  constant kOverclockingFactor : integer := 2;
  
  constant kNumCoefficients : integer := kHbDecCoefficients'length;
  constant kMidCoeffIndex : integer := kNumCoefficients / 2;
  -- There are 16 unique non-zero coefficients.  Taking advantage of symmetry,
  -- this means that we need 16 MACs (assuming no overclocking).
  constant kNumMacsPerFilter : integer := 16;
  constant kNumMacsPerFilter2xOc : integer := kNumMacsPerFilter / kOverclockingFactor;
  constant kDecimationFactor : integer := 2;
  constant kPipelineDelay : integer := 13;
      
  type Signed18Array_t is array( natural range <> ) of signed(17 downto 0);
  type Signed37Array_t is array( natural range <> ) of signed(36 downto 0);
  type Signed48Array_t is array( natural range <> ) of signed(47 downto 0);
  
  function CalcOutputSamplesPerCycle (InputSamplesPerCycle : integer) return integer;
  function CalcCycleCountLength (CyclesPerInput : integer; InputSamplesPerCycle : integer) return integer;
  function CalcNumOfMacs (CyclesPerInput : integer; InputSamplesPerCycle : integer) return integer;
      
end Package FlxRioPkgHbDec;

Package body FlxRioPkgHbDec is

  -- This function calculates the output samples per cycle
  function CalcOutputSamplesPerCycle (InputSamplesPerCycle : integer) return integer is
  begin
      if(InputSamplesPerCycle = 1) then
        return 1;
      else
        return  InputSamplesPerCycle / kDecimationFactor;
      end if;
  end function CalcOutputSamplesPerCycle;
  
  -- This function calculates the length of the counter that counts 
  -- the number of Clk cycles by each MAC used to calculate each output.
  function CalcCycleCountLength (CyclesPerInput : integer; InputSamplesPerCycle : integer) return integer is
  begin
    -- If kInputSamplesPerCycle > 1, then the length is 1 since we only have the two
    -- overclock cycles in each MAC to calculate each output.
    if(InputSamplesPerCycle > 1) then
      return 1;
    else
      return log2(CyclesPerInput*kOverclockingFactor*kDecimationFactor);
    end if;
  end function CalcCycleCountLength;

  -- This function calculates the number of MACs.
  function CalcNumOfMacs (CyclesPerInput : integer; InputSamplesPerCycle : integer) return integer is
  begin
    -- If kInputSamplesPerCycle > 1, then the number of MACs is simply equal to 
    -- kNumMacsPerFilter2xOc since we have to be able to calculate a new output  
    -- every 1x clock cycle.
    if(InputSamplesPerCycle > 1) then
      return kNumMacsPerFilter2xOc;
    else
      return kNumMacsPerFilter2xOc / CyclesPerInput / kDecimationFactor;
    end if; 
  end function CalcNumOfMacs;
  
end Package body FlxRioPkgHbDec;
