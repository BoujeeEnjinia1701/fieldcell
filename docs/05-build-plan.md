---
doc_id: FCL-BLD-001
title: FieldCell prototype build plan
project: FieldCell
doc_type: Build plan
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan; design made constructable (FCL-DDR-003)
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
---

# FieldCell prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order. The wings and their parts (13 to 17) are drawn off to the front so the boxes stay visible.*

The prototype is one FieldCell cart: a welded steel frame on two 16 in wheels, carrying a battery case and an electronics box under a reflective shade, with two solar wings hinged along its sides. Parked, the wings fold out on legs at 15° and the cart stands on four legs; for travel the wings fold up as the cart sides and two tie bars hold them together at the top. Figure 1 shows the 21 components in the order you make or fit them. The made parts are the frame, axle, stand legs, handle, hinge spacer angles, wing frames, outrigger legs, tie bars and shade; the battery case and electronics box are bought and drilled or cut. The rest is bought: wheels, battery pack, charge controller, inverter, outlets, fusing, hinges, latches, solar modules, bin, cables and fixings. The work is cutting, drilling and MIG welding steel tube and plate, cutting, drilling and riveting aluminium tube and angle, cutting plastic enclosures, and wiring bought parts with crimped lugs. The parts cost about $2,101 from the bill of materials, against a value-engineering target of $2,100. The finished cart weighs about 80 kg: a two-person lift.

> **Safety:** The prototype holds a 1.28 kWh lithium iron phosphate battery, makes 120 V AC, carries up to about 100 A of DC and has solar panels that are live whenever light falls on them. Keep the class T fuse out until section 6 says otherwise, never connect FieldCell to building wiring, and never charge the pack below 0 °C or above 45 °C. Welding needs a welding helmet, gloves, a fire watch and a clear floor. Cut steel and aluminium edges are sharp: deburr everything. The finished cart is about 80 kg: lift it with two people and keep fingers out of the hinges and folding legs.

## 2. What changed to make it buildable

The concept showed what the cart does; some of its parts could not be made or fixed as drawn. Each change below keeps what the cart does, and all of them are recorded in decision record FCL-DDR-003, open for Amish's review.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Deck | A sheet inside the frame, cutting into the cross tubes | An expanded steel sheet laid on the cross tubes between the rails; tubes 5 mm lower, deck top still 460 mm (Figure 2) | The sheet is carried, not hung |
| Axle and wheels | Axle ending at the wheel centres; wheels with no bore; brackets cut into the rails | A welded 820 mm axle through braced brackets; each wheel between a spacer collar and a washer, held by a linch pin (Figure 5) | A fixed axle with bearings in the bought wheels |
| Stand legs | Legs touching the rails, no pivot | Legs on welded clevis plates with a pivot bolt and detent pin, folding along the rail (Figure 7) | The legs fold as the concept says |
| Handle | Tubes running into the frame end with no joint | Two welded sockets with gussets; the handle legs drop in and are pinned (Figure 26) | The handle still detaches |
| Hinge line | Spacer angles standing 20 mm clear of the rails; hinge inside the wing | Steel tabs welded to the rails carry the spacer angle; a real piano hinge with its pin just above the panel face (Figure 9) | The wing sits exactly where the concept put it, 28 mm over the tyre |
| Wings | A solid block | A module bonded to a frame of aluminium tube with three ribs (Figure 17) | The backing frame made definite |
| Outrigger legs | Pushed into the wing, no fixing | A riveted U bracket, a pivot bolt and a detent; the leg folds flat under the wing (Figure 19) | They fold and lock |
| Wing latches | Latches with nothing to latch to | Two tie bars across the tops of the stowed wings, with an over-centre latch (Figures 21 and 22) | Nothing may press on the solar face, which faces in when stowed |
| Sun shade | Posts in mid air beside the boxes; the shade blocked the battery lid | Four uprights bolted to tabs on the rails; the shade lifts off (Figure 24) | It stands on the frame and comes off for service |
| Electronics | Parts stacked on each other and drawn outside the box wall; class T fuse far from the battery | Parts side by side on the mounting plate, outlets and fans through cut-outs; class T fuse in the battery case (Figure 14) | Every part fixed; the fuse within 150 mm of the battery terminal |
| Box spacing | 50 mm between the boxes: the glands did not fit | Electronics box 10 mm nearer the handle; 60 mm gap with two glands each side (Figure 12) | A straight cable run |
| Fixings | Boxes and bin loose on the deck | Cam straps, four floor bolts and a bin strap | Nothing moves on rough ground |

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Front" is the bin end and "handle end" is the other; "left" and "right" are as seen standing behind the handle looking forward along the cart (the right wing is on your right). Workshop tolerance is 1 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Frame

![Figure 2. Making sketch of the frame](../cad/drawings/FCL-DWG-101.png)

*Figure 2. Frame making sketch (FCL-DWG-101).*

![Figure 3. Where each welded part sits on the frame](05-build-plan/frame-layout.png)

*Figure 3. Where each welded part sits, measured from the front end of the frame.*

**What it is and what it is made from.** The welded steel frame everything sits on: two rails, three cross tubes, a deck sheet, and the small plates and tubes the other parts bolt to. Steel square tube 40 x 40 x 1.5 mm (S235 or similar), expanded steel sheet (about 4.5 kg per square metre), steel flat bar and plate 3 to 5 mm, and steel tube 33.7 x 2.6 mm.

**How to make it.**

1. Cut two rails 1,200 long and three cross tubes 520 long from 40 x 40 x 1.5 tube; square the ends.
2. On a flat table, set the rails 600 apart outside to outside, with the cross tubes between them at the two ends and in the middle (centres at 20, 600 and 1,180 from the front end). Tack, check the diagonals are equal within 2 mm, then weld all round.
3. Weld a 40 x 40 x 3 end cap on each of the four rail ends.
4. Deck: cut expanded steel sheet to 1,200 x 520, lay it on the cross tubes between the rails and stitch weld 25 mm every 150 mm to the cross tubes and the rail inner faces.
5. Axle brackets: cut two 60 x 5 plates 247 long; drill a 20.5 hole on the centre line 35 from one end. Weld one under each rail, square to it, hole end down, plate centre 630 from the front end and 290 from the centre line (it sits under the outer half of the rail). Cut two right-angle triangles 87 x 85 from 5 plate and weld one between the inboard face of each bracket and the underside of the middle cross tube.
6. Hinge tabs: cut eight 75 lengths of 30 x 3 flat bar; drill a 5.5 hole 11 below one end. Weld four to the outer face of each rail, upright, hole end up, bottom end 4 above the rail underside, centred 60, 420, 780 and 1,140 from the front end. Their tops stand 39 above the rail top.
7. Stand leg clevises: cut sixteen 40 x 55 plates from 3 plate; drill a 10.5 hole 20 from one end and a 6.5 detent hole 30 below it. Weld them in pairs under each rail, 26 apart inside, centred on the rail centre line, 40 from each rail end (Figure 3), holes lined up. Drill a second 6.5 detent hole in each plate, 30 from the pivot hole toward the middle of the cart, for the folded position.
8. Handle sockets: cut two 150 lengths of 33.7 x 2.6 tube; mitre one end at 30.5° so it sits flat on the rail top. Weld each on a rail top, centred on the rail, its axis meeting the rail top 1,145 from the front end, leaning toward the handle end at 30.5° and turned in by 3° (the handle legs close from 560 to 480 apart). Weld a 4 mm triangular gusset from the end cap to the underside of each socket. Drill an 8.5 hole across each socket 120 up its axis for the quick-release pin.
9. Shade upright tabs: four 60 lengths of 20 x 3 flat bar with a 6.5 hole 30 from the top; weld upright on the rail tops, on the outer side of where each upright stands (400 and 1,100 from the front end, 280 out from the centre line).
10. Clean the welds, deburr, prime and paint.

**How it fits the parts next to it.** The axle passes through both bracket holes (Figure 5). The battery case, electronics box and bin sit on the deck. The hinge spacer angles bolt to the outside of the tabs (Figure 9). The stand legs hang between the clevis plates (Figure 7). The shade uprights stand on the rail tops against their tabs (Figure 24). The handle legs drop into the sockets (Figure 26).

**Check before moving on.** The deck is flat within 3 mm; a 20 mm bar slides through both bracket holes at once; the tab holes line up along a straight line on each side.

### 3.2 Axle

![Figure 4. Making sketch of the axle](../cad/drawings/FCL-DWG-102.png)

*Figure 4. Axle making sketch (FCL-DWG-102).*

**What it is and what it is made from.** A fixed axle welded to both brackets; the wheels turn on their own bearings. Bright mild steel bar 20 mm diameter.

**How to make it.**

1. Cut 820 of 20 bar; chamfer both ends 1 mm.
2. Drill a 5 cross hole 10 from each end, both in the same plane.
3. Slide it through both brackets so 410 stands each side of the centre line, cross holes vertical, and weld it to both faces of both brackets.

**How it fits the parts next to it.**

![Figure 5. Joint 1: axle, bracket, collar and wheel hub](05-build-plan/joint-01.png)

*Figure 5. Cut through the axle: the spacer collar sits between the bracket and the wheel hub; the washer and linch pin hold the hub on.*

Each end takes, in order from the bracket: a spacer collar 26 outside, 20 bore, 37.5 long; the wheel (hub 60 long, 20 bore with bearings); a 20 washer 3 thick; the linch pin through the cross hole.

**Check before moving on.** Both wheels spin freely with 0.5 to 1 mm of end float.

### 3.3 Stand legs (make 4)

![Figure 6. Making sketch of the stand leg](../cad/drawings/FCL-DWG-103.png)

*Figure 6. Stand leg making sketch (FCL-DWG-103).*

**What it is and what it is made from.** The four legs that hold the deck level when parked. Steel tube 25 x 2 mm and 5 mm plate.

**How to make it.**

1. Cut four 387 lengths of 25 x 2 tube; round one end.
2. Drill 10.5 across the tube 12 from the rounded end (pivot), and 6.5 across 30 below it (detent).
3. Weld a 60 x 60 x 5 foot square on the other end.

**How it fits the parts next to it.**

![Figure 7. Joint 2: stand leg on its clevis](05-build-plan/joint-02.png)

*Figure 7. The leg hangs between the clevis plates on an M10 bolt; a spring detent pin through the plates and the leg locks it.*

The rounded end goes between a pair of clevis plates; an M10 bolt with a nyloc nut, snug so the leg swings. Down, the detent pin goes through the lower plate holes and the leg. Folded, the leg swings inward along the rail, foot toward the axle, and the pin goes through the second plate holes; it then clears the wheels by 8 mm and the rail by 5 mm.

**Check before moving on.** With all four legs down on a flat floor the deck is level within 1° and the wheels just touch the floor.

### 3.4 Hinge spacer angles (make 2)

![Figure 8. Making sketch of the hinge spacer angle](../cad/drawings/FCL-DWG-105.png)

*Figure 8. Hinge spacer angle making sketch (FCL-DWG-105).*

**What it is and what it is made from.** The aluminium angle along each side rail that carries the hinge 20 mm higher than the rail, so the folded-out wing clears the tyre. Aluminium equal angle 20 x 20 x 2 mm, 6063 class.

**How to make it.**

1. Cut two 1,200 lengths; deburr.
2. Upright leg: four 5.5 holes 11 below the top, at 60, 420, 780 and 1,140 from one end.
3. Flat leg: 4.5 holes every 150, starting 75 from one end, 10 in from the outer edge; countersink from the top.

**How it fits the parts next to it.**

![Figure 9. Joint 4: the hinge line, cut through a tab](05-build-plan/joint-04.png)

*Figure 9. Seen from the handle end, cut through a tab: tab welded to the rail, angle bolted to the tab, hinge on the angle, wing on the hinge.*

The upright leg lies flat on the outside of the four tabs, its flat leg pointing outward and its top flush with the tab tops, 494 above the ground; M5 bolts through each tab, nyloc nuts inside. The hinge's fixed leaf lies on the flat leg with its knuckle just beyond the angle's edge.

**Check before moving on.** The angle top is straight and level within 1 mm along its length.

### 3.5 Battery case, drilled

![Figure 10. Drilling sketch of the battery case](../cad/drawings/FCL-DWG-111.png)

*Figure 10. Battery case drilling sketch (FCL-DWG-111).*

**What it is and what it is made from.** A bought IP65 polypropylene case, about 420 x 360 x 300 with a lid, a pressure vent and room for the pack, the class T fuse and foam. Only its end facing the electronics box is drilled.

**How to make it.**

1. Tape the end wall. Mark two holes 40 each side of the centre line, 150 up from the outside bottom.
2. Pilot 3, open to 25.5 with a step drill at low speed, deburr; no solvents.
3. Fit two M25 cable glands, seal outside, nut inside.
4. Inside, lay a 3 rubber mat on the floor. Screw the class T fuse holder to the floor beside where the pack will stand, at the gland end, so the lead from the pack's positive terminal to the fuse is under 150 long.

**How it fits the parts next to it.**

![Figure 11. Joint 8: battery cables between the boxes](05-build-plan/joint-08.png)

*Figure 11. 60 mm between the boxes: two gland domes and a short straight run of 16 mm² cable.*

The case stands on the deck centred on the middle cross tube, gland end toward the handle, held by two cam straps that go over the lid and through the deck. Its glands line up with those in the electronics box.

**Check before moving on.** Each gland seats flat; the lid closes on its seal.

### 3.6 Electronics box, cut and fitted out

![Figure 12. Cutting sketch of the electronics box](../cad/drawings/FCL-DWG-110.png)

*Figure 12. Electronics box cutting sketch (FCL-DWG-110).*

![Figure 13. Cut-outs in each wall](05-build-plan/ebox-cutouts.png)

*Figure 13. Every cut-out, each wall seen from outside.*

**What it is and what it is made from.** A bought IP54 polycarbonate box, about 320 x 460 x 300 with a lid and a mounting plate, that holds the inverter, charge controller and breakers and carries the outlets on its handle-end wall.

**How to make it.**

1. Tape each wall and mark the cut-outs from Figure 13, then check each against the template of the part you bought; the part's own template wins.
2. Drill corner holes and cut the rectangles with a fine jigsaw blade; drill round holes with a step drill. Deburr; no solvents.
3. Floor: four 6.5 holes, about 20 in from each corner, for the deck bolts.
4. On the bench, screw the inverter, the charge controller and the DIN rail (breakers and shunt) to the mounting plate as Figure 14 shows: inverter along the left half, charge controller and DIN rail side by side on the right, at least 10 apart.
5. Fit the plate on its bosses. Fit the outlets, isolator, filter fan, exhaust filter and glands through their cut-outs with their gaskets (step 8).
6. Wire as Figure 15 and section 3.6.1.

![Figure 14. Step 7 picture: parts on the mounting plate](05-build-plan/step-07.png)

*Figure 14. Where each part goes on the mounting plate.*

**How it fits the parts next to it.** The box stands on the deck, its handle-end wall 10 in from the frame end, held by four M6 bolts through the floor and the deck with large washers under the deck. Its two battery glands face the battery case 60 away (Figure 11). The shade uprights stand 28 clear of its sides.

**Check before moving on.** Every part sits flat; the lid closes with no wire across its seal.

#### 3.6.1 Wiring

![Figure 15. Block-level wiring](05-build-plan/wiring.png)

*Figure 15. Block-level wiring with wire sizes.*

Wire it like this, with stranded copper and a crimped lug or ferrule on every terminal:

1. Pack positive to the class T fuse holder (fuse out): 16 mm² (6 AWG), under 150 long.
2. Fuse holder through a battery gland to the isolator on the outlet face: 16 mm².
3. Isolator to the DIN rail busbar: 16 mm².
4. Inverter breaker to the inverter positive: 16 mm².
5. Pack negative through the other battery gland to the battery side of the shunt: 16 mm².
6. Shunt load side to a negative bus; inverter, charge controller and DC panel negatives to that bus: 16 mm² for the inverter, 6 mm² for the others.
7. Charge controller output through its breaker to the busbar: 6 mm².
8. DC panel (24 to 12 V converter, USB-C modules, 12 V sockets) through its breaker: 6 mm².
9. Inverter AC output to the GFCI outlet: 2.5 mm² (14 AWG), green-yellow earth to the frame only as the inverter maker specifies.
10. Each wing's leads through its PV gland, joined in parallel at the PV breaker, then to the charge controller input: 4 mm².
11. Fan thermostat and filter fan from a 24 V breaker: 0.75 mm².

Set every breaker from the datasheets of the parts you bought; the ratings in Figure 15 are a starting point.

**Check before moving on.** Every wire continuous end to end; with the fuse out, the busbar reads open to the negative bus; every wire labelled.

### 3.7 Wing frames, modules and hinges (make 2)

![Figure 16. Making sketch of the wing frame](../cad/drawings/FCL-DWG-106.png)

*Figure 16. Wing frame making sketch (FCL-DWG-106).*

**What it is and what it is made from.** Each wing is a 200 W semi-flexible solar module bonded to a light frame. Aluminium rectangular tube 30 x 20 x 1.5 mm (6063 class), aluminium corner cleats, 4.8 mm blind rivets, structural bonding tape.

**How to make it.**

1. Cut two long members 1,400 and five cross members 660 (two ends, three ribs), the 30 side upright.
2. Lay them out flat: ribs at 350, 700 and 1,050 from one end. Fit a corner cleat inside each butt joint and rivet with four rivets (or TIG weld). Frame 1,400 x 700.
3. Inner long member (the hinge side): M4 rivet nuts every 150 in its inner face, 10 below the top.
4. Clean the top faces, lay structural tape on every member, and lay the module on from one end, centred with a 10 rim all round, rolling it down as you go (step 11).
5. Screw the hinge's moving leaf to the inner member's rivet nuts with M4 screws, knuckle toward the top face.

![Figure 17. Step 11 picture: module onto the wing frame](05-build-plan/step-11.png)

*Figure 17. The module goes on the frame's top faces.*

**How it fits the parts next to it.** The hinge's fixed leaf screws to the spacer angle (Figure 9) with M4 countersunk screws every 150, nyloc nuts beneath. The hinge pin is 4.5 above the panel face, so the knuckle clears the module; folded out, the wing's underside passes 28 over the tyre and its outer edge is 309 above the ground.

**Check before moving on.** The frame's diagonals are equal within 2 mm and it does not rock on a table; the module is bonded flat with no bubbles over the members.

### 3.8 Outrigger legs and brackets (make 4)

![Figure 18. Making sketch of the outrigger leg](../cad/drawings/FCL-DWG-107.png)

*Figure 18. Outrigger leg making sketch (FCL-DWG-107).*

**What it is and what it is made from.** Two legs under each wing's outer edge that set the 15° tilt and take a stake each. Steel tube 25 x 2 mm, 4 mm plate, and a 3 mm aluminium strip for the bracket.

**How to make it.**

1. Cut four 269 lengths of tube; round one end; drill 8.5 across 10 from that end (pivot) and 6.5 across 30 below it (detent).
2. Feet: 50 x 50 x 4 plates with a 28 x 30 tab on one side, 11 hole 15 from the plate edge; weld square on the leg, tab pointing toward the nearer end of the cart.
3. Brackets: bend a 3 aluminium strip into a U 26 inside, legs 29 deep, web 45 long; drill 8.5 through both legs.

**How it fits the parts next to it.**

![Figure 19. Joint 5: outrigger leg on its bracket](05-build-plan/joint-05.png)

*Figure 19. The U bracket is riveted under the wing's outer member; the leg turns on an M8 bolt.*

The bracket web is riveted under the outer long member, 80 from each end of the frame (step 12). M8 bolt, nyloc nut, snug. Down, the leg is vertical with the wing at 15°; folded, it lies flat under the wing 7 clear of the frame, its foot lying flat too.

**Check before moving on.** Legs down on a flat floor, the wing's outer edge is 309 above the floor at both ends.

### 3.9 Tie bars (make 2)

![Figure 20. Making sketch of the tie bar](../cad/drawings/FCL-DWG-108.png)

*Figure 20. Tie bar making sketch (FCL-DWG-108).*

**What it is and what it is made from.** One bar at each end of the cart that holds the two stowed wings together at the top. Aluminium square tube 20 x 20 x 1.5 mm, a 3 mm aluminium pivot bracket, an over-centre latch and keeper.

**How to make it.**

1. Cut two 731 lengths; drill 6.5 across 10 from one end.
2. Rivet the latch body to the other end, hook outward (743 overall).
3. Pivot brackets: rivet one to the back of the left wing frame at each top corner (the outer member's end, beside the end member), its ear standing 35 above the frame top, beside where the bar lies. M6 bolt and nyloc nut through the ear and the bar, snug so the bar swings.
4. Keepers: screw one to the top of the right wing's outer member at each end, opposite the latch.

**How it fits the parts next to it.**

![Figure 21. Joint 9: tie bar pivot on the left wing](05-build-plan/joint-09.png)

*Figure 21. The bar sits on the wing top and turns on the bracket ear.*

![Figure 22. Joint 6: tie bar latch on the right wing](05-build-plan/joint-06.png)

*Figure 22. The latch hooks the keeper and pulls the right wing in against the bar.*

In travel the bar lies across the tops of both stowed wings and the latch pulls them together; nothing presses on the solar faces, which face each other inside. Parked, the bar swings up and over and lies down the back of the left wing, held by a spring clip.

**Check before moving on.** Latched, neither wing moves when pushed outward at its top corner.

### 3.10 Sun shade frame and uprights

![Figure 23. Making sketch of the shade frame and uprights](../cad/drawings/FCL-DWG-109.png)

*Figure 23. Shade making sketch (FCL-DWG-109).*

**What it is and what it is made from.** A reflective shade 50 above both boxes, on four uprights. Aluminium square tube 20 x 20 x 1.5 mm and reflective aluminized fabric with eyelets.

**How to make it.**

1. Frame: two 830 sides and three 540 cross tubes (ends and middle); corner cleats and rivets; 830 x 580 outside.
2. Lace the fabric round the frame, shiny side up.
3. Uprights: four 355 lengths with a 6.5 hole 30 from the bottom.
4. Rivet a small 20 x 20 angle clip under each long side tube where it meets an upright, with a 6.5 hole for a wing bolt.

**How it fits the parts next to it.**

![Figure 24. Joint 7: shade upright on its tab](05-build-plan/joint-07.png)

*Figure 24. The upright stands on the rail top, bolted to its tab; the shade frame rests on its top.*

Each upright stands on the rail top against its tab, M6 bolt through both. The shade frame's long sides rest on the four upright tops, 810 above the ground, held by an M6 wing bolt through each clip and upright. Undo four wing bolts to lift the shade off and open the battery case.

**Check before moving on.** The shade is level within 5 and 50 clear of both boxes.

### 3.11 Handle

![Figure 25. Making sketch of the handle](../cad/drawings/FCL-DWG-104.png)

*Figure 25. Handle making sketch (FCL-DWG-104).*

**What it is and what it is made from.** The detachable T-handle. Steel tube 28 x 1.5 mm (legs) and 32 x 1.5 mm (grip), foam grip.

**How to make it.**

1. Cut two legs 843 and a grip 520.
2. Lay out on the bench: leg feet 560 apart, leg tops 480 apart, meeting the grip 20 in from each grip end. Fish-mouth the leg tops, weld, clean up, paint, fit the foam grip.
3. With the legs in the sockets, drill 8.5 across each leg through the socket's pin hole.

**How it fits the parts next to it.**

![Figure 26. Joint 3: handle leg in its socket](05-build-plan/joint-03.png)

*Figure 26. The leg drops into the welded socket; one quick-release pin holds it.*

**Check before moving on.** The handle drops in and lifts out of both sockets without forcing; the grip is 900 above the ground.

### 3.12 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Wheels (line 2).** Two 16 in (406 mm) flat-free tyres on steel rims, 20 mm bore with bearings, hub about 60 long, about 90 wide, 100 kg or more each; with a spacer collar (26 outside, 20 bore, 37.5 long), a 20 washer and a linch pin each.
- **Battery case (line 5).** IP65 case about 420 x 360 x 300 outside, with a pressure vent and a flat end wall for two glands. Drill as section 3.5.
- **Pack (line 6).** 25.6 V 50 Ah lithium iron phosphate, about 330 x 175 x 220, with a 100 A battery management system that blocks charging below 0 °C and above 45 °C.
- **Electronics box (line 7).** IP54 polycarbonate box about 320 x 460 x 300 with lid and mounting plate; IP54 24 V filter fan (about 40 m³/h) with thermostat and a matching exhaust filter. Cut as section 3.6.
- **Charge controller (line 8).** 100 V 20 A MPPT for a 24 V battery, lithium iron phosphate profile, about 150 x 140 x 70.
- **Inverter (line 9).** 1,000 W pure sine, 2,000 W surge, 24 V in, 120 V 60 Hz out, 10 W or less no-load draw, about 270 x 210 x 110.
- **DC panel (line 10) and AC outlet (line 11).** Two 100 W USB-C PD modules, two 12 V sockets and a 24 to 12 V 20 A converter on a sealed panel; a GFCI duplex outlet with an in-use cover.
- **Fusing (line 12).** Class T 100 A fuse and holder; battery isolator for panel mounting; DIN rail breakers for the inverter, charge controller, DC panel and PV; shunt battery monitor.
- **Solar modules (line 13).** 200 W semi-flexible, Vmp 36 V or more at standard test conditions, no larger than 1,380 x 680, with leads long enough to reach the electronics box along the hinge line.
- **Hinges and latches (line 14).** Two stainless piano hinges cut to 1,200, leaves about 26 wide and 1.5 thick; two over-centre latches with keepers.
- **Bin (line 16).** Open plastic bin about 320 x 460 x 240 with a tie-down strap.
- **Wiring and hardware (line 17).** 16 mm² battery cable with lugs; four M25 and two M16 glands; 4 mm² PV cable and connectors; two cam straps; M4, M5, M6, M8 and M10 bolts with nyloc nuts; M4 rivet nuts; 4.8 mm blind rivets; structural bonding tape; foam blocks and a rubber mat.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: axle through the brackets

![Step 1](05-build-plan/step-01.png)

Slide the axle through both brackets, 410 each side of the centre line, cross holes vertical; weld to both faces of both brackets.

### Step 2: wheels onto the axle

![Step 2](05-build-plan/step-02.png)

Collar, wheel, washer, linch pin, each side the same. Grease the bearings if the maker says so.

### Step 3: stand legs into their clevises

![Step 3](05-build-plan/step-03.png)

M10 bolt and nyloc nut each, snug; detent pin in the down holes. The cart now stands level on its own.

### Step 4: hinge spacer angles onto the tabs

![Step 4](05-build-plan/step-04.png)

Upright leg on the outside of the four tabs, flat leg outward and flush with the tab tops; four M5 bolts per side, nyloc nuts inside.

### Step 5: battery case onto the deck

![Step 5](05-build-plan/step-05.png)

Glands fitted. Stand the case on the deck centred on the middle cross tube, gland end toward the handle. Pass the two cam straps through the deck and round the case, loose for now.

### Step 6: pack and class T fuse into the case

![Step 6](05-build-plan/step-06.png)

**Hold point:** safety stop S1. Pack on its mat in the middle of the case; foam blocks round it; fuse holder beside it at the gland end. Connect the short positive lead from the pack to the fuse holder. **The fuse stays out.**

### Step 7: inverter, charge controller and DIN rail on the mounting plate

![Step 7](05-build-plan/step-07.png)

On the bench, screw each part to the plate as Figure 14 shows; then fit the plate into the box on its bosses.

### Step 8: outlets, isolator, fan and exhaust filter

![Step 8](05-build-plan/step-08.png)

Each through its cut-out from outside, with its gasket, fixed from inside. Fit the battery and PV glands.

### Step 9: electronics box onto the deck

![Step 9](05-build-plan/step-09.png)

Handle-end wall 10 in from the frame end, battery glands lined up with the case's. Four M6 bolts through the floor and the deck, large washers under the deck.

### Step 10: battery cables, then the lids

![Step 10](05-build-plan/step-10.png)

Pass the two 16 mm² cables through both pairs of glands, crimp the lugs and connect them as section 3.6.1; finish the wiring. Close both lids; tighten the cam straps over the battery lid. **Hold point:** safety stop S2.

### Step 11: module onto each wing frame (on the bench)

![Step 11](05-build-plan/step-11.png)

Structural tape on every member, module on from one end, rolled down; then the moving hinge leaf onto the inner member.

### Step 12: outriggers onto the wings

![Step 12](05-build-plan/step-12.png)

Seen from below. Rivet the U brackets under each outer member 80 from the ends and fit the legs on M8 bolts. On the left wing rivet the two tie bar brackets and fit the tie bars; on the right wing screw on the two keepers.

### Step 13: wings onto the hinge angles

![Step 13](05-build-plan/step-13.png)

With a helper and the outrigger legs down, lay each wing in place and screw the hinge's fixed leaf to the spacer angle with M4 countersunk screws every 150, nyloc nuts beneath. Route each wing's leads along the hinge line to its PV gland but **do not connect them** (safety stop S3).

### Step 14: shade uprights, then the shade

![Step 14](05-build-plan/step-14.png)

M6 bolt through each upright into its tab; lay the shade frame on the uprights and fit a wing bolt at each.

### Step 15: handle into its sockets

![Step 15](05-build-plan/step-15.png)

Both legs into the sockets; a quick-release pin through each.

### Step 16: accessory bin and strap

![Step 16](05-build-plan/step-16.png)

Bin at the front end, strap over it and through the deck.

### Step 17: fold for travel and tie the wings

![Step 17](05-build-plan/step-17.png)

Fold each wing's outrigger legs flat under it; raise both wings until they stand upright; swing each tie bar over the tops and close its latch. Fold the stand legs. **Hold point:** safety stop S6 before the cart is moved.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of FCL-REQ-001.

*Table 2. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Mass and handle force | R6 | Weigh the cart; spring balance under the grip, level and at 5° either way | Mass recorded (about 80 kg estimated); handle force 10 to 150 N, never negative |
| Pull force | R7 | Spring balance at the grip on a measured 10 % grade, gravel and grass | Recorded against 150 N (125 and 156 N estimated) |
| Ground clearance and step | R7 | Measure under the axle; pull over a 150 mm step | 150 mm or more; the step climbed by pulling |
| Wing to tyre and tilt | R3 (tilt); design check (gap) | Wings out on flat ground: gap over the tyre, angle finder on the panel | Gap 25 mm or more (28 mm modelled); 15°, give or take 1° |
| Deploy and stow | R5 | One person, timed, from arrival to power on and back | 10 minutes or less each (6.5 and 5.5 min estimated) |
| Tie bars hold | Design check | Stowed, latched: push each wing outward at the top | Nothing moves |
| Stand legs | Design check | Fold and unfold each leg; deck level when down | Detent holds both ways; deck level within 1° |
| Glands and lids | R8 | Look at every gland and seal; lids closed with cables in | Seals even, no gaps (the spray test comes later) |
| Fusing | R12 | Continuity and polarity with the fuse out; isolator off and on | Busbar open to negative with the isolator off; correct polarity everywhere |
| Charge | R3, R9 | Wings connected in sun; charge current at the controller | Current flows; charging stops above 45 °C cell temperature per the pack's datasheet |
| AC output | R2, R12 | Inverter on; GFCI test button | 120 V; GFCI trips |
| DC output | R2 | USB-C and 12 V outlets under a test load | Rated output at each |
| Stakes | R10 | Pull each staked outrigger foot upward | Holds 50 N or more |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the pack comes into the workshop.** Pack voltage about 24 to 27 V; no swelling, dents or leaks; a datasheet from its maker. Class T fuse out of its holder. A clear non-combustible floor area, and an extinguisher for electrical fires within reach. Two people to lift the 12 kg pack into its case.
- **S2. Before the class T fuse goes in.** Every connection tight and insulated; polarity checked with a meter, not by wire colour; with the isolator off, the busbar reads open to the negative bus; every breaker off; both lids closed.
- **S3. Before the wings are connected.** Cover both modules with an opaque sheet; the PV breaker off; polarity of each wing's leads checked at the gland; the open-circuit voltage of each wing measured below the charge controller's 100 V limit. PV leads are live whenever light falls on the modules.
- **S4. First charge.** Attended the whole time, in the open, on a dry day; pack temperature checked every 15 minutes. Stop if the pack passes 45 °C or any cable or terminal is warm to the touch.
- **S5. Before the inverter is switched on.** GFCI outlet wired and tested with its button; the inverter's earth and neutral connected only as its maker specifies for a stand-alone source; no cord connected to any building wiring, ever.
- **S6. Before the cart is moved or lifted.** Tie bars latched, stand legs folded and pinned, handle pinned. The cart is about 80 kg: two people to lift it into a vehicle, with the pack removed first if possible. Do not cross slopes across the fall line.
- **S7. Before deploying outdoors.** Stake the four outrigger feet whenever wind is expected; unstaked, the wings can lift at about 9 m/s; stow above that if they cannot be staked. Keep fingers out of the hinges and folding legs.

## 7. Tools, skills and workspace

**Tools.** MIG welder with a 0.8 mm wire for 1.5 to 5 mm steel; angle grinder with cutting and flap discs; metal-cutting chop saw or bandsaw; bench drill and drills 3 to 20.5 mm; step drill to 30 mm; countersink; jigsaw with fine metal and plastic blades; files and a deburring tool; welding table or a flat bench; clamps and magnetic squares; tape measure, steel rule, square, angle finder and calipers; hand rivet tool for 4.8 mm rivets and a rivet nut tool for M4; spanners and sockets to 17 mm; crimp tool for 16 mm² lugs and ferrules, wire strippers; digital multimeter and a DC clamp meter; spring balance to 25 kg and a platform scale to 100 kg; stopwatch.

**Skills.** Basic MIG welding of thin steel tube, marking out, drilling, riveting, and crimping heavy battery cable. The DC system is extra-low voltage (up to about 29 V at the pack and about 50 V from the wings), but it carries up to about 100 A; the 120 V AC side is limited to bought parts plugged and wired as their makers specify. Anyone wiring the AC outlet must be competent with mains-voltage wiring under local code.

**Workspace.** A garage bay about 3 x 4 m with a welding area kept clear of anything that burns, and a separate clean bench for the electronics so grinding dust stays off them.

**Personal protective equipment.** Welding helmet, gloves and jacket; safety glasses for cutting, grinding and drilling; hearing protection; cut-resistant gloves for sheet and tube; insulated tools and no rings or watch when working on the battery.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/FCL-DWG-101` to `FCL-DWG-111`.
- General arrangement: `cad/drawings/FCL-DWG-002.pdf`, Rev P4.
- Calculations: `docs/04-calcs/01-sizing.md` (FCL-CAL-001 v0.3) and `docs/04-calcs/sizing.py`; mass [E1] to [E8], pull and step [F1], [F2], wing to tyre [F4], wind [H1], [H2], deploy and stow [I1], envelope [K1].
- Bill of materials: `bom/bom.csv`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (FCL-DDR-003), with FCL-DDR-001 and FCL-DDR-002.
- Requirements: `docs/03-requirements.md` (FCL-REQ-001 v0.5).
