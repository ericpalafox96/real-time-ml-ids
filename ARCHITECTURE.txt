                          ┌──────────────────────────────┐
                          │          CONTROL PLANE        │
                          │------------------------------│
                          │ • Model Management           │
                          │   (versioning, reload)       │
                          │ • Config & Policy            │
                          │   (thresholds, rules)        │
                          │ • Monitoring / Metrics       │
                          │ • Alert Aggregation          │
                          └───────────────▲──────────────┘
                                          │
                                          │  metrics / logs
                                          │
┌───────────────────────────────────────────────────────────────────┐
│                         DATA PLANE (Real-Time)                    │
│                                                                   │
│  Packet Capture (pcap / live NIC)                                 │
│            ↓                                                      │
│  Preprocessing / Parsing                                          │
│            ↓                                                      │
│  Window Buffer (circular, in-memory)                              │
│            ↓                                                      │
│  Feature Extraction (timing + payload stats)                      │
│            ↓                                                      │
│  Feature Scaling (pre-fitted scaler)                              │
│            ↓                                                      │
│  Classifier / Detector (ML + rule-based hybrid)                   │
│            ↓                                                      │
│  Decision & Alerting (log, dashboard, webhook)                    │
└───────────────────────────────────────────────────────────────────┘
                                          ↑
                                          │
                           model + config injection
                                          │
                          ┌───────────────┴──────────────┐
                          │       CONTROL PLANE          │
                          └──────────────────────────────┘