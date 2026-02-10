# architecture.md  
## MCP AI Project Generator — System Architecture

### 1. Architectural Goal

Design a **modular AI-assisted troubleshooting system** that:

- Integrates **telemetry via MCP**
- Enables **LLM reasoning over real signals**
- Produces **deterministic RCA artifacts**
- Scales from **MVP → production-like architecture**

---

# 2. High-Level Architecture

[Telemetry Sources] → [MCP Server Layer] → [AI Reasoning Agent] → [RCA + Remediation Output] → [Reports / CLI / API]

---

# 3. Core Components

## Telemetry Layer
MVP sources:

- Log files  
- Metrics JSON  
- Sample counters  

Future:

- SNMP / gNMI  
- Syslog streams  
- Cloud monitoring APIs  

---

## MCP Server Layer

Responsibilities:

- Normalize telemetry  
- Expose deterministic **tools**  
- Provide safe execution boundary  

Example tools:

- get_interface_errors()  
- get_recent_logs()  
- detect_anomaly()  
- generate_rca_data()  

---

## AI Reasoning Layer

Functions:

- Select MCP tools  
- Correlate signals  
- Infer root cause  
- Propose remediation  
- Generate explanation  

---

## RCA Output Layer

Produces:

- Markdown incident reports  
- CLI remediation steps  
- Structured JSON for future UI  

---

# 4. Scaling Path

### Add streaming telemetry  
Kafka / Webhooks / Cloud metrics  

### Add memory + history  
Incident timelines  
Pattern detection  

### Add automation  
Self-healing scripts  
Runbook execution  

### Add UI  
Dashboard  
Searchable incidents  
Customer portal  
