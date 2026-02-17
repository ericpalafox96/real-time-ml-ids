# Real-Time ML-Based Intrusion Detection System

A production-oriented intrusion detection system that processes network traffic (pcap or live NIC)
in real time using a streaming feature pipeline and lightweight ML + rule-based detection.

## Architecture
See: `ARCHITECTURE.md`

High-level flow (data plane):
Packet Capture → Parsing → Window Buffer → Feature Extraction → Scaling → Classifier/Detector → Alerts

Control plane:
Model management (versioning/reload), config/policy, monitoring/metrics.

## Goals
- Build a real-time streaming pipeline (not batch-only).
- Engineer deterministic timing + packet-stat features (CE-style signal thinking).
- Achieve low false positive rate under normal traffic.
- Provide deployable artifacts: CLI + Docker + simple dashboard.
- Track operational metrics: latency, throughput, CPU/memory.

## Roadmap
### Milestone 1 — Data pipeline (Week 1)
- Parse pcap into packet records (timestamp, 5-tuple, size, flags, payload length)
- Implement time-based windowing (e.g., 1s windows, optional overlap)
- Produce `features.csv` from a sample pcap
- Unit tests for windowing + feature determinism

### Milestone 2 — Baselines + evaluation (Weeks 2–3)
- Train baseline models (logistic regression, random forest)
- Evaluation: precision/recall/F1 + false positive rate + ROC
- Serialize model + scaler (joblib)

### Milestone 3 — Streaming detector (Weeks 4–6)
- Online feature extraction + inference loop
- Latency/throughput measurement
- JSON alert output + structured logging

### Milestone 4 — Deployment + demo (Weeks 7–10)
- Docker container
- Minimal dashboard (Streamlit or web UI)
- Demo replay: run a pcap and show alerts + metrics

### Milestone 5 — Polish (Weeks 11–12)
- Documentation, design write-up, results table
- Short demo video/GIF
- Resume bullets + interview story prep
