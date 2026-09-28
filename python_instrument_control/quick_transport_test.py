# -*- coding: utf-8 -*-
"""Quick linear current sweep: Keithley 6221 + modified OE1022D driver."""

from __future__ import annotations

import csv
import time
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from homemade_servers.SSI_OE1022D_modified import LockInOE1022D
from homemade_servers.Keithley6221 import Keithley6221


KEITHLEY_6221_RESOURCE = "GPIB1::12::INSTR"
LOCKIN_RESOURCE = "ASRL9::INSTR"

FREQUENCY_HZ = 79
CURRENT_START_A = 0.01e-6
CURRENT_STOP_A = 0.4e-6
POINTS = 15

SETTLE_S = 1.5
SAMPLES_PER_POINT = 5
SAMPLE_DELAY_S = 0.1

LOCKIN_CH1_SENSITIVITY = "1 mV"
LOCKIN_CH2_SENSITIVITY = "5 mV"
LOCKIN_TIME_CONSTANT_INDEX = 9
LOCKIN_PRE_AUTOPHASE_SETTLE_S = 1.5

TIME_CONSTANT_SECONDS = [
    10e-6, 30e-6, 100e-6, 300e-6,
    1e-3, 3e-3, 10e-3, 30e-3,
    100e-3, 300e-3,
    1.0, 3.0, 10.0, 30.0,
    100.0, 300.0, 1000.0, 3000.0,
]

DATA_DIR = Path(__file__).resolve().parent / "data"




def do_auto_phase(lockin, time_constant_index):
    tc_s = (
        TIME_CONSTANT_SECONDS[time_constant_index]
        if 0 <= time_constant_index < len(TIME_CONSTANT_SECONDS)
        else 0.1
    )
    wait = max(1.0, 5.0 * tc_s)

    print(f"Auto phase CH-A + CH-B: wait {wait:g} s")
    lockin.auto_phase_all()
    time.sleep(wait)

    phase1 = float(lockin.get_phase_shift(channel=1))
    phase2 = float(lockin.get_phase_shift(channel=2))
    print(
        f"Auto phase done: CH-A={phase1:.6f} deg, "
        f"CH-B={phase2:.6f} deg"
    )

    print("Settling 5 s after auto phase")
    time.sleep(5.0)
    return phase1, phase2

def main():
    current_axis = np.linspace(CURRENT_START_A, CURRENT_STOP_A, POINTS)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / f"quick_transport_{datetime.now():%Y%m%d_%H%M%S}.csv"

    source = Keithley6221(KEITHLEY_6221_RESOURCE)
    print("6221:", source.connect())

    lockin = LockInOE1022D(LOCKIN_RESOURCE)
    print("OE1022D:", lockin.identify())

    lockin.set_input_mode(1, "differential")
    lockin.set_input_mode(2, "differential")

    lockin.set_sensitivity(1, LOCKIN_CH1_SENSITIVITY)
    lockin.set_sensitivity(2, LOCKIN_CH2_SENSITIVITY)

    for channel in (1, 2):
        lockin.set_time_constant(channel, LOCKIN_TIME_CONSTANT_INDEX)
        lockin.set_harmonic(channel, 1, 2)

    # Same successful external-reference commands.
    lockin.set_reference_source(1, 0)
    lockin.set_ref_slope(1)

    # CH-B single-reference / REF IN A routing is deliberately preserved.

    rows = []

    try:
        source.configure_sine(
            FREQUENCY_HZ,
            current_axis[0],
            range_a=CURRENT_STOP_A,
        )
        source.start()
        time.sleep(LOCKIN_PRE_AUTOPHASE_SETTLE_S)

        phase1, phase2 = do_auto_phase(
            lockin,
            LOCKIN_TIME_CONSTANT_INDEX,
        )
        print(
            f"Auto-phase result: "
            f"CH-A={phase1:.6f} deg, CH-B={phase2:.6f} deg"
        )

        with path.open("w", newline="", encoding="utf-8") as f:
            fields = [
                "current_peak_A",
                "ch1_R_1w_Vrms", "ch1_theta_1w_deg",
                "ch1_R_2w_Vrms", "ch1_theta_2w_deg",
                "ch2_R_1w_Vrms", "ch2_theta_1w_deg",
                "ch2_R_2w_Vrms", "ch2_theta_2w_deg",
            ]
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

            for current in current_axis:
                source.update_sine(float(current))
                time.sleep(SETTLE_S)

                ch1, _std1, ch2, _std2 = lockin.read_average_dual(
                    params=[2, 3, 7, 8],
                    num_avgs=SAMPLES_PER_POINT,
                    delay=SAMPLE_DELAY_S,
                )

                if ch1 is None or ch2 is None:
                    raise RuntimeError(
                        "OE1022D read_average_dual returned no valid data."
                    )

                row = {
                    "current_peak_A": float(current),
                    "ch1_R_1w_Vrms": float(ch1[0]),
                    "ch1_theta_1w_deg": float(ch1[1]),
                    "ch1_R_2w_Vrms": float(ch1[2]),
                    "ch1_theta_2w_deg": float(ch1[3]),
                    "ch2_R_1w_Vrms": float(ch2[0]),
                    "ch2_theta_1w_deg": float(ch2[1]),
                    "ch2_R_2w_Vrms": float(ch2[2]),
                    "ch2_theta_2w_deg": float(ch2[3]),
                }
                rows.append(row)
                writer.writerow(row)
                f.flush()

                print(
                    f"I={current*1e6:6.3f} uA | "
                    f"CH1 1w={ch1[0]*1e6: .4g} uV, "
                    f"2w={ch1[2]*1e6: .4g} uV | "
                    f"CH2 1w={ch2[0]*1e6: .4g} uV, "
                    f"2w={ch2[2]*1e6: .4g} uV"
                )

    except KeyboardInterrupt:
        print("Stopped; completed rows remain saved.")

    finally:
        source.shutdown()
        lockin.close()

    if not rows:
        return

    current_ua = np.array([r["current_peak_A"] for r in rows]) * 1e6

    fig, ax = plt.subplots()
    ax.plot(
        current_ua,
        np.array([r["ch1_R_1w_Vrms"] for r in rows]) * 1e6,
        "o-",
        label="CH1 1w",
    )
    ax.plot(
        current_ua,
        np.array([r["ch1_R_2w_Vrms"] for r in rows]) * 1e6,
        "o-",
        label="CH1 2w",
    )
    ax.set_xlabel("Current amplitude (uA peak)")
    ax.set_ylabel("Voltage (uV RMS)")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    fig, ax = plt.subplots()
    ax.plot(
        current_ua,
        np.array([r["ch2_R_1w_Vrms"] for r in rows]) * 1e6,
        "o-",
        label="CH2 1w",
    )
    ax.plot(
        current_ua,
        np.array([r["ch2_R_2w_Vrms"] for r in rows]) * 1e6,
        "o-",
        label="CH2 2w",
    )
    ax.set_xlabel("Current amplitude (uA peak)")
    ax.set_ylabel("Voltage (uV RMS)")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
