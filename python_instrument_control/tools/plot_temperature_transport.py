# -*- coding: utf-8 -*-
"""Read-only viewer for a CSV being written by temperature_transport.py."""

from __future__ import annotations

import argparse
import io
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def read_snapshot(path):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    if not text.endswith("\n"):
        text = text.rsplit("\n", 1)[0] + "\n"
    return pd.read_csv(io.StringIO(text), comment="#")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv")
    parser.add_argument("--refresh", type=float, default=1.0)
    args = parser.parse_args()

    plt.ion()

    fig1, ax1 = plt.subplots()
    c11, = ax1.plot([], [], ".-", label="CH1 1w")
    c12, = ax1.plot([], [], ".-", label="CH1 2w")
    ax1.set_xlabel("Lake Shore B temperature (K)")
    ax1.set_ylabel("Voltage (uV)")
    ax1.legend()
    ax1.grid(True)

    fig2, ax2 = plt.subplots()
    c21, = ax2.plot([], [], ".-", label="CH2 1w")
    c22, = ax2.plot([], [], ".-", label="CH2 2w")
    ax2.set_xlabel("Lake Shore B temperature (K)")
    ax2.set_ylabel("Voltage (uV)")
    ax2.legend()
    ax2.grid(True)

    try:
        while plt.get_fignums():
            try:
                df = read_snapshot(args.csv)
                t = df["T_lakeshore_B_K"].to_numpy()

                c11.set_data(t, df["ch1_R_1w_V"].to_numpy() * 1e6)
                c12.set_data(t, df["ch1_R_2w_V"].to_numpy() * 1e6)
                c21.set_data(t, df["ch2_R_1w_V"].to_numpy() * 1e6)
                c22.set_data(t, df["ch2_R_2w_V"].to_numpy() * 1e6)

                for ax in (ax1, ax2):
                    ax.relim()
                    ax.autoscale_view()
                    if not ax.xaxis_inverted():
                        ax.invert_xaxis()

            except (FileNotFoundError, pd.errors.ParserError, KeyError):
                pass

            plt.pause(max(0.2, args.refresh))

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
