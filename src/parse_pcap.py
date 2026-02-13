# src/parse_pcap.py
from scapy.all import PcapReader
from scapy.layers.inet import IP, TCP, UDP
import pandas as pd
import os

def parse_pcap(file_path):
    parsed_data = []

    with PcapReader(file_path) as pcap:
        for pkt in pcap:
            # default values
            src_port = None
            dst_port = None
            tcp_flags = None

            # determine L4 proto and ports/flags safely
            if TCP in pkt:
                l4_proto = "TCP"
                src_port = pkt[TCP].sport
                dst_port = pkt[TCP].dport
                tcp_flags = str(pkt[TCP].flags)
            elif UDP in pkt:
                l4_proto = "UDP"
                src_port = pkt[UDP].sport
                dst_port = pkt[UDP].dport
            else:
                l4_proto = None

            row = {
                "timestamp": float(pkt.time),
                "src_ip": pkt[IP].src if IP in pkt else None,
                "dst_ip": pkt[IP].dst if IP in pkt else None,
                "l4_proto": l4_proto,
                "src_port": src_port,
                "dst_port": dst_port,
                "tcp_flags": tcp_flags,
                "length": len(pkt),
            }
            parsed_data.append(row)

    if not parsed_data:
        return pd.DataFrame()  # empty DF if no packets parsed

    df = pd.DataFrame(parsed_data)

    # add relative time column for windowing (seconds since first packet)
    first_ts = df["timestamp"].iloc[0]
    df["relative_time"] = df["timestamp"] - first_ts

    # ensure outputs directory exists and save a CSV for inspection
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "outputs"), exist_ok=True)
    out_path = os.path.join(os.path.dirname(__file__), "..", "outputs", "parsed.csv")
    df.to_csv(out_path, index=False)

    return df

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Parse a pcap/pcapng into packet metadata CSV")
    parser.add_argument("--pcap", "-p", required=True, help="Path to pcap or pcapng file")
    args = parser.parse_args()

    df = parse_pcap(args.pcap)
    if df.empty:
        print("No packets parsed.")
    else:
        print(df.head().to_string(index=False))
        print(f"\nSaved parsed CSV to: ../outputs/parsed.csv (rows: {len(df)})")
