# -*- coding: utf-8 -*-
"""
Control panel / entry point for continuous temperature transport.

"""

from __future__ import annotations

import logging
import traceback
from datetime import datetime
from pathlib import Path

from experiments import temperature_transport


logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

OPTICOOL_IP = "192.168.50.1"
OPTICOOL_PORT = 5000

KEITHLEY_6221_RESOURCE = "GPIB1::12::INSTR"
LOCKIN_RESOURCE = "ASRL9::INSTR"

LAKESHORE_RESOURCE = "GPIB0::11::INSTR"
LAKESHORE_CHANNEL = "B"

START_TEMP_K = 1.7
START_TOLERANCE_K = 0.3
END_TEMP_K = 330.0
END_TOLERANCE_K = 42.0

START_RATE_K_PER_MIN = 20.0
MEASUREMENT_RATE_K_PER_MIN = 10.0
FINAL_HOLD_RATE_K_PER_MIN = 20.0

FREQUENCY_HZ = 79.0
CURRENT_PEAK_A = 0.4e-6

SAMPLES_PER_POINT = 5
SAMPLE_DELAY_S = 0.1

LOCKIN_SENSITIVITY = "5 mV"
LOCKIN_TIME_CONSTANT_INDEX = 8      # 100 ms
LOCKIN_PRE_AUTOPHASE_SETTLE_S = 0.5
HARMONIC = 2

DATA_DIR = Path(__file__).resolve().parent / "data"


def _build_addresses():
    return {
        "opticool_ip": OPTICOOL_IP,
        "opticool_port": OPTICOOL_PORT,
        "6221": KEITHLEY_6221_RESOURCE,
        "lockin": LOCKIN_RESOURCE,
        "lakeshore": LAKESHORE_RESOURCE,
        "lakeshore_channel": LAKESHORE_CHANNEL,
    }


def _build_params():
    return temperature_transport.TransportParams(
        start_temp_k=START_TEMP_K,
        start_tolerance_k=START_TOLERANCE_K,
        end_temp_k=END_TEMP_K,
        end_tolerance_k=END_TOLERANCE_K,
        start_rate_k_per_min=START_RATE_K_PER_MIN,
        measurement_rate_k_per_min=MEASUREMENT_RATE_K_PER_MIN,
        final_hold_rate_k_per_min=FINAL_HOLD_RATE_K_PER_MIN,
        frequency_hz=FREQUENCY_HZ,
        current_peak_a=CURRENT_PEAK_A,
        samples_per_point=SAMPLES_PER_POINT,
        sample_delay_s=SAMPLE_DELAY_S,
        lockin_sensitivity=LOCKIN_SENSITIVITY,
        lockin_time_constant_index=LOCKIN_TIME_CONSTANT_INDEX,
        lockin_pre_autophase_settle_s=LOCKIN_PRE_AUTOPHASE_SETTLE_S,
        harmonic=HARMONIC,
    )


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = DATA_DIR / f"temperature_transport_{timestamp}.csv"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    logging.info("Data file: %s", save_path)

    try:
        temperature_transport.main(
            addrs=_build_addresses(),
            params=_build_params(),
            save_path=save_path,
            log=logging.info,
        )
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()
