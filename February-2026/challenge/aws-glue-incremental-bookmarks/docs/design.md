# Design Notes (Template)

## 1. Business Logic
- Describe what the pipeline achieves and why incremental processing matters.

## 2. Source Definition
- Raw source location(s):
- Data format and schema assumptions:
- Arrival/update behavior:

## 3. Target Definition
- Curated target location:
- Output format and partition strategy:
- Data retention considerations:

## 4. Incremental Strategy
- How job bookmarks are enabled:
- Which part of the read path is bookmark-tracked:
- How updates/late records are handled:

## 5. Schedule & Operations
- Trigger type and cadence:
- Expected runtime window:
- Monitoring/alerting approach:
