# Paid (paid.ai)

## Key Links
- Website: https://www.paid.ai/
- Blog/updates: https://blog.paid.ai/

## Hackathon Perk
- Winning project receives free billing for the first $100k revenue processed through Paid (free tier already covers $10k).

## Product Snapshot
- Billing and business engine built for AI agents.
- Mix subscription, usage, and outcome-based pricing in one platform with minimal code.
- Tracks agent-level signals, margins, and ROI; includes invoicing, renewals, and reporting.

## Implementation Steps (Suggested)
1. Define "value events" your agent creates (e.g., tasks completed, leads qualified, time saved).
2. Emit simple events from your app (customer_id, workflow_id, timestamp) to a metering layer; buffer now, integrate with Paid later.
3. Prototype 1–2 pricing packages (flat + usage, outcome fee) to showcase during demos.

## Demo Tips
- Show a lightweight dashboard (table/chart) estimating invoices or ROI using your metered events.
- Highlight how Paid simplifies onboarding (5 lines of code) and auto margin tracking.
