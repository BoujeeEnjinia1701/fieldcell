---
doc_id: FCL-DEC-001
title: FieldCell design decisions register
project: FieldCell
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
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
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for all eight open decisions (FCL-DDR-003 accepted); moved to decisions made"
---

# FieldCell design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

*Table 1. Items to confirm when parts are bought.*

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
- Webbing straps with cam buckles in place of the tie bars were the other place to look for a small saving; the tie bars were kept on 2026-10-02.

## Decisions made

*Table 2. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D8: 25.6 V 50 Ah pack, fixed east-west wings at 15° as the cart walls, 24 V class panels in parallel, 120 V 60 Hz first, welded steel frame and flat-free tyres, SwapCell as a future variant only, budget held until quotes, disaster response first | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | FCL-DDR-001 |
| 2026-09-25 | Budget raised to $2,100; R6 limit relaxed to 75 kg; thermostat filter fan; reflective sun shade; 20 mm hinge spacer; "peak sun hours" read as global horizontal irradiation; heavy parts low and over the axle | Amish: "i accept all your recommendations, go with them across all repos." | FCL-DDR-002 |
| 2026-09-25 | TRL 4 on hold: no building, testing or purchasing | Amish, same instruction as D1 to D8 | FCL-DDR-001 |
| 2026-09-26 | FieldCell chosen for the first batch of product renders | Amish (words not recorded) | `docs/REVIEW.md`, session 2026-09-26 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; record outstanding decisions in this register, not in the build plan. The changes made under this instruction (FCL-DDR-003) are open for Amish's review (Table 1, item 1) | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." and "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | FCL-DDR-003 (Draft) |
| 2026-10-02 | Design for construction accepted: the changes P1 to P13 as made (open item 1) | Amish: "i approve your recommendations for all 555 open decisions." | FCL-DDR-003, Table 1 |
| 2026-10-02 | Mass and pull: steel frame and flat-free tyres kept; R6 set at 82 kg and the R7 grass pull at 160 N (sharpened from the 80 kg first proposed, to keep a margin); the prototype is weighed at TRL 4 and moves to the bolted aluminium frame (option b) if it is over 82 kg (open item 2) | Amish: "i approve your recommendations for all 555 open decisions." | FCL-DDR-003, A1; FCL-CAL-001 [E3], [E5], [F1]; FCL-REQ-001 R6 and R7 |
| 2026-10-02 | Stowed wings held by the two tie bars with over-centre latches, as modelled (option a) (open item 3) | Amish: "i approve your recommendations for all 555 open decisions." | FCL-DDR-003, A3 |
| 2026-10-02 | The shade lifts off on four wing bolts to open the battery case, for service only (option a) (open item 4) | Amish: "i approve your recommendations for all 555 open decisions." | FCL-DDR-003, A4 |
| 2026-10-02 | Seek a responder organization now, for a paper review of the deployment sequence and load profile only; first candidate to approach a US volunteer disaster response organization such as Team Rubicon, since the first build is 120 V 60 Hz (open item 5) | Amish: "i approve your recommendations for all 555 open decisions." | FCL-DDR-001, O1 |
| 2026-10-02 | Positioning: FieldCell is the mobile field-site unit (PV only, 1 kW AC, one-person cart, own 25.6 V pack), PowerBox the household outage unit (multi-input, indoor, SwapCell pack) and SwapCell the shared pack standard; one paragraph saying so goes in each README (open item 6) | Amish: "i approve your recommendations for all 555 open decisions." | FCL-DDR-001, O2 |
| 2026-10-02 | No AC charger; the vehicle 12 V input is left out of the first prototype and may be offered later as a DC-to-DC charging option if the responder review asks for it (open item 7) | Amish: "i approve your recommendations for all 555 open decisions." | FCL-DDR-001, O3 |
| 2026-10-02 | Appearance model rebuilt from the constructable model and re-rendered on Amish's Mac, with the clear side window as a render aid only (option a) (open item 8) | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, sessions 2026-09-26 and 2026-10-01; FCL-DDR-003 |
