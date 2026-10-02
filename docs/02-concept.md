---
doc_id: FCL-PRC-001
title: FieldCell design precis
project: FieldCell
doc_type: Design precis
version: "0.7"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-24'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, first-order numbers, design choices, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update. Decisions of FCL-DDR-001 recorded; numbers replaced by FCL-CAL-001; parametric model, drawing FCL-DWG-002 and priced BOM
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Constructable design (FCL-DDR-003); component table, numbers and safety notes follow FCL-CAL-001 v0.3; build plan FCL-BLD-001
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Mass and pull limits, charging inputs and portfolio positioning decided by Amish on 2026-10-02 (FCL-DEC-001)"
---

# FieldCell design precis

FieldCell is a two-wheel hand cart whose two sides are 200 W solar panels. For travel the panels stand up as the cart walls; on site they fold out as wings on outrigger legs. Between them sit a 1.28 kWh LiFePO4 pack, an MPPT charger, a 1 kW inverter and DC outlets. The TRL 3 calculations (FCL-CAL-001) show that it stores about 1.17 kWh a day from its own PV at 4 kWh/m²/day of global horizontal irradiation, carries a 0.9 kWh/day field load for 1.08 days without sun, and deploys in about 6.5 minutes. A reflective sun shade covers the battery and electronics enclosures, and the wing hinges sit on 20 mm spacers to clear the tyres. The design is constructable (FCL-DDR-003): every part can be made or bought and is fixed to its neighbours, as the prototype build plan FCL-BLD-001 shows. The parts that made it buildable bring the cart to about 80 kg against a 75 kg limit (R6) and the pull on a grass grade to 156 N against 150 N (R7), and the parts cost an estimated $2,101 against a $2,100 value-engineering target (R12, USD 1 over); how to close the mass and pull gaps is awaiting Amish and the savings worth trying are in FCL-DEC-001.

![Hero render](../media/hero.png)

*Figure 1. FieldCell deployed (front) and stowed for travel (behind), with a 1.75 m person for scale. Generated from the parametric model `cad/src/model.py`.*

## How it works

1. **Travel.** The wings stand upright as the cart sides, over the battery and electronics, held together at the top by two tie bars with over-centre latches. One person pulls or pushes the cart by the T-handle on two 16 in (406 mm) flat-free wheels. The sun shade sits on four uprights on the frame, 50 mm above the enclosures, and stays in place in travel. The center of gravity sits about 54 mm on the handle side of the axle, so the handle carries a light, positive load.
2. **Park.** Four stand legs fold down so the deck sits level at 460 mm.
3. **Deploy.** The tie bars unlatch and fold down the back of the left wing; each wing swings out on a continuous hinge, mounted on a 20 mm spacer angle bolted to tabs on the side rail, coming to rest 15° below horizontal on two fold-down outrigger legs. With the cart's long axis north to south, one wing faces east and one faces west. In wind, the four outrigger feet are staked.
4. **Charge.** The panels are pre-wired in parallel to the MPPT charge controller, which charges the 25.6 V pack. No cable is connected on site.
5. **Power.** The operator switches on the battery isolator and the inverter. Loads plug into the 120 V AC outlet (GFCI protected) and the DC panel (USB-C PD and 12 V sockets) on the handle end of the electronics box. A shunt monitor shows state of charge. A thermostat runs an IP54 filter fan when the box is warm, and the shade keeps direct sun off both enclosures.

![Energy flow](../media/flow.png)

*Figure 2. Daily energy flow at 4.5 kWh/m²/day global horizontal irradiation. All values are estimates from FCL-CAL-001.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`. Drawing FCL-DWG-002 gives the general arrangement and main dimensions.

*Table 1. Main components.*

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Cart frame and axle | 40 x 40 x 1.5 mm steel square tube, 1,200 x 600 mm, expanded-metal deck on the cross tubes, braced axle brackets, 20 mm axle, hinge tabs, handle sockets, leg clevises | Welded steel, decided (FCL-DDR-001, D5); about 15.4 kg (FCL-DDR-003) |
| 2 | Wheels (2) | 16 in (406 mm) flat-free, 720 mm track | Flat-free, decided (D5); about 4 kg each |
| 3 | Handle | Steel T-handle, grip at 900 mm, in two welded sockets with quick-release pins | Detaches for vehicle transport |
| 4 | Stand legs (4) | Tube legs on welded clevises, folding along the rails, detent pins | Level the deck when parked |
| 5 | Battery enclosure | IP65 case, about 420 x 360 x 300 mm | Sits over the axle, lowest heavy item |
| 6 | LiFePO4 pack | 25.6 V 50 Ah (1.28 kWh), 100 A BMS with low- and high-temperature charge cutoff | 24 V system, decided (D1) |
| 7 | Electronics enclosure | IP54, about 320 x 460 x 300 mm, IP54 filter fan (about 40 m³/h) and exhaust filter | Outlet face toward the handle; thermostat filter fan decided (FCL-DDR-002) |
| 8 | MPPT charge controller | 100 V, 20 A | At most 15 A from 400 W |
| 9 | Inverter | 1 kW continuous, 2 kW surge, pure sine, high-frequency, 24 V input, 120 V 60 Hz | 120 V first, 230 V 50 Hz variant documented, decided (D4) |
| 10 | DC outlet panel | 2 x USB-C PD 100 W, 2 x 12 V sockets, 24 to 12 V 20 A converter | 440 W DC in total |
| 11 | AC outlet with GFCI | GFCI duplex (120 V), in-use cover; 30 mA RCD socket for the 230 V variant | |
| 12 | Fusing and disconnect | Class T 100 A main fuse in the battery case within 150 mm of the terminal, isolator on the outlet face, DC breakers, shunt monitor | Fuse position fixed by FCL-DDR-003 |
| 13 | PV wings (2) | 200 W semi-flexible module bonded to a 1,400 x 700 mm frame of 30 x 20 mm aluminium tube with three ribs, 35 mm deep, about 6.0 kg, 24 V class (Vmp about 36 V) | Parallel wiring, decided (D3) |
| 14 | Panel hinges, spacers and latches | 1.2 m piano hinge per side on a 20 × 20 × 2 mm aluminium angle spacer bolted to steel tabs on the rail; two over-center latches for the tie bars | Spacer raises the hinge line, decided (FCL-DDR-002); pinch points, see Safety |
| 15 | Outrigger legs (4) | Legs on riveted brackets under the wing's outer edge, folding flat under the wing, with stake loops and stakes; set the 15° tilt | Stakes required above about 9 m/s wind |
| 16 | Accessory and cable bin | Open bin, balances the electronics box | Cords, lights, stakes |
| 17 | Wiring and hardware | 16 mm² (6 AWG) battery cable, PV cable, glands, cam straps, fasteners | Battery cables, glands and straps modeled |
| 18 | Sun shade | Reflective aluminized fabric on a light aluminium frame, about 830 × 580 mm, on four 355 mm uprights bolted to the rails, about 1.55 kg | Over both enclosures, decided (FCL-DDR-002); lifts off to open the battery case |
| 19 | Wing tie bars (2) | 20 × 20 mm aluminium bars pivoted on the left wing, latched to the right wing across the tops in travel | Added by FCL-DDR-003 |

## Key numbers

All values are estimates from FCL-CAL-001 (`docs/04-calcs/sizing.py`), which checks every requirement.

*Table 2. Key numbers.*

| Quantity | Value | Basis | Requirement |
| --- | --- | --- | --- |
| Stored energy | 1.28 kWh nominal, 1.15 kWh usable | 25.6 V x 50 Ah; 90 % depth of discharge | R1 met |
| PV energy into battery | 1.17 kWh/day at 4 kWh/m²/day, 1.31 at 4.5, 1.46 at 5 (25 °C air) | 400 W x GHI x 0.729 (transposition 0.947, temperature 0.915, other losses) | R3 met |
| East-west penalty | About 14 % against one panel aimed south at latitude tilt | Clear-sky model at 15, 30 and 45° N | |
| Peak charge power | About 260 to 290 W | Noon, east-west wings | |
| Full recharge, 10 to 100 %, no load | 0.79 day at 5 kWh/m²/day | 1,152 Wh / daily yield | R3 met |
| Reference load from battery | 1,063 Wh/day | 897 Wh at the outlets, Table 4 | |
| Autonomy with no sun | 1.08 days | 1,152 / 1,063 Wh | R4 met |
| Battery current | 46 A at 1 kW AC; 66 A with full DC; 98 A surge | 24 V at the low end | R2 met |
| Total mass | About 80.0 kg | Table 5 | R6 met (2.0 kg under the 82 kg limit set on 2026-10-02) |
| Center of gravity | 54 mm toward the handle from the axle, 561 mm above ground | Table 5 | R6 |
| Handle force, travel | 34 N level; 14 to 54 N at a 5° pitch | CG offset x weight / 1,240 mm axle to grip | R6 met |
| Lateral static tip angle | 32.7° | atan(360 mm half-track / 564 mm CG height) | R7 met |
| Pull force, 10 % grade | 125 N (gravel) to 156 N (grass) | 785 N weight x (grade + rolling resistance) | R7 met (grass, 160 N limit set on 2026-10-02) |
| Ground clearance | 193 mm | Under the axle, legs folded | R7 met |
| Deploy and stow time | 6.5 and 5.5 min | Table 6 | R5 met |
| Deployed footprint | About 2.0 x 2.0 m including the handle | Model, wings at 15° | |
| Stowed size, handle off | 1,400 x 830 x 1,220 mm | Model | |
| Wing to tyre clearance, deployed | 28 mm | Model, 20 mm hinge spacer | |
| Electronics box at 45 °C ambient | About 53 °C with the fan and shade, 70 °C sealed and unshaded, at 1 kW | Section G of FCL-CAL-001 | R9 at risk |
| Pack under the shade, noon, 45 °C ambient | About 48 °C (55 °C unshaded) | Section G of FCL-CAL-001 | R9 at risk |
| Wing lift-off wind speed, unstaked | About 8.9 m/s | Normal force coefficient 1.2 on 0.98 m², wing weight 59 N | R10 met only staked |
| Parts cost | About $2,101 against the $2,100 value-engineering target | `bom/bom.csv` | **R12 over the value-engineering target by USD 1** |

### PV yield

FCL-CAL-001 reads "peak sun hours" as daily global horizontal irradiation (GHI) and converts it to the wings with a clear-sky transposition model. At 15° the east-west wings collect about 0.95 of GHI, nearly as much as a horizontal panel, but about 14 % less than one panel aimed south at latitude tilt; the penalty is larger in winter at high latitude. With the cells at about 47 °C in 25 °C air, the 400 W array delivers about 0.78 of its rating times GHI at its terminals and 0.73 into the battery. At 4.5 kWh/m²/day that is 1.80 kWh at rating, 1.41 kWh at the array, 1.35 kWh after the MPPT and 1.31 kWh into the battery (Figure 2).

### Load profile and days of autonomy

The reference load is a small field post: a responder team's comms and lighting, one laptop station, and occasional tool use.

*Table 3. Reference load profile (assumed).*

| Load | Power | Hours per day | Energy at outlet | Path |
| --- | --- | --- | --- | --- |
| LED area lighting | 30 W | 8 | 240 Wh | DC |
| Radio, phone and satellite messenger charging | 30 W | 8 | 240 Wh | DC |
| Laptop and Wi-Fi router | 50 W | 6 | 300 Wh | AC |
| Power tool or small pump | 700 W | 1/6 (10 min) | 117 Wh | AC |
| **Total** | | | **897 Wh** | |

*Table 4. Energy drawn from the battery (assumed efficiencies, FCL-CAL-001).*

| Path | At outlet | Efficiency | From battery |
| --- | --- | --- | --- |
| DC (USB-C and 12 V converters) | 480 Wh | 0.93 | 516 Wh |
| AC (inverter), including 10 W idle for 7 h | 417 Wh | 0.92 plus idle | 523 Wh |
| Standby and filter fan | | | 24 Wh |
| **Total** | **897 Wh** | **0.844 overall** | **1,063 Wh** |

With 1.15 kWh usable, the pack carries this load for 1.08 days with no sun. At 4 kWh/m²/day the PV stores 1.17 kWh/day, a surplus of about 10 %; at 4.5 the surplus is about 24 %. The system breaks even at about 3.6 kWh/m²/day. A run of cloudy days is not covered. Inverter idle draw is the most sensitive assumption: each extra 5 W costs about 3 % of the daily load.

### Mass and center of gravity

*Table 5. Mass budget, wings stowed, deck level. X is measured from the deck center toward the handle; the axle is at X = 30 mm. From FCL-CAL-001 v0.3.*

| Item | Mass (kg) | X (mm) | Z (mm) |
| --- | --- | --- | --- |
| Frame, deck and axle (welded steel) | 15.4 | 5 | 420 |
| Wheels, flat-free (2), collars, pins | 8.3 | 30 | 203 |
| Handle | 2.6 | 950 | 700 |
| Stand legs | 2.5 | 0 | 230 |
| Battery enclosure | 3.0 | 0 | 610 |
| LiFePO4 pack | 12.0 | 0 | 576 |
| Electronics enclosure, filter fan, inverter, MPPT, fusing, monitor and outlets | 11.3 | 430 | 568 |
| Accessory bin and cables | 4.0 | −420 | 560 |
| PV wings, stowed (2) | 12.0 | 0 | 845 |
| Hinges, latches, outriggers and stakes | 4.1 | 0 | 820 |
| Hinge spacers (2) | 0.5 | 0 | 484 |
| Sun shade, frame and uprights | 1.6 | 185 | 760 |
| Wing tie bars (2) | 0.5 | 0 | 1,205 |
| Wiring, hardware and straps | 2.3 | 200 | 600 |
| **Total** | **80.0** | **84** | **561** |

The center of gravity is 54 mm on the handle side of the axle. At the 900 mm grip the handle carries about 34 N (3.5 kgf), and it stays positive between 14 and 54 N if the user holds the cart 5° nose-up or nose-down. The load in the accessory bin is the trim: moving 4 kg of cords from the bin to the electronics end raises the handle force by about 27 N. Amish relaxed the R6 limit to 75 kg on 2026-09-25 to keep the decided steel frame and flat-free tyres (FCL-DDR-002). Making the design buildable (FCL-DDR-003) added the brackets, gussets, tabs, sockets, clevises, fixings, tie bars and shade uprights the massing model did not have, about 4.9 kg, so the cart is about 5 kg over the limit and the pull on a 10 % grass grade is 156 N against 150 N. A bolted aluminium frame would bring the cart to about 72.7 kg. How to close the gap is an open decision, awaiting Amish (FCL-DEC-001, item 2).

### Deployment sequence

*Table 6. Deploy and stow time estimates, one person.*

| Deploy step | Time | Stow step | Time |
| --- | --- | --- | --- |
| Turn the cart north to south, drop four stand legs | 1.0 min | Loads off, inverter off, isolator off | 0.5 min |
| Unlatch both tie bars, fold each down the left wing | 0.5 min | Pull four stakes | 1.0 min |
| Fold the first wing out, swing down its two outrigger legs | 1.5 min | Fold the first wing's outriggers, raise it | 1.5 min |
| Same for the second wing | 1.5 min | Same for the second wing | 1.5 min |
| Stake the four outrigger feet (when wind is expected) | 1.0 min | Swing both tie bars over and latch them | 0.5 min |
| Isolator on, check the monitor, inverter on, plug in loads | 1.0 min | Raise four stand legs | 0.5 min |
| **Total** | **6.5 min** | **Total** | **5.5 min** |

## Key design choices

- **Panels as the cart walls, in fixed east-west wings at 15°.** The wings protect the battery and electronics in travel and need no separate storage, cables or aiming on site; they cost about 14 % of the energy a south-aimed panel would collect. Decided by Amish, 2026-09-25 (FCL-DDR-001, D2).
- **24 V class panels in parallel.** With Vmp about 36 V each, the panels can be paralleled into one MPPT and still charge a 25.6 V pack, so the off-sun wing does not limit the other. At 70 °C cell the headroom above the absorption voltage is under 1 V, so the chosen module must have Vmp of at least 36 V at STC. Decided by Amish, 2026-09-25 (D3).
- **25.6 V battery system.** Halves the current of a 12.8 V system (46 A instead of about 90 A at 1 kW), allowing thinner cable and a smaller fuse, while 24 V inverters and MPPT controllers remain common. Decided by Amish, 2026-09-25 (D1).
- **120 V 60 Hz output first.** A 230 V 50 Hz variant swaps the inverter and uses a 30 mA RCD socket. Decided by Amish, 2026-09-25 (D4).
- **Welded steel frame and flat-free tyres.** Easiest garage build and no punctures on debris, at a mass cost that put the cart over the earlier 75 kg R6 limit. Decided by Amish, 2026-09-25 (D5), and kept on 2026-10-02 with R6 set at 82 kg (FCL-DEC-001).
- **SwapCell compatibility as a future option only.** A later variant could take a SwapCell 48 V pack in place of item 6, which would need a 48 V inverter and charger. It would rely on three SwapCell interface v0.3 items approved portfolio-wide: a wake method for hosts without CAN, a charge-while-discharging mode (FieldCell charges from PV while loads run) and a latch vibration rating for vehicles. Decided by Amish, 2026-09-25 (D6).
- **Heavy parts low and over the axle.** The battery sits directly over the axle; the electronics box and the accessory bin balance each other fore and aft. Kept as a layout rule, decided by Amish, 2026-09-25 (FCL-DDR-002).
- **Forced ventilation of the electronics box.** A thermostat-controlled IP54 filter fan (40 to 60 m³/h) and exhaust filter keep the box within about 10 K of ambient at 1 kW; a sealed box would reach about 70 °C at 45 °C ambient. Decided by Amish, 2026-09-25 (FCL-DDR-002).
- **Sun shade over the enclosures.** A reflective shade on four posts keeps direct sun off the battery case and electronics box, holding the pack at about 48 °C instead of 55 °C at 45 °C ambient, for about $30 and 1 kg. Decided by Amish, 2026-09-25 (FCL-DDR-002).
- **Hinge spacer.** A 20 mm aluminium angle under each hinge raises the hinge line from 470 to 490 mm and opens the deployed wing-to-tyre clearance from 8 to 28 mm. Decided by Amish, 2026-09-25 (FCL-DDR-002).
- **Irradiance basis.** "Peak sun hours" in R3 and R4 means daily global horizontal irradiation in kWh/m²/day. Confirmed by Amish, 2026-09-25 (FCL-DDR-002).

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching `bom/bom.csv`. The wings and their hinges, outriggers and tie bars (13, 14, 15, 19) are drawn off to the front so the boxes stay visible.*

## Safety

> **Safety:** FieldCell combines a 1.28 kWh lithium battery, 120 V or 230 V AC output, high-current DC wiring, always-live PV panels and a cart of about 75 kg with folding wings. Every one of these is hazardous if the design or the build is wrong.

- **Lithium battery.** Use a LiFePO4 pack with a BMS that protects against overcharge, over-discharge, overcurrent, short circuit and over-temperature, and blocks charging below 0 °C and above about 45 °C. Put a class T fuse within about 150 mm of the positive terminal; in the constructable design it sits inside the battery case beside the pack. Secure the pack so it cannot shift in a tip-over, keep the enclosure vented to outside air, and keep sharp objects and debris out of it. In noon sun at 45 °C ambient the pack can reach about 55 °C unshaded and about 48 °C under the sun shade, so keep the shade in place. Shipping a pack of this size is regulated as dangerous goods.
- **AC output (120 V or 230 V).** Protect every AC outlet with a GFCI (120 V) or a 30 mA RCD (230 V). Bond the inverter neutral and ground to the frame only as the inverter maker specifies for a stand-alone portable source. Use in-use covers in rain, and keep outlets off wet ground.
- **Not for building wiring.** FieldCell has no power inlet and must never be connected to building or grid wiring, including by a "suicide cord" into an outlet. Back-feed can kill utility workers and damage both systems. Any such connection is out of scope.
- **DC wiring and fusing.** Fuse every circuit at its source: main class T fuse at the battery, breakers for the inverter, MPPT and DC outlets, and a PV breaker as the array disconnect. Size cables for the fuse rating. A battery isolator must be reachable without tools. The 2 kW surge with full DC load draws about 118 A for a few seconds; the BMS and fuse must tolerate this.
- **PV panels are live whenever lit.** Open-circuit voltage is about 45 V per panel, up to about 50 V in cold weather, and cannot be switched off at the panel. Do not disconnect PV connectors under load, and cover or disconnect the panels before working in the electronics box.
- **Lifting and handling.** At about 80 kg the cart must not be lifted by one person. Use two people to load it into a vehicle, and remove the battery pack (12 kg) first when possible.
- **Tipping.** The lateral tip angle is about 32.6° when stowed; do not traverse slopes across the fall line, and keep the handle low when descending. When deployed, wings can lift in wind above about 9 m/s unless the outrigger feet are staked; stow the wings in high wind. A stowed cart can be blown over at about 21 m/s side wind.
- **Pinch points.** The wing hinges, tie bar latches and folding legs can trap fingers. The tie bars must be latched to hold the wings firmly in travel. The deployed wing clears the tyre by about 28 mm; keep fingers out of that gap when folding.
- **Heat.** The inverter and MPPT shed up to about 140 W inside the electronics box. Keep the filter fan and exhaust filter clear, and do not run at high load with the vents covered or with the sun shade removed.

## Open questions

- Mass, pull force and cost: about 80 kg and 156 N on a grass grade after the design was made buildable. Decided by Amish, 2026-10-02: R6 set at 82 kg and the R7 grass pull at 160 N, keeping steel and flat-free tyres; the prototype is weighed at TRL 4 and moves to a bolted aluminium frame if it is over 82 kg (FCL-DEC-001). The cost is $2,101 against the $2,100 value-engineering target (R12).
- Inverter derating data at 45 °C (R9) and supplier quotes for the pack, PV wings and inverter to set the real cost against the $2,100 value-engineering target. Decided by Amish, 2026-09-25 (FCL-DDR-002); to be obtained with supplier selection.
- Confirm the inverter idle draw and fan noise (R11) and the filter fan noise from datasheets.
- Whether an AC charger or a vehicle 12 V input should be added for cloudy periods. Decided by Amish, 2026-10-02: no AC charger, since a power inlet is ruled out by the safety case; the vehicle 12 V input is left out of the first prototype and may be offered later as a DC-to-DC charging option if the responder review asks for it (FCL-DEC-001).
- How FieldCell relates to PowerBox and SwapCell in the portfolio. Decided by Amish, 2026-10-02: FieldCell is the mobile field-site unit (PV only, 1 kW AC, one-person cart, own 25.6 V pack), PowerBox the household outage unit (multi-input, indoor, SwapCell pack) and SwapCell the shared pack standard (FCL-DEC-001).
- Handle geometry and grip height for users from 1.55 to 1.90 m tall.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [cutaway](../media/cutaway.png), [interactive 3D model](../media/viewer.html). General arrangement: [FCL-DWG-002](../cad/drawings/FCL-DWG-002.pdf). Prototype build plan: [FCL-BLD-001](05-build-plan.md).
