# Review note: FieldCell

## Session 2026-09-24: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (FCL-PRB-001 v0.2): the problem, users and context, constraints, out of scope, prior work (described without links), open questions.
- `docs/03-requirements.md` (FCL-REQ-001 v0.2): 12 measurable requirements (R1 to R12) with targets, concept estimates and planned verification.
- `docs/02-concept.md` (FCL-PRC-001 v0.2): how it works, 17-item component table, first-order numbers (PV yield, load profile and autonomy, mass and center of gravity, deploy time, wind), design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model (frame and axle, two wheels, handle, stand legs, battery enclosure and pack, electronics enclosure with MPPT, inverter, outlets and fusing, two PV wings deployed on hinges and outrigger legs, accessory bin). The hero also shows the same cart stowed for travel. The script computes and prints the mass budget, center of gravity and energy flow.
- `media/`: hero with the 1.75 m figure, blueprint sheet FCL-DWG-001 (PNG and PDF), cutaway, exploded view with BOM callouts, energy flow diagram (estimates marked), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 17 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md`.
- `README.md`: hero image and links line.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Stored energy | 1.28 kWh nominal, about 1.15 kWh usable | R1 met |
| PV into battery | 1.12 to 1.40 kWh/day at 4 to 5 peak sun hours (0.754 array derating) | R3 met, thin at 4 h |
| Autonomy, 0.9 kWh/day reference load | about 1.1 days with no sun; about 9 % surplus at 4 h | R4 met, thin |
| Deploy time | about 6 min, one person | R5 met |
| Mass | about 68.5 kg against a 70 kg limit | R6 met, thin |
| Center of gravity | about 63 mm toward the handle from the axle; handle force 17 to 52 N | R6 met |
| Pull force, 10 % grade | about 110 to 135 N against 150 N | R7 met, thin |
| Lateral tip angle | about 32 degrees | R7 met |
| Parts cost | about $1,462 against $1,500 | R12 met, 2.5 % margin |

Requirements not met or not yet shown:

- **R10 (wind):** unstaked wings may lift at about 9 m/s. The requirement is met only with the four outrigger feet staked or ballasted.
- **R8 and R9 (weather and temperature):** design intent only. Venting the inverter heat while keeping the electronics box IP54 is unresolved.
- **R11 (noise):** depends on the inverter fan; unverified.
- Several margins are thin (R3, R4, R6, R7, R12). The energy balance at 4 peak sun hours is the main technical risk.

### Proposed, awaiting Amish

1. Battery system voltage: 25.6 V 50 Ah (recommended), 12.8 V 100 Ah, or 51.2 V.
2. Wing layout: fixed east-west wings at 15 degrees (recommended, fastest), or detachable panels on kickstands aimed at the sun (about 10 to 15 % more energy, 3 to 5 min slower).
3. Panels: 24 V class (Vmp about 36 V) wired in parallel into one MPPT (recommended), rather than 12 V class panels in series.
4. AC output: 120 V 60 Hz for the first build (recommended), with a 230 V 50 Hz variant documented.
5. Frame and wheels: welded steel with flat-free tyres (recommended for a garage build and debris), or bolted aluminium (about 4 to 5 kg lighter) and pneumatic tyres.
6. SwapCell: record compatibility with a SwapCell 48 V pack as a future variant only; the concept is not designed around it.
7. Budget: keep $1,500 (parts about $1,462, no contingency) or raise to about $1,750 to cover price variation, stakes, tools and spares. Recommendation: keep $1,500 for now and decide after supplier quotes at TRL 3. `project.yaml` is unchanged.
8. First user group: disaster response (recommended), humanitarian field teams or remote crews; and whether to seek a responder organization to review the deployment sequence.
9. Portfolio overlap: how FieldCell relates to PowerBox and SwapCell.

### Safety concerns

- 1.28 kWh lithium pack: BMS with low-temperature charge cutoff, class T fuse at the terminal, secured and vented enclosure; shipping is regulated as dangerous goods.
- 120 V or 230 V AC output outdoors: GFCI or 30 mA RCD on every outlet, neutral bonding per the inverter maker, in-use covers.
- Must never be connected to building wiring; there is no inlet, and back-feed is a lethal hazard to utility workers.
- PV is live whenever lit (about 45 V open circuit per panel).
- 68 kg cart: two-person lift into vehicles; tipping on cross-slopes; wing lift in wind; pinch points at hinges and latches.
- Heat build-up in a sealed electronics box.

### Recommended next step

Review this note and the media, and decide the proposals above, especially items 1 to 3 and 7. If approved, run `/advance-trl3` to check the PV yield, energy balance, thermal and wind loads by calculation, and to produce the parametric model and drawing sheet.
