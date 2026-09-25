---
doc_id: FCL-REQ-001
title: FieldCell requirements
project: FieldCell
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-24'
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
---

# FieldCell requirements

These are first-pass requirements for the concept. Targets are proposals for review and will be checked by calculation at TRL 3. The estimate column comes from the first-order numbers in FCL-PRC-001.

*Table 1. Requirements.*

| ID | Requirement | Target | Concept estimate | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Store enough energy for a day of field use | 1.2 kWh nominal or more; 1.0 kWh usable or more | 1.28 kWh nominal, about 1.15 kWh usable at 90 % depth of discharge. Met | Datasheet and energy calculation |
| R2 | Supply AC and DC loads | 1,000 W continuous pure sine AC, 2,000 W surge; DC outlets 300 W or more in total (USB-C PD and 12 V) | 1 kW inverter; about 440 W DC (2 x 100 W USB-C, 240 W at 12 V). Met by selection | Datasheets; current and cable calculation |
| R3 | Recharge from its own PV | 1.1 kWh/day or more into the battery at 4 peak sun hours; full recharge from 10 % in one day at 5 peak sun hours with no load | 1.12 kWh/day at 4 h (thin); full recharge in about 0.8 day at 5 h. Met, thin at 4 h | PV yield calculation with stated derating |
| R4 | Carry a reference load through a day without sun | Reference load of 0.9 kWh/day at the outlets for 1 day or more with no sun; energy-neutral at 4 peak sun hours or more | About 1.1 days; about 9 % surplus at 4 h. Met, thin | Load profile and energy balance |
| R5 | Deploy fast with one person | From arrival to power available in 10 min or less, one person, no tools; stow in 10 min or less | About 6 min (step estimate). Met | Task analysis; later timed trial |
| R6 | Movable by one person | Total mass 70 kg or less; vertical handle force 10 to 150 N (never negative) over a 5 degree pitch either way; heaviest removable module 25 kg or less | About 68.5 kg (thin); 17 to 52 N; battery pack about 12 kg. Met, mass margin thin | Mass budget and center of gravity calculation |
| R7 | Cross rough ground | 16 in (406 mm) wheels or larger; ground clearance 150 mm or more; climb a 150 mm step; pull force 150 N or less on a 10 % grade over gravel or grass; static lateral tip angle 25 degrees or more | 406 mm wheels; about 190 mm clearance; pull about 110 to 135 N; tip about 32 degrees. Met, pull force thin | Geometry and force calculation |
| R8 | Work in rain and dust | Electronics enclosure IP54 while operating; battery enclosure IP65; all cable entries through glands or sealed connectors | Design intent; ventilation of the electronics box against IP54 not yet resolved. Open | Design review; later spray test |
| R9 | Stay safe across field temperatures | Operate at -10 to 45 °C ambient; BMS blocks charging below 0 °C cell temperature; inverter derating known at 45 °C | Design intent; thermal model not done. Open | Datasheets and thermal estimate |
| R10 | Stay put in wind when deployed | Wings and cart stable to 15 m/s (54 km/h) with the four outrigger feet staked or ballasted; stow instruction above that | Unstaked wings may lift at about 9 m/s. Met only with stakes | Wind load calculation |
| R11 | Be quiet | 45 dB(A) or less at 1 m at 500 W load | Depends on inverter fan; unverified | Datasheet; later sound level measurement |
| R12 | Be electrically safe and affordable | Every circuit fused at its source; GFCI (120 V) or 30 mA RCD (230 V) on all AC outlets; battery disconnect reachable without tools; no inlet or path to building wiring; parts cost $1,500 or less | Design intent; parts about $1,462 (indicative), about 2.5 % margin. Met, no contingency | Design review; priced BOM |

## Assumptions

- Peak sun hours of 4 to 5 per day (clear-season mid-latitude sites); a cloudy week is not covered by R3 or R4.
- The reference load in R4 is defined in FCL-PRC-001: lighting, radio and phone charging, a laptop and router, and short power-tool bursts.
- Usable battery capacity is 90 % of nominal, for LiFePO4 cells with a conservative BMS.
- "Arrival" in R5 means the cart has been wheeled to the chosen spot; choosing the spot is not timed.
