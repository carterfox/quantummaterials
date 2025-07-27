-------------------------------------------------------------------------------
--
-- File: FlxRioDFlopDsp.vhd
-- Author: Craig Conway
-- Original Project: NiCores
-- Date: 7 April 2010
--
-------------------------------------------------------------------------------
-- (c) 2010 Copyright National Instruments Corporation
-- All Rights Reserved
-- National Instruments Internal Information
-------------------------------------------------------------------------------
--
-- Purpose:
--    This creates a flip-flop using the Xilinx
-- FDCPE to try to guarantee the clock enable and
-- get a post-synthesis name that is easier to find.
--
-------------------------------------------------------------------------------

library ieee;
  use ieee.std_logic_1164.all;

library work;
  use work.FlxRioPkgNiUtilitiesDsp.all;

library UNISIM;
  use UNISIM.vcomponents.all;

entity FlxRioDFlopDsp is
  generic (kResetVal : std_logic := '0');
  port (
    aReset, cEn  : in boolean;
    Clk, cD   : in std_logic;
    cQ   : out std_logic := kResetVal
  );
  attribute direct_enable : boolean;
  attribute direct_enable of cEn : signal is true;
end FlxRioDFlopDsp;

architecture rtl of FlxRioDFlopDsp is

  --vhook_sigstart
  --vhook_sigend

  function kGetStr(ResetVal : std_logic) return bit is
  begin
    if ResetVal='0' then return '0'; else return '1'; end if;
  end function kGetStr;

begin

  GenClr: if kResetVal='0' generate

    --vhook_i FDCE FFcx
    --vhook_a INIT open
    --vhook_h IS_CLR_INVERTED
    --vhook_h IS_C_INVERTED
    --vhook_h IS_D_INVERTED
    --vhook_a CLR To_StdLogic(aReset)
    --vhook_a C Clk
    --vhook_a CE To_StdLogic(cEn)
    --vhook_a D cD
    --vhook_a Q cQ
    FFcx: FDCE
      generic map (INIT => open)  --bit:='0'
      port map (
        Q   => cQ,                   --out std_ulogic:=TO_X01(INIT)
        C   => Clk,                  --in  std_ulogic
        CE  => To_StdLogic(cEn),     --in  std_ulogic
        CLR => To_StdLogic(aReset),  --in  std_ulogic
        D   => cD);                  --in  std_ulogic

  end generate GenClr;

  GenSet: if kResetVal='1' generate

    --vhook_i FDPE FFpx
    --vhook_a INIT open
    --vhook_h IS_C_INVERTED
    --vhook_h IS_D_INVERTED
    --vhook_h IS_PRE_INVERTED
    --vhook_a PRE To_StdLogic(aReset)
    --vhook_a C Clk
    --vhook_a CE To_StdLogic(cEn)
    --vhook_a D cD
    --vhook_a Q cQ
    FFpx: FDPE
      generic map (INIT => open)  --bit:='1'
      port map (
        Q   => cQ,                   --out std_ulogic:=TO_X01(INIT)
        C   => Clk,                  --in  std_ulogic
        CE  => To_StdLogic(cEn),     --in  std_ulogic
        D   => cD,                   --in  std_ulogic
        PRE => To_StdLogic(aReset)); --in  std_ulogic

  end generate GenSet;

end rtl;

-- The following comment is a checksum VScan uses to determine whether this
-- file has been modified.  Please don't try to get around it.  It's there
-- for a reason.
--VScan_CS 1518044
