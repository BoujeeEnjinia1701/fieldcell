# FieldCell

**Area:** Situational Field Hardware · **Status:** Concept · **Prototype budget:** about $1,500 USD · **Difficulty:** 3 of 5

Two-wheel hand cart carrying fold-out PV and a LiFePO4 bank, with an inverter and DC outlets, that one person can deploy in under 10 minutes.

## Problem

Disaster responders and remote crews rely on noisy, fuel-hungry generators.

## Concept

Two-wheel hand cart carrying fold-out PV and a LiFePO4 bank, with an inverter and DC outlets, that one person can deploy in under 10 minutes.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Folding PV panels 200 W (2)
- LiFePO4 bank 1.2 kWh
- MPPT charge controller
- Inverter 1 kW
- Steel cart frame
- Weatherproof enclosure

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

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
