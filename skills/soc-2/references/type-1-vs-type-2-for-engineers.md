# Type 1 vs Type 2 — Engineer's View

## What the report says

| | Type 1 | Type 2 |
|---|---|---|
| Scope of the opinion | Design of controls at a point in time | Design **and operating effectiveness** of controls **over a period** |
| Observation window | A single date | Typically 6–12 months |
| Evidence sampled | "Do these controls exist, are they designed to meet the criterion" | "Did these controls operate as designed, every time, across the period" |
| Sample size | Walkthroughs, one per control | Population-based sampling (often 25 per control, more for higher-frequency controls) |
| Typical use | First-ever report; proof you are on the path | What buyers ask for; what you live with every renewal |
| Time to produce | Weeks | Months of observation + weeks of fieldwork |

## What changes in system design when preparing for Type 2

Type 1 rewards a clean snapshot. Type 2 rewards a reliable stream.

| Design choice | Type 1 is OK with... | Type 2 requires... |
|---|---|---|
| Evidence storage | Screenshots in a folder | Queryable store with retention for the full period |
| Control events | "We do UARs" with one sample | Structured event for every review in the period with reviewer, date, population, outcome |
| Change management | A merge policy in a README | A typed approval receipt per change for the full period |
| Termination | A documented process | Actual termination events in the population, every one deprovisioned inside SLA, evidence of it |
| Vendor management | An onboarding template | Onboarding events for every vendor added in the period, with risk scores and approvals |

The common thread: Type 2 needs **populations**, not samples. Every control event that happened has to be findable in the evidence store.

## Sampling in practice

Auditors test operating effectiveness by sampling from the population of control instances. Frequency drives sample size:

| Control frequency | Typical sample size (Type 2, 12-month period) |
|---|---|
| Continuous (always on) | Observation of the configuration + population of exceptions |
| Daily | 25 |
| Weekly | 10 |
| Monthly | 5 |
| Quarterly | All (4) |
| Annually | All (1) |
| Per-event (e.g., new joiner, termination) | 25 or full population if smaller |

This is not AICPA guidance — it is pattern-recognition from real engagements. Your auditor will have their own table and you should ask for it up front.

## Evidence retention for Type 2

Retain raw evidence for the entire observation window, plus a margin for the fieldwork phase (auditors start sampling during the period, not only after). 18 months of retention for a 12-month period is a safe default.

Derived tables (populations, summaries) can be materialized from raw events. Keep the raw events; you can always re-derive, but you cannot un-drop them.

## Bridge letters

A bridge letter extends the assurance of a completed Type 2 to cover the gap between the report's period end and a buyer's current date. It is signed by management, not the auditor, and asserts that controls have continued to operate as described.

Engineering impact: you need to be able to say truthfully that nothing has materially changed. If you rolled out a new IdP, replaced your HRIS, or changed your change-management process during the gap, the bridge letter cannot cover that change — it becomes fieldwork for the next report.

## Going from Type 1 to Type 2 cleanly

1. Treat the Type 1 as a design specification, not a finish line. Every control described in the Type 1 needs to emit operating evidence for the Type 2 period.
2. Pick a period-start date that gives you enough time to fix the gaps Type 1 surfaced. Six weeks of runway is typical.
3. Turn on population logging for every control **before** the period starts. Retrofitting is painful and often generates "exceptions" that are actually instrumentation gaps.
4. Run an internal mock audit at month 3. The goal is to surface instrumentation gaps while there is still time to fix them and re-test within the period.
5. At month 5, freeze control definitions — changing a control mid-period creates two periods' worth of work.

## Who decides Type 1 vs Type 2

Buyers. If the RFP says "SOC 2 Type 2", a Type 1 will not clear the security review. Most buyers accept a Type 1 plus a committed Type 2 start date if you are early in your compliance journey, but the ask always resolves to "when will the Type 2 be ready."

Engineering teams should push back on "just get a Type 1 before the conference" asks unless the subsequent Type 2 is resourced. A Type 1 without a Type 2 plan is a yellow flag that the program is theater.
