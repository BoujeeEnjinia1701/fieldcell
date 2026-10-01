---
doc_id: FCL-DEC-001
title: FieldCell design decisions register
project: FieldCell
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions of FCL-DDR-001 to 003 and the review note, items to confirm when parts are bought, and decisions made
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
---

# FieldCell design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Open decisions, Proposed, awaiting Amish.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes P1 to P13 (deck on the cross tubes, braced axle brackets, clevis stand legs, handle sockets, hinge tabs and real hinge, wing frame, outrigger brackets, tie bars, shade uprights, electronics layout and class T fuse in the battery case, 60 mm box gap, fixings) | (a) accept all; (b) accept with named changes | (a) | The whole build plan, every making sketch and step | FCL-DDR-003, Table 1 |
| 2 | The buildable cart is about 80 kg: R6 (75 kg) missed by 5 kg and the R7 grass pull (150 N) by 6 N. Supersedes the 0.06 kg gap of the 2026-09-25 review | (a) relax R6 to 80 kg and the R7 grass figure to 160 N, keeping steel and flat-free tyres; (b) bolted aluminium frame (about 72.7 kg, 142 N), reversing D5; (c) pneumatic tyres (about 77.6 kg); (d) both (about 70.3 kg) | (a) for the first prototype, weighed at TRL 4; (b) if it weighs over 80 kg | Frame material and joints (section 3.1), wheels | FCL-DDR-003, A1; FCL-CAL-001 [E3], [E5], [F1] |
| 3 | How the stowed wings are held together | (a) two tie bars with over-centre latches, as modelled; (b) two webbing straps with cam buckles | (a) | Tie bars (section 3.9), steps 12 and 17; deploy and stow times | FCL-DDR-003, A3 |
| 4 | The shade lifts off (four wing bolts) to open the battery case | (a) accept, service only; (b) hinge the shade on its handle-end uprights | (a) | Shade (section 3.10) | FCL-DDR-003, A4 |
| 5 | Whether to seek a responder organization to review the deployment sequence and load profile, and which one | Name an organization, or not now | None yet | None in the build | FCL-DDR-001, O1 |
| 6 | How FieldCell relates to PowerBox and SwapCell in the portfolio | Position FieldCell against both | None yet | None in the build | FCL-DDR-001, O2 |
| 7 | Whether to add an AC charger or a vehicle 12 V input for cloudy periods | Add one, or not | None yet. An AC charger would add a power inlet, which the safety case now rules out | Electronics box wiring and cut-outs | FCL-DDR-001, O3 |
| 8 | Bring the appearance model and photoreal renders up to the constructable design; settle the render deviations of 2026-09-26 (hinge tabs, in-use cover depth, isolator and monitor position and cable route are now in the model; the clear side window and stake loop direction remain) | (a) rebuild the appearance model from the constructable model and re-render on Amish's Mac, side window as a render aid only; (b) keep the concept renders | (a) | None in the build | `docs/REVIEW.md`, sessions 2026-09-26 and 2026-10-01; FCL-DDR-003 |

## To confirm when parts are bought

*Table 2. Items to confirm when parts are bought.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The solar module is no larger than 1,380 x 680 mm, has Vmp of 36 V or more at standard test conditions, has a back that takes structural tape, and leads long enough to reach the electronics box | Sets the 10 mm rim on the wing frame and the charge headroom at 70 °C | FCL-DDR-003, P7; FCL-DDR-001, D3; FCL-CAL-001 [B4] |
| 2 | The wheel hub is about 60 mm long with a 20 mm bore and bearings | Sets the spacer collar length (37.5 mm) and the axle length (820 mm) | FCL-DDR-003, P3 |
| 3 | The electronics box's mounting plate, its bosses, and the cut-out templates of the DC panel, GFCI and in-use cover, isolator, filter fan and exhaust filter | They set the cut-outs and the layout on the plate | FCL-DDR-003, P11 |
| 4 | The inverter (about 270 x 210 x 110 mm) and charge controller (about 150 x 140 x 70 mm) fit the mounting plate with 10 mm between parts | The layout is drawn for these sizes | FCL-DDR-003, P11 |
| 5 | The battery case has a flat end wall for two M25 glands 150 mm up, and room beside the pack for the class T fuse holder (about 60 x 50 x 45 mm) | The fuse must be within 150 mm of the positive terminal | FCL-DDR-003, P11, P12 |
| 6 | The piano hinge leaves are about 26 x 1.5 mm and the knuckle no more than 8 mm across | The pin sits 4.5 mm above the panel face; a bigger knuckle needs more | FCL-DDR-003, P6 |
| 7 | The over-centre latch and its keeper close on the 12 mm the model allows | Sets the tie bar length (731 mm) | FCL-DDR-003, P9 |
| 8 | The inverter's derating at 45 °C, no-load draw of 10 W or less, and fan noise | R9, R4 and R11 rest on these figures | FCL-DDR-002, A4; FCL-CAL-001 [D6], [I2] |
| 9 | The pack's battery management system peak rating and the class T fuse curve cover about 118 A for a few seconds; charging blocked below 0 °C and above 45 °C | Surge with full DC load | FCL-CAL-001 [B2] |
| 10 | Supplier quotes for the pack, the wings and the inverter | They replace the indicative prices and show the real cost against the value-engineering target | FCL-DDR-002, A1 |

## Value engineering

Value-engineering target: USD 2,100 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 2,101 (USD 1 over the target). Main cost drivers and savings worth trying:

- The largest lines are the two PV wings (USD 460), the pack (USD 300) and the inverter (USD 220).
- Making the design buildable took the BOM from USD 2,051 to USD 2,101: frame steel +USD 12, wheel collars and linch pins +USD 5, outrigger brackets +USD 6, two latches fewer and new fixings -USD 6, cam straps and PV glands +USD 15, shade uprights +USD 9 and tie bars +USD 9.
- The USD 1 gap is well inside the accuracy of indicative prices. Supplier quotes for the pack, wings and inverter are the first saving to try.
- Webbing straps with cam buckles in place of the tie bars (decision 3 above) are the other place to look for a small saving.

## Decisions made

*Table 3. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D8: 25.6 V 50 Ah pack, fixed east-west wings at 15° as the cart walls, 24 V class panels in parallel, 120 V 60 Hz first, welded steel frame and flat-free tyres, SwapCell as a future variant only, budget held until quotes, disaster response first | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | FCL-DDR-001 |
| 2026-09-25 | Budget raised to $2,100; R6 limit relaxed to 75 kg; thermostat filter fan; reflective sun shade; 20 mm hinge spacer; "peak sun hours" read as global horizontal irradiation; heavy parts low and over the axle | Amish: "i accept all your recommendations, go with them across all repos." | FCL-DDR-002 |
| 2026-09-25 | TRL 4 on hold: no building, testing or purchasing | Amish, same instruction as D1 to D8 | FCL-DDR-001 |
| 2026-09-26 | FieldCell chosen for the first batch of product renders | Amish (words not recorded) | `docs/REVIEW.md`, session 2026-09-26 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; record outstanding decisions in this register, not in the build plan. The changes made under this instruction (FCL-DDR-003) are open for Amish's review (Table 1, item 1) | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." and "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | FCL-DDR-003 (Draft) |
