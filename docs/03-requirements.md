---
doc_id: FCL-REQ-001
title: FieldCell requirements
project: FieldCell
doc_type: Requirements
version: "0.6"
status: Draft
date: '2026-10-01'
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
  change: First measurable requirements for TRL 2
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Status of every requirement from FCL-CAL-001; R2 names 120 V 60 Hz for the first build (FCL-DDR-001); irradiance basis stated
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Values and status from FCL-CAL-001 v0.3 for the constructable design (FCL-DDR-003); no target changed
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# FieldCell requirements

These are the requirements for the concept. The value and status columns come from the TRL 3 calculation note FCL-CAL-001 v0.3, which checks each one by calculation against the constructable design of FCL-DDR-003. Six are met, two are not met (R6 mass by 5.0 kg, R7 grass pull by 6 N), one is over its value-engineering target (R12 cost, by $1), one is at risk (R9) and two cannot be verified until test (R8 and R11). No target has changed since v0.4; how to close the R6 and R7 gaps is proposed in the design decisions register (FCL-DEC-001), awaiting Amish; the cost savings worth trying for R12 are in its Value engineering section. On 2026-09-25 Amish accepted the TRL 3 recommendations (FCL-DDR-002): the R6 mass limit is relaxed from 70 kg to 75 kg, the value-engineering target behind R12 moves from $1,500 to $2,100, R3 and R4 are stated in global horizontal irradiation, and R8 and R9 name the filter fan and sun shade.

*Table 1. Requirements.*

| ID | Requirement | Target | Value at TRL 3 (FCL-CAL-001 v0.3) | Status | Verification |
| --- | --- | --- | --- | --- | --- |
| R1 | Store enough energy for a day of field use | 1.2 kWh nominal or more; 1.0 kWh usable or more | 1.28 kWh nominal, 1.15 kWh usable at 90 % depth of discharge | Met | Calculation; datasheet |
| R2 | Supply AC and DC loads | 1,000 W continuous pure sine AC at 120 V 60 Hz for the first build (230 V 50 Hz variant), 2,000 W surge; DC outlets 300 W or more in total (USB-C PD and 12 V) | 1 kW inverter by selection; 440 W DC; 66 A continuous battery current on a 100 A fuse and BMS | Met | Calculation; datasheets |
| R3 | Recharge from its own PV | 1.1 kWh/day or more into the battery at 4 kWh/m²/day of global horizontal irradiation (GHI, "peak sun hours"); full recharge from 10 % in one day at 5 kWh/m²/day GHI with no load | 1.17 kWh/day at 4 kWh/m²/day (1.09 in 40 °C air); full recharge in 0.79 day at 5 | Met | PV yield calculation; later logged trial |
| R4 | Carry a reference load through a day without sun | Reference load of 0.9 kWh/day at the outlets for 1 day or more with no sun; energy-neutral at 4 kWh/m²/day GHI or more | 1.08 days; +10 % surplus at 4 kWh/m²/day; break-even at 3.64 | Met | Load and energy balance; later logged trial |
| R5 | Deploy fast with one person | From arrival to power available in 10 min or less, one person, no tools; stow in 10 min or less | 6.5 min deploy, 5.5 min stow by task analysis, including the tie bars | Met | Task analysis; later timed trial |
| R6 | Movable by one person | Total mass 75 kg or less (relaxed from 70 kg, FCL-DDR-002); vertical handle force 10 to 150 N (never negative) over a 5° pitch either way; heaviest removable module 25 kg or less | 80.0 kg; 14 to 54 N; pack 12.0 kg | **Not met** (mass 5.0 kg over) | Mass budget and CG calculation; later weighing |
| R7 | Cross rough ground | 16 in (406 mm) wheels or larger; ground clearance 150 mm or more; climb a 150 mm step; pull force 150 N or less on a 10 % grade over gravel or grass; static lateral tip angle 25° or more | 406 mm wheels; 193 mm clearance; step with about 149 N pull at the grip; 125 N gravel, 156 N grass; 32.7° | **Not met** (grass pull 6 N over) | Geometry and force calculation |
| R8 | Work in rain and dust | Electronics enclosure IP54 while operating, ventilated by a thermostat-controlled IP54 filter fan and exhaust filter (FCL-DDR-002); battery enclosure IP65; all cable entries through glands or sealed connectors | IP54 enclosure with IP54 filter fan and exhaust filter; IP65 case; glands, by selection | Not verifiable at TRL 3 | Design review; later spray and dust test |
| R9 | Stay safe across field temperatures | Operate at −10 to 45 °C ambient; BMS blocks charging below 0 °C cell temperature; inverter derating known at 45 °C; reflective sun shade over both enclosures when deployed (FCL-DDR-002) | Charge block by BMS selection; electronics box about 53 °C at 45 °C ambient with the fan and shade (70 °C sealed, unshaded); pack under the shade about 48 °C at 45 °C ambient, so charging stops only above about 42 °C ambient; derating data not yet obtained | At risk | Thermal estimate; datasheets |
| R10 | Stay put in wind when deployed | Wings and cart stable to 15 m/s (54 km/h) with the four outrigger feet staked or ballasted; stow instruction above that | Staked: 28 N pull-out per foot at 15 m/s (50 N with a 1.5 factor); unstaked wings lift at about 8.9 m/s | Met (staked) | Wind load calculation |
| R11 | Be quiet | 45 dB(A) or less at 1 m at 500 W load | About 41 dB(A) from assumed fan levels, not datasheet values | Not verifiable at TRL 3 | Datasheets; later sound level measurement |
| R12 | Be electrically safe and affordable | Every circuit fused at its source; GFCI (120 V) or 30 mA RCD (230 V) on all AC outlets; battery disconnect reachable without tools; no inlet or path to building wiring; parts cost at or below the value-engineering target of $2,100 | Safety provisions met by design (class T fuse inside the battery case, within 150 mm of the terminal); parts about $2,101 | Safety provisions met by design; **over the value-engineering target by USD 1** | Design review; priced BOM |

## Assumptions

- "Peak sun hours" in R3 and R4 is daily global horizontal irradiation in kWh/m²/day, the figure most climate data give. FCL-CAL-001 converts it to the east-west wings with a transposition ratio of about 0.95. Confirmed by Amish, 2026-09-25 (FCL-DDR-002).
- 4 to 5 kWh/m²/day covers clear-season sites at low and middle latitudes; a cloudy week or a high-latitude winter is not covered by R3 or R4.
- The reference load in R4 is defined in FCL-PRC-001, Table 3: lighting, radio and phone charging, a laptop and router, and short power-tool bursts.
- Usable battery capacity is 90 % of nominal, for LiFePO4 cells with a conservative BMS.
- "Arrival" in R5 means the cart has been wheeled to the chosen spot; choosing the spot is not timed.
- The target in R12 is `budget_usd` in `project.yaml`, a hypothetical control target that keeps the design thinking along a value-engineering lens. It moved from $1,500 to $2,100 (BOM plus a small contingency) by Amish's decision of 2026-09-25 (FCL-DDR-002). Supplier quotes for the pack, PV wings and inverter will give the real cost.
- The R6 mass limit of 75 kg keeps the decided steel frame and flat-free tyres. The cart is a two-person lift either way; the handle force is what one person feels, and it stays within limits. The constructable cart is about 80 kg, so the R7 pull force on grass is over its limit.
