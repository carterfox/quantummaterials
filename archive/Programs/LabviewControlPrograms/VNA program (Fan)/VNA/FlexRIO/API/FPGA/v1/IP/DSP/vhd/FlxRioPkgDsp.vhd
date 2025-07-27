-------------------------------------------------------------------------------
--
-- File: FlxRioPkgDsp.vhd
-- Author: Dan Baker, Jose Centeno and Stephen Dark
-- Original Project: PXIe_5645R
-- Date: 8 July 2010
--
-------------------------------------------------------------------------------
-- (c) 2012 Copyright National Instruments Corporation
-- All Rights Reserved
-- National Instruments Internal Information
-------------------------------------------------------------------------------
--
-- Purpose:
--   Misc DSP tools
-------------------------------------------------------------------------------


library ieee,work;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;
  use work.FlxRioPkgNiUtilitiesDsp.all;

Package FlxRioPkgDsp is

  type Slv36Ary_t is array ( natural range <> ) of std_logic_vector(35 downto 0);
  
  -- Type created to support multiple samples per cycle.
  type Signed18Array_t is array ( natural range<> ) of signed(17 downto 0); -- S18.1

  function to_Sl25 (x : integer) return std_logic_vector;
  function to_Sl18 (x : integer) return std_logic_vector;
  function minimum (x, y : integer) return integer;
  function maximum (x, y : integer) return integer;
  function smaller (x : integer ; y : unsigned) return integer;
  function smaller (x : unsigned; y : integer ) return integer;
  function smaller (x, y : unsigned) return integer;
  function Log2Less1(arg : integer) return integer;

end FlxRioPkgDsp;

package body FlxRioPkgDsp is

  -- Returns x as 25-bit SLV
  function to_Sl25 (x : integer) return std_logic_vector is
  begin
    return std_logic_vector(to_unsigned(X, 25));
  end function to_Sl25;

  -- Returns x as 18-bit SLV
  function to_Sl18 (x : integer) return std_logic_vector is
  begin
    return std_logic_vector(to_unsigned(X, 18));
  end function to_Sl18;

  -- Returns the larger of x and y
  function minimum (x, y : integer) return integer is
  begin
    if x < y then
      return x;
    else
      return y;
    end if;
  end function minimum;

  -- Returns the larger of x and y
  function maximum (x, y : integer) return integer is
  begin
    if x > y then
      return x;
    else
      return y;
    end if;
  end function maximum;

  -- Returns the smaller of x and y
  function smaller (x: integer; y : unsigned) return integer is
  begin
    assert y'high < 32
    report "Unsigned range is too large to be compared to an integer"
    severity error;
    return smaller(x,to_integer(y));
  end function smaller;

  -- Returns the smaller of x and y
  function smaller (x: unsigned; y : integer) return integer is
  begin
    assert x'high < 32
    report "Unsigned range is too large to be compared to an integer"
    severity error;
    return smaller(to_integer(x),y);
  end function smaller;

  -- Returns the smaller of x and y
  function smaller (x, y : unsigned) return integer is
  begin
    assert x'high < 32 and y'high < 32
    report "Unsigned range is too large to return it's value as an integer"
    severity error;
    return smaller(to_integer(x),to_integer(y));
  end function smaller;

  -- Log2Less1 returns log(Arg)-1 for Arg>1 and returns 0 for Arg=1.
  -- Log2(positive Arg) in the FlxRioPkgNiUtilitiesDsp returns values from 0 to infinity.
  -- When we substract 1 to the result of Log2(positive Arg), for an Arg := 1
  -- then Log2(1) - 1 = -1. To avoid this negative result this function handles
  -- the Arg := 1 case with an exception.
  function Log2Less1(Arg : integer) return integer is
    variable ReturnVal : integer;
  begin
    if Arg = 1 then
      ReturnVal := 0;
    else
      ReturnVal := Log2(Arg) - 1;
    end if;
    return ReturnVal;
  end Log2Less1;
end FlxRioPkgDsp;
