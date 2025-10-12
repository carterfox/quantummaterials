# sweep_test.py
import numpy as np
import time
import traceback
from homemade_servers.ThorlabsKCube import RotationMount
from pylablib.devices import Thorlabs # Import for specific error handling

# --- Global list to keep track of server instances for safe shutdown ---
servers = []

def list_thorlabs_devices():
    """Lists all connected Thorlabs Kinesis devices to help with debugging."""
    print("--- Searching for connected Thorlabs devices... ---")
    try:
        devices = Thorlabs.list_kinesis_devices()
        if not devices:
            print("WARNING: No Thorlabs Kinesis devices found.")
            print("Please check the USB connection, device power, and drivers.")
        else:
            print("Found the following devices (serial, description):")
            for dev in devices:
                print(f"- {dev[0]}, {dev[1]}")
        print("--------------------------------------------------")
        return devices
    except Exception as e:
        print(f"An error occurred while searching for devices: {e}")
        print("This may indicate a driver issue.")
        print("--------------------------------------------------")
        return []

def get_rotation_stage(serial):
    """Initializes and returns the Thorlabs K-Cube Rotation Mount."""
    print(f"Initializing Rotation Mount with serial: {serial}...")
    rot = RotationMount(serial)
    servers.append(rot)
    print("Rotation mount initialized.")
    return rot

def close_all_servers():
    """Closes all active server connections."""
    print("\nClosing all server connections...")
    for server in servers:
        try:
            server.close()
        except Exception as e:
            print(f"Error closing server {server}: {e}")
    servers.clear()
    print("All servers closed.")

if __name__ == "__main__":
    # --- IMPORTANT: Replace with your K-Cube's serial number ---
    K_CUBE_SERIAL_NUMBER = "27268499"  # <--- VERIFY THIS

    # --- Control whether servers are closed at the end of the script ---
    leave_servers_open = False
    waveplate = None # Define waveplate here to ensure it exists for the finally block

    try:
        # --- 1. List all devices for diagnostics before trying to connect ---
        list_thorlabs_devices()

        # --- 2. Initialize Instrument ---
        waveplate = get_rotation_stage(K_CUBE_SERIAL_NUMBER)

        # --- Get Initial Position ---
        initial_pos = waveplate.get_pos()
        print(f"Successfully connected. Initial position: {initial_pos:.2f}°")

        # --- Define Angle Sweep Parameters ---
        angles = np.arange(0, 181, 15) # From 0 to 180 (inclusive) in 15-degree steps

        print(f"\nStarting sweep from {angles[0]}° to {angles[-1]}°...")
        # --- Perform Sweep ---
        for angle in angles:
            print(f"\nMoving to {angle}°...")
            waveplate.move_to(angle, wait=False) # Start moving without blocking
            waveplate.wait_for_stop() # Wait until the movement is complete
            
            print("Movement stopped. Waiting for 10-second buffer...")
            time.sleep(10) # Wait for the requested 10-second buffer
            
            current_pos = waveplate.get_pos()
            print(f"Move complete. Current position: {current_pos:.2f}°")
        
        print("\nSweep finished.")
        # --- Move back to initial position ---
        time.sleep(1) # A brief pause
        print(f"\nMoving back to initial position ({initial_pos:.2f}°)...")
        waveplate.move_to(initial_pos)
        final_pos_return = waveplate.get_pos()
        print(f"Move complete. Final position: {final_pos_return:.2f}°")

    except Thorlabs.ThorlabsBackendError:
        print("\n--- CONNECTION FAILED ---")
        print("A 'ThorlabsBackendError' occurred. This means the PC cannot communicate with the K-Cube.")
        print("\nOriginal Error Traceback:")
        traceback.print_exc()
        
    except Exception:
        print("\n--- An unexpected error occurred during the rotation test ---")
        traceback.print_exc()

    finally:
        # --- Cleanup ---
        if not leave_servers_open:
            close_all_servers()
        else:
            print("\nScript finished. Servers are left open as requested.")

