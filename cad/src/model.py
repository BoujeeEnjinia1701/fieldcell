"""FieldCell parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    fieldcell-deployed.step / .stl   whole cart, parked, wings folded out (as in the media)
    fieldcell-stowed.step / .stl     whole cart, wings up as the cart sides (travel)
    frame.step, pv-wing.step, battery-enclosure.step, electronics-enclosure.step (and .stl)

Rev for DDR-002 (2026-09-25): hinge line raised by a 20 mm spacer (hinge_z 470 to 490 mm)
and a reflective sun shade (item 18) added over the battery and electronics enclosures.

Axes: X along the cart (handle toward +X), Y across the cart, Z up, ground at Z = 0.
Main dimensions and interfaces only (frame, axle and wheel track, hinge line, enclosure
envelopes, outlet face, outrigger feet). Not fabrication detail; not for fabrication.
The same PARAMS feed docs/04-calcs/sizing.py (FCL-CAL-001).
"""
from math import radians, sin, cos
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # cart frame (welded steel square tube, decided 2026-09-25)
    "deck_l": 1200.0, "deck_w": 600.0,       # frame footprint
    "rail": 40.0, "rail_wall": 1.5,          # 40 x 40 x 1.5 mm square tube
    "deck_z": 460.0,                         # deck top when parked level on the stand legs
    "deck_t": 5.0,                           # expanded-metal deck (massing thickness)
    # wheels and axle
    "wheel_r": 203.0, "wheel_w": 90.0,       # 16 in (406 mm) flat-free tyre
    "wheel_y": 360.0,                        # wheel center from cart center line (track 720 mm)
    "axle_x": 30.0, "axle_d": 20.0,          # axle position from deck center, solid axle diameter
    "bracket_y": 290.0,                      # axle bracket plane from center line
    # handle (detachable)
    "grip_x": 1270.0, "grip_z": 900.0, "handle_d": 28.0,
    # stand legs and outriggers
    "leg_d": 25.0, "leg_y": 260.0,
    "out_d": 25.0,
    # PV wings (2 x 200 W semi-flexible module on an aluminium backing frame)
    "pv_l": 1400.0, "pv_w": 700.0, "pv_t": 35.0,
    "hinge_y": 330.0, "hinge_z": 490.0,      # continuous hinge line, on a 20 mm spacer over each side rail (DDR-002)
    "spacer": 20.0,                          # hinge spacer height (20 x 20 x 2 mm aluminium angle, DDR-002)
    "tilt": 15.0,                            # deployed wing tilt below horizontal
    # enclosures and main parts (outer envelopes)
    "batt_box": (420.0, 360.0, 300.0),       # IP65 battery case, centered over the deck center
    "pack": (330.0, 175.0, 220.0),           # 25.6 V 50 Ah LiFePO4 pack
    "ebox": (320.0, 460.0, 300.0),           # IP54 electronics enclosure, outlet face toward the handle
    "bin": (320.0, 460.0, 240.0),            # accessory and cable bin at the far end
    "wall": 6.0,                             # massing wall thickness of enclosures
    "fan": (125.0, 125.0, 20.0),             # IP54 filter fan (intake, +Y wall) and exhaust filter (-Y wall)
    # reflective sun shade over both enclosures (DDR-002): x from, x to, width, gap above the enclosure tops
    "shade": (-230.0, 600.0, 540.0, 50.0), "shade_t": 6.0,
}


def _tube(p1, p2, r):
    from build123d import Solid, Plane, Vector
    v = Vector(*p2) - Vector(*p1)
    return Solid.make_cylinder(r, v.length, Plane(origin=p1, z_dir=v))


def _shell(lx, ly, lz, t, open_top=False):
    from build123d import Box, Pos
    outer = Box(lx, ly, lz)
    inner = Pos(0, 0, t if open_top else 0) * Box(lx - 2 * t, ly - 2 * t, lz - (t if open_top else 2 * t))
    return outer - inner


def _comp(*shapes):
    from build123d import Compound
    return Compound(children=list(shapes))


def derived(P=PARAMS):
    """Positions that other parts and the calc note depend on."""
    d = {}
    d["rail_z"] = P["deck_z"] - P["rail"] / 2
    d["ebox_x"] = P["deck_l"] / 2 - 20 - P["ebox"][0] / 2
    d["bin_x"] = -P["deck_l"] / 2 + 20 + P["bin"][0] / 2
    t = radians(P["tilt"])
    d["out_y"] = P["hinge_y"] + (P["pv_w"] - 30) * cos(t)
    d["out_top"] = P["hinge_z"] - (P["pv_w"] - 30) * sin(t) - P["pv_t"] / cos(t)
    d["span"] = 2 * (P["hinge_y"] + P["pv_w"] * cos(t))
    d["edge_z"] = P["hinge_z"] - P["pv_w"] * sin(t)
    # clearance between the deployed wing underside and the tyre top, at the tyre outer edge
    y_out = P["wheel_y"] + P["wheel_w"] / 2
    s = (y_out - P["hinge_y"]) / cos(t)
    d["wing_tyre_gap"] = (P["hinge_z"] - s * sin(t) - P["pv_t"] / cos(t)) - 2 * P["wheel_r"]
    return d


def build_parts(P=PARAMS, deployed=True):
    """Return [(key, name, shape, bom_no)] for the assembly."""
    from build123d import Box, Cylinder, Pos, Rot
    D = derived(P)
    L, Wd, R, rz = P["deck_l"], P["deck_w"], P["rail"], D["rail_z"]
    rt = P["rail_wall"]

    def rail_tube(length, axis):
        outer = Box(length, R, R) if axis == "x" else Box(R, length, R)
        inner = Box(length + 2, R - 2 * rt, R - 2 * rt) if axis == "x" else Box(R - 2 * rt, length + 2, R - 2 * rt)
        return outer - inner

    # 1 frame, deck, axle brackets, axle
    rails = [Pos(0, s * (Wd / 2 - R / 2), rz) * rail_tube(L, "x") for s in (-1, 1)]
    cross = [Pos(x, 0, rz) * rail_tube(Wd - 2 * R, "y") for x in (-L / 2 + R / 2, 0, L / 2 - R / 2)]
    deck = Pos(0, 0, P["deck_z"] - P["deck_t"] / 2) * Box(L - 2 * R, Wd - 2 * R, P["deck_t"])
    bh = P["deck_z"] - R - P["wheel_r"] + 20
    brackets = [Pos(P["axle_x"], s * P["bracket_y"], P["wheel_r"] + bh / 2 - 10) * Box(70, 6, bh) for s in (-1, 1)]
    axle = _tube((P["axle_x"], -P["wheel_y"], P["wheel_r"]), (P["axle_x"], P["wheel_y"], P["wheel_r"]), P["axle_d"] / 2)
    frame = _comp(*rails, *cross, deck, *brackets, axle)

    # 2 wheels
    def wheel(y):
        c = Pos(P["axle_x"], y, P["wheel_r"]) * Rot(90, 0, 0)
        tyre = c * (Cylinder(P["wheel_r"], P["wheel_w"]) - Cylinder(P["wheel_r"] - 55, P["wheel_w"] + 2))
        hub = c * Cylinder(P["wheel_r"] - 55, P["wheel_w"] - 30)
        return tyre + hub

    # 3 handle
    hy = Wd / 2 - R / 2
    gx, gz, hr = P["grip_x"], P["grip_z"], P["handle_d"] / 2
    handle = _comp(_tube((L / 2 - 20, -hy, rz), (gx, -hy + 40, gz), hr),
                   _tube((L / 2 - 20, hy, rz), (gx, hy - 40, gz), hr),
                   _tube((gx, -hy - 20, gz), (gx, hy + 20, gz), hr + 2))

    # 4 stand legs
    def legs_at(x):
        out = []
        for s in (-1, 1):
            out.append(_tube((x, s * P["leg_y"], 25), (x, s * P["leg_y"], P["deck_z"] - R), P["leg_d"] / 2))
            out.append(Pos(x, s * P["leg_y"], 12.5) * Box(90, 70, 25))
        return _comp(*out)

    # 5, 6 battery enclosure and pack
    bb, pk, t = P["batt_box"], P["pack"], P["wall"]
    batt_box = Pos(0, 0, P["deck_z"] + bb[2] / 2) * _shell(*bb, t)
    pack = Pos(0, 0, P["deck_z"] + t + pk[2] / 2) * Box(*pk)

    # 7 to 12 electronics enclosure and contents
    eb, ex = P["ebox"], D["ebox_x"]
    ebox = Pos(ex, 0, P["deck_z"] + eb[2] / 2) * _shell(*eb, t)
    fx, fy, fz = P["fan"]
    fan_in = Pos(ex - 40, eb[1] / 2 + fz / 2, P["deck_z"] + 90) * Box(fx, fz, fy)
    fan_out = Pos(ex + 40, -eb[1] / 2 - fz / 2, P["deck_z"] + eb[2] - 90) * Box(fx, fz, fy)
    ebox = _comp(ebox, fan_in, fan_out)
    z0 = P["deck_z"] + t
    mppt = Pos(ex - 40, 140, z0 + 35) * Box(150, 140, 70)
    inverter = Pos(ex - 10, -95, z0 + 55) * Box(270, 210, 110)
    face = ex + eb[0] / 2
    dc_panel = Pos(face + 6, 115, P["deck_z"] + 170) * Box(12, 170, 180)
    ac_outlet = Pos(face + 6, -120, P["deck_z"] + 180) * Box(12, 80, 130)
    fusing = Pos(ex - 40, 140, z0 + 70 + 50) * Box(150, 150, 100)

    # 13 PV wings, 14 hinges, 15 outriggers
    pl, pw, pt, hyy, hz, tilt = P["pv_l"], P["pv_w"], P["pv_t"], P["hinge_y"], P["hinge_z"], P["tilt"]

    def wing(s):
        if deployed:
            panel = Pos(0, s * pw / 2, -pt / 2) * Box(pl, pw, pt)
            return Pos(0, s * hyy, hz) * Rot(-s * tilt, 0, 0) * panel
        return Pos(0, s * (hyy + pt / 2), hz + pw / 2) * Box(pl, pt, pw)

    sp = P["spacer"]
    hinges = _comp(*[_tube((-pl / 2 + 50, s * hyy, hz - 8), (pl / 2 - 50, s * hyy, hz - 8), 9) for s in (-1, 1)],
                   *[Pos(0, s * hyy, hz - 17 - sp / 2) * Box(pl - 100, 20, sp) for s in (-1, 1)])

    def outriggers_at(s):
        xs = (-pl / 2 + 80, pl / 2 - 80)
        r = P["out_d"] / 2
        if deployed:
            return _comp(*[_tube((x, s * D["out_y"], 20), (x, s * D["out_y"], D["out_top"]), r) for x in xs],
                         *[Pos(x, s * D["out_y"], 10) * Box(80, 80, 20) for x in xs])
        # stowed: legs folded flat against the outside face of the upright wing
        yy = s * (hyy + pt + r + 2)
        return _comp(*[_tube((x, yy, hz + 60), (x, yy, hz + pw - 60), r) for x in xs])

    # 16 accessory bin
    bn = P["bin"]
    acc_bin = Pos(D["bin_x"], 0, P["deck_z"] + bn[2] / 2) * _shell(*bn, t, open_top=True)

    # 18 sun shade: reflective panel on four short posts over the battery and electronics enclosures
    x0, x1, sw, gap = P["shade"]
    top = P["deck_z"] + max(bb[2], eb[2])
    sz = top + gap + P["shade_t"] / 2
    posts = [_tube((x, s * (sw / 2 - 30), top), (x, s * (sw / 2 - 30), sz), 6)
             for x in (x0 + 30, x1 - 30) for s in (-1, 1)]
    shade = _comp(Pos((x0 + x1) / 2, 0, sz) * Box(x1 - x0, sw, P["shade_t"]), *posts)

    FX, RX = -L / 2 + 40, L / 2 - 40
    return [
        ("frame", "Cart frame and axle", frame, 1),
        ("wheel_l", "Wheels, 16 in (2)", wheel(-P["wheel_y"]), 2),
        ("wheel_r", "Wheel, far side", wheel(P["wheel_y"]), None),
        ("handle", "Handle", handle, 3),
        ("legs_f", "Stand legs (4)", legs_at(FX), 4),
        ("legs_r", "Stand legs, handle end", legs_at(RX), None),
        ("batt_box", "Battery enclosure", batt_box, 5),
        ("pack", "LiFePO4 pack, 25.6 V 50 Ah", pack, 6),
        ("ebox", "Electronics enclosure with filter fan", ebox, 7),
        ("mppt", "MPPT charge controller", mppt, 8),
        ("inverter", "Inverter, 1 kW", inverter, 9),
        ("dc_panel", "DC outlet panel", dc_panel, 10),
        ("ac_outlet", "AC outlet with GFCI", ac_outlet, 11),
        ("fusing", "Fusing and disconnect", fusing, 12),
        ("wing_l", "PV panels, 200 W (2)", wing(-1), 13),
        ("wing_r", "PV panel, far side", wing(1), None),
        ("hinges", "Panel hinges and latches", hinges, 14),
        ("out_l", "Outrigger legs (4)", outriggers_at(-1), 15),
        ("out_r", "Outrigger legs, far side", outriggers_at(1), None),
        ("bin", "Accessory and cable bin", acc_bin, 16),
        ("shade", "Sun shade", shade, 18),
    ]


def build(P=PARAMS, deployed=True):
    """Whole assembly as one Compound."""
    return _comp(*[s for _, _, s, _ in build_parts(P, deployed)])


if __name__ == "__main__":
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    D = derived()
    for name, dep in (("fieldcell-deployed", True), ("fieldcell-stowed", False)):
        asm = build(deployed=dep)
        export_step(asm, str(out / "step" / f"{name}.step"))
        export_stl(asm, str(out / "stl" / f"{name}.stl"))
        bb = asm.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm (L x W x H)")
    parts = {k: s for k, _, s, _ in build_parts()}
    for fname, key in (("frame", "frame"), ("pv-wing", "wing_l"), ("battery-enclosure", "batt_box"),
                       ("electronics-enclosure", "ebox")):
        export_step(parts[key], str(out / "step" / f"{fname}.step"))
        export_stl(parts[key], str(out / "stl" / f"{fname}.stl"))
    print(f"wingspan {D['span']:.0f} mm, wing outer edge {D['edge_z']:.0f} mm above ground, "
          f"wing to tyre clearance {D['wing_tyre_gap']:.0f} mm")
    print("exported STEP and STL to cad/step and cad/stl")
