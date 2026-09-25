---
doc_id: FCL-PRB-001
title: FieldCell problem statement
project: FieldCell
doc_type: Problem statement
version: "0.3"
status: Draft
date: '2026-09-25'
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
  change: Populate to TRL 2 (users, context, constraints, out of scope, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record decisions of FCL-DDR-001 (first user group, 120 V first build); budget note from FCL-CAL-001
---

# FieldCell problem statement

Disaster responders and remote crews power small loads (radios, lights, laptops, chargers) with portable fuel generators that are loud, give off carbon monoxide, need a steady fuel supply and run far below their rated power most of the time.

## The problem

A typical field post draws a few hundred watts on average: radio and phone charging, LED area lighting, a laptop and a router, with short bursts from a power tool or a small pump. The usual answer is a 2 to 5 kW petrol or diesel generator. At these loads a generator spends most of its life near idle, where fuel use per kilowatt-hour is worst, and it must be refuelled every few hours from a supply chain that a disaster may have cut.

The generator also shapes the site. Open-frame units are commonly rated at about 65 to 75 dB(A) at 7 m, loud enough to mask radio traffic and voices, so they are placed away from people and run on long cords. Exhaust carbon monoxide is a recurring cause of injury and death after storms, when generators are run in or near shelters, garages and tents. Fuel adds a storage and spill hazard.

Solar plus battery systems solve the noise, fumes and fuel problems, but the field options fall into two awkward groups. Portable power stations are easy to carry but hold under about 1 kWh in most sizes under 15 kg and need separate folding panels that must be laid out, aimed and cabled. Towed solar trailers and containerized systems carry several kilowatts but need a vehicle and often a crew to deploy. There is no open, inspectable design in between: a single-person, wheel-it-in unit with about 1 kWh of storage and a few hundred watts of built-in PV that is working within minutes of arrival.

## Users and context

*Table 1. Users, needs and context.*

| User | Need | Context |
| --- | --- | --- |
| Disaster responder (search and rescue, field medical post, incident command) | Quiet, fume-free power for comms, lighting and chargers from the first hour; no refuelling | Damaged areas, debris, mud, rain; set up next to people and tents |
| Humanitarian field team | Power a registration or water point for days with little resupply | Camps and distribution sites, hot or cold climates |
| Remote crew (trail, survey, environmental monitoring, utility) | Daytime power for tools and battery charging away from any vehicle track | Rough ground, hills, grass and gravel |
| Community resilience hub or event | A shareable unit to power phones, lights and a router during outages | Parks, schools, community centers |
| Open hardware builder | A reproducible design to build, audit and adapt | Garage or makerspace |

## Constraints

- Prototype parts cost about $1,500 USD (`project.yaml`), using off-the-shelf electronics and a welded steel frame. The TRL 3 BOM totals about $2,006 (FCL-CAL-001), so the budget is under review; see `docs/REVIEW.md`.
- One person must move, deploy and stow it, without tools, on uneven ground.
- Must work in rain and dust, and through a range of field temperatures, while its lithium cells stay within safe charging limits.
- Electrical safety: fused circuits, ground-fault protection on AC outlets, a clear disconnect, and no connection to building wiring.
- Garage-buildable: common tools, no custom printed circuit boards for the first build.
- Must fit a pickup bed or van with the handle removed, and be light enough for two people to lift into one.

## Out of scope

- Connection to building or grid wiring, including back-feeding through an outlet or a transfer switch.
- Fuel-hybrid operation (a generator input may be discussed later as an option, not designed here).
- Life-critical medical loads that need a certified uninterruptible power supply.
- Towing behind a vehicle at road speed.
- Megawatt-hour or multi-kilowatt site power; that is the domain of trailers and containers.

## Prior work

- **Portable power stations** (for example EcoFlow, Jackery and Bluetti) package a lithium battery, inverter and outlets in one box, with folding panels sold separately. They are closed designs, and most units above 1 kWh are heavy to carry by hand.
- **Towed solar trailers and solar light towers** are used on construction sites and in military expeditionary power. They carry more energy and PV but need a vehicle to move.
- **Hybrid generator programs** in humanitarian and military logistics pair a generator with a battery bank so the engine runs less often, which shows the value of storage at small field loads.
- **Open designs** for solar carts and DIY "solar generators" exist as hobby builds and videos, but few publish a complete, reviewed design with requirements, safety analysis and a bill of materials.

## Open questions

- First user group: disaster response. Decided by Amish, 2026-09-25 (FCL-DDR-001, D8). Humanitarian field teams and remote crews remain secondary users.
- Which responder organization, if any, could review the deployment sequence and load profile? Proposed, awaiting Amish (FCL-DDR-001, O1).
- Output voltage: 120 V 60 Hz for the first build, with a 230 V 50 Hz variant documented. Decided by Amish, 2026-09-25 (FCL-DDR-001, D4).
