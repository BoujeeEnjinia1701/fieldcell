"""FieldCell concept media (TRL 3), generated from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Massing-plus model: main dimensions and interfaces; not for fabrication.

Axes: X along the cart (handle toward +X), Y across the cart, Z up, ground at Z = 0.
The cart is shown parked and deployed: stand legs down, both PV wings folded out
on their hinges and resting on outrigger legs. For travel the wings fold up to
form the sides of the cart (shown behind in the hero). Numbers on the media come
from docs/04-calcs/sizing.py (FCL-CAL-001).
"""
import sys
from pathlib import Path
sys.path[:0] = [str(Path(__file__).resolve().parents[2] / ".kit"), str(Path(__file__).resolve().parent),
                str(Path(__file__).resolve().parents[2] / "docs" / "04-calcs")]
from build123d import Pos
from concept import Part, render_all
from model import PARAMS as P, build_parts

COLORS = {"frame": "#4B5563", "wheel_l": "#1F2937", "wheel_r": "#1F2937", "handle": "#6B7280", "legs_f": "#9CA3AF",
          "legs_r": "#9CA3AF", "batt_box": "#D1D5DB", "pack": "#C2410C", "ebox": "#E5E7EB", "mppt": "#0F766E",
          "inverter": "#0E7490", "dc_panel": "#D4A017", "ac_outlet": "#F59E0B", "fusing": "#B91C1C",
          "wing_l": "#1E3A5F", "wing_r": "#1E3A5F", "hinges": "#94A3B8", "out_l": "#64748B", "out_r": "#64748B",
          "bin": "#65A30D"}
EXPLODE = {"wheel_l": (0, -260, -200), "wheel_r": (0, 260, -200), "handle": (320, 0, 120), "legs_f": (-200, 0, -420),
           "legs_r": (200, 0, -420), "batt_box": (0, 0, 380), "pack": (0, 0, 900), "ebox": (140, 0, 380),
           "mppt": (140, 0, 820), "inverter": (140, 0, 820), "dc_panel": (420, 0, 380), "ac_outlet": (420, 0, 380),
           "fusing": (140, 0, 1020), "wing_l": (0, -700, 250), "wing_r": (0, 700, 250), "hinges": (0, 0, 260),
           "out_l": (0, -700, -60), "out_r": (0, 700, -60), "bin": (-300, 0, 200)}
parts = [Part(name, shape, COLORS[k], bom, EXPLODE.get(k, (0, 0, 0))) for k, name, shape, bom in build_parts(deployed=True)]

# Hero only: the same cart stowed for travel (wings up as the cart sides), parked behind the deployed one.
STOW = Pos(-1700, 2300, 0)
context = [Part("Stowed cart, " + name, STOW * shape, COLORS[k]) for k, name, shape, _ in build_parts(deployed=False)]

# ---------------------------------------------------------------- numbers from FCL-CAL-001 (estimates)
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import sizing as C

GHI = 4.5
E_sun = GHI * C.P_STC / 1000
E_arr = E_sun * C.PR
E_mppt = E_arr * C.ETA_MPPT
E_batt = E_mppt * C.ETA_CHG
E_out = E_batt * C.LOAD_OUT / C.LOAD_BATT

if __name__ == "__main__":
    print(f"mass {C.M:.1f} kg, CG {C.d_cg:.0f} mm toward handle; sun {E_sun:.2f}, array {E_arr:.2f}, mppt {E_mppt:.2f}, "
          f"battery {E_batt:.2f}, outlets {E_out:.2f} kWh/day")
    render_all(
        parts, context=context, project="FieldCell", title="Solar power cart concept", dwg_no="FCL-DWG-001",
        key_figures=["Shown deployed; wings fold up to form the cart sides",
                     "2 x 200 W PV, 1.28 kWh LiFePO4 (25.6 V 50 Ah)",
                     "1 kW AC inverter, DC outlets (USB-C, 12 V)",
                     f"About {E_batt:.2f} kWh/day stored at {GHI} kWh/m2/day (estimate)",
                     f"About {C.M:.1f} kg, CG {C.d_cg:.0f} mm from axle (estimate)",
                     "Deploy in about 6 min, one person (estimate)"],
        flow={"title": f"daily energy flow at {GHI} kWh/m2/day global horizontal (all values estimates, FCL-CAL-001)",
              "unit": "kWh/day",
              "stages": [("Sun on 400 W array", round(E_sun, 2)), ("Array DC output", round(E_arr, 2)),
                         ("MPPT output", round(E_mppt, 2)), ("Stored in battery", round(E_batt, 2)),
                         ("Outlets, AC and DC", round(E_out, 2))],
              "losses": [(0, "Heat, dirt, tilt, wiring", round(E_sun - E_arr, 2)),
                         (1, "MPPT", round(E_arr - E_mppt, 2)),
                         (2, "Charge", round(E_mppt - E_batt, 2)),
                         (3, "Inverter, DC-DC, idle", round(E_batt - E_out, 2))]},
    )
