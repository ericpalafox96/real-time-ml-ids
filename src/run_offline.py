# src/run_offline.py
import argparse
import os
import numpy as np

from parse_pcap import parse_pcap
from windowing import assign_windows
from features import compute_window_features

def validate_features(features_df):
    # basic sanity checks
    if features_df.empty:
        raise ValueError("features_df is empty (no windows produced).")

    # no NaN / inf
    if features_df.isnull().any().any():
        bad_cols = features_df.columns[features_df.isnull().any()].tolist()
        raise ValueError(f"NaNs found in features columns: {bad_cols}")

    numeric = features_df.select_dtypes(include=[np.number])
    if np.isinf(numeric.to_numpy()).any():
        raise ValueError("Infinity values found in numeric features.")

def main():
    parser = argparse.ArgumentParser(description="Offline IDS feature pipeline (pcap -> windowed features)")
    parser.add_argument("--pcap", "-p", required=True, help="Path to pcap/pcapng file")
    parser.add_argument("--window", "-w", type=float, default=1.0, help="Window size in seconds (default: 1.0)")
    args = parser.parse_args()

    # 1) parse
    df = parse_pcap(args.pcap)
    if df.empty:
        print("No packets parsed. Exiting.")
        return

    # 2) windowing
    df = assign_windows(df, window_size=args.window)

    # 3) features
    features_df = compute_window_features(df)

    # baseline stats
    print("\n=== Baseline Stats ===")
    print("Mean pkt_count:", features_df["pkt_count"].mean())
    print("Max pkt_count:", features_df["pkt_count"].max())
    print("99th percentile pkt_count:", features_df["pkt_count"].quantile(0.99))
    print("Mean mean_itt:", features_df["mean_itt"].mean())
    print("Mean entropy:", features_df["pkt_size_entropy"].mean())

    threshold = features_df["pkt_count"].quantile(0.99)
    alerts = features_df[features_df["pkt_count"] > threshold]

    # baseline threshold detector
    print("\n=== Baseline Threshold Detector ===")
    print(f"Threshold (99th percentile): {threshold}")
    print(f"Flagged windows: {len(alerts)}")
    print(alerts[["window_id", "pkt_count"]])

    # 4) validate
    validate_features(features_df)

    # 5) print summary
    print("\n=== Pipeline Summary ===")
    print(f"PCAP: {args.pcap}")
    print(f"Packets parsed: {len(df)}")
    print(f"Window size: {args.window:.3f}s")
    print(f"Windows produced: {features_df['window_id'].nunique()}")
    print("\nTop 5 windows by pkt_count:")
    top = features_df.sort_values("pkt_count", ascending=False).head(5)
    print(top[["window_id", "pkt_count", "mean_itt", "pkt_size_entropy", "tcp_syn_rate", "tcp_rst_rate"]].to_string(index=False))

if __name__ == "__main__":
    main()
