-------------------------------------------------------------------------------
--
-- File: I2cBridge.vhd
-- Author: Tony Liechty
-- Original Project: Chimera
-- Date: 12 May 2020
--
-------------------------------------------------------------------------------
-- (c) 2012 Copyright National Instruments Corporation
-- All Rights Reserved
-- National Instruments Internal Information
-------------------------------------------------------------------------------
-- Purpose:
--------------------------
--  This core has 2 main purposes:
--  1)  Monitor I2C transactions present on PortA.
--    The core always has this purpose independent of if the bridge is enabled or disabled
--    VIA cConnectBridge.  This can be useful if just monitoring of I2C traffic is needed
--    without any bridging.  NOTE:  Transactions on PortB are not monitored.
--
--    Bus monitor operation:  cBusMonWordValid pulses high for one clock cycle whenever
--    cBusMonWord, cBusMonWordIsHeader, cBusMonWordReadWrite_n, and cBusMonWordAck are valid.
--    These contain the low level I2C packet information for the I2C data, if that data is a header,
--    or data packet, if the data is read or write data, and if the current data has been acked.
--
--  2)  Bridge I2C transactions between PortA and PortB
--    The main reason for purpose 2 is to support the TAP use case.  In TAP mode
--    I2C transactions need to cross from the ECE's deserializer, to Chimera
--    serializer, into the FPGA, across the bridge, into the Chimera's de-serializer
--    and into the camera's serializer as if the ECU was connected directly to the
--    camera.  The I2C transaction is forwarded on a bit by bit basis to reduce latency
--    and increase the apearence that the ECU is directly connected to the camera.  The Master
--    may be on either PortA or PortB side as the core auto detects which side the master is on.
--    The bus monitor is only on PortA, however when the bridge is connected PortA and PortB
--    contain the same information in normal operation.
--
--  CAUTION on enabling the bridge and initiating I2C transactions from the FPGA:
--  The core does support I2C transactions initiated both within the internal
--  FPGA master, or external master, however the bridging functionality is only
--  intended to be used with external I2C masters for Chimera.  The reason for this is
--  that initiating an I2C transaction from within the FPGA with the bridge connected
--  can cause the transaction to go to both the serializer and de-serizer, and in
--  some cases (case of Maxim) both respond and cause contention on the bus.  Therefore
--  if initiating I2C transactions from the FPGA, ensure that cConnectBridge is false.
--
--  IMPORTANT:  Therefore it is important to only enable the bridge when all I2C communcation
--  from the FPGA master is complete.  You can still use the monitor functionality in this case
--  as the monitor functionality is still enabled when cConnectBridge is false.
--
--------------------------
--  Theory of operation:
--------------------------
--  General operation:  The core works by determining on a bit by bit basis the direction
--  that the bus should be connected and then connecting the bridge in the appropriate
--  direction (master to slave or slave to master).  For example, the side of the bridge
--  that initiates a start condition is considered the master.  When start is seen, the
--  bridge is connected from the master to the slave.  Also, for example, if the monitor
--  notices that the I2C read_write_n bit is set to '1' it knows that the following data
--  bytes will be from slave to master and that the ack bit for those will be master to slave.
--  By doing this on a bit by bit basis, no buffering is required and minimal latency is
--  acheived.
--
--  Note about the ACK bit:
--  During the ack bit this component forces clock low to both sides for the
--  measured low time in the previous bit.  This is done because both master and
--  slave drive clock during the ack bit and we must choose one, not both of them
--  to listen to.  We choose to therefore guarantee that the master low time occurs
--  by driving both sides low for at least that amount of time, and then listen
--  to the slave for when it is done clock stretching.  It is not ideal, but most ideal
--  method that could be thought up of, and works for our specific situation.  The assumption
--  is that the master drives the clock low the same amount of time as the previous bit,
--  which was shown to be true for our situation.
--
--  We only need to hold the clock low for the longest clock fall to data out time
--  plus required setup time.  For fast mode slave this 250ns, 100ns, or 50ns depending
--  on the I2C mode you are in.  Master clock to out time is not defined by I2C spec,
--  other than it must be quick enough to meet the setup time of the slave device.
--  This makes it tricky to know how long to hold it for, which is another reason why
--  we just drive it low for the measured low time of the previous bit.  Our assumption
--  is that the low time of the previous bit is long enough to also guarantee setup time
--  of the ack bit.  This makes the core flexible over different I2C frequencies.
--
--
--
--------------------------
-- Assumptions:
--------------------------
--    -Clock stetching only occurs durin the Ack bit.
--
--    -Clock low time of bit before the ack bit will be a sufficent amount of time to
--     guarantee that the ack bit will be clocked out after clock falling edge.
--
--    -Clock low time will be no longer than 1.34 seconds when using a 100Mhz top
--     level clock.  Scale 1.34 seconds apropriately if using a different frequency
--     clock.
--
--------------------------
-- Not currently supported:
--------------------------
--    -Filtering of I2c signals.
--vhook_warn test 10-bit addressing.  This core should support this, but needs tested.
--vhook_warn test this core with a multi-master when the multi master resides on the same side (both on PortA or both on PortB) and bridge disabled.  This core should support this, but not if they are on opposite sides.
--    -Error reporting if a non multiple of 9 bits is sent received between start and start/stop.
--
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------

Library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.MATH_REAL.all;

library work;

entity I2cBridge is
port(
  ------------------------------------------------
  --Clock and reset
  ------------------------------------------------
  Clk            : in std_logic;
  cReset        : in std_logic; --synchronous reset

  ------------------------------------------------
  --Bridge enable signal
  ------------------------------------------------
  cConnectBridge : in std_logic;

  ------------------------------------------------
  --I2c Signals
  ------------------------------------------------
  --Inputs from external pin, already syncronized to Clk
  cPortASclIn     : in std_logic;
  cPortASdaIn     : in std_logic;
  cPortBSclIn     : in std_logic;
  cPortBSdaIn     : in std_logic;

  --Open Drain outputs.  '0' is drive low.  '1' is let float.
  cPortASclTriOut    : out std_logic;
  cPortASdaTriOut    : out std_logic;
  cPortBSclTriOut    : out std_logic;
  cPortBSdaTriOut    : out std_logic;

  ------------------------------------------------
  --I2C Bus Monitor signals
  ------------------------------------------------
  --These pulse high for one Clk cycle when a start or stop condition is seen.
  cBusMonStart           : out std_logic;
  cBusMonStop            : out std_logic;

  --cBusMonWordValid pulses high for one clock cycle when a new word is observed
  --cBusMonWord* is valid with cBusMonWordValid is high.  Though it should
  --be valid between cBusMonWordValid cycles, this has not been tested and therefore
  --should not be relied on it being valid elsewhere.
  cBusMonWordValid       : out std_logic;
  --Data contents.  Bits 8 downto 1 of data from I2C spec
  cBusMonWord            : out std_logic_vector(7 downto 0);
  --Is this the first byte after a start condition.
  cBusMonWordIsHeader    : out std_logic;
  --Is the current word a write (to slave), or read (to master) transaction.
  cBusMonWordReadWrite_n : out std_logic;
  --Is the current word Acked (Ack bit per I2C Spec)
  cBusMonWordAck         : out std_logic
);
end I2cBridge;

architecture arch of I2cBridge is

  --------------------------------------------------------------
  --Combinatory I2C Status signals
  --------------------------------------------------------------
  signal cPortAStart, cPortBStart, cPortAStop, cPortBStop : boolean;
  signal cSclLow, cSclHigh, cSdaHigh, cStart, cStop : boolean;

  --These are combinatorial rather than in state machine to reduce latency by one clock cycle
  --Actual output signals for scl and sda are registered based off of these.
  type I2cSclDirection_t is (HIGH_Z, MASTER_TO_SLAVE, SLAVE_TO_MASTER, FORCE_SCL_LOW_BOTH_SIDES);
  signal cSclDirection : I2cSclDirection_t;

  type I2cSdaDirection_t is (HIGH_Z, MASTER_TO_SLAVE, SLAVE_TO_MASTER);
  signal cSdaDirection : I2cSdaDirection_t;

  --------------------------------------------------------------
  --Registered I2C Status signals
  --------------------------------------------------------------
  signal cPortAisMaster, cAck, cReadWrite_n : boolean;
  signal cHeaderWord : boolean := true;
  signal cWord : std_logic_vector(7 downto 0);

  --used to detect rising/falling edges of Sda
  signal cPortASdaInDelay, cPortBSdaInDelay : std_logic;
  signal cPortASclInDelay, cPortBSclInDelay : std_logic;

  --------------------------------------------------------------
  --I2C Bit information
  --------------------------------------------------------------
  --Using -1 as an ack bit as data is sent on bus MSB first, followed by Ack, hence last bit being 0 index, and Ack being -1
  signal cCurBit : integer  range -1 to 7;
  constant kFirstBit : integer := 7;
  constant kBitBeforeAckBit : integer := 0;
  constant kAckBit : integer := -1;
  constant kReadWriteBit : integer := 0;

  --------------------------------------------------------------
  --Track low time and enforce this low time during ack bit
  --------------------------------------------------------------
  signal cCounter, cRequiredSclLowTicks : unsigned(26 downto 0);

  --------------------------------------------------------------
  --State machine signal
  --------------------------------------------------------------
  type State_t is (I2CStopped_WaitForStart, I2CStarted_WaitingForSclLow, I2cSclLow_ForceSclLowBothSides, I2cSclLow_WaitForSclHigh, I2cSclHigh_WaitForLowStopOrStart, I2CStopped_WaitForSdaTristateOnPortAandB);
  signal cState : State_t;

  --Copied from PkgNiUtilities so that we don't have that dependency to allow flexibility when building within LabviewFPGA
  function to_StdLogicLocal(b : boolean) return std_ulogic is
  begin
    if b then
      return '1';
    else
      return '0';
    end if;
  end to_StdLogicLocal;

  --Copied from PkgNiUtilities so that we don't have that dependency to allow flexibility when building within LabviewFPGA
  function to_BooleanLocal (s : std_ulogic) return boolean is
  begin
    return (To_X01(s)='1');
  end to_BooleanLocal;

begin

  -----------------------------------------------------------------------------
  -- Generate I2C Start Flags
  -----------------------------------------------------------------------------
  -- I2C Start condition = Falling Edge on cSDA while cSCL is high and not currently changing
  -- Not currently changing condition is there in case master changes SCL and SDA at same time
  -- or due to slow sampling of IO the signals get detected as changing at the same time
  cPortAStart <= (cPortASclIn = '1' and cPortASclInDelay = '1') and (cPortASdaIn = '0' and cPortASdaInDelay = '1');
  cPortBStart <= (cPortBSclIn = '1' and cPortBSclInDelay = '1') and (cPortBSdaIn = '0' and cPortBSdaInDelay = '1');

  --Making it so that the bus monitor only reports a single start condition.
  --Rather than one for each side of the bridge.
  cBusMonStart <= to_StdLogicLocal(cStart)            when cState = I2CStopped_WaitForStart --Look at both sides when in stopped case
                  else to_StdLogicLocal(cPortAStart)  when cPortAisMaster                   --Only look at Master side for start conditions
                  else to_StdLogicLocal(cPortBStart);                                       --Only look at Master side for start conditions

  -----------------------------------------------------------------------------
  -- Generate I2C Stop Flags
  -----------------------------------------------------------------------------
  -- I2C Stop condition = Rising Edge on cSDA while cSCL is high and has not just changed
  cPortAStop <=  (cPortASclIn = '1' and cPortASclInDelay = '1') and (cPortASdaIn = '1' and cPortASdaInDelay = '0');
  cPortBStop <=  (cPortBSclIn = '1' and cPortBSclInDelay = '1') and (cPortBSdaIn = '1' and cPortBSdaInDelay = '0');

  --Making it so that the bus monitor only reports a single stop condition,
  --Rather than one for each side of the bridge.
  cBusMonStop <= to_StdLogicLocal(cStop)      when cState = I2CStopped_WaitForStart --Look at both sides when in stopped case
            else to_StdLogicLocal(cPortAStop) when cPortAisMaster                   --Only look at Master side for stop conditions
            else to_StdLogicLocal(cPortBStop);                                      --Only look at Master side for stop conditions


  -----------------------------------------------------------------------------
  -- Combinatory status signals
  -----------------------------------------------------------------------------
  --Create combined signals for both A and B side if brige is enabled
  --if bridge is disabled, only look at the A side for I2C monitoring
  cSclLow  <= cPortASclIn = '0' and cPortBSclIn = '0' when cConnectBridge = '1' else cPortASclIn = '0';
  cSclHigh <= cPortASclIn = '1' and cPortBSclIn = '1' when cConnectBridge = '1' else cPortASclIn = '1';
  cSdaHigh <= cPortASdaIn = '1' and cPortBSdaIn = '1' when cConnectBridge = '1' else cPortASdaIn = '1';

  cStart <= cPortAStart or cPortBStart when cConnectBridge = '1' else cPortAStart;
  cStop  <= cPortAStop  or cPortBStop  when cConnectBridge = '1' else cPortAStop;


  Statemachine: process(Clk)
    variable cNextReadWriteVar_n : boolean;
    variable cNextBitVar : integer  range -1 to 7;
  begin
  if rising_edge(Clk) then
    if cReset = '1' then
      cPortASdaInDelay <= '1';
      cPortBSdaInDelay <= '1';
      cPortASclInDelay <= '1';
      cPortBSclInDelay <= '1';

      cCounter <= (others => '0');
      cRequiredSclLowTicks <= (others => '0');

      cCurBit <= kFirstBit;
      cPortAisMaster <= false;
      cHeaderWord <= true;
      cReadWrite_n <= false;
      cWord <= (others => '0');
      cAck <= false;
      cState <= I2CStopped_WaitForStart;

      cBusMonWord <= (others => '0');
      cBusMonWordIsHeader <= '0';
      cBusMonWordAck <= '0';
      cBusMonWordReadWrite_n <= '0';
      cBusMonWordValid <= '0';
    else
      cPortASdaInDelay <= cPortASdaIn;
      cPortBSdaInDelay <= cPortBSdaIn;
      cPortASclInDelay <= cPortASclIn;
      cPortBSclInDelay <= cPortBSclIn;

      --Counter gets reset to zero unless otherwise counting
      cCounter <= (others => '0');
      --This signal is a pulsed signal out of the core
      cBusMonWordValid <= '0';


      case cState is
        ----------------------------------------------------------------------------------------------
        when I2CStopped_WaitForStart =>
        ----------------------------------------------------------------------------------------------

          cHeaderWord <= true;
          cCurBit <= kFirstBit;
          cReadWrite_n <= false;
          cRequiredSclLowTicks <= (others => '0');

          if cStart then
            --Master is whichever side sent the start signal
            cPortAisMaster <= cPortAStart;
            cState <= I2CStarted_WaitingForSclLow;
          end if;

        ----------------------------------------------------------------------------------------------
        when I2CStarted_WaitingForSclLow =>
        ----------------------------------------------------------------------------------------------

          cHeaderWord <= true;
          cCurBit <= kFirstBit;
          cReadWrite_n <= false;
          cRequiredSclLowTicks <= (others => '0');

          if cSclLow then
            --Go directly to WaitForSclHigh state, forcing of Scl low only occurs during ack bit.
            cState <= I2cSclLow_WaitForSclHigh;
          end if;

        ----------------------------------------------------------------------------------------------
        when I2cSclLow_ForceSclLowBothSides =>
        ----------------------------------------------------------------------------------------------

          --Drive both sides of SCL low for required low time before giving control to slave to
          --clock stretch.  If control was given right away to slave, then a slave that does not
          --clock stretch would cause the slave's SCL line to go high right away.
          --if control was kept with the master, then the slave would not be able to clock stretch
          --We essentially force clock stretch for required min time, and then allow slave to hold longer
          --if needed.  This should not affect performance much because master will be holding low
          --during this time anyway.
          cCounter <= cCounter + 1;
          if cCounter = cRequiredSclLowTicks - 1 then
            cState <= I2cSclLow_WaitForSclHigh;
          end if;

        ----------------------------------------------------------------------------------------------
        when I2cSclLow_WaitForSclHigh =>
        ----------------------------------------------------------------------------------------------

          --Determine the clock low period only on the header word, during the bit just before the ack
          --bit.  This time will be assumed during the entire I2C transaction, and reset during a stop
          --or repeated start condtion, and then remeasured during bit before the next head'ers ack bit.
          --This time is used to force the SCL lines low during a potential clock stretching condition
          --in order to prevent them from going high in case clock stretching is not supported.
          if cHeaderWord and (cCurBit = kBitBeforeAckBit)  then
            cRequiredSclLowTicks <= cRequiredSclLowTicks + 1;
          end if;

          --Wait for master and slave to release bus (Rising edge of Scl)
          if cSclHigh then
            --If this is the Ack bit, then latch the ack and forward information to bus monitor
            if cCurBit = kAckBit then
              --An ack is if either side is low in the case that the master is on the
              --same side of the bridge as the slave, then the ack will stay local to
              --one side and not be transmitted across the bridge
              cAck                   <=             not cSdaHigh;
              cBusMonWordAck         <= to_StdLogicLocal(not cSdaHigh);
              cBusMonWord            <= cWord;
              cBusMonWordIsHeader    <= to_StdLogicLocal(cHeaderWord);
              cBusMonWordReadWrite_n <= to_StdLogicLocal(cReadWrite_n);
              cBusMonWordValid       <= '1';
            else
              --Logic low if either side of bridge is low as low won't propigate to other
              --side in case that the master and slave are on the same side as the bridge points
              --to the master when reading.
              cWord(cCurBit) <= to_StdLogicLocal(cSdaHigh);
            end if;

            cState <= I2cSclHigh_WaitForLowStopOrStart;
          end if;

        ----------------------------------------------------------------------------------------------
        when I2cSclHigh_WaitForLowStopOrStart =>
        ----------------------------------------------------------------------------------------------
          --Using a variable to store next value of cReadWrite_n for this state so it can be referenced later in this state.
          --Next value is equal to current, unless being written to in this state.
          cNextReadWriteVar_n := cReadWrite_n;
          --Next bit begins on falling edge and latches on rising edge
          if cSclLow then
            ---------------------------------------------
            --if Falling edge of Ack Bit
            ---------------------------------------------
            if cCurBit = kAckBit then
              -- if it is the header word then latch the read/write bit
              if cHeaderWord then
                --Change cReadWrite_n on falling edge as this is when bus direction changes and
                --direction is dependent on if we are reading or writing
                cNextReadWriteVar_n := to_BooleanLocal(cWord(kReadWriteBit));
              end if;

              --When an Ack bit is recieved we are no longer the header
              cHeaderWord <= false;

              --reset curBit to first bit on Ack bit as that is final bit in word
              cNextBitVar := kFirstBit;

            ---------------------------------------------
            --if Falling edge of Data bit (non Ack bits)
            ---------------------------------------------
            else
              --Decrement current bit on data bits (non Ack bits)
              cNextBitVar := cCurBit - 1;
            end if;
            --Set cur values to next values.  Doing it this way to use the variable later on.
            cReadWrite_n  <= cNextReadWriteVar_n;
            cCurBit       <= cNextBitVar;

            -----------------------------------------------------
            --if Next bit is an ack bit and Bridge is connected
            -----------------------------------------------------
            --There are two cases for clock stretching, both are for when we are waiting for the slave.
            --  1.  Waiting until the slave is ready to ack when writing data to the slave.
            --  2.  Waiting until the slave has read data available.  This is only observed on the first read bit of read data, but we will allow clock stretching on any bit.
            --  There is a chance that the master is not ready for the next bit, that is fine because the slave clock will go high when it's done clock stretching, with it's data bit at next value.
            --  Master will remove clock when it is ready to clock that bit in.  
            --  If clock stretching is not implemented by the slave, then we move to the force low state, enforcing the observed clock low time to be seen by the slave.
            if ((cNextBitVar  = kAckBit and (not cNextReadWriteVar_n )) or    --If next bit is the ack    bit when writing then force clock low to both sides to allow slave to clock stretch until its ready to ack.
                (cNextBitVar /= kAckBit and (    cNextReadWriteVar_n ))) and  --If next bit is not an ack bit when reading then force clock low to both sides to allow slave to clock stretch until it is ready to provide read data.
               cConnectBridge = '1' then
              cState <= I2cSclLow_ForceSclLowBothSides;
            else
              --We don't want to modify the Scl line when bridge is not connected or when next bit is not an ack bit.
              cState <= I2cSclLow_WaitForSclHigh;
            end if;
          end if;

        ----------------------------------------------------------------------------------------------
        when I2CStopped_WaitForSdaTristateOnPortAandB =>
        ----------------------------------------------------------------------------------------------
          --When stopping the I2C bus wait for the rising edge of sda to make it across to both sides.
          --This should only matter when reporting a stop condition VIA the bus monitor.  Without this two stop
          --conditions will be reported, one for both sides of the bus as it is possible that 2 stop conditions
          --get sent in the stopped case.
          if cSdaHigh then
            cState <= I2CStopped_WaitForStart;
          end if;

      end case;

      --if a stop or start is seen on either side, return to the stopped or started state
      if cStop then
        cState <= I2CStopped_WaitForSdaTristateOnPortAandB;
      elsif cStart then
         --A repeated start should be for the same master, so no need to detect again
        cState <= I2CStarted_WaitingForSclLow;
      end if;

    end if;
  end if;
  end process;
  -----------------------------------------------------------------------------
  -- Determine Scl direction
  -----------------------------------------------------------------------------
  --Only drive to slave when writing and and on the Ack bit or when reading and data bit to allow clock stretching by the slave whenever it is driving a bit to the master
  --The ack bit when reading comes from the master, therefore the master dictates how long to hold the clock for here.
  cSclDirection <=  SLAVE_TO_MASTER          when cState = I2cSclLow_WaitForSclHigh and ((not cReadWrite_n and cCurBit  = kAckBit) or
                                                                                        (     cReadWrite_n and cCurBit /= kAckBit)) else
                    FORCE_SCL_LOW_BOTH_SIDES when cState = I2cSclLow_ForceSclLowBothSides                 else
                    HIGH_Z                   when cState = I2CStopped_WaitForStart or
                                                  cState = I2CStopped_WaitForSdaTristateOnPortAandB       else --High Z in stopped case
                    MASTER_TO_SLAVE;  --Drive to master in all other cases

  -----------------------------------------------------------------------------
  -- Determine Sda direction
  -----------------------------------------------------------------------------
  cSdaDirection <= HIGH_Z          when cState = I2CStopped_WaitForStart or
                                        cState = I2CStopped_WaitForSdaTristateOnPortAandB else
                   MASTER_TO_SLAVE when (not cReadWrite_n and cCurBit /= kAckBit) or (cReadWrite_n and cCurBit = kAckBit) or --When writing or acking a read
                                        (cReadWrite_n and cAck = false and cCurBit = kFirstBit)                                   --When reading and the master Nacked the last byte, aka waiting for stop condition from master
            else   SLAVE_TO_MASTER;

  -----------------------------------------------------------------------------
  -- Generate and register I2C outputs to be glitch free
  -----------------------------------------------------------------------------
  process (Clk)
  begin
  if rising_edge(Clk) then
    if cReset = '1' then
      cPortASdaTriOut <= '1';
      cPortBSdaTriOut <= '1';

      cPortASclTriOut <= '1';
      cPortBSclTriOut <= '1';
    else
      case cSclDirection is
        --------------------------------------
        when MASTER_TO_SLAVE =>
        --------------------------------------
          if cPortAisMaster then
            cPortASclTriOut <= '1';
            cPortBSclTriOut  <= cPortASclIn;
          else
            cPortASclTriOut <= cPortBSclIn;
            cPortBSclTriOut <= '1';
          end if;

        --------------------------------------
        when SLAVE_TO_MASTER =>
        --------------------------------------
          if cPortAisMaster then
            cPortASclTriOut <= cPortBSclIn;
            cPortBSclTriOut <= '1';
          else
            cPortASclTriOut <= '1';
            cPortBSclTriOut  <= cPortASclIn;
          end if;

        --------------------------------------
        when FORCE_SCL_LOW_BOTH_SIDES =>
        --------------------------------------
          cPortASclTriOut <= '0';
          cPortBSclTriOut <= '0';

        --------------------------------------
        when HIGH_Z =>
        --------------------------------------
          cPortASclTriOut <= '1';
          cPortBSclTriOut <= '1';

      end case;

      case cSdaDirection is
        --------------------------------------
        when MASTER_TO_SLAVE =>
        --------------------------------------
          if cPortAisMaster then
            cPortASdaTriOut <= '1';
            cPortBSdaTriOut <= cPortASdaIn;
          else
            cPortASdaTriOut <= cPortBSdaIn;
            cPortBSdaTriOut <= '1';
          end if;

        --------------------------------------
        when SLAVE_TO_MASTER =>
        --------------------------------------
          if cPortAisMaster then
            cPortASdaTriOut <= cPortBSdaIn;
            cPortBSdaTriOut <= '1';
          else
            cPortASdaTriOut <= '1';
            cPortBSdaTriOut <= cPortASdaIn;
          end if;

        --------------------------------------
        when HIGH_Z =>
        --------------------------------------
          cPortASdaTriOut <= '1';
          cPortBSdaTriOut <= '1';
      end case;

      --If the bridge is not connected then keep lines in high impedance state
      if cConnectBridge = '0' then
        cPortASdaTriOut <= '1';
        cPortBSdaTriOut <= '1';

        cPortASclTriOut <= '1';
        cPortBSclTriOut <= '1';
      end if;
    end if;
  end if;
  end process;


end arch;
