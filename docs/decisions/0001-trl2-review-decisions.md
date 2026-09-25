---
doc_id: FCL-DDR-001
title: FieldCell TRL 2 review decisions
project: FieldCell
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's decisions on the TRL 2 review items and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for items D1 to D8; items O1 to O5 remain proposed

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-24) listed nine items as "Proposed, awaiting Amish", most with a recommendation. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided in favor of that recommendation. Items without a recommendation stay open. The same instruction approved portfolio-wide decisions on the SwapCell interface, which bear on item D6.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-24) and in FCL-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Decided items.*

| # | Item | Decision |
| --- | --- | --- |
| D1 | Battery system voltage | 25.6 V 50 Ah LiFePO4 (rather than 12.8 V 100 Ah or 51.2 V). Decided by Amish, 2026-09-25: go with recommendation. |
| D2 | Wing layout | Fixed east-west wings at 15° that fold up as the cart walls (rather than detachable panels on kickstands). Decided by Amish, 2026-09-25: go with recommendation. |
| D3 | Panels | 24 V class panels (Vmp about 36 V) wired in parallel into one MPPT (rather than 12 V class in series). Decided by Amish, 2026-09-25: go with recommendation. |
| D4 | AC output | 120 V 60 Hz for the first build, with a 230 V 50 Hz variant documented. Decided by Amish, 2026-09-25: go with recommendation. |
| D5 | Frame and wheels | Welded steel frame with flat-free tyres (rather than bolted aluminium and pneumatic tyres). Decided by Amish, 2026-09-25: go with recommendation. |
| D6 | SwapCell | Compatibility with a SwapCell 48 V pack is recorded as a future variant only; the concept is not designed around it. Decided by Amish, 2026-09-25: go with recommendation. |
| D7 | Budget | Keep `budget_usd` at $1,500 for now and decide after supplier quotes at TRL 3 (rather than raising it to about $1,750 now). Decided by Amish, 2026-09-25: go with recommendation. |
| D8 | First user group | Disaster response first (rather than humanitarian field teams or remote crews). Decided by Amish, 2026-09-25: go with recommendation. |

Notes on the decided items:

- **D6.** Portfolio-wide, Amish also approved on 2026-09-25 that the SwapCell interface adds a wake method for hosts without CAN, a charge-while-discharging mode and a latch vibration rating for vehicles. A future FieldCell SwapCell variant would rely on all three, cited as SwapCell interface v0.3 items: FieldCell's baseline electronics have no CAN bus, PV charging while loads run is its normal operating state, and the cart shakes its payload on rough ground. Shared SwapCell packs are priced once in the SwapCell repo and excluded from dependent kit budgets; the FieldCell baseline uses its own 25.6 V pack, so this does not change the FieldCell BOM.
- **D7.** The TRL 3 BOM now totals about $2,006 (FCL-CAL-001, section J). `budget_usd` stays at $1,500 as decided, and a new budget proposal is recorded in `docs/REVIEW.md` as "Proposed, awaiting Amish".
- **D2** covers the wings-as-walls architecture, since the recommended wing layout is the hinged wing that forms the cart side in travel.

*Table 2. Items that remain open (Proposed, awaiting Amish).*

| # | Item | Why it stays open |
| --- | --- | --- |
| O1 | Whether to seek a responder organization to review the deployment sequence and load profile, and which one | No recommendation was made; needs Amish |
| O2 | How FieldCell relates to PowerBox and SwapCell in the portfolio, so the three do not overlap | No recommendation was made; needs Amish |
| O3 | Whether to add an AC charger or a vehicle 12 V input for cloudy periods | Listed as an open option with no recommendation |
| O4 | Heavy parts low and over the axle, with the electronics box and bin balancing fore and aft | Listed in FCL-PRC-001 as proposed but not among the review items Amish decided |
| O5 | New TRL 3 proposals: budget, mass limit, electronics box fan, sun shade, hinge spacer, reading of "peak sun hours" | Raised by FCL-CAL-001 after the decision; see `docs/REVIEW.md`, session 2026-09-25 |

## Consequences

- FCL-PRB-001, FCL-PRC-001 and FCL-REQ-001 are revised to v0.3: the decided choices are no longer marked proposed, and R2 names 120 V 60 Hz for the first build.
- No requirement target was relaxed or redefined by these decisions. `budget_usd` is unchanged at $1,500.
- The decided steel frame and flat-free tyres put the cart at about 73.5 kg, over the 70 kg limit of R6 (FCL-CAL-001, section E). This is reported, not redesigned; options are proposed in `docs/REVIEW.md`.
- TRL 4 work stays on hold by Amish's instruction.
