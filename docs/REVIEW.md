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

1. Battery system voltage: 25.6 V 50 Ah (recommended), 12.8 V 100 Ah, or 51.2 V. **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-001).
2. Wing layout: fixed east-west wings at 15 degrees (recommended, fastest), or detachable panels on kickstands aimed at the sun (about 10 to 15 % more energy, 3 to 5 min slower). **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-001).
3. Panels: 24 V class (Vmp about 36 V) wired in parallel into one MPPT (recommended), rather than 12 V class panels in series. **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-001).
4. AC output: 120 V 60 Hz for the first build (recommended), with a 230 V 50 Hz variant documented. **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-001).
5. Frame and wheels: welded steel with flat-free tyres (recommended for a garage build and debris), or bolted aluminium (about 4 to 5 kg lighter) and pneumatic tyres. **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-001).
6. SwapCell: record compatibility with a SwapCell 48 V pack as a future variant only; the concept is not designed around it. **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-001).
7. Budget: keep $1,500 (parts about $1,462, no contingency) or raise to about $1,750 to cover price variation, stakes, tools and spares. Recommendation: keep $1,500 for now and decide after supplier quotes at TRL 3. `project.yaml` is unchanged. **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-001). Superseded by FCL-DDR-002 A1 ($2,100).
8. First user group: disaster response (recommended), humanitarian field teams or remote crews; and whether to seek a responder organization to review the deployment sequence. First user group: disaster response,**Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-001). Responder organization: no recommendation, stays Proposed, awaiting Amish.
9. Portfolio overlap: how FieldCell relates to PowerBox and SwapCell. No recommendation; stays Proposed, awaiting Amish.

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
4. Heavy parts low and over the axle as a layout rule (O4); recommendation: keep it. **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-002).

New from TRL 3:

5. **Budget (R12).** Options: (a) raise `budget_usd` to about $2,100 (BOM plus about 5 % contingency); (b) cost-down to about $1,600 with generic inverter, MPPT and monitor, at a risk to idle draw, noise and reliability; (c) keep $1,500 and cut the PV to one wing, which breaks R3 and R4. Recommendation: (a), after quotes for the pack, the PV wings and the inverter. `project.yaml` is unchanged. **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-002). `budget_usd` is now 2,100.
6. **Mass (R6).** Options: (a) relax the R6 mass limit to 75 kg, keeping the decided steel frame and flat-free tyres (the handle force is what one person feels, and it stays within limits; the cart is a two-person lift either way); (b) change to a bolted aluminium frame, about 67.4 kg, which reverses D5 and adds cost; (c) pneumatic tyres, about 71.1 kg, still over. Recommendation: (a), with a note that R7 pull force on grass is then at its limit. **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-002). R6 limit is now 75 kg.
7. **Electronics box ventilation (R8, R9).** Adopt a thermostat-controlled IP54 filter fan (40 to 60 m³/h) with an IP54 exhaust filter, already priced in BOM line 7 and modeled. Recommendation: adopt. **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-002).
8. **Sun shade (R9).** Add a light reflective shade over the battery and electronics enclosures when deployed (about $30 and 1 kg, not yet in the BOM or model), and obtain inverter derating data at 45 °C. Recommendation: add at the next revision. **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-002). Shade added; derating data on hold with supplier selection.
9. **Hinge spacer.** Raise each hinge line by a 20 mm spacer to open the 8 mm wing-to-tyre clearance. Recommendation: adopt; the model's `hinge_z` parameter is left at 470 mm until decided. **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-002). `hinge_z` is now 490 mm.
10. **"Peak sun hours" basis (R3, R4).** Read as daily global horizontal irradiation in kWh/m²/day, as FCL-CAL-001 does. Recommendation: confirm. **Decided by Amish, 2026-09-25: go with recommendation** (FCL-DDR-002).

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

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (FCL-DDR-002 v0.1). The TRL 2 items above are also marked decided (FCL-DDR-001, now v0.2).

### Decisions applied and what changed

| # | Decision | Before | After |
| --- | --- | --- | --- |
| A1 | Raise the budget (option a) | `budget_usd` $1,500; BOM $2,006, 34 % over | `budget_usd` $2,100; BOM $2,051, $49 (2.4 %) contingency |
| A2 | Relax the R6 mass limit (option a) | 70 kg limit; 73.5 kg | 75 kg limit; 75.06 kg after A4 and A5 |
| A3 | Adopt the thermostat IP54 filter fan | Proposed, already in BOM item 7 and the model | Decided; R8 wording names it |
| A4 | Add a reflective sun shade | None; pack about 55 °C, box about 54 °C at 45 °C ambient and 1 kW | BOM item 18 ($30, 1 kg) and model part; pack about 48 °C, box about 53 °C |
| A5 | 20 mm hinge spacer | `hinge_z` 470 mm; wing to tyre 8 mm; stowed height 1,170 mm; BOM item 14 $45 | `hinge_z` 490 mm; 28 mm; 1,190 mm; $60 with two aluminium angles (0.53 kg) |
| A6 | "Peak sun hours" is GHI in kWh/m²/day | Assumption, proposed | R3 and R4 restated in kWh/m²/day GHI |
| A7 | Heavy parts low and over the axle | Proposed (O4) | Kept as a layout rule |

Other knock-on numbers (FCL-CAL-001 v0.2): CG height 557 to 564 mm; handle force 14 to 50 N to 14 to 52 N; tip angle 32.9 to 32.6°; pull on grass 144 to 147 N; step pull 136 to 138 N. Energy, electrical, wind lift, deploy and noise figures are unchanged.

Files changed: `project.yaml`, `README.md`, `bom/bom.csv`, `bom/bom-notes.md`, `cad/src/model.py` (and all STEP and STL files), `cad/src/sheets.py` and `cad/drawings/FCL-DWG-002.*` (Rev P2), `cad/src/concept_media.py` and all of `media/`, `docs/04-calcs/sizing.py` and FCL-CAL-001 v0.2, FCL-PRB-001 v0.4, FCL-PRC-001 v0.4, FCL-REQ-001 v0.4, FCL-DDR-001 v0.2, FCL-DDR-002 v0.1. PDFs in `docs/pdf/` were rebuilt, and the older-version PDFs removed.

### Requirement status (FCL-CAL-001 v0.2)

7 met, 1 not met, 2 at risk, 2 not verifiable at TRL 3 (before: 6 met, 2 not met).

| ID | Status | Value against target |
| --- | --- | --- |
| R6 | **Not met** | 75.06 kg against 75 kg (0.06 kg over, within estimate accuracy); handle force 14 to 52 N; pack 12 kg |
| R7 | At risk | Pull 147 N on grass against 150 N; step at 138 N; clearance 193 mm; tip 32.6° |
| R9 | At risk | Box 53 °C at 45 °C ambient with fan and shade; pack about 48 °C under the shade, so charging stops above about 42 °C ambient; inverter derating data not yet obtained |
| R8 | Not verifiable at TRL 3 | IP54 box with decided filter fan; IP65 case |
| R11 | Not verifiable at TRL 3 | About 41 dB(A) at 1 m from assumed levels |
| R1, R2, R3, R4, R5, R10, R12 | Met | As before; R12 now met at $2,051 against $2,100 |

### Proposed, awaiting Amish

Still open, no recommendation was made:

1. Whether to seek a responder organization to review the deployment sequence and load profile, and which one (O1).
2. How FieldCell relates to PowerBox and SwapCell in the portfolio (O2).
3. Whether to add an AC charger or a vehicle 12 V input for cloudy periods (O3).

New from this session:

4. **Close the 0.06 kg R6 gap.** Options: (a) specify the sun shade at 0.9 kg or less (fabric on a lighter frame), which meets R6 with about 0.04 kg margin; (b) set the limit at 76 kg; (c) accept the figure as within estimate accuracy and settle it by weighing at TRL 4. Recommendation: (a), since it costs nothing and leaves the decided frame and tyres untouched.

### Cross-repo actions

None. No decision in this session needs a change in another repo (D6 on SwapCell was settled in FCL-DDR-001).

### Safety concerns

Unchanged from the TRL 3 session, with two updates: the cart is now about 75 kg (two-person lift), and the deployed wing to tyre gap is 28 mm instead of 8 mm, which reduces but does not remove the pinch point. The shade must stay in place in hot weather to keep the pack below its charge limit.

### TRL 4

TRL 4 remains on hold by Amish's instruction. `trl: 3` and `trl_target: 3` are unchanged. Supplier quotes, inverter derating data from a chosen supplier, building, weighing and testing are recorded as decided or needed but not started.

### Recommended next step

Decide item 4 above. Otherwise stay at TRL 3 until Amish lifts the TRL 4 hold.

## Session 2026-09-26: sources strengthened

- "Where it could be used", country table: the uncited "Caribbean and Central America" row is replaced by "Caribbean (Puerto Rico and US Virgin Islands)", citing US GAO report GAO-19-296 (2019): after Hurricanes Irma and Maria, restoring power to all customers with structures safe for reconnection took about 11 months in Puerto Rico and about 5 months in the US Virgin Islands. Old source: none. The link was opened on 2026-09-26.
- All other rows, "Concept rationale", "Burning platform" and "What sparked the idea" already rested on primary or reputable secondary sources and are unchanged. No budget change. No controlled doc changed.
