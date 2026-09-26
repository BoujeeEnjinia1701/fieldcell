---
doc_id: FCL-DDR-002
title: FieldCell recommendations accepted
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
  change: Record Amish's acceptance of all open recommendations and what changed in the repo
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted for items A1 to A7; items O1 to O3 remain proposed

## Context

After the TRL 3 session, `docs/REVIEW.md` (session 2026-09-25) listed ten items as "Proposed, awaiting Amish", seven of them with a recommendation, and FCL-DDR-001 left items O1 to O5 open. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every open item that carries a recommendation is therefore decided in favor of it; where the recommendation chose among options, the recommended option is the decision. Items without a recommendation stay open. TRL 4 remains on hold by Amish's instruction, so any part of a decision that needs building, testing or purchasing is recorded but not done.

## Options considered

The options for each item are those listed in `docs/REVIEW.md`, session 2026-09-25, "Proposed, awaiting Amish", items 4 to 10, and in FCL-DDR-001, Table 2.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| A1 | Budget (R12); REVIEW item 5 | Option (a): raise `budget_usd` to about $2,100 (BOM plus a small contingency), to be confirmed by quotes for the pack, PV wings and inverter | `project.yaml` `budget_usd` 1,500 to 2,100; R12 target $2,100; BOM $2,051 after A4 and A5, so R12 is now met with about 2.4 % contingency. Obtaining quotes is purchasing work and is on hold with TRL 4 |
| A2 | Mass limit (R6); REVIEW item 6 | Option (a): relax the R6 mass limit from 70 kg to 75 kg, keeping the steel frame and flat-free tyres | FCL-REQ-001 R6 target 75 kg. The cart is 75.06 kg after A4 and A5, so R6 is still not met, by 0.06 kg; a follow-up is proposed in `docs/REVIEW.md` |
| A3 | Electronics box ventilation (R8, R9); REVIEW item 7 | Adopt the thermostat-controlled IP54 filter fan (40 to 60 m³/h) with IP54 exhaust filter | Already priced (BOM item 7) and modeled; now marked decided in FCL-PRC-001, FCL-REQ-001 (R8 wording) and the BOM |
| A4 | Sun shade (R9); REVIEW item 8 | Add a light reflective shade over the battery and electronics enclosures; obtain inverter derating data at 45 °C | New BOM item 18 ($30, 1 kg); shade added to `cad/src/model.py` and the media; FCL-CAL-001 section G: pack in noon sun at 45 °C ambient 55 to 48 °C, box at 1 kW 54 to 53 °C. The derating data comes with supplier selection and is on hold with the quotes |
| A5 | Hinge spacer; REVIEW item 9 | Raise each hinge line by a 20 mm spacer | `hinge_z` 470 to 490 mm; BOM item 14 $45 to $60 with two 20 × 20 × 2 mm aluminium angles (0.53 kg); wing to tyre clearance 8 to 28 mm; stowed height 1,170 to 1,190 mm; drawing FCL-DWG-002 Rev P1 to P2 |
| A6 | "Peak sun hours" basis (R3, R4); REVIEW item 10 | Confirm the reading as daily global horizontal irradiation in kWh/m²/day | R3 and R4 targets restated in kWh/m²/day GHI; the assumption no longer marked proposed |
| A7 | Heavy parts low and over the axle; FCL-DDR-001 O4, REVIEW item 4 | Keep it as a layout rule | FCL-PRC-001 key design choice marked decided |

*Table 2. Items that remain open (Proposed, awaiting Amish).*

| # | Item | Why it stays open |
| --- | --- | --- |
| O1 | Whether to seek a responder organization to review the deployment sequence and load profile, and which one | No recommendation was made |
| O2 | How FieldCell relates to PowerBox and SwapCell in the portfolio | No recommendation was made |
| O3 | Whether to add an AC charger or a vehicle 12 V input for cloudy periods | Listed as an open option with no recommendation |

## Consequences

- Controlled documents revised: FCL-PRB-001 v0.4, FCL-PRC-001 v0.4, FCL-REQ-001 v0.4, FCL-CAL-001 v0.2 and FCL-DDR-001 v0.2. The model, STEP and STL files, drawing FCL-DWG-002 (Rev P2), BOM and concept media were regenerated.
- Requirement status (FCL-CAL-001 v0.2): 7 met (R1, R2, R3, R4, R5, R10, R12), 1 not met (R6, by 0.06 kg), 2 at risk (R7, R9), 2 not verifiable at TRL 3 (R8, R11). Before: 6 met, 2 not met (R6, R12).
- The decisions add 1.5 kg. With the relaxed limit the cart sits at 75 kg, so R7 pull force on grass is 147 N against 150 N.
- No cross-repo change follows from these decisions.
- `trl` and `trl_target` stay at 3. TRL 4 work (quotes and purchasing, building, testing) stays on hold by Amish's instruction.
