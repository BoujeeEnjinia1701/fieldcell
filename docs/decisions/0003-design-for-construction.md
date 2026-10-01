---
doc_id: FCL-DDR-003
title: FieldCell design for construction
project: FieldCell
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. The changes in Tables 1 and 2 were made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are Proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model of FCL-DDR-002 showed what FieldCell does, but it was a massing model: build123d checks found parts cutting into each other, parts standing in mid air and parts with no fixing. Examples: the deck sheet cut 5 mm into all three cross tubes (36,660 mm³ of overlap); the hinge spacers stood 20 mm clear of the rails, which the appearance-model session of 2026-09-26 had already noted; the hinge tubes cut 1.25 million mm³ into the folded-out wings; the axle stopped at the wheel centres and the wheels had no bore; the sun shade posts stood beside the boxes, 300 mm above the frame, touching nothing; and the fusing block sat on top of the charge controller.

The changes keep what FieldCell does: the same cart, frame size, wheels, deck height, wings, 15° tilt, hinge line and 28 mm wing-to-tyre clearance, the same battery, electronics, outlets and shade, the same layout rule (heavy parts low and over the axle) and the same deploy-by-one-person sequence. They do not change the pitch or the safety case; the class T fuse moves to where the safety section already says it must be. Every change is in `cad/src/model.py`, which now runs 96 constructability checks in both the parked and travel poses (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must not touch are apart by at least the stated clearance. All 96 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | Deck sheet inside the frame, cutting 5 mm into the cross tubes | Expanded steel sheet 1,200 x 520 mm laid on top of the three cross tubes, between the rails, stitch welded; all tubes 5 mm lower so the deck top stays 460 mm above the ground | The sheet is carried by the cross tubes instead of hanging in the frame opening; deck height, clearance and every height above it are unchanged |
| P2 | Open rail ends | 3 mm steel end caps on the four rail ends | Seals the tubes and gives the handle socket gussets a face to weld to |
| P3 | Axle brackets cut 10 mm into the rails, unbraced; axle ended at the wheel centres; wheels had no bore | Brackets 60 x 5 mm plate, 247 mm long, welded under each rail 290 mm out, with a 5 mm gusset to the middle cross tube; 20 mm axle 820 mm long welded to both brackets; each wheel (20 mm bore with bearings) between a 37.5 mm spacer collar and a washer, held by a linch pin | A fixed axle with the bearings in the bought wheels is the simplest garage build; the collar sets the wheel clear of the bracket; the gusset carries side loads into the frame |
| P4 | Stand legs half under the rails, touching them, with no pivot or lock | Legs under the rail centre line on pairs of 3 mm clevis plates welded under the rails 40 mm from each end; M10 pivot bolt 35 mm below the rail; spring detent pin; 60 x 60 x 5 mm feet; legs fold inward along the rail | The concept says the legs fold; this is a fold that clears the wheels (8.6 mm) and the rails (5 mm) |
| P5 | Handle tubes ran into the end cross tube with no joint, although the handle detaches | Two 33.7 x 2.6 mm sockets welded on the rail ends at 30.5°, each with a 4 mm gusset to the end cap; the 28 mm handle legs slide in (0.25 mm clearance) and a quick-release pin holds each | Keeps the detachable handle and the 900 mm grip height |
| P6 | Hinge spacer angles 20 mm clear of the rails; hinge tube inside the folded-out wing; no hinge leaves | Eight 30 x 3 mm steel tabs welded to the rail outer faces carry the decided 20 x 20 x 2 mm angle on M5 bolts; a 1.2 m stainless piano hinge with 26 x 1.5 mm leaves, fixed leaf screwed to the angle, moving leaf to the wing's inner member; hinge pin 4.5 mm above the panel face (330 mm out, 495 mm up) | The angle decided in FCL-DDR-002 is kept and given something to bolt to. The pin sits just above the panel face so the panel clears the knuckle and lies exactly where the concept put it: 28 mm over the tyre, 15° tilt, 2,012 mm span |
| P7 | Each wing a solid block | 200 W semi-flexible module (about 1,380 x 680 mm) bonded with structural tape to a 1,400 x 700 mm frame of 30 x 20 x 1.5 mm aluminium tube with three ribs, joined by inside corner cleats and rivets; wing about 6.0 kg (6.5 kg assumed) | The "ventilated aluminium backing frame" of the BOM made definite: open bays ventilate the module, every member supports it |
| P8 | Outrigger legs pushed into the wing underside with no fixing | Aluminium U bracket riveted under the wing's outer member, 80 mm from each end; M8 pivot; 269 mm leg of 25 x 2 mm steel tube; 50 x 50 x 4 mm foot with its stake loop pointing along the cart; legs fold flat under the wing, 7.5 mm clear of the frame | A leg that folds and locks, with the loop placed so the folded leg lies flat |
| P9 | Over-centre latches with nothing to latch to: stowed, the wing's inside face is the PV module | Two tie bars (20 x 20 x 1.5 mm aluminium, 731 mm) pivoted on brackets at the top corners of the left wing; in travel each lies across the tops of both wings and an over-centre latch on its end pulls the right wing in against it; parked, it folds down the back of the left wing. Two latches and keepers instead of four | Nothing may press on the module face, and the frame's only free faces are its tops and backs. One bar at each end, both kept on the wing, nothing loose. Adds about 0.5 min to deploy and to stow |
| P10 | Shade posts stood beside the boxes in mid air; the shade blocked the battery lid | Four 20 x 20 x 1.5 mm aluminium uprights, 355 mm, bolted to tabs on the rail tops at 400 and 1,100 mm from the front end; shade frame 830 x 580 mm (was 540 mm wide) rests on them with a wing bolt at each; lift it off to open the battery lid | Same 50 mm air gap over both boxes; the uprights sit on the frame, 28 mm clear of every box; the frame rests on the uprights, so the extra 40 mm of width is where they stand |
| P11 | Fusing block sat on top of the charge controller; outlets and fans drawn as boxes outside the wall; class T fuse in the electronics box, more than 250 mm from the battery terminal | Inverter, charge controller and DIN rail (breakers and shunt) side by side on the box's mounting plate; outlets, isolator, filter fan and exhaust filter through cut-outs; class T fuse holder inside the battery case beside the pack, within 150 mm of the positive terminal; isolator on the outlet face | Every part has a fixing and at least 10 mm to its neighbours. The fuse goes where the safety section (FCL-PRC-001) already requires it |
| P12 | 50 mm between the boxes: two M25 gland domes and the cables did not fit | Electronics box moved 10 mm toward the handle (its end 10 mm inside the frame end); 60 mm between the boxes; two M25 glands in each facing wall, 40 mm each side of centre, 150 mm up; 16 mm of cable between the domes; two M16 PV glands in the electronics box side walls | Shortest, straight cable run; nothing bends between the boxes |
| P13 | Battery case, electronics box and bin not fixed to the deck; pack loose in its case | Two cam straps round the battery case and lid, through the deck; four M6 bolts through the electronics box floor with large washers under the deck; bin strap through the deck; pack on a rubber mat with foam blocks | So nothing moves on rough ground or in a tip |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 75.06 kg to 79.99 kg (+4.93 kg) [E3]. Frame 12.8 to 15.4 kg, weighed from the model's own solids [E1]; stand legs 1.8 to 2.5 kg; hinges, latches, outriggers and stakes 3.0 to 4.1 kg; shade 1.0 to 1.55 kg; tie bars 0.5 kg and straps 0.3 kg added; wings 13.0 to 12.0 kg [E8] | Brackets, gussets, tabs, sockets, clevises, end caps and fixings that the massing model did not have |
| Requirements | R6 not met by 5.0 kg (was 0.06 kg); handle force 14 to 54 N [E4]. R7 now not met: 156 N pull on grass against 150 N [F1]. R12 cost over the value-engineering target by USD 1 [J1]. Unstaked wing lift 9.2 to 8.9 m/s [H1]; stake pull-out 28 N [H2]. Deploy 6.0 to 6.5 min, stow 5.0 to 5.5 min [I1] | Follows the mass and the tie bars |
| Envelope | Stowed without the handle 1,400 x 784 x 1,190 to 1,400 x 830 x 1,220 mm [K1] | Folded outrigger feet and the tie bars, now in the model |
| Cost | BOM lines 1, 2, 3, 4, 12, 13, 14, 15, 16, 17 and 18 re-specified, line 19 (tie bars) added; $2,051 to $2,101 against the unchanged $2,100 value-engineering target (`budget_usd`) | Parts added for construction |
| Drawing | FCL-DWG-002 Rev P4; making sketches FCL-DWG-101 to 111 added | Follows the model |
| Documents | FCL-CAL-001 v0.3, FCL-PRC-001 v0.5, FCL-REQ-001 v0.5 | Follows the model |
| Thermal | Unchanged: boxes, shade gap and fan unchanged; the class T fuse adds no heat of note | |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The buildable cart is about 80 kg: R6 (75 kg) is missed by 5 kg and R7 (150 N on a 10 % grass grade) by 6 N | (a) relax R6 to 80 kg and the R7 grass figure to 160 N, keeping the decided steel frame and flat-free tyres; (b) bolted aluminium frame, about 72.7 kg and 142 N, meeting both but reversing D5 (FCL-DDR-001); (c) pneumatic tyres, about 77.6 kg, still over; (d) both, about 70.3 kg | (a) for the first prototype, and weigh it at TRL 4; take (b) if the weighed cart is over 80 kg |
| A2 | The BOM is $2,101 against the $2,100 value-engineering target (`budget_usd`, a hypothetical control target), USD 1 over | No decision needed. The target stays $2,100; supplier quotes for the pack, wings and inverter will give the real cost | Carry in the value engineering section of FCL-DEC-001 |
| A3 | Tie bars add a step to deploy and stow (R5 still met at 6.5 and 5.5 min) | (a) tie bars as modelled; (b) two webbing straps with cam buckles over the wing tops | (a): stiffer, nothing to lose, and they hold both wings at once |
| A4 | The shade must be lifted off (four wing bolts) to open the battery case | (a) accept, since the battery case is opened only for service; (b) hinge the shade on its handle-end uprights | (a) |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan FCL-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); open items are in the design decisions register FCL-DEC-001.
- Requirement status (FCL-CAL-001 v0.3): 6 met, 2 not met (R6, R7), 1 over its value-engineering target (R12), 1 at risk (R9), 2 not verifiable at TRL 3 (R8, R11). Before: 7 met, 1 not met, 2 at risk, 2 not verifiable.
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept hinge spacer, shade posts, outrigger feet and electronics layout, and have no tie bars; they need updating on Amish's Mac, where Blender is.
- The wing module, wheels, enclosures and outlets are chosen at TRL 4; their sizes must be checked then against the model (FCL-DEC-001, "To confirm when parts are bought").
