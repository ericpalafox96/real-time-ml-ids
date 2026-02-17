from parse_pcap import parse_pcap
from windowing import assign_windows
from features import compute_window_features

df = parse_pcap("../captures/capture1.pcapng")
df = assign_windows(df, window_size=1.0)
feat = compute_window_features(df)
print(feat.head())
print("num windows:", len(feat))
