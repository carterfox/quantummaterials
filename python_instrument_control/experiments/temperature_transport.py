# -*- coding: utf-8 -*-
"""
Unified continuous temperature transport experiment layer.

"""

from __future__ import annotations

import csv
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict

from homemade_servers.QDopticool import Opticool
from homemade_servers.SSI_OE1022D_modified import LockInOE1022D
from homemade_servers.Keithley6221 import Keithley6221
from homemade_servers.LakeShore336Temperature import LakeShore336Temperature


LOGGER = logging.getLogger(__name__)

# Internal implementation constants. These are not normal control-panel knobs.
PREP_POLL_S = 2.0
TIME_CONSTANT_SECONDS = [
    10e-6, 30e-6, 100e-6, 300e-6,
    1e-3, 3e-3, 10e-3, 30e-3,
    100e-3, 300e-3,
    1.0, 3.0, 10.0, 30.0,
    100.0, 300.0, 1000.0, 3000.0,
]


@dataclass
class TransportParams:
    """All user-facing settings for one continuous temperature run."""

    # OptiCool start/end setpoints and Lake Shore B offsets.
    start_temp_k: float
    start_tolerance_k: float
    end_temp_k: float
    end_tolerance_k: float

    # Thermal rates.
    start_rate_k_per_min: float
    measurement_rate_k_per_min: float
    final_hold_rate_k_per_min: float

    # Keithley 6221 excitation.
    frequency_hz: float
    current_peak_a: float

    # Software averaging.
    samples_per_point: int
    sample_delay_s: float

    # OE1022D settings.
    lockin_sensitivity: str
    lockin_time_constant_index: int
    lockin_pre_autophase_settle_s: float
    harmonic: int = 2


class TemperatureTransportScheme:
    """Scheme-style owner of the temperature-transport instruments and run."""

    name = "Continuous temperature transport"
    required = ["opticool", "lakeshore", "6221", "lockin"]

    def __init__(self, addrs: Dict[str, object]):
        self.addrs = dict(addrs)
        self.inst: Dict[str, object] = {}

    # ------------------------------------------------------------------
    # Connection / shutdown: kept here, not in the control panel.
    # ------------------------------------------------------------------
    def connect(self, log: Callable[[str], None] = print):
        """Connect all instruments; roll back cleanly if any connection fails."""
        try:
            opticool_ip = str(self.addrs["opticool_ip"])
            opticool_port = int(self.addrs["opticool_port"])
            self.inst["opticool"] = Opticool(opticool_ip, opticool_port)
            log(f"✓ OptiCool: {opticool_ip}:{opticool_port}")

            thermometer = LakeShore336Temperature(
                resource_name=str(self.addrs["lakeshore"]),
                channel=str(self.addrs["lakeshore_channel"]),
            )
            self.inst["lakeshore"] = thermometer
            log(f"✓ Lake Shore: {thermometer.connect()}")
            log(
                f"  Lake Shore {str(self.addrs['lakeshore_channel']).upper()}: "
                f"{thermometer.read_temperature_k():.3f} K"
            )

            source = Keithley6221(str(self.addrs["6221"]))
            self.inst["6221"] = source
            log(f"✓ Keithley 6221: {source.connect()}")

            # This tested OE1022D driver opens the serial resource in __init__.
            lockin = LockInOE1022D(str(self.addrs["lockin"]))
            self.inst["lockin"] = lockin
            log(f"✓ OE1022D: {lockin.identify()}")

            log(f"Scheme '{self.name}' connected: {', '.join(self.required)}")

        except Exception:
            self.shutdown()
            raise

    def _safe_off(self):
        """Immediately remove the 6221 excitation if it exists."""
        source = self.inst.get("6221")
        if source is not None:
            try:
                source.output_off()
            except Exception:
                pass

    def shutdown(self):
        """Turn off excitation and close every instrument session."""
        self._safe_off()

        source = self.inst.get("6221")
        if source is not None:
            try:
                # Successful 6221 cleanup method: shutdown(), not close().
                source.shutdown()
            except Exception:
                pass

        lockin = self.inst.get("lockin")
        if lockin is not None:
            try:
                lockin.close()
            except Exception:
                pass

        thermometer = self.inst.get("lakeshore")
        if thermometer is not None:
            try:
                thermometer.close()
            except Exception:
                pass

        opticool = self.inst.get("opticool")
        if opticool is not None:
            try:
                opticool.close()
            except Exception:
                pass

        self.inst.clear()

    # ------------------------------------------------------------------
    # Temperature logic.
    # ------------------------------------------------------------------
    @staticmethod
    def _direction(p: TransportParams) -> int:
        if float(p.end_temp_k) > float(p.start_temp_k):
            return 1   # warming
        if float(p.end_temp_k) < float(p.start_temp_k):
            return -1  # cooling
        raise ValueError("start_temp_k and end_temp_k must be different.")

    @staticmethod
    def _local_start_temp(p: TransportParams, direction: int) -> float:
        return float(p.start_temp_k) + direction * float(p.start_tolerance_k)

    @staticmethod
    def _local_end_temp(p: TransportParams, direction: int) -> float:
        return float(p.end_temp_k) - direction * float(p.end_tolerance_k)

    @staticmethod
    def _start_reached(local_temp_k: float, target_k: float, direction: int) -> bool:
        if direction > 0:
            return float(local_temp_k) <= float(target_k)
        return float(local_temp_k) >= float(target_k)

    @staticmethod
    def _end_reached(local_temp_k: float, target_k: float, direction: int) -> bool:
        if direction > 0:
            return float(local_temp_k) >= float(target_k)
        return float(local_temp_k) <= float(target_k)

    @staticmethod
    def _validate_params(p: TransportParams):
        if p.start_tolerance_k < 0 or p.end_tolerance_k < 0:
            raise ValueError("Temperature tolerances must be >= 0.")
        if p.start_rate_k_per_min <= 0 or p.measurement_rate_k_per_min <= 0:
            raise ValueError("Temperature rates must be > 0.")
        if p.final_hold_rate_k_per_min <= 0:
            raise ValueError("final_hold_rate_k_per_min must be > 0.")
        if p.frequency_hz <= 0:
            raise ValueError("frequency_hz must be > 0.")
        if p.current_peak_a < 0:
            raise ValueError("current_peak_a must be >= 0.")
        if int(p.samples_per_point) < 1:
            raise ValueError("samples_per_point must be >= 1.")
        if p.sample_delay_s < 0 or p.lockin_pre_autophase_settle_s < 0:
            raise ValueError("Timing delays must be >= 0.")
        if not 0 <= int(p.lockin_time_constant_index) < len(TIME_CONSTANT_SECONDS):
            raise ValueError("lockin_time_constant_index is outside 0..17.")

    def _opticool_temperature(self):
        """Occasional OptiCool TEMP? errors must not abort a long run."""
        opticool = self.inst["opticool"]
        try:
            value, status = opticool.get_temperature()
            return float(value), str(status)
        except Exception as exc:
            LOGGER.warning("OptiCool temperature read failed, ignored: %s", exc)
            return float("nan"), "ReadError"

    def _local_temperature(self) -> float:
        return float(self.inst["lakeshore"].read_temperature_k())

    def _prepare_start(
        self,
        p: TransportParams,
        direction: int,
        local_start_temp_k: float,
        log: Callable[[str], None],
    ) -> float:
        """
        Preserve the established thermal sequence:
        drive OptiCool to the start setpoint; when Lake Shore B reaches the
        derived start threshold, immediately command the end setpoint/ramp.
        """
        opticool = self.inst["opticool"]
        mode = opticool.temperature.approach_mode.no_overshoot

        opticool.set_temperature(
            float(p.start_temp_k),
            float(p.start_rate_k_per_min),
            mode,
        )

        log(
            "Preparation: OptiCool -> %.3f K @ %.3f K/min; "
            "waiting for Lake Shore B %s %.3f K"
            % (
                float(p.start_temp_k),
                float(p.start_rate_k_per_min),
                "<=" if direction > 0 else ">=",
                local_start_temp_k,
            )
        )

        while True:
            t_opt, status = self._opticool_temperature()
            t_local = self._local_temperature()

            log(
                "Preparation: OptiCool %.3f K (%s), Lake Shore B %.3f K"
                % (t_opt, status, t_local)
            )

            if self._start_reached(t_local, local_start_temp_k, direction):
                log(
                    "Lake Shore B start condition reached at %.3f K; "
                    "OptiCool -> %.3f K @ %.3f K/min"
                    % (
                        t_local,
                        float(p.end_temp_k),
                        float(p.measurement_rate_k_per_min),
                    )
                )
                opticool.set_temperature(
                    float(p.end_temp_k),
                    float(p.measurement_rate_k_per_min),
                    mode,
                )
                return t_local

            time.sleep(PREP_POLL_S)

    # ------------------------------------------------------------------
    # Electrical measurement logic.
    # ------------------------------------------------------------------
    @staticmethod
    def _do_auto_phase(
        lockin,
        time_constant_index: int,
        log: Callable[[str], None],
    ):
        tc_s = TIME_CONSTANT_SECONDS[int(time_constant_index)]
        wait = max(1.0, 5.0 * tc_s)

        log(
            "Auto phase: running CH-A + CH-B, waiting %.3g s "
            "(5 x time constant)" % wait
        )

        lockin.auto_phase_all()
        time.sleep(wait)

        try:
            phase1 = float(lockin.get_phase_shift(channel=1))
            phase2 = float(lockin.get_phase_shift(channel=2))
            log(
                "Auto phase done: CH-A = %.6f deg, CH-B = %.6f deg"
                % (phase1, phase2)
            )
        except Exception as exc:
            LOGGER.warning("Auto phase phase-readback failed: %s", exc)
            phase1 = float("nan")
            phase2 = float("nan")

        log("Settling 5 s after auto phase before measurement")
        time.sleep(5.0)
        return phase1, phase2

    def run(
        self,
        p: TransportParams,
        save_path,
        log: Callable[[str], None] = print,
    ):
        """Run one continuous warming or cooling transport measurement."""
        self._validate_params(p)

        opticool = self.inst["opticool"]
        thermometer = self.inst["lakeshore"]
        current_source = self.inst["6221"]
        lockin = self.inst["lockin"]

        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        direction = self._direction(p)
        direction_name = "warming" if direction > 0 else "cooling"
        local_start_temp_k = self._local_start_temp(p, direction)
        local_end_temp_k = self._local_end_temp(p, direction)

        start_trigger_temp_k = self._prepare_start(
            p=p,
            direction=direction,
            local_start_temp_k=local_start_temp_k,
            log=log,
        )

        # OE1022D signal inputs.
        lockin.set_input_mode(channel=1, mode="differential")
        lockin.set_input_mode(channel=2, mode="differential")

        # Preserve the tested OE1022D API/semantics.
        for channel in (1, 2):
            lockin.set_sensitivity(
                channel=channel,
                sensitivity=p.lockin_sensitivity,
            )
            lockin.set_time_constant(
                channel=channel,
                index=int(p.lockin_time_constant_index),
            )
            lockin.set_harmonic(
                channel=channel,
                slot=1,
                order=int(p.harmonic),
            )

        # Successful external-reference settings.
        lockin.set_reference_source(channel=1, mode=0)
        lockin.set_ref_slope(channel=1)
        # Do NOT send FMODD 2,0. CH-B keeps the tested shared REF IN A routing.

        fields = [
            "timestamp_iso", "elapsed_s",
            "T_lakeshore_B_K", "T_opticool_K", "opticool_status",
            "current_peak_A", "frequency_Hz",
            "ch1_R_1w_Vrms", "ch1_theta_1w_deg",
            "ch1_R_2w_Vrms", "ch1_theta_2w_deg",
            "ch2_R_1w_Vrms", "ch2_theta_1w_deg",
            "ch2_R_2w_Vrms", "ch2_theta_2w_deg",
        ]

        mode = opticool.temperature.approach_mode.no_overshoot

        try:
            # Preserve the successful 6221 external-reference setup.
            current_source.configure_sine(
                frequency_hz=float(p.frequency_hz),
                amplitude_a=float(p.current_peak_a),
                offset_a=0.0,
                range_a=float(p.current_peak_a),
            )
            current_source.start()

            time.sleep(float(p.lockin_pre_autophase_settle_s))

            auto_phase_ch1_deg, auto_phase_ch2_deg = self._do_auto_phase(
                lockin,
                time_constant_index=int(p.lockin_time_constant_index),
                log=log,
            )

            started = time.monotonic()

            with save_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                f.write("# continuous_temperature_transport\n")
                f.write(f"# direction={direction_name}\n")
                f.write(f"# start_opticool_setpoint_K={p.start_temp_k:g}\n")
                f.write(f"# start_tolerance_K={p.start_tolerance_k:g}\n")
                f.write(f"# start_lakeshore_B_target_K={local_start_temp_k:g}\n")
                f.write(f"# start_trigger_lakeshore_B_K={start_trigger_temp_k:g}\n")
                f.write(f"# end_opticool_setpoint_K={p.end_temp_k:g}\n")
                f.write(f"# end_tolerance_K={p.end_tolerance_k:g}\n")
                f.write(f"# end_lakeshore_B_target_K={local_end_temp_k:g}\n")
                f.write(f"# start_rate_K_per_min={p.start_rate_k_per_min:g}\n")
                f.write(
                    f"# measurement_rate_K_per_min={p.measurement_rate_k_per_min:g}\n"
                )
                f.write(
                    f"# final_hold_rate_K_per_min={p.final_hold_rate_k_per_min:g}\n"
                )
                f.write(f"# lockin_sensitivity={p.lockin_sensitivity}\n")
                f.write(
                    f"# lockin_time_constant_index={int(p.lockin_time_constant_index)}\n"
                )
                f.write(f"# harmonic={int(p.harmonic)}\n")
                f.write(f"# current_peak_A={p.current_peak_a:g}\n")
                f.write(f"# frequency_Hz={p.frequency_hz:g}\n")
                f.write(f"# samples_per_point={int(p.samples_per_point)}\n")
                f.write(f"# sample_delay_s={p.sample_delay_s:g}\n")
                f.write(f"# auto_phase_ch1_deg={auto_phase_ch1_deg:.9g}\n")
                f.write(f"# auto_phase_ch2_deg={auto_phase_ch2_deg:.9g}\n")
                writer.writeheader()
                f.flush()

                while True:
                    t_opt, status = self._opticool_temperature()
                    t_local = float(thermometer.read_temperature_k())

                    ch1, _std1, ch2, _std2 = lockin.read_average_dual(
                        params=[2, 3, 7, 8],
                        num_avgs=int(p.samples_per_point),
                        delay=float(p.sample_delay_s),
                    )

                    if ch1 is None or ch2 is None:
                        raise RuntimeError(
                            "OE1022D read_average_dual returned no valid data."
                        )

                    writer.writerow({
                        "timestamp_iso": datetime.now().astimezone().isoformat(),
                        "elapsed_s": time.monotonic() - started,
                        "T_lakeshore_B_K": t_local,
                        "T_opticool_K": t_opt,
                        "opticool_status": status,
                        "current_peak_A": float(p.current_peak_a),
                        "frequency_Hz": float(p.frequency_hz),
                        "ch1_R_1w_Vrms": float(ch1[0]),
                        "ch1_theta_1w_deg": float(ch1[1]),
                        "ch1_R_2w_Vrms": float(ch1[2]),
                        "ch1_theta_2w_deg": float(ch1[3]),
                        "ch2_R_1w_Vrms": float(ch2[0]),
                        "ch2_theta_1w_deg": float(ch2[1]),
                        "ch2_R_2w_Vrms": float(ch2[2]),
                        "ch2_theta_2w_deg": float(ch2[3]),
                    })
                    f.flush()

                    if self._end_reached(t_local, local_end_temp_k, direction):
                        log(
                            "Lake Shore B end condition reached at %.3f K; "
                            "holding OptiCool at %.3f K"
                            % (t_local, local_end_temp_k)
                        )
                        opticool.set_temperature(
                            local_end_temp_k,
                            float(p.final_hold_rate_k_per_min),
                            mode,
                        )
                        break

        except KeyboardInterrupt:
            log("Stopped by user; completed CSV rows are already saved.")

        finally:
            # Same safety invariant as the successful measurement engine:
            # the excitation is removed even if acquisition raises.
            self._safe_off()

        return save_path


def main(
    addrs: Dict[str, object],
    params: TransportParams,
    save_path,
    log: Callable[[str], None] | None = None,
):

    if log is None:
        log = LOGGER.info

    scheme = TemperatureTransportScheme(addrs)
    try:
        scheme.connect(log)
        return scheme.run(params, save_path, log)
    finally:
        scheme.shutdown()
