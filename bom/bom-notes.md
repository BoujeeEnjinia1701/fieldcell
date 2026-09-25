# BOM notes

Prices are indicative TRL 3 estimates (2026) by supplier type, not quotes. Item numbers match the exploded view (`media/exploded.png`) and the component table in FCL-PRC-001; item 17 (wiring and hardware) is not modeled.

The 17 lines total about $2,006 (checked by `docs/04-calcs/sizing.py`, FCL-CAL-001 section J), which is $506 (34 %) over the $1,500 `budget_usd` in `project.yaml`. Amish decided on 2026-09-25 to keep $1,500 until supplier quotes are in (FCL-DDR-001, D7); a revised budget or a cost-down is proposed in `docs/REVIEW.md` and awaits Amish. The total has no allowance for tools, spares, shipping or contingency.

Changes from the TRL 2 BOM ($1,462):

- PV wings (item 13) are now 200 W semi-flexible modules on a light aluminium frame, about $230 each, instead of $135 rigid panels. A rigid glass 200 W panel weighs about 11 to 12 kg and would push the cart about 10 kg further over its mass limit.
- Electronics enclosure (item 7) now includes an IP54 filter fan and exhaust filter, which the thermal estimate needs (proposed, awaiting Amish).
- Fusing and monitoring (item 12), DC outlets (item 10), inverter (item 9), MPPT (item 8), battery case (item 5) and wiring (item 17) were re-estimated upward to typical prices for parts of adequate quality, for example an inverter with a low no-load draw.
- The frame tube wall is 1.5 mm, and each outrigger now includes its stake.

The pack (item 6), the PV wings (item 13) and the inverter (item 9) are about half the total, so their quotes decide the budget. Make items are priced at material cost only. FieldCell does not use a shared SwapCell pack, so the portfolio rule that SwapCell packs are priced once in the SwapCell repo does not change this BOM.
