"""FieldCell concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the cart (handle toward +X), Y across the cart, Z up, ground at Z = 0.
The cart is shown parked and deployed: stand legs down, both PV wings folded out
on their hinges and resting on outrigger legs. For travel the wings fold up to
form the sides of the cart.
"""
import sys
from math import radians, sin, cos, tan, atan, degrees
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector, Compound
from concept import Part, render_all

# ---------------------------------------------------------------- dimensions (mm)
DECK_L, DECK_W = 1200.0, 600.0         # frame footprint
RAIL = 40.0                            # square tube size
DECK_Z = 460.0                         # deck top when parked level
WHEEL_R, WHEEL_W = 203.0, 90.0         # 16 in pneumatic or flat-free wheel
WHEEL_Y = 360.0                        # wheel center, track 720 mm
AXLE_X = 30.0                          # axle slightly toward the handle end
PV_L, PV_W, PV_T = 1400.0, 700.0, 35.0  # one 200 W lightweight module, about 0.98 m2
HINGE_Y, HINGE_Z = 330.0, 470.0        # hinge line along each side rail
TILT = 15.0                            # deployed wing tilt, degrees below horizontal
GRIP = (1270.0, 900.0)                 # handle grip (x, z) when parked level


def tube(p1, p2, r):
    v = Vector(*p2) - Vector(*p1)
    return Solid.make_cylinder(r, v.length, Plane(origin=p1, z_dir=v))


def shell(lx, ly, lz, t=6.0, open_top=False):
    outer = Box(lx, ly, lz)
    inner = Pos(0, 0, t if open_top else 0) * Box(lx - 2 * t, ly - 2 * t, lz - (t if open_top else 2 * t))
    return outer - inner


def comp(*shapes):
    return Compound(children=list(shapes))


# ---------------------------------------------------------------- 1 cart frame
rz = DECK_Z - RAIL / 2
rails = [Pos(0, s * (DECK_W / 2 - RAIL / 2), rz) * Box(DECK_L, RAIL, RAIL) for s in (-1, 1)]
cross = [Pos(x, 0, rz) * Box(RAIL, DECK_W - 2 * RAIL, RAIL) for x in (-DECK_L / 2 + RAIL / 2, 0, DECK_L / 2 - RAIL / 2)]
deck = Pos(0, 0, DECK_Z - 2.5) * Box(DECK_L - 2 * RAIL, DECK_W - 2 * RAIL, 5)
brackets = [Pos(AXLE_X, s * (DECK_W / 2 - 10), (WHEEL_R + DECK_Z - RAIL) / 2) * Box(70, 12, DECK_Z - RAIL - WHEEL_R + 20)
            for s in (-1, 1)]
axle = tube((AXLE_X, -WHEEL_Y, WHEEL_R), (AXLE_X, WHEEL_Y, WHEEL_R), 12)
frame = comp(*rails, *cross, deck, *brackets, axle)

# ---------------------------------------------------------------- 2 wheels
def wheel(y):
    tyre = Pos(AXLE_X, y, WHEEL_R) * Rot(90, 0, 0) * (Cylinder(WHEEL_R, WHEEL_W) - Cylinder(WHEEL_R - 55, WHEEL_W + 2))
    hub = Pos(AXLE_X, y, WHEEL_R) * Rot(90, 0, 0) * Cylinder(WHEEL_R - 55, WHEEL_W - 30)
    return tyre + hub

# ---------------------------------------------------------------- 3 handle
hy = DECK_W / 2 - RAIL / 2
handle = comp(tube((DECK_L / 2 - 20, -hy, rz), (GRIP[0], -hy + 40, GRIP[1]), 14),
              tube((DECK_L / 2 - 20, hy, rz), (GRIP[0], hy - 40, GRIP[1]), 14),
              tube((GRIP[0], -hy - 20, GRIP[1]), (GRIP[0], hy + 20, GRIP[1]), 16))

# ---------------------------------------------------------------- 4 stand legs (front and rear, fold up for travel)
def legs_at(x):
    legs = []
    for s in (-1, 1):
        legs.append(tube((x, s * 260, 25), (x, s * 260, DECK_Z - RAIL), 13))
        legs.append(Pos(x, s * 260, 12.5) * Box(90, 70, 25))
    return comp(*legs)

# ---------------------------------------------------------------- 5, 6 battery enclosure and LiFePO4 pack
BATT_BOX = (420.0, 360.0, 300.0)
batt_box = Pos(0, 0, DECK_Z + BATT_BOX[2] / 2) * shell(*BATT_BOX)
battery = Pos(0, 0, DECK_Z + 6 + 110) * Box(330, 175, 220)       # 25.6 V 50 Ah pack, about 12 kg

# ---------------------------------------------------------------- 7 to 12 electronics box and contents
EBX = (320.0, 460.0, 300.0)
ex0 = DECK_L / 2 - 20 - EBX[0] / 2        # box center x, face toward the handle
ebox = Pos(ex0, 0, DECK_Z + EBX[2] / 2) * shell(*EBX)
mppt = Pos(ex0 - 40, 140, DECK_Z + 6 + 35) * Box(150, 140, 70)
inverter = Pos(ex0 - 10, -95, DECK_Z + 6 + 55) * Box(270, 210, 110)
face = ex0 + EBX[0] / 2
dc_panel = Pos(face + 6, 115, DECK_Z + 170) * Box(12, 170, 180)
ac_outlet = Pos(face + 6, -120, DECK_Z + 180) * Box(12, 80, 130)
fusing = Pos(ex0 - 40, 140, DECK_Z + 6 + 70 + 50) * Box(150, 150, 100)

# ---------------------------------------------------------------- 13 PV wings, 14 hinges, 15 outrigger legs
def wing(s):
    panel = Pos(0, s * PV_W / 2, -PV_T / 2) * Box(PV_L, PV_W, PV_T)
    return Pos(0, s * HINGE_Y, HINGE_Z) * Rot(-s * TILT, 0, 0) * panel
hinges = comp(*[tube((-PV_L / 2 + 50, s * HINGE_Y, HINGE_Z - 8), (PV_L / 2 - 50, s * HINGE_Y, HINGE_Z - 8), 9)
                for s in (-1, 1)])
out_y = HINGE_Y + (PV_W - 30) * cos(radians(TILT))
out_top = HINGE_Z - (PV_W - 30) * sin(radians(TILT)) - PV_T / cos(radians(TILT))
def outriggers_at(s):
    xs = (-PV_L / 2 + 80, PV_L / 2 - 80)
    return comp(*[tube((x, s * out_y, 20), (x, s * out_y, out_top), 12) for x in xs],
                *[Pos(x, s * out_y, 10) * Box(80, 80, 20) for x in xs])

# ---------------------------------------------------------------- 16 accessory and cable bin
BIN = (320.0, 460.0, 240.0)
bin_x = -DECK_L / 2 + 20 + BIN[0] / 2
acc_bin = Pos(bin_x, 0, DECK_Z + BIN[2] / 2) * shell(*BIN, open_top=True)

FRONT_X, REAR_X = -DECK_L / 2 + 40, DECK_L / 2 - 40
parts = [
    Part("Cart frame and axle", frame, "#4B5563", 1),
    Part("Wheels, 16 in (2)", wheel(-WHEEL_Y), "#1F2937", 2, (0, -260, -200)),
    Part("Wheel, far side", wheel(WHEEL_Y), "#1F2937", None, (0, 260, -200)),
    Part("Handle", handle, "#6B7280", 3, (320, 0, 120)),
    Part("Stand legs (4)", legs_at(FRONT_X), "#9CA3AF", 4, (-200, 0, -420)),
    Part("Stand legs, handle end", legs_at(REAR_X), "#9CA3AF", None, (200, 0, -420)),
    Part("Battery enclosure", batt_box, "#D1D5DB", 5, (0, 0, 380)),
    Part("LiFePO4 pack, 25.6 V 50 Ah", battery, "#C2410C", 6, (0, 0, 900)),
    Part("Electronics enclosure", ebox, "#E5E7EB", 7, (140, 0, 380)),
    Part("MPPT charge controller", mppt, "#0F766E", 8, (140, 0, 820)),
    Part("Inverter, 1 kW", inverter, "#0E7490", 9, (140, 0, 820)),
    Part("DC outlet panel", dc_panel, "#D4A017", 10, (420, 0, 380)),
    Part("AC outlet with GFCI", ac_outlet, "#F59E0B", 11, (420, 0, 380)),
    Part("Fusing and disconnect", fusing, "#B91C1C", 12, (140, 0, 1020)),
    Part("PV panels, 200 W (2)", wing(-1), "#1E3A5F", 13, (0, -700, 250)),
    Part("PV panel, far side", wing(1), "#1E3A5F", None, (0, 700, 250)),
    Part("Panel hinges and latches", hinges, "#94A3B8", 14, (0, 0, 260)),
    Part("Outrigger legs (4)", outriggers_at(-1), "#64748B", 15, (0, -700, -60)),
    Part("Outrigger legs, far side", outriggers_at(1), "#64748B", None, (0, 700, -60)),
    Part("Accessory and cable bin", acc_bin, "#65A30D", 16, (-300, 0, 200)),
]

# Hero only: the same cart stowed for travel (wings up as the cart sides), parked behind the deployed one.
def stowed_wing(s):
    return Pos(0, s * (HINGE_Y + PV_T / 2), HINGE_Z + PV_W / 2) * Box(PV_L, PV_T, PV_W)
STOW = Pos(-1700, 2300, 0)
context = [Part("Stowed cart, " + p.name, STOW * p.shape, p.color) for p in parts
           if not p.name.startswith(("PV panel", "Outrigger legs"))]
context += [Part("Stowed cart, PV wing", STOW * stowed_wing(s), "#1E3A5F") for s in (-1, 1)]

# ---------------------------------------------------------------- first-order numbers (estimates)
# Mass budget: (name, kg, x, z) with x, z of each item's center of mass, cart parked level, wings stowed.
MASS = [
    ("Frame, deck and axle", 11.0, 0, 440), ("Wheels (2)", 6.0, AXLE_X, WHEEL_R), ("Handle", 3.0, 950, 700),
    ("Stand legs", 1.5, 0, 230), ("Battery enclosure", 3.0, 0, 610), ("LiFePO4 pack", 12.0, 0, 570),
    ("Electronics box and contents", 11.0, ex0, 590), ("Accessory bin and cables", 4.0, bin_x, 560),
    ("PV panels, stowed (2)", 13.0, 0, HINGE_Z + PV_W / 2), ("Hinges and outriggers", 2.0, 0, 800),
    ("Wiring and hardware", 2.0, 200, 600),
]
M = sum(m for _, m, _, _ in MASS)
cg_x = sum(m * x for _, m, x, _ in MASS) / M
cg_z = sum(m * z for _, m, _, z in MASS) / M
d = cg_x - AXLE_X                                  # CG ahead of the axle, toward the handle
lever = GRIP[0] - AXLE_X
F_handle = M * 9.81 * d / lever
tip_side = degrees(atan(WHEEL_Y / cg_z))
dx5 = (cg_z - WHEEL_R) * sin(radians(5))          # CG shift for a 5 degree pitch in travel
F_lo, F_hi = M * 9.81 * (d - dx5) / lever, M * 9.81 * (d + dx5) / lever

PV_STC, PSH = 400.0, 4.5
PR_ARRAY = 0.90 * 0.95 * 0.98 * 0.90   # temperature, soiling and mismatch, wiring, east-west 15 degree wings
ETA_MPPT, ETA_CHG = 0.96, 0.97
E_sun = PV_STC * PSH / 1000
E_arr = E_sun * PR_ARRAY
E_mppt = E_arr * ETA_MPPT
E_batt = E_mppt * ETA_CHG
# Reference load: DC 480 Wh at 0.95 converter efficiency, AC 417 Wh at 0.90 plus 56 Wh inverter idle
LOAD_OUT = 0.897
LOAD_BATT = 0.480 / 0.95 + 0.417 / 0.90 + 0.056
ETA_OUT = LOAD_OUT / LOAD_BATT
E_out = E_batt * ETA_OUT

if __name__ == "__main__":
    print(f"mass {M:.1f} kg, CG x {cg_x:.0f} mm (axle {AXLE_X:.0f}, offset {d:.0f} mm toward handle), CG z {cg_z:.0f} mm")
    print(f"handle force {F_handle:.0f} N level, {F_lo:.0f} to {F_hi:.0f} N at +/-5 deg; side tip {tip_side:.0f} deg")
    print(f"PR {PR_ARRAY:.3f}; sun {E_sun:.2f}, array {E_arr:.2f}, mppt {E_mppt:.2f}, battery {E_batt:.2f}, "
          f"outlets {E_out:.2f} kWh/day; load from battery {LOAD_BATT:.3f}, eta_out {ETA_OUT:.3f}")
    for psh in (4.0, 5.0):
        print(f"  PSH {psh}: stored {PV_STC * psh / 1000 * PR_ARRAY * ETA_MPPT * ETA_CHG:.2f} kWh/day")
    print(f"wingspan {2 * (HINGE_Y + PV_W * cos(radians(TILT))):.0f} mm, outer edge height {HINGE_Z - PV_W * sin(radians(TILT)):.0f} mm")

    render_all(
        parts, context=context, project="FieldCell", title="Solar power cart concept", dwg_no="FCL-DWG-001",
        key_figures=["Shown deployed; wings fold up to form the cart sides",
                     "2 x 200 W PV, 1.28 kWh LiFePO4 (25.6 V 50 Ah)",
                     "1 kW AC inverter, DC outlets (USB-C, 12 V)",
                     f"About {E_batt:.1f} kWh/day stored at 4.5 sun hours (estimate)",
                     f"About {M:.0f} kg, CG {d:.0f} mm from axle (estimate)",
                     "Deploy in about 6 min, one person (estimate)"],
        flow={"title": "daily energy flow at 4.5 peak sun hours (all values estimates)", "unit": "kWh/day",
              "stages": [("Sun on 400 W array", round(E_sun, 2)), ("Array DC output", round(E_arr, 2)),
                         ("MPPT output", round(E_mppt, 2)), ("Stored in battery", round(E_batt, 2)),
                         ("Outlets, AC and DC", round(E_out, 2))],
              "losses": [(0, "Heat, dirt, tilt, wiring", round(E_sun - E_arr, 2)),
                         (1, "MPPT", round(E_arr - E_mppt, 2)),
                         (2, "Charge", round(E_mppt - E_batt, 2)),
                         (3, "Inverter, DC-DC, idle", round(E_batt - E_out, 2))]},
    )
