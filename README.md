# Real-Time ML-Based Intrusion Detection System

A production-oriented intrusion detection system that processes network traffic (pcap or live NIC)
in real time using a streaming feature pipeline and lightweight ML + rule-based detection.

## Results

Using 2-second window aggregation and engineered temporal + duplication-based features:

- 86% mean accuracy (5-fold cross-validation)
- 95% recall on replay attack windows
- 75% recall on normal windows
- Performance improved from 73% (1s window) → 86% (2s window) through window-size tuning

Top contributing features:
- Inter-arrival timing statistics (mean_itt, std_itt)
- Packet size distribution metrics
- Duplication ratio within window

## Architecture
See: `ARCHITECTURE.md`

High-level flow (data plane):
Packet Capture → Parsing → Window Buffer → Feature Extraction → Scaling → Classifier/Detector → Alerts

Control plane:
Model management (versioning/reload), config/policy, monitoring/metrics.

## Feature Engineering

Window-level features include:
- Packet count
- Mean and standard deviation of inter-arrival time
- Packet size entropy and variance
- Duplication ratio of dominant packet size
- Flow concentration metrics (5-tuple based)

Replay detection benefits from temporal aggregation and duplication-based signals.

## How to Reproduce

```bash
python src/run_offline.py --pcap <normal.pcapng> --window 2.0
python src/run_offline.py --pcap <replay_attack.pcapng> --window 2.0
python src/make_dataset.py --normal outputs/features_normal.csv --replay outputs/features_replay.csv
python src/train_model.py --data outputs/dataset.csv