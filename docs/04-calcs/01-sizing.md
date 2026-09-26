---
doc_id: FCL-CAL-001
title: FieldCell sizing calculations
project: FieldCell
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (energy, PV yield, load, electrical, mass and stability, thermal, wind, deploy, noise, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# FieldCell sizing calculations

On paper, FieldCell meets seven of its twelve requirements, misses one and has two at risk; two more cannot be verified at TRL 3. The energy case works: the 400 W east-west array stores about 1.17 kWh/day at 4 kWh/m²/day of global horizontal irradiation, which carries the 0.9 kWh/day reference load with about 10 % surplus, and the 1.15 kWh usable pack gives 1.08 days with no sun. Version 0.2 applies Amish's decisions of 2026-09-25 (FCL-DDR-002): the R6 mass limit is 75 kg, the budget is $2,100, the hinge line sits on a 20 mm spacer, and a reflective sun shade covers both enclosures. With the spacer and shade the cart weighs about 75.1 kg, 0.06 kg over the new limit, so R6 is still not met by a hair. Cost (about $2,051 against $2,100, R12) is now met. Heat (R9) and pull force on grass (R7) remain at risk. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [C4], is the line of that script's output that carries it.

> **Safety:** These calculations concern a 1.28 kWh lithium battery, 120 V AC output, 100 A DC circuits, always-live PV panels and a 75 kg cart. They are first-principles estimates for a paper proof of concept and are not a substitute for component datasheets, a qualified electrical review or test. See FCL-PRC-001, Safety.

## Scope and method

The note checks every requirement in FCL-REQ-001 v0.4 against the design in FCL-PRC-001 v0.4 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, so the frame, wheel, hinge and enclosure dimensions used here are the ones in the STEP files and in drawing FCL-DWG-002. Run it from the repo root with `python docs/04-calcs/sizing.py`.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Battery | 8S LiFePO4, 25.6 V nominal, 50 Ah, 90 % usable; 24 V at the low end for current sizing; pack resistance 10 mΩ including BMS | Common 24 V LiFePO4 packs |
| Irradiance | "Peak sun hours" in R3 and R4 is daily global horizontal irradiation (GHI, kWh/m²/day), as confirmed by Amish on 2026-09-25 (FCL-DDR-002). Transposition ratios come from a clear-sky model (Meinel beam attenuation, Kasten-Young air mass, diffuse 12 % of beam, albedo 0.2, ASHRAE incidence modifier b₀ = 0.05) at 15, 30 and 45° N on the equinox and both solstices | Standard textbook model; ratios only, not absolute yield |
| PV module | 200 W semi-flexible monocrystalline module bonded to a ventilated aluminium frame; Vmp 36 V, Voc 45 V, Isc 6 A; NOCT 48 °C; power coefficient −0.38 %/K; Voc −0.29 %/K, Vmp −0.35 %/K | Typical datasheet values for the class; to confirm with the chosen module |
| PV losses | Nameplate and early degradation 0.97, soiling 0.97, mismatch between the two wings on one MPPT 0.98, wiring 0.98, MPPT 0.96, battery charge 0.97 | Engineering judgment |
| Load | Reference load of FCL-PRC-001, Table 3 (897 Wh/day at the outlets); DC converters 0.93; inverter 0.92 marginal efficiency plus 10 W no-load draw for 7 h; standby 12 Wh/day; filter fan 3 W for 4 h | Typical high-frequency 1 kW inverter; to confirm from datasheets |
| Mass | Steel 7,850 kg/m³, aluminium 2,700 kg/m³; expanded steel deck 4.5 kg/m²; flat-free 16 in wheel 4.0 kg; PV wing 6.5 kg (module about 3.5 kg, frame about 3 kg); hinge spacers 20 × 20 × 2 mm aluminium angle, 1.3 m per side; sun shade 1.0 kg | Tube geometry from the model; others estimated |
| Ground | Rolling resistance 0.04 hard, 0.06 gravel, 0.10 grass; friction 0.4 | Handbook ranges for 400 mm wheels |
| Thermal | Enclosure absorptance 0.4 (light grey), noon sun 1,000 W/m²; external film coefficient from laminar natural convection plus radiation (emissivity 0.9); filter fan 40 m³/h; the sun shade leaves 25 % of the direct solar gain on the enclosures (sides at low sun) | Textbook correlations; shade factor assumed |
| Wind | Normal force coefficient 1.2 on a wing at 15°; air 1.225 kg/m³; side-force coefficient 1.3 on a stowed wing wall | Flat-plate data, conservative |
| Noise | Inverter fan 40 dB(A) and filter fan 35 dB(A) at 1 m at 500 W | Placeholder levels, not datasheet values |

## A. Stored energy (R1)

The pack stores 25.6 V × 50 Ah = 1,280 Wh nominal and 1,152 Wh usable at 90 % depth of discharge [A1]. R1 asks for 1.2 kWh nominal and 1.0 kWh usable: met.

## B. Electrical sizing (R2)

- **DC outlets.** Two 100 W USB-C PD ports and a 12 V 20 A converter give 440 W, against the 300 W target [B1].
- **Battery current.** At 1 kW AC the pack supplies 46.3 A, and 98 A in a 2 kW surge. With the DC outlets also at full output (19.7 A) the continuous total is 66.0 A, 66 % of the 100 A class T fuse and BMS rating [B2]. The surge plus full DC load is about 118 A for a few seconds, which the BMS peak rating (typically 150 to 200 A for several seconds) and the class T fuse curve must tolerate; confirm from the chosen parts.
- **Cable.** A 1.5 m loop of 16 mm² (6 AWG) copper has 1.61 mΩ, so the drop at 66 A is 0.11 V (0.4 %) with 7 W of heat [B3].
- **PV window.** Two panels in parallel keep Voc at −10 °C cell to 49.6 V, well under the 100 V MPPT limit. At 70 °C cell, Vmp falls to 30.3 V, only 0.9 V above the 29.4 V the MPPT needs to finish absorption at 28.4 V [B4]. Charging may stall near full charge on very hot days; a module with Vmp of 36 V or more at STC is required, and a 72-cell class module is preferred.
- **PV current.** The parallel pair gives 12 A short circuit and at most 15.0 A of MPPT output at 400 W, inside the 20 A rating. Reverse current into one panel is at most 6 A, so two panels in parallel need no per-panel fuse; the PV breaker remains as the disconnect [B5].

R2 is met by selection.

## C. PV yield (R3)

*Table 2. Transposition ratios, plane of array over global horizontal, clear sky [C0].*

| Site | Day | GHI (kWh/m²) | East-west wings at 15° | South at latitude tilt | East-west over south |
| --- | --- | --- | --- | --- | --- |
| 15° N | Equinox | 7.5 | 0.959 | 1.017 | 0.94 |
| 15° N | June solstice | 7.9 | 0.959 | 0.883 | 1.09 |
| 15° N | December solstice | 5.6 | 0.948 | 1.162 | 0.82 |
| 30° N | Equinox | 6.6 | 0.954 | 1.120 | 0.85 |
| 30° N | June solstice | 8.5 | 0.959 | 0.843 | 1.14 |
| 30° N | December solstice | 3.7 | 0.934 | 1.505 | 0.62 |
| 45° N | Equinox | 5.1 | 0.946 | 1.328 | 0.71 |
| 45° N | June solstice | 8.5 | 0.956 | 0.846 | 1.13 |
| 45° N | December solstice | 1.8 | 0.908 | 2.241 | 0.40 |

The east-west wings collect on average 0.947 of the horizontal irradiation (lowest 0.908, at 45° N in December), because a 15° tilt costs little and the incidence modifier removes a few percent [C1]. Against a single panel aimed south at latitude tilt they average 0.86, a 14 % penalty, larger than the 10 % assumed at TRL 2 [C1]. The penalty is worst in winter at high latitude, where the east-west layout collects well under half of what a south panel would; FieldCell is sized for clear-season sites, not high-latitude winters.

The energy-weighted irradiance on the wings is about 636 W/m², which puts the cells at 47 °C in 25 °C air (factor 0.915) and 62 °C in 40 °C air (factor 0.858) [C2]. The overall factor from GHI to array DC output is 0.783, and 0.729 into the battery [C3].

*Table 3. Energy into the battery [C4].*

| GHI (kWh/m²/day) | 25 °C ambient | 40 °C ambient | Lowest transposition ratio |
| --- | --- | --- | --- |
| 4.0 | 1.17 kWh | 1.09 kWh | 1.12 kWh |
| 4.5 | 1.31 kWh | 1.23 kWh | 1.26 kWh |
| 5.0 | 1.46 kWh | 1.37 kWh | 1.40 kWh |

A full recharge from 10 % (1,152 Wh) takes 0.79 day at 5 kWh/m²/day and 0.99 day at 4 [C5]. Peak charge power at noon is about 260 to 290 W [C6]. R3 asks for 1.1 kWh/day at 4 and a full recharge in one day at 5: met at 25 °C, with the 4 kWh/m²/day figure falling to 1.09 kWh in 40 °C air.

## D. Load and autonomy (R4)

*Table 4. Reference load drawn from the battery [D1, D2].*

| Path | At outlet | From battery |
| --- | --- | --- |
| DC (lighting, charging), 0.93 converters | 480 Wh | 516 Wh |
| AC (laptop, router, tool), 0.92 plus 10 W idle for 7 h | 417 Wh | 523 Wh (70 Wh of it idle) |
| Standby (BMS, monitor, MPPT at night, converter idle) | | 12 Wh |
| Electronics box filter fan, 3 W for 4 h | | 12 Wh |
| **Total** | **897 Wh** | **1,063 Wh (overall 0.844)** |

With 1,152 Wh usable, the pack carries the load for 1.08 days with no sun [D3]. The energy balance is +104 Wh/day (+10 %) at 4 kWh/m²/day, +250 Wh (+24 %) at 4.5 and +396 Wh (+37 %) at 5 [D4]. The system breaks even at 3.64 kWh/m²/day in 25 °C air and 3.88 in 40 °C air [D5]. Inverter idle draw is the most sensitive assumption: every extra 5 W of no-load draw costs 35 Wh/day, 3.3 % of the load [D6]. R4 is met, with thin margins.

## E. Mass, center of gravity and handle force (R6)

The frame tubes total 3.96 m of 40 × 40 × 1.5 mm steel at 1.81 kg/m (7.2 kg). With the deck (2.6 kg), axle (1.8 kg) and brackets (1.2 kg) the welded steel frame is 12.8 kg; a bolted aluminium frame would be about 6.7 kg [E1].

*Table 5. Mass budget, wings stowed, parked level. X from the deck center toward the handle; the axle is at X = 30 mm [E2, E3].*

| Item | Mass (kg) | X (mm) | Z (mm) |
| --- | --- | --- | --- |
| Frame, deck and axle | 12.8 | 0 | 430 |
| Wheels, flat-free (2 × 4.0 kg) | 8.0 | 30 | 203 |
| Handle | 2.7 | 950 | 700 |
| Stand legs (4) | 1.8 | 0 | 230 |
| Battery enclosure | 3.0 | 0 | 610 |
| LiFePO4 pack | 12.0 | 0 | 576 |
| Electronics enclosure and filter fan | 3.3 | 420 | 610 |
| Inverter (high-frequency) | 4.0 | 420 | 521 |
| MPPT, fusing, monitor, outlets | 4.0 | 420 | 580 |
| Accessory bin and cables | 4.0 | −420 | 560 |
| PV wings, stowed (2 × 6.5 kg) | 13.0 | 0 | 840 |
| Hinges, latches, outriggers, stakes | 3.0 | 0 | 780 |
| Hinge spacers (2 × aluminium angle) | 0.5 | 0 | 463 |
| Sun shade on four posts | 1.0 | 185 | 810 |
| Wiring and hardware | 2.0 | 200 | 600 |
| **Total** | **75.1** | **85** | **564** |

The cart weighs about 75.06 kg [E3]. Amish relaxed the R6 limit from 70 kg to 75 kg on 2026-09-25 (FCL-DDR-002), keeping the steel frame and flat-free tyres; the same decisions added the hinge spacers (0.53 kg) and the sun shade (1.0 kg), which take the cart from 73.5 kg to 0.06 kg over the new limit. The TRL 2 budget of 68.5 kg had underestimated the steel frame (11.0 kg budgeted), the flat-free wheels (6.0 kg for two) and the hinges and outriggers (2.0 kg). The center of gravity is 55 mm toward the handle from the axle, so the handle carries 33 N when level and 14 to 52 N over a 5° pitch either way, inside the 10 to 150 N band [E4]. The heaviest removable module is the 12.0 kg pack, against a 25 kg limit [E6].

An aluminium frame would bring the cart to 69.0 kg; pneumatic tyres alone to 72.7 kg; both to 66.6 kg [E5]. R6 is **not met** by 0.06 kg, well inside the accuracy of this estimate; a shade of 0.9 kg or less would meet it. How to close the gap is proposed in `docs/REVIEW.md`, awaiting Amish.

## F. Rough ground and structure (R7)

*Table 6. Pull force on a 10 % grade [F1].*

| Surface | Rolling resistance | Pull force |
| --- | --- | --- |
| Hard or packed | 0.04 | 103 N |
| Gravel | 0.06 | 117 N |
| Grass | 0.10 | 147 N |

- **Step.** Pulled handle first onto a 150 mm step, the 203 mm wheel meets the edge 196 mm ahead of the axle. Taking moments about the edge, the user needs about 138 N of horizontal pull at the grip; a straight push at the axle would need about 2,720 N, so the step is climbed by pulling at the handle, not by pushing [F2].
- **Clearance and tipping.** Ground clearance under the axle is 193 mm and the lateral static tip angle is 32.6° [F3].
- **Wing to tyre.** With the hinge line raised from 470 to 490 mm on a 20 mm spacer (FCL-DDR-002), the deployed wing underside clears the tyre top by 28 mm at the tyre's outer edge [F4], up from 8 mm. This leaves room for tyre growth, mud and hinge tolerance.
- **Strength.** At a 2 g bump, a side rail with 30 kg cantilevered 0.4 m sees 118 N·m and 41 MPa, a factor of 5.7 on S235 yield; the 20 mm axle sees 52 N·m and 66 MPa, a factor of about 5.3 on bright mild steel [F5]. Welds, fatigue and the handle joint are not assessed at TRL 3.

R7 is **at risk**: every target is met on paper, but the pull force on grass is within 2 % of the 150 N limit, and it grows with any further mass.

## G. Thermal (R8, R9)

The electronics enclosure has 0.62 m² of walls and top. Its heat load is 68 W at 500 W AC and 140 W at 1 kW AC, and noon sun can add up to 86 W on a light grey box [G1].

*Table 7. Electronics enclosure air temperature at 45 °C ambient [G2].*

| Case | Sealed box | With a 40 m³/h filter fan |
| --- | --- | --- |
| 500 W AC | 56 °C (+10.7 K) | 49 °C (+3.5 K) |
| 1 kW AC | 65 °C (+20.2 K) | 52 °C (+7.3 K) |
| 1 kW AC with half the solar gain | 70 °C (+25.5 K) | 54 °C (+9.5 K) |
| 1 kW AC under the sun shade [G6] | 67 °C (+21.5 K) | 53 °C (+7.8 K) |

A sealed box is not workable at 1 kW in hot weather. An IP54 filter fan with a matching exhaust filter keeps the box within about 10 K of ambient; a 10 K rise at 1 kW in sun needs about 55 m³/h [G3], so the fan should be sized at 40 to 60 m³/h. Amish adopted the thermostat-controlled IP54 filter fan on 2026-09-25 (FCL-DDR-002). This resolves the TRL 2 question of ventilation against IP54 (R8), since IP54 filter fans are standard parts; it adds a fan to the noise budget (R11) and about 12 Wh/day to the load. At 45 °C ambient, the box interior still reaches about 54 °C, above the 40 °C at which most 1 kW inverters begin to derate, so full 1 kW output at 45 °C is not assured.

The battery case in noon sun absorbs about 60 W and settles about 10 K above ambient with a time constant of about 0.8 h [G4]. The pack therefore reaches about 55 °C at 45 °C ambient and 45 °C at 35 °C [G5], at or above the usual 45 °C charge limit of LiFePO4 cells, so the BMS will block charging in the hottest hours. Pack self-heating is small: 21 W at 1 kW and under 1 Wh/day at the reference load [G4]. At −10 °C the BMS blocks charging below 0 °C cell temperature as required, so on cold days little PV energy is stored until the pack warms.

**Sun shade.** Amish added a light reflective shade over both enclosures on 2026-09-25 (FCL-DDR-002). Assuming it leaves 25 % of the direct solar gain, the battery case absorbs about 15 W and settles about 3 K above ambient, so the pack reaches about 48 °C at 45 °C ambient, 43 °C at 40 °C and 38 °C at 35 °C [G7], against about 55 °C, 50 °C and 45 °C unshaded. Charging now continues in the hottest hours up to about 42 °C ambient instead of 35 °C. The electronics box gains less: about 53 °C inside at 1 kW and 45 °C ambient, against 54 °C [G6], because its heat is mostly internal.

R8 is **not verifiable at TRL 3** (it needs a spray and dust test). R9 is **at risk**: the low-temperature charge block is met by selection and the shade keeps the pack below its charge limit up to about 42 °C ambient, but the box interior still reaches about 53 °C at 45 °C ambient and the inverter derating data at 45 °C, which the requirement asks for, is not yet in hand; it comes with the supplier selection.

## H. Wind (R10)

- **Unstaked wing.** A 0.98 m² wing of 6.5 kg lifts about its hinge at about 9.2 m/s [H1].
- **Staked at 15 m/s.** The dynamic pressure is 138 Pa and the normal force 162 N per wing. Each staked outrigger foot must resist 27 N of pull-out, or 49 N with a 1.5 load factor [H2], well within a 300 mm steel stake in firm soil (commonly a few hundred newtons).
- **Whole cart at 15 m/s.** Worst-case uplift on both wings is 313 N against a weight of 736 N. The lateral load of 125 N is below the 169 N friction of an unstaked cart; staked, it is about 31 N per foot [H3].
- **Stowed.** Side wind on one wing wall overturns the stowed cart at about 20 m/s [H4].

R10 is met with the four feet staked or ballasted, as the requirement states. Unstaked, the wings must be stowed above about 9 m/s.

## I. Deployment and noise (R5, R11)

Task analysis gives 6.0 min to deploy and 5.0 min to stow, against 10 min each [I1]. R5 is met by analysis; a timed trial is TRL 4 work. With the assumed source levels, the inverter fan and filter fan together give about 41.2 dB(A) at 1 m at 500 W [I2], but neither level comes from a datasheet, so R11 is **not verifiable at TRL 3**.

## J. Cost (R12)

The 18-line BOM totals $2,051 [J1] against the $2,100 budget that Amish set on 2026-09-25 (FCL-DDR-002), leaving $49, about 2.4 % contingency. The decisions added the sun shade (item 18, $30) and the hinge spacers ($15, in item 14) to the $2,006 of v0.1. The largest lines are the two PV wings ($460), the pack ($300) and the inverter ($220) [J2]. The TRL 2 figure of $1,462 priced rigid-frame 200 W panels at $135 each; a rigid glass panel of that rating weighs about 11 to 12 kg, which would add about 10 kg to a cart already over its mass limit, so the semi-flexible module on a light frame is kept and costs more. Fusing, monitoring and outlets were also underpriced. R12 is **met** on cost, with a thin contingency; its electrical safety provisions are met by design. Supplier quotes for the pack, PV wings and inverter will decide whether $2,100 holds.

## K. Envelope

Deployed, the cart covers 1,984 × 2,012 mm including the handle; stowed with the handle removed it is 1,400 × 784 × 1,190 mm [K1], which fits a pickup bed between the wheel wells and most vans.

## Results

*Table 8. Requirement status. Status is one of met, not met, at risk, or not verifiable at TRL 3.*

| ID | Quantity | Value (FCL-CAL-001) | Target (FCL-REQ-001) | Status |
| --- | --- | --- | --- | --- |
| R1 | Stored energy | 1.28 kWh nominal, 1.15 kWh usable [A1] | 1.2 kWh nominal, 1.0 kWh usable | Met |
| R2 | AC and DC output | 1 kW AC, 2 kW surge by selection; 440 W DC; 66 A continuous on a 100 A fuse [B1, B2] | 1 kW AC, 2 kW surge; 300 W DC | Met |
| R3 | PV recharge | 1.17 kWh/day at 4 kWh/m²/day (1.09 at 40 °C); full recharge 0.79 day at 5 [C4, C5] | 1.1 kWh/day at 4; full recharge in 1 day at 5 | Met |
| R4 | Autonomy | 1.08 days with no sun; +10 % at 4 kWh/m²/day [D3, D4] | 1 day; energy-neutral at 4 | Met |
| R5 | Deploy and stow | 6.0 min deploy, 5.0 min stow by task analysis [I1] | 10 min each | Met |
| R6 | Mass and handle force | 75.1 kg; 14 to 52 N; pack 12.0 kg [E3, E4, E6] | 75 kg; 10 to 150 N; module 25 kg | **Not met** (mass 0.06 kg over) |
| R7 | Rough ground | 406 mm wheels; 193 mm clearance; step at 138 N pull; 147 N on grass; tip 32.6° [F1 to F3] | 406 mm; 150 mm; 150 mm step; 150 N; 25° | At risk |
| R8 | Rain and dust | IP54 box with IP54 filter fan and filter; IP65 battery case; glands (by selection) | IP54 operating; IP65; glands | Not verifiable at TRL 3 |
| R9 | Temperature | Box 53 °C at 45 °C ambient with fan and shade; pack under the shade about 48 °C; charge blocked below 0 °C by BMS [G6, G7] | −10 to 45 °C; charge block below 0 °C; derating known | At risk |
| R10 | Wind | Staked: 27 N pull-out per foot at 15 m/s (49 N factored); unstaked lift at 9.2 m/s [H1, H2] | Stable to 15 m/s staked or ballasted | Met |
| R11 | Noise | About 41 dB(A) at 1 m from assumed source levels [I2] | 45 dB(A) at 1 m at 500 W | Not verifiable at TRL 3 |
| R12 | Safety and cost | Fusing, GFCI, isolator, no inlet by design; parts $2,051 [J1] | Safety provisions; $2,100 | Met |

Summary: 7 met (R1, R2, R3, R4, R5, R10, R12), 1 not met (R6, by 0.06 kg), 2 at risk (R7, R9), 2 not verifiable at TRL 3 (R8, R11).

## Checks against earlier figures

The TRL 2 figures in FCL-PRC-001 v0.2 and FCL-REQ-001 v0.2 were checked against this note and corrected in v0.3 of both documents: mass 68.5 to 73.5 kg; CG offset 63 to 55 mm; handle force 17 to 52 N to 14 to 50 N; lateral tip 32 to 32.9°; pull on grass 135 to 144 N; east-west penalty 10 to 14 %; stored energy at 4 h 1.12 to 1.17 kWh/day, now against GHI; load from the battery 1,025 to 1,063 Wh/day; autonomy 1.1 to 1.08 days; surplus at 4 h 9 to 10 %; parts $1,462 to $2,006. The unstaked lift-off speed (about 9 m/s) and deploy time (about 6 min) are confirmed.

Version 0.2 (FCL-DDR-002) changed: mass 73.5 to 75.1 kg against a limit relaxed from 70 to 75 kg; CG height 557 to 564 mm; handle force 14 to 50 N to 14 to 52 N; tip angle 32.9 to 32.6°; pull on grass 144 to 147 N; step pull 136 to 138 N; wing to tyre clearance 8 to 28 mm; stowed height 1,170 to 1,190 mm; pack in noon sun at 45 °C ambient 55 to 48 °C; electronics box at 1 kW 54 to 53 °C; BOM $2,006 to $2,051 against a budget raised from $1,500 to $2,100. The energy, electrical, wind lift, deploy and noise figures are unchanged.
