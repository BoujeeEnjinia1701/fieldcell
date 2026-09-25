# FieldCell

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Situational Field Hardware · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $1,500 USD · **Difficulty:** 3 of 5

Two-wheel hand cart carrying fold-out PV and a LiFePO4 bank, with an inverter and DC outlets, that one person can deploy in under 10 minutes.

![FieldCell concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement FCL-DWG-002 (PDF)](cad/drawings/FCL-DWG-002.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Disaster responders and remote crews rely on noisy, fuel-hungry generators.

## Concept

Two-wheel hand cart carrying fold-out PV and a LiFePO4 bank, with an inverter and DC outlets, that one person can deploy in under 10 minutes.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Folding PV panels 200 W (2)
- LiFePO4 bank 1.28 kWh (25.6 V 50 Ah)
- MPPT charge controller
- Inverter 1 kW
- Welded steel cart frame, 16 in flat-free wheels
- IP65 battery case and IP54 electronics enclosure with filter fan

The priced bill of materials is in [bom/bom.csv](bom/bom.csv) (about $2,006 at TRL 3, over the $1,500 budget; see the review note).

## Safety

> Contains a high-energy battery and AC output. Fuse every circuit and follow local electrical code.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (FCL-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `FCL-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
