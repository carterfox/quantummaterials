-------------------------------------------------------------------------------
--
-- File: FlxRioPkgHbInterp.vhd
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
-- Purpose:  This package file contains constants and types for the halfband 
--           interpolator.
--
-------------------------------------------------------------------------------

library IEEE, work;
  use IEEE.std_logic_1164.all;
  use IEEE.numeric_std.all;
  use work.FlxRioPkgHbInterpCoefficients.all;
  use work.FlxRioPkgNiUtilitiesDsp.all;

Package FlxRioPkgHbInterp is

  -- Only 1, 2, 4, 8, and 16 input SPC are currently supported
  constant kMinInputSpc  : integer := 1;
  constant kMaxInputSpc  : integer := 32;
  constant kMinOutputSpc : integer := 1;
  constant kMaxOutputSpc : integer := 32;
  
  -- Only 1, 2, and 4 cycles per input is currently supported
  constant kMinCyclesPerInput : integer := 1;
  constant kMaxCyclesPerInput : integer := 8;
  
  -- Only 2x overclocking is currently supported
  constant kOverclockingFactor : integer := 2;
  
  constant kNumInterpCoefficients : integer := kHbInterpCoefficients'length;
  constant kNumDecCoefficients : integer := kHbDecCoefficients'length;
  constant kMidCoeffIndex   : integer := kNumDecCoefficients / 2;
  
  -- There are 16 unique non-zero coefficients.  Taking advantage of symmetry,
  -- this means that we need 16 MACs (assuming no overclocking).
  -- Due to symmetry and ever other coefficient being zero,
  -- there are (#Coeff+1)/4 unique non-zero coefficients in any generic even order
  -- halfband filter not including the center tap. Including the center tap, this becomes 
  -- 1+(#Coeff+1)/4. For the current fixed filter, there are 59 coefficients.
  constant kNumMacsPerFilter : integer := 16;
  constant kNumMacsPerFilter2xOc : integer := kNumMacsPerFilter / kOverclockingFactor;
  constant kDecimationFactor : integer := 2;
  constant kInterpolationFactor : integer := 2;
  constant kPipelineDelay : integer := 13;
      
  type Signed18Array_t is array( natural range <> ) of signed(17 downto 0);
  type Signed37Array_t is array( natural range <> ) of signed(36 downto 0);
  type Signed48Array_t is array( natural range <> ) of signed(47 downto 0);
  
  function CalcOutputSamplesPerCycle (InputSamplesPerCycle : integer; 
                                      CyclesPerInput       : integer; 
                                      IsInterpolation      : boolean) return integer;
  function CalcNumSingleFilters (InputSamplesPerCycle : integer;
                                 CyclesPerInput       : integer; 
                                 IsInterpolation      : boolean) return integer;
  function CalcCycleCountLength (CyclesPerInput       : integer; 
                                 InputSamplesPerCycle : integer;
                                 IsInterpolation      : boolean) return integer;
  function CalcNumOfMacs (InputSamplesPerCycle : integer;
                          CyclesPerInput       : integer; 
                          IsInterpolation      : boolean) return integer;
      
end Package FlxRioPkgHbInterp;

Package body FlxRioPkgHbInterp is

  -- This function calculates the output samples per cycle
  -- !!!Try seeing if real data types will work here and still synthesize
  function CalcOutputSamplesPerCycle (InputSamplesPerCycle : integer;
                                      CyclesPerInput       : integer; 
                                      IsInterpolation      : boolean) return integer is
    variable OutputSamplesPerCycle : integer := 1;
  begin
    if(IsInterpolation) then
      OutputSamplesPerCycle := (2*InputSamplesPerCycle)/CyclesPerInput;
    else
      OutputSamplesPerCycle := (InputSamplesPerCycle/2)/CyclesPerInput;
    end if;

    if (OutputSamplesPerCycle < 1) then 
      return 1;
    else
      return OutputSamplesPerCycle;
    end if;      
  end function CalcOutputSamplesPerCycle;
  
  -- The number of single filters for interpolation is half since the
  -- center tap causes the input data to be pipelined along to become
  -- half of the needed output data.
  function CalcNumSingleFilters (InputSamplesPerCycle : integer;
                                 CyclesPerInput       : integer;
                                 IsInterpolation      : boolean) return integer is
    variable OutputSamplesPerCycle : integer := 
      CalcOutputSamplesPerCycle(InputSamplesPerCycle,CyclesPerInput,IsInterpolation);
  begin
  
    if OutputSamplesPerCycle=1 then
      return 1;
    end if;
  
    if(IsInterpolation) then
      return OutputSamplesPerCycle/2;
    else 
      return OutputSamplesPerCycle;
    end if;    
  end function CalcNumSingleFilters;
  
  -- This function calculates the length of the counter that counts 
  -- the number of Clk cycles by each MAC used to calculate each output.
  function CalcCycleCountLength (CyclesPerInput       : integer; 
                                 InputSamplesPerCycle : integer; 
                                 IsInterpolation      : boolean) return integer is
  begin

    if(InputSamplesPerCycle > 1) then
      return 1;
    elsif(InputSamplesPerCycle = 1 and IsInterpolation and CyclesPerInput = 1) then
      return 1;
    elsif IsInterpolation then
      return log2(CyclesPerInput*kOverclockingFactor);
    else
      return log2(CyclesPerInput*kOverclockingFactor*kDecimationFactor);
    end if;
  
    -- If kInputSamplesPerCycle > 1, then the length is 1 since we only have the two
    -- overclock cycles in each MAC to calculate each output.
    -- if(InputSamplesPerCycle > 1) then
      -- return 1;
    -- else
      -- return log2(CyclesPerInput*kOverclockingFactor*kDecimationFactor);
    -- end if;
  end function CalcCycleCountLength;

  -- This function calculates the number of MACs.
  function CalcNumOfMacs (InputSamplesPerCycle : integer;
                          CyclesPerInput       : integer; 
                          IsInterpolation      : boolean) return integer is
  begin
  
    if IsInterpolation then
      if(InputSamplesPerCycle > 1) then
        return kNumMacsPerFilter2xOc;
      else
        return kNumMacsPerFilter2xOc / CyclesPerInput;
      end if;
      
    else -- Decimation
      -- If kInputSamplesPerCycle > 1, then the number of MACs is simply equal to 
      -- kNumMacsPerFilter2xOc since we have to be able to calculate a new output  
      -- every 1x clock cycle.
      if(InputSamplesPerCycle > 1) then
        --This is really the same as below except CPI=1 and kDecimationFactor
        --is taken into account be having InputSpc/DecimationFactor single filters.
        return kNumMacsPerFilter2xOc;
      else
        return kNumMacsPerFilter2xOc / CyclesPerInput / kDecimationFactor;
      end if; 
    end if;
  end function CalcNumOfMacs;
  
end Package body FlxRioPkgHbInterp;
