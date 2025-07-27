-------------------------------------------------------------------------------
--
-- File: FlxRioOverclockingSyncCounter.vhd
-- Author: Dan Baker and Jose Centeno
-- Original Project: PXIe_5645R
-- Date: 21 August 2012
--
-------------------------------------------------------------------------------
-- (c) 2012 Copyright National Instruments Corporation
-- All Rights Reserved
-- National Instruments Internal Information
-------------------------------------------------------------------------------
--
-- Purpose: This component implements a counter that lets you synchronize
--          data to a faster clock whose frequency is a multiple of the
--          data's original clock.
--          Use kOverclockFactor to specify the frequency relationship
--          between BaseClk and OverClk.
--
--          Use bStart to tell the FlxRioOverclockingSyncCounter when it is safe
--          to toggle internal states and outputs. You can hold bStart low
--          after downloading the FPGA image to keep this counter from
--          toggling any outputs or internal state signals until all the
--          clocks are stable. This feature is added to avoid problems when
--          BaseClk or Overclk come from derived clocks that can have an
--          unsafe startup.
--
--          oCount equals 0 at the rising edge of BaseClk and increments by 1
--          every OverClk cycle. One cycle after oCount reaches
--          kOverclockFactor - 1, a new rising edge of BaseClk will happen,
--          therefore oCount rolls back to 0. (See timing diagram below)
--
--          oCount needs some cycles after aReset to be synced correctly. During
--          these transition cycles oCountValid is false. oCount valid becomes
--          true when oCount is synced and starts counting.
--
--          oBaseClkEdgeNext is true the cycle before the rising edge of BaseClk.
--          oBaseClkEdgeNext can be used as an enable signal for any process
--          that needs to register BaseClk signals in the OverClk domain right
--          before the next BaseClk rising edge.
--
--          The following diagram illustrates the signals for a kOverclocking factor
--          of 3.
--                          ________          ________          ________
--          BaseClk      __|        |________|        |________|        |________|
--                          __    __    __    __    __    __    __    __    __
--          OverClk      __|  |__|  |__|  |__|  |__|  |__|  |__|  |__|  |__|  |__
--
--          oCount         |  0  |  0  |  0  |  0  |  1  |  2  |  0  |  1  |  2  |
--                                            ____________________________________
--          oCountValid  ____________________|
--                                      _____             _____             _____
--     oBaseClkEdgeNext  ______________|     |___________|     |___________|     |
--     (Note: oBaseClkEdgeNext is not guaranteed  to pulse for the first time before
--            oCountValid asserts. For example if kOverclockingFactor = 2 the first
--            oBaseClkEdgeNext will happen after oCountValid asserts.)
--
--          The outputs need 3 rising edges of BaseClk plus 2 Overclock cycles
--          after reset deasserts to sync properly.
-------------------------------------------------------------------------------


library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;
library work;
  use work.FlxRioPkgDsp.all;
  use work.FlxRioPkgNiUtilitiesDsp.all;

entity FlxRioOverclockingSyncCounter is
generic(
  kOverclockFactor    : in integer := 3;
  kCountMaxFanout     : in integer := 30);
port(
  aReset                : in boolean;
  BaseClk               : in std_logic;
  bStart                : in boolean := true;
  OverClk               : in std_logic;
  oCount                : out unsigned(log2less1(kOverclockFactor) downto 0) := (others=>'0');
  oCountValid           : out boolean;
  oBaseClkEdgeNext      : out boolean);
end FlxRioOverclockingSyncCounter;

-------------------------------------------------------------------------------
-- The strategy is simple.
--   1) Toggle a FF every cycle in the BaseClk domain.
--   2) Detect the edges of the Toggling FF.
--   3) Delay the edge detection pulse enough cycles to properly reinitialize
--      the counter, assert oCountValid and  pulse oBaseClkEdgeNext.
-------------------------------------------------------------------------------
architecture RTL of FlxRioOverclockingSyncCounter is
  signal bToggleFf    : boolean := false;
  -- Determine the size of the FF chain.
  -- We want to avoid logic with inputs from the two clock domains. Clock skew
  -- makes timing hard to meet. Therefore we need at least two FFs to detect
  -- an edge in the Toggling FF.
  signal oToggleFf     : boolean := false;
  signal oToggleFFPipe : boolean := false;
  -- Create a Shift Register to pipeline delayed versions of the edge detection.
  -- (We declare at least two flip flops to avoid out of bounds indexing in the Shift
  -- register assignment)
  constant  kDelayChainSize : integer := Larger (2,kOverclockFactor);
  -- The signal oEdgeDetectPipe splits itself across a synchronous process. bit0 is a
  -- combinatorial signal and vsmake discourages this design approach.
  signal    oEdgeDetectPipe : BooleanVector(kDelayChainSize - 1  downto 0)
                            := (others=> false);
  -- oEdgeDetectPipe(0) will pulse one cycle after a rising edge of BaseClk.
  -- oBaseClkEdgeNext should pulse kOverclockFactor - 2 cycles later, therefore we
  -- need to drive it from oEdgeDetectPipe(kOverclockFactor - 3). The mod operation
  -- is used to handle cases where kOverclockFactor is less than 3.
  constant  kBaseClkEdgeNextIndex : integer
                                  := (kOverclockFactor - 3) mod kOverclockFactor;
  -- oCount is restarted one clock cycle after oBaseClkEdgeNext pulses.
  constant  kRestartCountIndex    : integer
                                  := (kOverclockFactor - 2) mod kOverclockFactor;

  -- Create local signals for outputs we will read inside this module.
  signal    oCountLcl       : unsigned(oCount'range) := (others => '0');
  signal    oCountValidLcl  : boolean := false;

  -- Create sync Reset Signals.
  signal    bEnable_ms       : boolean := false;
  signal    bEnable          : boolean := false;

  -- The FlxRioOverclockingSyncCounter can be used on many components at the same time
  -- sharing the same Clock and Reset inputs. This implies the compile tools may
  -- merge all the FlxRioOverclockingSyncCounter into a single component and try to
  -- connect its outputs to FFs on very distant Slices on the FPGA. To avoid
  -- this we use a keep attribute. This will make sure every time the
  -- FlxRioOverclockingSyncCounter is instantiated a new oCountLcl is created.
  attribute keep : string;
  attribute keep of oCountLcl: signal is "true";

  -- Some components use oCount to drive multiple signals. Driving too many signals
  -- makes placing and routing more difficult.
  -- The max_fanout attribute allow each instance of FlxRioOverclockingSyncCounter to
  -- choose a maximum fan out for oCount.
  attribute max_fanout: integer;
  attribute max_fanout of oCountLcl : signal is kCountMaxFanout;

begin
  -------------------------------------------------------------------------------
  -- 1) Create a toggle FF.  This is used to show where BaseClk edge is in the
  --    OverClk domain
  -------------------------------------------------------------------------------
  ToggleFf:
  process(aReset, BaseClk) is
  begin
    if aReset then
      bEnable_ms <= false;
      bEnable    <= false;
      bToggleFf  <= false;
    elsif rising_edge(BaseClk) then
      if bStart then
        bEnable_ms <= true;
      end if;
      bEnable    <= bEnable_ms;
      -- We don't want bToggleFf to change immediately out of aReset to avoid
      -- metastability problems.
      if bEnable then
        bToggleFf <= not bToggleFf;
      end if;
    end if;
  end process ToggleFf;

  -------------------------------------------------------------------------------
  -- 2) Detect the edges of the Toggling FF.
  -- 3) Delay the edge detection pulse enough cycles to properly reinitialize
  --    the counter, assert oCountValid and  pulse oBaseClkEdgeNext.
  -------------------------------------------------------------------------------
  -- oEdgeDetectPipe(0) is combinatorial and not a Flop. we get a vsmake warning that
  -- it is not properly reset to the correct value even though it is not reset at all.
  -- we put vhook_nowarn on the Counter process but thats not safe.
  -- TODO: this code should be rewritten when/if it needs to be modified.
  --vhook_nowarn Counter
  Counter:
  process(aReset, OverClk) is
  begin
    if aReset then
      oToggleFf       <= false;
      oToggleFFPipe   <= false;
      oEdgeDetectPipe(oEdgeDetectPipe'high downto 1) <= (others => false);
      oBaseClkEdgeNext <= false;
      oCountLcl      <= (others => '0');
      oCountValidLcl <= false;

    elsif rising_edge(OverClk) then
      -- This clock domain transfer should be handled properly by the Xilinx
      -- tools, because they are related clock domains.
      oToggleFf     <= bToggleFf;
      oToggleFfPipe <= oToggleFf;

      -- Outside this process: oEdgeDetectPipe(0) := oToggleFf xor oToggleFfPipe
      -- Propagate an edge detected through the oEdgeDetectPipe FF chain.
      oEdgeDetectPipe(oEdgeDetectPipe'high downto 1)  <= oEdgeDetectPipe(oEdgeDetectPipe'high - 1 downto 0);

      -- Create the oBaseClkEdgeNext. It will be true only for one cycle, the cycle
      -- before the next BaseClk rising edge.
      oBaseClkEdgeNext <= oEdgeDetectPipe(kBaseClkEdgeNextIndex);

      -- Create the counter. Restart it to 0 after a rising edge of BaseClk
      if oEdgeDetectPipe(kRestartCountIndex) then
        oCountLcl      <= (others => '0');
        oCountValidLcl <= true;

      -- !COUNTER STARTUP! oCountLcl cannot start immediately after aReset
      -- deasserts because oEdgeDetectPipe and oCountValidLcl are false while
      -- bToggleFf is disabled; thus, the asynchronous reset is safe.
      elsif oCountValidLcl then
        oCountLcl <= oCountLcl + 1;
      end if;
    end if;
  end process Counter;

  -- Detect an edge on oToggleFf.
  oEdgeDetectPipe(0) <= (oToggleFf xor oToggleFfPipe);

  -- Assign the outputs
  oCountValid <= oCountValidLcl;
  oCount      <= oCountLcl;
end RTL;
