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

## Session 2026-09-25: TRL 3

Amish's instruction for this session (2026-09-25): "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." FieldCell now claims TRL 3 (proof of concept on paper). TRL 4 is on hold by Amish's instruction.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (FCL-DDR-001 v0.1): the eight TRL 2 review items with a recommendation recorded as decided by Amish, 2026-09-25, and five items that stay open.
- `docs/04-calcs/01-sizing.md` (FCL-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: first-principles sizing with stated assumptions: stored energy; battery current, cable, PV voltage window; a clear-sky transposition model for the east-west wings at 15, 30 and 45° N; temperature derating; load and autonomy; mass and center of gravity from the model's tube geometry; pull force, step climb, tip angle and frame and axle stress; enclosure and battery thermal estimates; wind on the wings and the cart; deploy and stow time; noise; BOM total. The script imports the model's `PARAMS` and prints every number the note quotes, tagged [A1] to [K1].
- `cad/src/model.py`: parametric build123d model (frame of hollow tube, axle, wheels, handle, legs, enclosures with filter fan, contents, hinged PV wings deployed or stowed, outriggers, bin), exporting `cad/step/fieldcell-deployed.step`, `fieldcell-stowed.step`, `frame.step`, `pv-wing.step`, `battery-enclosure.step`, `electronics-enclosure.step` and matching STL files in `cad/stl/`.
- `cad/src/sheets.py` and `cad/drawings/FCL-DWG-002.svg`, `.pdf`, `.png`: general arrangement at Rev P1, scale 1:25, with overall dimensions drawn from the model, the stowed cart in the isometric view and a main-dimensions box. The sheet carries "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet remains FCL-DWG-001.
- `bom/bom.csv` and `bom/bom-notes.md`: all 17 lines priced with a supplier type; total $2,006 against the $1,500 budget.
- `cad/src/concept_media.py` now builds the media from `model.py` and takes its figures from the calc script; all media in `media/` were regenerated and checked by eye; temporary `media/_views*` folders were deleted.
- FCL-PRB-001, FCL-PRC-001 and FCL-REQ-001 revised to v0.3 (decisions recorded, numbers replaced by FCL-CAL-001, requirement status column); `README.md` updated to TRL 3 with links; `project.yaml` set to `trl: 3`, `trl_target: 3`, with the evidence files listed. PDFs are in `docs/pdf/`.

### Requirements (FCL-CAL-001, Table 8)

6 met, 2 not met, 2 at risk, 2 not verifiable at TRL 3.

| ID | Status | Value against target |
| --- | --- | --- |
| R6 | **Not met** | 73.5 kg against 70 kg. Handle force 14 to 50 N and 12 kg pack are within limits. The decided steel frame (12.8 kg) and flat-free wheels (8 kg) are the cause; TRL 2 budgeted 68.5 kg |
| R12 | **Not met** | Parts $2,006 against $1,500 (+34 %). Safety provisions met by design |
| R7 | At risk | Pull force 144 N on grass on a 10 % grade against 150 N; step climbed with about 136 N at the grip; clearance 193 mm; tip 32.9° |
| R9 | At risk | Electronics box about 54 °C at 45 °C ambient at 1 kW with a filter fan (70 °C sealed); battery case in noon sun about 10 K above ambient, so charging is blocked in the hottest hours |
| R8 | Not verifiable at TRL 3 | IP54 enclosure with IP54 filter fan and filter, IP65 case, by selection |
| R11 | Not verifiable at TRL 3 | About 41 dB(A) at 1 m from assumed fan levels |
| R1 | Met | 1.28 kWh nominal, 1.15 kWh usable |
| R2 | Met | 1 kW AC, 440 W DC; 66 A continuous on a 100 A fuse |
| R3 | Met | 1.17 kWh/day into the battery at 4 kWh/m²/day GHI (1.09 in 40 °C air); full recharge 0.79 day at 5 |
| R4 | Met | 1.08 days with no sun; +10 % surplus at 4 kWh/m²/day; break-even at 3.64 |
| R5 | Met | 6.0 min deploy, 5.0 min stow by task analysis |
| R10 | Met | Staked: 27 N pull-out per foot at 15 m/s (49 N factored); unstaked wings lift at 9.2 m/s |

Other key numbers: east-west penalty about 14 % against a south-aimed panel (10 % was assumed at TRL 2); PV Vmp headroom at 70 °C cell only 0.9 V above what the MPPT needs; deployed wing to tyre clearance 8 mm; stowed cart overturns in about 20 m/s side wind; stowed size with the handle off 1,400 x 784 x 1,170 mm. Every TRL 2 number in the docs was checked against the script and corrected where it differed (FCL-CAL-001, "Checks against earlier figures").

### Decisions recorded (FCL-DDR-001)

Decided by Amish, 2026-09-25, going with the recommendation: D1 25.6 V 50 Ah battery; D2 fixed east-west wings at 15° (wings as cart walls); D3 24 V class panels in parallel; D4 120 V 60 Hz first, 230 V variant documented; D5 welded steel frame and flat-free tyres; D6 SwapCell as a future variant only (a future variant would cite SwapCell interface v0.3 items: wake without CAN, charge-while-discharging, latch vibration rating); D7 keep `budget_usd` at $1,500 until supplier quotes; D8 disaster response as the first user group. No requirement target was relaxed; `budget_usd` is unchanged.

### Proposed, awaiting Amish

Still open from TRL 2 (no recommendation was made):

1. Whether to seek a responder organization to review the deployment sequence and load profile, and which one (O1).
2. How FieldCell relates to PowerBox and SwapCell in the portfolio (O2).
3. Whether to add an AC charger or a vehicle 12 V input for cloudy periods (O3).
4. Heavy parts low and over the axle as a layout rule (O4); recommendation: keep it.

New from TRL 3:

5. **Budget (R12).** Options: (a) raise `budget_usd` to about $2,100 (BOM plus about 5 % contingency); (b) cost-down to about $1,600 with generic inverter, MPPT and monitor, at a risk to idle draw, noise and reliability; (c) keep $1,500 and cut the PV to one wing, which breaks R3 and R4. Recommendation: (a), after quotes for the pack, the PV wings and the inverter. `project.yaml` is unchanged.
6. **Mass (R6).** Options: (a) relax the R6 mass limit to 75 kg, keeping the decided steel frame and flat-free tyres (the handle force is what one person feels, and it stays within limits; the cart is a two-person lift either way); (b) change to a bolted aluminium frame, about 67.4 kg, which reverses D5 and adds cost; (c) pneumatic tyres, about 71.1 kg, still over. Recommendation: (a), with a note that R7 pull force on grass is then at its limit.
7. **Electronics box ventilation (R8, R9).** Adopt a thermostat-controlled IP54 filter fan (40 to 60 m³/h) with an IP54 exhaust filter, already priced in BOM line 7 and modeled. Recommendation: adopt.
8. **Sun shade (R9).** Add a light reflective shade over the battery and electronics enclosures when deployed (about $30 and 1 kg, not yet in the BOM or model), and obtain inverter derating data at 45 °C. Recommendation: add at the next revision.
9. **Hinge spacer.** Raise each hinge line by a 20 mm spacer to open the 8 mm wing-to-tyre clearance. Recommendation: adopt; the model's `hinge_z` parameter is left at 470 mm until decided.
10. **"Peak sun hours" basis (R3, R4).** Read as daily global horizontal irradiation in kWh/m²/day, as FCL-CAL-001 does. Recommendation: confirm.

### Safety concerns

- 1.28 kWh LiFePO4 pack: class T fuse at the terminal, BMS with low- and high-temperature charge cutoff; the pack can reach about 55 °C in noon sun at 45 °C ambient, so shading matters. Dangerous-goods rules for shipping.
- 120 V AC outdoors: GFCI on every outlet, neutral bonding per the inverter maker, in-use covers; no inlet and no connection to building wiring, ever.
- DC surge: 2 kW surge with full DC load is about 118 A for seconds; the BMS peak rating and fuse curve must be confirmed.
- PV is live whenever lit (about 45 V, up to about 50 V cold).
- 73.5 kg cart: two-person lift; tipping on cross-slopes; wing lift above about 9 m/s unstaked; stowed cart can blow over at about 20 m/s; pinch points at hinges, latches and the 8 mm wing-to-tyre gap.
- Heat: up to about 140 W inside the electronics box at 1 kW; a sealed box would reach about 70 °C at 45 °C ambient.

### Other notes

- No existing TRL 4 material was found (`build-log/` holds only its README; `electronics/` and `firmware/` are empty). None was created. STANDARDS section 9 asks for a TRL change to be recorded in the build log; no build-log entry was written this session, since the brief did not name one.
- No unchecked citations were listed at TRL 2 (prior work is described without links), so no web verification was needed. BOM prices are indicative estimates by supplier type, not quotes.
- The deliverable list in `.claude/commands/advance-trl3.md` names the drawing DWG-001; because the concept sheet already uses FCL-DWG-001, the general arrangement is FCL-DWG-002, as this session's brief directs.

### Recommended next step

Stay at TRL 3. TRL 4 is on hold by Amish's instruction. Decide items 5 to 10 above, starting with the budget and the mass limit, and get supplier quotes for the pack, the PV wings and the inverter (including idle draw, fan noise and 45 °C derating data), then revise FCL-CAL-001 and the BOM on paper.

For reference only, TRL 4 would need: a lab test report (TST, `environment: lab`) on a built cart or key subassemblies (PV yield logged against irradiance, inverter idle draw and enclosure temperature at 1 kW, noise at 500 W, mass and handle force, deploy and stow timed trials, wing lift and stake pull-out), build-log entries, and the purchasing and build work that goes with them. None of this has been started.
