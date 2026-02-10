# Example: Company, Arista Networks.
Technical Solutions Engineer - Cloud, Hyperscalers and AI networks

## Purpose
Demonstrates AI-driven troubleshooting for data-center and AI networking environments, aligned with TAC / Solutions Engineer responsibilities such as:

L1–L3 diagnostics

High-speed optics and QoS troubleshooting

Linux + packet analysis

Customer-facing root-cause communicationMCP server collects real-time telemetry → Cursor AI agent correlates failures → Generates RCA and remediation.

Flow:

Network / Linux / SONiC telemetry ingested via MCP

AI agent queries structured diagnostics tools

Cross-layer reasoning performed (L1 → L3 → QoS)

Outputs:

Root cause

Fix commands

Preventive actions

Customer-ready summary

System Components
1. Telemetry MCP Server

Collects:

SNMP / gNMI → interface stats, optics, counters

Syslog → BGP, LACP, STP, QoS events

sFlow / NetFlow → traffic anomalies

Linux tools → tcpdump, ethtool, ip link

SONiC CLI / REST → switch health + routing

Exposes tools like:

get_interface_errors()

get_bgp_flaps()

capture_packets()

get_qos_drops()

analyze_optics()

2. Cursor AI Troubleshooting Agent

Responsibilities:

Detect anomalies

Correlate multi-layer failures

Recommend remediation CLI

Produce TAC-style RCA

Reasoning examples:

FEC errors + link flaps → optic failure

MAC flapping + STP changes → loop / mis-patch

BGP resets + packet loss → upstream congestion

PFC pauses + buffer drops → GPU workload congestion

3. RCA & Customer Report Generator

Single command:

generate_rca(ticket_id)

Outputs:

Timeline of events

Root cause analysis

Immediate remediation

Long-term prevention

Customer-friendly explanation

Key Troubleshooting Domains Covered
L1 / Optics / 400-800G

Detects:

FEC errors

PRBS failures

Link instability

AI suggests:

Cable reseat / replace

FEC compatibility check

Speed downgrade mitigation

L2 Stability

Detects:

LACP mismatch

STP topology storms

MAC flapping

Produces:

Misconfiguration location

Corrective CLI

L3 Routing

Monitors:

BGP session resets

OSPF adjacency drops

ECMP imbalance

Correlates with:

Interface errors

CPU spikes

Congestion

QoS / AI Datacenter Traffic

Finds:

PFC pause storms

Buffer drops

ECN misconfiguration

Explains GPU training congestion scenarios and remediation.

Value
Operational Impact

Faster MTTR through automated RCA

Reduced TAC investigation time

Proactive detection of optics / routing / QoS failures

Customer Impact

Clear executive-ready incident summaries

Consistent troubleshooting methodology

Improved customer trust and communication

Career / Portfolio Impact

Demonstrates:

Deep networking troubleshooting

Linux + packet analysis

Observability + telemetry pipelines

AI-assisted operations

Customer-facing engineering mindset

➡️ Strong alignment with Technical Solutions Engineer (Cloud / AI Networking) roles.
