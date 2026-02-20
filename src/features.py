import numpy as np
import pandas as pd
from scipy.stats import entropy

def pkt_size_entropy(sizes):
    counts = np.bincount(sizes)
    probs = counts[counts>0] / counts.sum()
    return float(entropy(probs))

def compute_window_features(df):
    # df: packet-level DataFrame with columns including window_id, relative_time, length, tcp_flags, src_ip, dst_ip
    groups = df.groupby("window_id")
    rows = []
    for wid, g in groups:
        timestamps = g["relative_time"].values
        itts = np.diff(timestamps) if len(timestamps) > 1 else np.array([0.0])
        row = {
            "window_id": int(wid),
            "pkt_count": len(g),
            "mean_itt": float(itts.mean()) if len(itts)>0 else 0.0,
            "std_itt": float(itts.std()) if len(itts)>0 else 0.0,
            "mean_pkt_size": float(g["length"].mean()),
            "pkt_size_std": float(g["length"].std()) if len(g)>1 else 0.0,
            "pkt_size_entropy": pkt_size_entropy(g["length"].astype(int).values),
            "unique_src_count": int(g["src_ip"].nunique()),
            # TCP derived features (safe checks)
            "tcp_syn_rate": float(g["tcp_flags"].str.contains("S", na=False).sum()) / len(g) if "tcp_flags" in g else 0.0,
            "tcp_rst_rate": float(g["tcp_flags"].str.contains("R", na=False).sum()) / len(g) if "tcp_flags" in g else 0.0,
            "dup_size_ratio": duplicate_size_ratio(g),
        }
        rows.append(row)
    features_df = pd.DataFrame(rows).sort_values("window_id").reset_index(drop=True)
    # save
    features_df.to_csv("outputs/features_replay.csv", index=False)
    return features_df

def duplicate_size_ratio(g):
    counts = g["length"].value_counts()
    if len(counts) == 0:
        return 0.0
    return counts.iloc[0] / len(g)