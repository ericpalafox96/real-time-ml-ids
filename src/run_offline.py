from parse_pcap import parse_pcap
from windowing import assign_windows

df = parse_pcap("../captures/capture1.pcapng")
df = assign_windows(df, window_size=1.0)

print(df[["relative_time", "window_id"]].head(100))
