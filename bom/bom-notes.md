# BOM notes

Prices are indicative TRL 3 estimates (2026) by supplier type, not quotes. Item numbers match the exploded view (`media/exploded.png`) and the component table in FCL-PRC-001; item 17 (wiring and hardware) is not modeled. Item 18 (sun shade) was added on 2026-09-25.

The 18 lines total about $2,051 (checked by `docs/04-calcs/sizing.py`, FCL-CAL-001 section J), against the $2,100 `budget_usd` in `project.yaml`. Amish raised the budget from $1,500 to $2,100 on 2026-09-25 (FCL-DDR-002), which leaves about $49 (2.4 %) of contingency and no allowance for tools, spares or shipping. Supplier quotes for the pack, PV wings and inverter will confirm it.

Changes from Amish's decisions of 2026-09-25 (FCL-DDR-002), $2,006 to $2,051:

- Item 18, sun shade, added ($30).
- Item 14 now includes two 20 mm aluminium angle hinge spacers ($45 to $60).
- Item 7, the thermostat filter fan and exhaust filter, is now decided rather than proposed.

Changes from the TRL 2 BOM ($1,462) to the first TRL 3 BOM ($2,006):

- PV wings (item 13) are now 200 W semi-flexible modules on a light aluminium frame, about $230 each, instead of $135 rigid panels. A rigid glass 200 W panel weighs about 11 to 12 kg and would push the cart about 10 kg further over its mass limit.
- Electronics enclosure (item 7) now includes an IP54 filter fan and exhaust filter, which the thermal estimate needs.
- Fusing and monitoring (item 12), DC outlets (item 10), inverter (item 9), MPPT (item 8), battery case (item 5) and wiring (item 17) were re-estimated upward to typical prices for parts of adequate quality, for example an inverter with a low no-load draw.
- The frame tube wall is 1.5 mm, and each outrigger now includes its stake.

The pack (item 6), the PV wings (item 13) and the inverter (item 9) are about half the total, so their quotes decide the budget. Make items are priced at material cost only. FieldCell does not use a shared SwapCell pack, so the portfolio rule that SwapCell packs are priced once in the SwapCell repo does not change this BOM.
