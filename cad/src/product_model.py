"""FieldCell product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of the cart parked and deployed: graphite powder-coated
frame with tube end plugs and an expanded-metal deck, flat-free tyres with tread on dished steel rims,
a T-handle with a foam grip and quick-release pins, stand legs with rubber feet, two PV wings (cell
grid, busbars, white backsheet, aluminium backing frame, teal corner guards, junction boxes) on
knuckled continuous hinges, staked outrigger feet, two tie bars with over-centre latches holding the stowed wings,
a reflective fabric sun shade on a flat-bar frame lifting off on four bolted uprights,
an IP65 battery case with latches, lid parting line, carry handle, pressure vent and gland plate, and
an IP54 electronics box with a clear side window onto the inverter, MPPT and breakers, a louvered
exhaust filter and intake fan, and the outlet face toward the handle: DC panel (two USB-C PD ports
with lit rings, two 12 V sockets with rubber caps, lit battery monitor), GFCI duplex under a clear
in-use cover, battery isolator knob and an inverter rocker with a lit indicator. The accessory bin
carries a coiled cord under a teal webbing strap. Context is a compact patch of ground and the
shared clay mannequin standing beside the cart for scale.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, derived() and build_parts() in model.py.
Axes as model.py: X along the cart (handle toward +X), Y across the cart (front is -Y), Z up,
ground at Z = 0.

Groups: "internal" holds the power system carried between the wings (battery case and pack,
electronics box with its contents, outlet face and the cables between them), so the "detail" view
can frame it closely; "shell" holds the cart, wings, shade and bin; "context" the ground patch
and the mannequin.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from math import radians, sin, cos
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import (Axis, Box, Compound, Cylinder, Plane, Pos, RectangleRounded, Rot, SlotOverall,
                       Sphere, Torus, extrude, fillet)
from model import PARAMS, derived, build_parts, build_components, _tube

TITLE = "FieldCell: solar power cart with fold-out panels and a battery bank"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); cart deployed on a "
             "patch of ground with both PV wings folded out on their outrigger legs, handle and outlet "
             "face at right, person standing beside it for scale"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): PV wings, hinges and "
             "outriggers; frame, wheels, handle and stand legs; battery case, lid and LiFePO4 pack; "
             "electronics box with inverter, MPPT, breakers and outlet face; sun shade; accessory bin"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 22, "az": -28,
     "note": "Detail from the front right and above (about 22 deg elevation), power system only: outlet "
             "face at right with USB-C, 12 V and GFCI outlets, isolator and lit monitor; clear side "
             "window onto the inverter and breakers; battery case at left"},
]

# Colours (restrained product palette; kit accent)
C_FRAME = "#3B4452"       # graphite powder coat
C_ACCENT = "#0F766E"
C_ALU = "#B8BEC6"
C_STEEL = "#9AA1AA"
C_BLACK = "#1F2329"
C_RUBBER = "#2B2F36"
C_CASE = "#343A42"        # battery case (charcoal polypropylene)
C_EBOX = "#D9DCE0"        # electronics box (light grey polycarbonate)
C_EBOX_LID = "#C6CBD1"
C_PANEL = "#2B2F36"
C_OFFWHITE = "#EDEBE6"
C_WINDOW = "#DCEBF5"
C_CELL = "#1B2536"
C_BACKSHEET = "#EEF0F2"
C_BUSBAR = "#C8CDD3"
C_SHADE = "#D6DADF"
C_BIN = "#56606C"
C_CORD = "#B7791F"
C_PACK = "#3E4A5A"
C_MPPT = "#2F4A6B"
C_LABEL = "#F4F4F2"
C_RED = "#B91C1C"
C_LIT_TEAL = "#5EEAD4"
C_LIT_GREEN = "#22C55E"
C_GROUND = "#C4BFB2"
C_CLAY = "#9CA3AF"

# Appearance-only layout (mm)
PERSON_AT = (1330.0, 640.0)     # mannequin pelvis over this ground point, beside the handle end
PERSON_ROT = 55.0               # turned toward the viewer
GROUND = (-820.0, 1580.0, -1100.0, 1000.0, 40.0)   # x0, x1, y0, y1, thickness (top at Z = 0)


# ---------------------------------------------------------------------------------------- helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _prism(lx, ly, r, z0, h, x=0.0, y=0.0):
    """Rounded-rectangle prism in plan, from z0 up by h."""
    r = max(min(r, min(lx, ly) / 2 - 0.01), 0.01)
    return Pos(x, y, z0) * extrude(RectangleRounded(lx, ly, r), amount=h)


def _yz_plate(x0, y, z, w, h, r, t):
    """Rounded plate in the YZ plane (w along Y, h along Z), from x0 toward +X by t."""
    r = max(min(r, min(w, h) / 2 - 0.01), 0.01)
    return Pos(x0, y, z) * extrude(Plane.YZ * RectangleRounded(w, h, r), amount=t)


def _xz_plate(x, y0, z, w, h, r, t):
    """Rounded plate in the XZ plane (w along X, h along Z), from y0 toward -Y by t."""
    r = max(min(r, min(w, h) / 2 - 0.01), 0.01)
    return Pos(x, y0, z) * extrude(Plane.XZ * RectangleRounded(w, h, r), amount=t)


def _comp(shapes):
    shapes = [s for s in shapes if s is not None]
    return shapes[0] if len(shapes) == 1 else Compound(children=shapes)


def _top_edges(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom_edges(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _vertical_edges(s):
    return s.edges().filter_by(Axis.Z)


# ---------------------------------------------------------------------------------------- cart
def _frame(P, D):
    """Frame rails and cross members as model.py (40 x 40 x 1.5 tube), expanded-metal deck, brackets, axle."""
    L, Wd, R, rz, rt = P["deck_l"], P["deck_w"], P["rail"], D["rail_z"], P["rail_wall"]

    def rail_tube(length, axis):
        outer = Box(length, R, R) if axis == "x" else Box(R, length, R)
        inner = Box(length + 2, R - 2 * rt, R - 2 * rt) if axis == "x" else Box(R - 2 * rt, length + 2, R - 2 * rt)
        return outer - inner

    rails = [Pos(0, s * (Wd / 2 - R / 2), rz) * rail_tube(L, "x") for s in (-1, 1)]
    cross = [Pos(x, 0, rz) * rail_tube(Wd - 2 * R, "y") for x in (-L / 2 + R / 2, 0, L / 2 - R / 2)]
    frame = _comp(rails + cross)

    # expanded-metal deck: plate with a staggered grid of diamond openings
    dl, dw, dt = L - 2 * R, Wd - 2 * R, P["deck_t"]
    deck = _box(0, 0, P["deck_z"] - dt / 2, dl, dw, dt)
    cutters = []
    px, py = 46.0, 26.0
    nx, ny = int(dl // px) - 1, int(dw // py) - 1
    for i in range(nx):
        for j in range(ny):
            x = -dl / 2 + px * (i + 1) + (px / 2 if j % 2 else 0) - px / 2
            y = -dw / 2 + py * (j + 1)
            if abs(x) > dl / 2 - 22 or abs(y) > dw / 2 - 12:
                continue
            cutters.append(Pos(x, y, P["deck_z"] - dt / 2) * Rot(0, 0, 45) * Box(21, 11, dt + 2))
    try:
        d2 = deck - Compound(children=cutters)
        if d2.is_valid:
            deck = d2
    except Exception:
        pass

    bh = P["deck_z"] - R - P["wheel_r"] + 20
    brackets = [Pos(P["axle_x"], s * P["bracket_y"], P["wheel_r"] + bh / 2 - 10) * Box(70, 6, bh) for s in (-1, 1)]
    brackets = [_fillet_try(b, b.edges().filter_by(Axis.Y), [8.0, 4.0]) for b in brackets]
    axle = _tube((P["axle_x"], -P["wheel_y"], P["wheel_r"]), (P["axle_x"], P["wheel_y"], P["wheel_r"]), P["axle_d"] / 2)

    # rail end plugs (black), flush with the tube ends
    plugs = [_box(sx * (L / 2 - 2), s * (Wd / 2 - R / 2), rz, 4, R, R) for sx in (-1, 1) for s in (-1, 1)]
    plugs = [_fillet_try(p, p.edges().filter_by(Axis.X), [3.0, 1.5]) for p in plugs]
    return frame, deck, _comp(brackets), axle, _comp(plugs)


def _wheel(P, s):
    """Flat-free tyre (tread, rounded shoulders), dished steel rim and hub cap. s = -1 near side, +1 far side."""
    r, w = P["wheel_r"], P["wheel_w"]
    ri = r - 55
    tyre = Cylinder(r, w) - Cylinder(ri, w + 2)
    outer_edges = [e for e in tyre.edges() if e.geom_type.name == "CIRCLE" and abs(e.radius - r) < 0.5]
    tyre = _fillet_try(tyre, outer_edges, [18.0, 12.0, 6.0])
    grooves = []
    n = 36
    for k in range(n):
        a = 360.0 * k / n
        zc = 14.0 if k % 2 else -14.0
        grooves.append(Rot(0, 0, a) * Pos(r, 0, zc) * Box(8, 11, 44))
    try:
        t2 = tyre - Compound(children=grooves)
        if t2.is_valid:
            tyre = t2
    except Exception:
        pass
    # rim: flange ring, dished centre disc with lightening holes, hub
    rim = Cylinder(ri, w - 30) - Cylinder(ri - 14, w - 28)
    disc = Pos(0, 0, 6) * Cylinder(ri - 13, 6)
    for k in range(5):
        disc -= Rot(0, 0, 72 * k) * Pos(82, 0, 6) * Cylinder(17, 10)
    rim = rim + disc + Cylinder(36, w - 14)
    cap = Pos(0, 0, (w - 14) / 2 + 3) * Cylinder(26, 6)
    cap = _fillet_try(cap, _top_edges(cap), [3.0, 2.0])
    loc = Pos(P["axle_x"], s * P["wheel_y"], P["wheel_r"]) * Rot(0, 0, 180 if s > 0 else 0) * Rot(90, 0, 0)
    return loc * tyre, loc * rim, loc * cap


def _handle(P, D):
    L, Wd, R, rz = P["deck_l"], P["deck_w"], P["rail"], D["rail_z"]
    hy = Wd / 2 - R / 2
    gx, gz, hr = P["grip_x"], P["grip_z"], P["handle_d"] / 2
    tubes = _comp([_tube((L / 2 - 20, -hy, rz), (gx, -hy + 40, gz), hr),
                   _tube((L / 2 - 20, hy, rz), (gx, hy - 40, gz), hr),
                   _tube((gx, -hy - 20, gz), (gx, hy + 20, gz), hr + 2),
                   Pos(gx, -hy + 40, gz) * Sphere(hr), Pos(gx, hy - 40, gz) * Sphere(hr)])
    grip = _ycyl(gx, 0, gz, hr + 7, 2 * (hy - 40) - 70)
    grip = _fillet_try(grip, grip.edges(), [5.0, 3.0])
    ends = [_ycyl(gx, s * (hy + 20 + 4), gz, hr + 3, 8) for s in (-1, 1)]
    ends = [_fillet_try(e, e.edges(), [2.5, 1.5]) for e in ends]
    # quick-release pins at the frame end: ring and pin head outboard of each side rail
    pins = []
    for s in (-1, 1):
        y = s * (hy + R / 2 + 3)
        pins.append(_ycyl(L / 2 - 30, y, rz, 7, 6))
        pins.append(Pos(L / 2 - 30, y + s * 4, rz - 16) * Rot(90, 0, 0) * Torus(14, 2.2))
    return tubes, grip, _comp(ends), _comp(pins)


def _legs(P, x):
    tubes, feet, clamps = [], [], []
    for s in (-1, 1):
        y = s * P["leg_y"]
        tubes.append(_tube((x, y, 25), (x, y, P["deck_z"] - P["rail"] - 30), P["leg_d"] / 2))
        c = _box(x, y, P["deck_z"] - P["rail"] - 18, 44, 40, 36)
        clamps.append(_fillet_try(c, _vertical_edges(c), [6.0, 3.0]))
        f = _prism(90, 70, 12, 0, 25, x=x, y=y)
        feet.append(_fillet_try(f, _top_edges(f), [6.0, 3.0]))
    return _comp(tubes + clamps), _comp(feet)


# ---------------------------------------------------------------------------------------- PV wings
def _wing_local(P):
    """One wing in a local frame: top face at z = 0, hinge edge at y = 0, spanning y 0 to pv_w."""
    pl, pw, pt = P["pv_l"], P["pv_w"], P["pv_t"]
    frame = _box(0, pw / 2, -3 - (pt - 3) / 2, pl, pw, pt - 3) - _box(0, pw / 2, -pt / 2, pl - 50, pw - 50, pt + 2)
    for x in (-pl / 6, pl / 6):
        frame += _box(x, pw / 2, -3 - 12, 25, pw - 40, 24)
    frame += _box(0, pw / 2, -3 - 12, pl - 40, 25, 24)
    back = _box(0, pw / 2, -1.7, pl - 6, pw - 6, 2.6)
    back = _fillet_try(back, _vertical_edges(back), [4.0, 2.0])
    # 8 x 4 grid of cells with clipped corners, three busbars per cell column
    ncx, ncy = 8, 4
    mx, my = pl - 40, pw - 40
    ptx, pty = mx / ncx, my / ncy
    cells, bars = [], []
    for i in range(ncx):
        cx = -mx / 2 + ptx * (i + 0.5)
        for j in range(ncy):
            cy = 20 + pty * (j + 0.5)
            c = _box(cx, cy, -0.2, ptx - 6, pty - 6, 0.4)
            for sx in (-1, 1):
                for sy in (-1, 1):
                    c -= Pos(cx + sx * (ptx - 6) / 2, cy + sy * (pty - 6) / 2, -0.2) * Rot(0, 0, 45) * Box(14, 14, 2)
            cells.append(c)
        for b in (-1, 0, 1):
            bars.append(_box(cx + b * (ptx - 6) / 3.2, pw / 2, 0.08, 1.4, my - 6, 0.16))
    # teal corner guards on the outer corners, junction box underneath
    guards = []
    for sx in (-1, 1):
        g = _box(sx * (pl / 2 - 20), pw - 20, -pt / 2 + 0.5, 44, 44, pt + 3)
        g -= _box(sx * (pl / 2 - 20) - sx * 3, pw - 23, -pt / 2 + 2, 44, 44, pt - 1)
        g = _fillet_try(g, _vertical_edges(g), [4.0, 2.0])
        guards.append(g)
    jb = _prism(120, 80, 8, -pt - 22, 22, x=pl / 2 - 260, y=160)
    jb = _fillet_try(jb, _bottom_edges(jb), [4.0, 2.0])
    return dict(frame=frame, back=back, cells=_comp(cells), bars=_comp(bars), guards=_comp(guards), jbox=jb)


def _wing_loc(P, s):
    return Pos(0, s * P["hinge_y"], P["hinge_z"]) * Rot(-s * P["tilt"], 0, 0) * Rot(0, 0, 180 if s < 0 else 0)


def _hinge(P, s):
    """Knuckled continuous hinge on its 20 mm aluminium angle spacer, with tabs to the side rail."""
    pl, hyy, hz, sp = P["pv_l"], P["hinge_y"], P["hinge_z"], P["spacer"]
    x0, x1 = -pl / 2 + 50, pl / 2 - 50
    n = 26
    seg = (x1 - x0) / n
    knuckles = [_xcyl(x0 + seg * (k + 0.5), s * hyy, hz - 8, 9, seg - 2) for k in range(n)]
    pin_caps = [_xcyl(x, s * hyy, hz - 8, 5, 4) for x in (x0 - 2, x1 + 2)]
    spacer = _box(0, s * hyy, hz - 17 - sp / 2, pl - 100, 20, sp)
    spacer -= _box(0, s * (hyy - 2), hz - 17 - sp / 2 + 2, pl - 98, 18, sp)
    tabs = []
    ry = P["deck_w"] / 2
    for x in (-pl / 2 + 140, -pl / 6, pl / 6, pl / 2 - 140):
        tabs.append(_box(x, s * (ry + (hyy - 10 - ry) / 2), hz - 17 - sp - 12, 30, hyy - 10 - ry, 24))
    return _comp(knuckles + pin_caps), _comp([spacer] + tabs)


def _outriggers(P, D, s):
    pl = P["pv_l"]
    r = P["out_d"] / 2
    tubes, feet, stakes = [], [], []
    for x in (-pl / 2 + 80, pl / 2 - 80):
        y = s * D["out_y"]
        tubes.append(_tube((x, y, 20), (x, y, D["out_top"]), r))
        tubes.append(_box(x, y, D["out_top"] - 12, 40, 40, 24))
        f = _prism(80, 80, 10, 0, 12, x=x, y=y)
        f = _fillet_try(f, _top_edges(f), [3.0, 1.5])
        f += _box(x, y, 16, 34, 34, 8)
        feet.append(f)
        # stake through the loop on the outer side of the foot
        sy = y + s * 58
        loop = Pos(x, sy - s * 8, 10) * Rot(0, 0, 0) * (Cylinder(16, 8) - Cylinder(9, 10))
        feet.append(loop)
        st = _zcyl(x, sy - s * 8, 40, 5, 60) + _zcyl(x, sy - s * 8, 72, 11, 6)
        stakes.append(st)
    return _comp(tubes), _comp(feet), _comp(stakes)


def _shade(P):
    x0, x1, sw, gap = P["shade"]
    bb, eb = P["batt_box"], P["ebox"]
    top = P["deck_z"] + max(bb[2], eb[2])
    t = P["shade_t"]
    sz = top + gap + t / 2
    ring = _box((x0 + x1) / 2, 0, sz, x1 - x0, sw, t) - _box((x0 + x1) / 2, 0, sz, x1 - x0 - 40, sw - 40, t + 2)
    ring = _fillet_try(ring, _vertical_edges(ring), [10.0, 5.0])
    fabric = _box((x0 + x1) / 2, 0, sz + 0.5, x1 - x0 - 30, sw - 30, 2.0)
    fabric = _fillet_try(fabric, _vertical_edges(fabric), [8.0, 4.0])
    return ring, fabric


def _bin(P, D):
    bn, t = P["bin"], P["wall"]
    x, z0 = D["bin_x"], P["deck_z"]
    body = _prism(bn[0], bn[1], 16, z0, bn[2], x=x)
    body = _fillet_try(body, _bottom_edges(body), [8.0, 4.0])
    body -= _prism(bn[0] - 2 * t, bn[1] - 2 * t, 12, z0 + t, bn[2], x=x)
    lip = _prism(bn[0] + 8, bn[1] + 8, 20, z0 + bn[2] - 12, 12, x=x) - _prism(bn[0] - 2 * t, bn[1] - 2 * t, 12, z0 + bn[2] - 14, 20, x=x)
    body = body + lip
    # teal webbing strap over the top, across the bin, with a buckle on the front
    sw, st = 38.0, 2.5
    yo = bn[1] / 2 + 4 + st / 2
    strap = _box(x, 0, z0 + bn[2] + st / 2, sw, 2 * yo + st, st)
    for s in (-1, 1):
        strap += _box(x, s * yo, z0 + (bn[2] + st) / 2 + 10, sw, st, bn[2] - 20 + st)
    buckle = _box(x, -yo - 4, z0 + bn[2] - 60, sw + 10, 6, 34) - _box(x, -yo - 4, z0 + bn[2] - 60, sw - 6, 10, 18)
    # coiled cord inside
    coil = None
    for k in range(4):
        c = Pos(x, 40, z0 + t + 8 + 14 * k) * Torus(90, 7)
        coil = c if coil is None else coil + c
    plug = _box(x - 60, -120, z0 + 60, 40, 30, 70)
    plug = _fillet_try(plug, plug.edges(), [6.0, 3.0])
    return body, strap, buckle, coil, plug


# ---------------------------------------------------------------------------------------- power system
def _battery(P):
    bb, t, z0 = P["batt_box"], P["wall"], P["deck_z"]
    lx, ly, lz = bb
    zs = z0 + lz - 70                     # lid parting line
    body = _prism(lx, ly, 26, z0, lz)
    body = _fillet_try(body, _top_edges(body), [10.0, 6.0, 3.0])
    body = _fillet_try(body, _bottom_edges(body), [6.0, 3.0])
    body -= _prism(lx - 2 * t, ly - 2 * t, 20, z0 + t, lz - 2 * t)
    groove = _prism(lx + 2, ly + 2, 27, zs - 1, 2) - _prism(lx - 2, ly - 2, 25, zs - 2, 4)
    body -= groove
    lower = body & _box(0, 0, (z0 + zs) / 2, lx + 20, ly + 20, zs - z0)
    lid = body & _box(0, 0, (zs + z0 + lz) / 2 + 1, lx + 20, ly + 20, z0 + lz - zs + 2)
    # lid ribs (texture) along X
    for y in (-100, -50, 0, 50, 100):
        lid += _box(0, y, z0 + lz + 1.5, lx - 90, 10, 3)
    # side ribs on the lower body
    for s in (-1, 1):
        for x in (-150, 150):
            lower += _box(x, s * (ly / 2 + 2), z0 + 130, 16, 4, 180)
    # latches straddling the parting line, front and back
    latches = []
    for s in (-1, 1):
        for x in (-110, 110):
            b = _box(x, s * (ly / 2 + 7), zs - 5, 52, 14, 66)
            b = _fillet_try(b, b.edges().filter_by(Axis.Y), [5.0, 3.0])
            latches.append(b)
    # fold-flat carry handle on the lid
    handle = _xcyl(0, 0, z0 + lz + 16, 8, 170) + _box(-95, 0, z0 + lz + 9, 22, 30, 18) + _box(95, 0, z0 + lz + 9, 22, 30, 18)
    vent = _ycyl(150, -ly / 2 - 2, z0 + 70, 12, 4) + _ycyl(150, -ly / 2 - 4.5, z0 + 70, 7, 3)
    label = _xz_plate(-40, -ly / 2, z0 + 150, 150, 70, 4, 0.8)
    stripe = _xz_plate(-40, -ly / 2 - 0.8, z0 + 190, 150, 10, 1, 0.4)
    # gland plate on the +X face toward the electronics box
    gland_plate = _yz_plate(lx / 2, 0, z0 + 120, 130, 70, 6, 4)
    return dict(lower=lower, lid=lid, latches=_comp(latches), handle=handle, vent=vent, label=label,
                stripe=stripe, gland_plate=gland_plate)


def _pack(P):
    pk, t, z0 = P["pack"], P["wall"], P["deck_z"] + P["wall"]
    body = _prism(pk[0], pk[1], 10, z0, pk[2] - 12)
    body = _fillet_try(body, _top_edges(body), [4.0, 2.0])
    top = _prism(pk[0] - 4, pk[1] - 4, 9, z0 + pk[2] - 12, 12)
    top = _fillet_try(top, _top_edges(top), [3.0, 1.5])
    zt = z0 + pk[2]
    term_red = _zcyl(-pk[0] / 2 + 45, 0, zt + 8, 14, 16)
    term_blk = _zcyl(pk[0] / 2 - 45, 0, zt + 8, 14, 16)
    term_red = _fillet_try(term_red, _top_edges(term_red), [4.0, 2.0])
    term_blk = _fillet_try(term_blk, _top_edges(term_blk), [4.0, 2.0])
    label = _xz_plate(0, -pk[1] / 2, z0 + pk[2] / 2, 200, 110, 4, 0.8)
    return body, top, term_red, term_blk, label


def _ebox(P, D):
    eb, t, z0, ex = P["ebox"], P["wall"], P["deck_z"], D["ebox_x"]
    lx, ly, lz = eb
    zs = z0 + lz - 40
    body = _prism(lx, ly, 14, z0, lz, x=ex)
    body = _fillet_try(body, _top_edges(body), [8.0, 5.0, 3.0])
    body = _fillet_try(body, _bottom_edges(body), [4.0, 2.0])
    body -= _prism(lx - 2 * t, ly - 2 * t, 10, z0 + t, lz - 2 * t, x=ex)
    groove = _prism(lx + 2, ly + 2, 15, zs - 1, 2, x=ex) - _prism(lx - 2, ly - 2, 13, zs - 2, 4, x=ex)
    body -= groove
    # clear side window on the -Y wall, onto the inverter and breakers
    wx0, wx1, wz0, wz1 = ex - 140, ex - 30, z0 + 30, z0 + 240
    wcx, wcz = (wx0 + wx1) / 2, (wz0 + wz1) / 2
    body -= _xz_plate(wcx, -ly / 2 + t + 1, wcz, wx1 - wx0, wz1 - wz0, 10, t + 4)
    lower = body & _box(ex, 0, (z0 + zs) / 2, lx + 20, ly + 20, zs - z0)
    lid = body & _box(ex, 0, (zs + z0 + lz) / 2 + 1, lx + 20, ly + 20, z0 + lz - zs + 2)
    screws = [_zcyl(ex + sx * (lx / 2 - 18), sy * (ly / 2 - 18), z0 + lz + 0.8, 5, 1.6)
              for sx in (-1, 1) for sy in (-1, 1)]
    window = _xz_plate(wcx, -ly / 2 + t + 0.5, wcz, wx1 - wx0 + 4, wz1 - wz0 + 4, 11, t - 1.0)
    bezel = _xz_plate(wcx, -ly / 2, wcz, wx1 - wx0 + 20, wz1 - wz0 + 20, 16, 2.0) - \
        _xz_plate(wcx, -ly / 2 + 1, wcz, wx1 - wx0 - 2, wz1 - wz0 - 2, 10, 4.0)

    fx, fy, fz = P["fan"]

    def grille(xc, y_out, zc, s):
        """Louvered filter grille on a wall; s = -1 on the -Y wall, +1 on the +Y wall."""
        f = _box(xc, y_out - s * fz / 2, zc, fx, fz, fy)
        f = _fillet_try(f, f.edges().filter_by(Axis.Y), [6.0, 3.0])
        f -= _box(xc, y_out + s * 2, zc, fx - 18, 8, fy - 18)
        for k in range(7):
            zz = zc - (fy - 18) / 2 + 7 + k * ((fy - 32) / 6)
            f += Pos(xc, y_out + s * 3, zz) * Rot(s * 30, 0, 0) * Box(fx - 20, 2.0, 10)
        return f & _box(xc, y_out - s * fz / 2, zc, fx + 2, fz + 2, fy + 2)

    # intake fan on the +Y wall and exhaust filter on the -Y wall, positions as model.py
    fan_in = grille(ex - 40, ly / 2 + fz, z0 + 90, +1)
    fan_out = grille(ex + 40, -ly / 2 - fz, z0 + lz - 90, -1)
    label = _xz_plate(ex + 80, -ly / 2, z0 + 60, 110, 44, 4, 0.8)
    return dict(lower=lower, lid=lid, screws=_comp(screws), window=window, bezel=bezel,
                fan_in=fan_in, fan_out=fan_out, label=label)


def _electronics(P, D):
    """Inverter, MPPT and breakers at their model.py envelopes, with product detail."""
    ex, z0 = D["ebox_x"], P["deck_z"] + P["wall"]
    # inverter: finned aluminium body with black end caps
    ix, iy, iz = ex - 10, -95, z0 + 55
    inv = _box(ix, iy, iz, 230, 210, 110)
    for k in range(9):
        inv -= _box(ix, iy - 84 + k * 21, iz + 55 - 5, 232, 8, 10)
    for k in range(4):
        inv -= _box(ix, iy - 105 + 1, iz - 36 + k * 22, 232, 6, 8)
    caps = _box(ix - 125, iy, iz, 20, 210, 110) + _box(ix + 125, iy, iz, 20, 210, 110)
    caps = _fillet_try(caps, caps.edges().filter_by(Axis.X), [6.0, 3.0])
    inv_led = _xcyl(ix + 135.5, iy + 70, iz + 30, 4, 1.0)
    # MPPT: dark blue body on a finned heat sink
    mx, my = ex - 40, 140
    mppt = _box(mx, my, z0 + 43, 150, 140, 54)
    mppt = _fillet_try(mppt, _top_edges(mppt), [5.0, 3.0])
    sink = _box(mx, my, z0 + 8, 150, 140, 16)
    for k in range(10):
        sink -= _box(mx - 67 + k * 15, my, z0 + 6, 6, 142, 12)
    # breakers and fuse on a DIN rail backplate (fusing envelope)
    fz0 = z0 + 70
    plate = _box(ex - 40, 212, fz0 + 50, 150, 6, 100)
    rail = _box(ex - 40, 200, fz0 + 50, 150, 18, 30)
    brk, tog = [], []
    for k in range(5):
        bx = ex - 40 - 60 + k * 30
        b = _box(bx, 160, fz0 + 50, 26, 70, 90)
        b = _fillet_try(b, b.edges().filter_by(Axis.X), [3.0, 1.5])
        brk.append(b)
        tog.append(_box(bx, 122, fz0 + 58, 10, 8, 18))
    fuse = _box(ex - 40 + 50, 110, fz0 + 20, 40, 30, 30)
    return dict(inv=inv, inv_caps=caps, inv_led=inv_led, mppt=mppt, sink=sink, plate=_comp([plate, rail]),
                breakers=_comp(brk), toggles=_comp(tog), fuse=fuse)


def _outlet_face(P, D):
    """Outlet face on the handle end of the electronics box, at the model.py panel positions."""
    ex, eb, z0 = D["ebox_x"], P["ebox"], P["deck_z"]
    face = ex + eb[0] / 2
    out = {}
    # DC panel (model.py: y 115, z deck + 170, 170 x 180, 12 mm deep)
    py, pz = 115.0, z0 + 170
    plate = _yz_plate(face, py, pz, 170, 180, 12, 4)
    plate = _fillet_try(plate, plate.faces().sort_by(Axis.X)[-1].edges(), [1.5, 0.8])
    out["dc_plate"] = plate
    cols = (py - 40, py + 40)
    usb, usb_ring, sock, caps = [], [], [], []
    for y in cols:
        u = _xcyl(face + 4 + 4, y, pz + 10, 17, 8)
        u = _fillet_try(u, u.faces().sort_by(Axis.X)[-1].edges(), [2.0, 1.0])
        u -= Pos(face + 10, y, pz + 10) * extrude(Plane.YZ * SlotOverall(9.2, 3.6), amount=6)
        u += _box(face + 9, y, pz + 10, 2, 6.4, 0.8)
        usb.append(u)
        usb_ring.append(_xcyl(face + 12.3, y, pz + 10, 20, 0.6) - _xcyl(face + 12.3, y, pz + 10, 17.5, 2))
        s = _xcyl(face + 4 + 5, y, pz - 52, 17, 10)
        s -= _xcyl(face + 12, y, pz - 52, 11, 8)
        sock.append(s)
        c = _xcyl(face + 14 + 3, y, pz - 52, 18.5, 6)
        c = _fillet_try(c, c.faces().sort_by(Axis.X)[-1].edges(), [2.5, 1.5])
        c += _box(face + 16, y, pz - 52 - 22, 5, 10, 10)
        caps.append(c)
    out["usb"] = _comp(usb)
    out["usb_ring"] = _comp(usb_ring)
    out["sockets"] = _comp(sock)
    out["socket_caps"] = _comp(caps)
    # battery monitor (fusing and disconnect, BOM 12) at the top of the panel
    mon = _yz_plate(face + 4, py, pz + 60, 130, 46, 6, 4)
    mon = _fillet_try(mon, mon.faces().sort_by(Axis.X)[-1].edges(), [1.5, 0.8])
    out["monitor"] = mon
    out["monitor_screen"] = _yz_plate(face + 8, py - 12, pz + 60, 86, 30, 2, 0.6)
    out["monitor_keys"] = _comp([_xcyl(face + 9, py + 46, pz + 60 + dz, 5, 2) for dz in (-9, 9)])

    # AC outlet with GFCI (model.py: y -120, z deck + 180, 80 x 130, 12 mm deep) under an in-use cover
    ay, az = -120.0, z0 + 180
    base = _yz_plate(face, ay, az, 80, 130, 8, 8)
    base = _fillet_try(base, base.faces().sort_by(Axis.X)[-1].edges(), [2.0, 1.0])
    rec = _yz_plate(face + 8, ay, az, 46, 104, 5, 3)
    for dz in (-30, 30):
        rec -= _box(face + 11, ay - 6, az + dz + 3, 4, 2.2, 10)
        rec -= _box(face + 11, ay + 6, az + dz + 3, 4, 2.2, 12)
        rec -= _xcyl(face + 11, ay, az + dz - 8, 2.4, 4)
    out["ac_face"] = _comp([base, rec])
    out["gfci_test"] = _box(face + 12, ay - 8, az, 3, 12, 8)
    out["gfci_reset"] = _box(face + 12, ay + 8, az, 3, 12, 8)
    cov = _yz_plate(face + 8, ay, az + 4, 76, 122, 10, 30)
    cov = _fillet_try(cov, cov.faces().sort_by(Axis.X)[-1].edges(), [8.0, 5.0, 3.0])
    cov -= _yz_plate(face + 6, ay, az + 2, 72, 118, 8, 30)
    cov -= _box(face + 22, ay, az - 58, 20, 40, 14)          # cord slot at the bottom
    out["cover"] = cov

    # battery isolator knob and inverter rocker between the two panels
    iy, iz = -25.0, z0 + 230
    ib = _yz_plate(face, iy, iz, 54, 54, 6, 5)
    out["iso_base"] = _fillet_try(ib, ib.faces().sort_by(Axis.X)[-1].edges(), [1.5, 0.8])
    knob = _xcyl(face + 5 + 5, iy, iz, 18, 10)
    knob = _fillet_try(knob, knob.faces().sort_by(Axis.X)[-1].edges(), [3.0, 1.5])
    bar = _box(face + 5 + 10 + 7, iy, iz, 14, 12, 46)
    bar = _fillet_try(bar, bar.edges().filter_by(Axis.X), [4.0, 2.0])
    out["iso_knob"] = knob + bar
    rz = z0 + 125
    rb = _yz_plate(face, iy, rz, 30, 44, 4, 4)
    out["rocker_bezel"] = rb
    rk = _yz_plate(face + 4, iy, rz, 22, 34, 3, 5) - Pos(face + 9, iy, rz + 17) * Rot(0, 30, 0) * Box(4, 30, 20)
    out["rocker"] = rk
    lamp = _xcyl(face + 3, iy, rz + 36, 4.5, 6)
    out["inv_lamp"] = _fillet_try(lamp, lamp.faces().sort_by(Axis.X)[-1].edges(), [2.0, 1.0])
    return out


def _cables(P, D):
    """Two battery cables with glands from the battery case gland plate to the electronics box."""
    bb, z0 = P["batt_box"], P["deck_z"]
    x0 = bb[0] / 2 + 4
    x1 = D["ebox_x"] - P["ebox"][0] / 2
    z = z0 + 120
    cables, glands = [], []
    for y in (-30, 30):
        cables.append(_xcyl((x0 + x1) / 2, y, z, 8, x1 - x0))
        glands.append(_xcyl(x0 + 6, y, z, 13, 12))
        glands.append(_xcyl(x1 - 6, y, z, 13, 12))
    return _comp(cables), _comp(glands)


def _ground():
    x0, x1, y0, y1, t = GROUND
    g = _prism(x1 - x0, y1 - y0, 60, -t, t, x=(x0 + x1) / 2, y=(y0 + y1) / 2)
    return _fillet_try(g, _top_edges(g), [12.0, 6.0])


# ---------------------------------------------------------------------------------------- assembly
def product_parts(P=PARAMS):
    D = derived(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ---- frame, wheels, handle, legs (BOM 1 to 4)
    frame, deck, brackets, axle, plugs = _frame(P, D)
    add("Cart frame, powder-coated steel tube", frame, C_FRAME, "painted", 1, "shell", (0, 0, 0))
    add("Expanded-metal deck", deck, C_FRAME, "painted", 1, "shell", (0, 0, 0))
    add("Axle brackets", brackets, C_FRAME, "painted", 1, "shell", (0, 0, -120))
    add("Axle, bright steel", axle, C_STEEL, "metal", 1, "shell", (0, 0, -120))
    add("Tube end plugs", plugs, C_BLACK, "rubber", 1, "shell", (0, 0, 0))
    for s, tag in ((-1, "near"), (1, "far")):
        tyre, rim, cap = _wheel(P, s)
        ex = (0, s * 360, -120)
        add(f"Flat-free tyre, {tag} side", tyre, C_RUBBER, "rubber", 2, "shell", ex)
        add(f"Steel rim, {tag} side", rim, "#8B939D", "painted", 2, "shell", ex)
        add(f"Hub cap, {tag} side", cap, C_BLACK, "plastic", 2, "shell", ex)
    tubes, grip, ends, pins = _handle(P, D)
    hx = (520, 0, 60)
    add("T-handle", tubes, C_FRAME, "painted", 3, "shell", hx)
    add("Handle foam grip", grip, C_RUBBER, "rubber", 3, "shell", hx)
    add("Handle end caps", ends, C_BLACK, "rubber", 3, "shell", hx)
    add("Handle quick-release pins", pins, C_STEEL, "metal", 3, "shell", (260, 0, 0))
    FX, RX = -P["deck_l"] / 2 + 40, P["deck_l"] / 2 - 40
    for x, tag, dx in ((FX, "bin end", -120), (RX, "handle end", 120)):
        legs, feet = _legs(P, x)
        add(f"Stand legs, {tag}", legs, C_FRAME, "painted", 4, "shell", (dx, 0, -300))
        add(f"Stand leg feet, {tag}", feet, C_BLACK, "rubber", 4, "shell", (dx, 0, -300))

    # ---- PV wings, hinges, outriggers (BOM 13 to 15)
    wl = _wing_local(P)
    for s, tag in ((-1, "near"), (1, "far")):
        loc = _wing_loc(P, s)
        ew = (0, s * 950, 260)
        add(f"PV wing backing frame, aluminium, {tag}", loc * wl["frame"], C_ALU, "metal", 13, "shell", ew)
        add(f"PV module backsheet, {tag}", loc * wl["back"], C_BACKSHEET, "plastic", 13, "shell", ew)
        add(f"PV cells, {tag}", loc * wl["cells"], C_CELL, "screen", 13, "shell", ew)
        add(f"PV cell busbars, {tag}", loc * wl["bars"], C_BUSBAR, "metal", 13, "shell", ew)
        add(f"PV wing corner guards, {tag}", loc * wl["guards"], C_ACCENT, "plastic", 13, "shell", ew)
        add(f"PV junction box, {tag}", loc * wl["jbox"], C_BLACK, "plastic", 13, "shell", ew)
        kn, sp = _hinge(P, s)
        eh = (0, s * 380, 160)
        add(f"Continuous hinge, stainless, {tag}", kn, C_ALU, "metal", 14, "shell", eh)
        add(f"Hinge spacer and tabs, aluminium, {tag}", sp, C_STEEL, "metal", 14, "shell", eh)
        ot, of, st = _outriggers(P, D, s)
        eo = (0, s * 1150, -60)
        add(f"Outrigger legs, {tag}", ot, C_FRAME, "painted", 15, "shell", eo)
        add(f"Outrigger feet, {tag}", of, C_FRAME, "painted", 15, "shell", eo)
        add(f"Outrigger stakes, {tag}", st, C_STEEL, "metal", 15, "shell", (0, s * 1150, 200))

    # ---- sun shade (BOM 18)
    ring, fabric = _shade(P)
    es = (0, 0, 1450)
    add("Sun shade frame, aluminium flat bar", ring, C_ALU, "metal", 18, "shell", es)
    add("Sun shade, reflective fabric", fabric, C_SHADE, "fabric", 18, "shell", es)
    # Shade uprights, bolted to four tabs on the side rails so the shade lifts off for battery service
    # (FCL-DEC-001, 2026-10-02): taken straight from the constructable model.
    M = build_components(P)
    add("Sun shade uprights, aluminium tube", M["uprights"].shape, C_ALU, "metal", 18, "shell", (0, 0, 1250))
    add("Shade upright tabs and wing bolts", M["up_tabs"].shape, C_STEEL, "metal", 18, "shell", (0, 0, 700))

    # ---- constructable hardware from model.py (FCL-DDR-003): tie bars with over-centre latches,
    #      hinge, handle socket, stand leg and outrigger brackets, axle collars, fuse and cam straps
    add("Wing tie bars, aluminium square tube", M["tie_bars"].shape, C_ALU, "metal", 19, "shell", (0, 0, 520))
    add("Tie bar pivot brackets", M["tie_brk"].shape, C_STEEL, "metal", 19, "shell", (0, 0, 380))
    add("Over-centre tie bar latches", M["latches"].shape, C_ACCENT, "metal", 14, "shell", (0, 0, 520))
    add("Latch keepers", M["keepers"].shape, C_STEEL, "metal", 14, "shell", (0, 0, 380))
    add("Hinge tabs on the side rails", M["tabs"].shape, C_FRAME, "painted", 1, "shell", (0, 0, 200))
    add("Handle sockets and gussets", M["sockets"].shape, C_FRAME, "painted", 1, "shell", (260, 0, 0))
    add("Stand leg clevises", M["clevises"].shape, C_FRAME, "painted", 1, "shell", (0, 0, -200))
    add("Stand leg pivot bolts", M["leg_bolts"].shape, C_STEEL, "metal", 4, "shell", (0, 0, -200))
    add("Axle spacer collars and linch pins", M["axle_hw"].shape, C_STEEL, "metal", 2, "shell", (0, 0, -120))
    add("Outrigger clevis brackets", M["out_brk"].shape, C_STEEL, "metal", 15, "shell", (0, 0, -60))
    add("Outrigger pivot bolts", M["out_bolts"].shape, C_STEEL, "metal", 15, "shell", (0, 0, -60))

    # ---- accessory bin (BOM 16)
    body, strap, buckle, coil, plug = _bin(P, D)
    eb = (-420, 0, 160)
    add("Accessory and cable bin", body, C_BIN, "plastic", 16, "shell", eb)
    add("Bin tie-down strap, webbing", strap, C_ACCENT, "fabric", 16, "shell", (-420, 0, 420))
    add("Strap buckle", buckle, C_BLACK, "plastic", 16, "shell", (-420, 0, 420))
    add("Coiled extension cord", coil, C_CORD, "rubber", None, "shell", (-420, 0, 300))
    add("Cord plug", plug, C_BLACK, "plastic", None, "shell", (-420, 0, 300))

    # ---- battery case and pack (BOM 5, 6)
    B = _battery(P)
    add("Battery case, IP65", B["lower"], C_CASE, "plastic", 5, "internal", (0, 0, 220))
    add("Battery case lid", B["lid"], C_CASE, "plastic", 5, "internal", (0, 0, 900))
    add("Battery case latches", B["latches"], C_BLACK, "plastic", 5, "internal", (0, 0, 220))
    add("Battery case carry handle", B["handle"], C_BLACK, "plastic", 5, "internal", (0, 0, 900))
    add("Battery case pressure vent", B["vent"], C_BLACK, "plastic", 5, "internal", (0, 0, 220))
    add("Battery case rating label", B["label"], C_LABEL, "paper", 5, "internal", (0, 0, 220))
    add("Battery case label stripe", B["stripe"], C_ACCENT, "plastic", 5, "internal", (0, 0, 220))
    add("Battery case gland plate", B["gland_plate"], C_BLACK, "plastic", 5, "internal", (0, 0, 220))
    pb, pt, tr, tb, pl = _pack(P)
    ep = (0, 0, 560)
    add("LiFePO4 pack, 25.6 V 50 Ah", pb, C_PACK, "plastic", 6, "internal", ep)
    add("LiFePO4 pack top cover", pt, C_BLACK, "plastic", 6, "internal", ep)
    add("Pack terminal cover, positive", tr, C_RED, "plastic", 6, "internal", ep)
    add("Pack terminal cover, negative", tb, C_BLACK, "plastic", 6, "internal", ep)
    add("Pack label", pl, C_LABEL, "paper", 6, "internal", ep)
    add("Class T fuse and holder", M["fuse_t"].shape, C_RED, "plastic", 12, "internal", (0, 0, 640))
    add("Battery case cam straps", M["straps"].shape, C_ACCENT, "fabric", 17, "internal", (0, 0, 900))

    # ---- electronics box and contents (BOM 7 to 12)
    E = _ebox(P, D)
    ee = (380, 0, 200)
    add("Electronics enclosure, IP54", E["lower"], C_EBOX, "plastic", 7, "internal", ee)
    add("Electronics enclosure lid", E["lid"], C_EBOX_LID, "plastic", 7, "internal", (380, 0, 700))
    add("Lid screws", E["screws"], C_STEEL, "metal", 7, "internal", (380, 0, 740))
    add("Side window, clear polycarbonate", E["window"], C_WINDOW, "clear", 7, "internal", (380, -140, 200))
    add("Side window bezel", E["bezel"], C_PANEL, "plastic", 7, "internal", (380, -140, 200))
    add("Intake filter fan grille", E["fan_in"], "#AEB4BB", "plastic", 7, "internal", (380, 140, 200))
    add("Exhaust filter grille", E["fan_out"], "#AEB4BB", "plastic", 7, "internal", (380, -140, 200))
    add("Electronics box rating label", E["label"], C_ACCENT, "plastic", 7, "internal", ee)
    X = _electronics(P, D)
    ei = (380, 0, 460)
    add("Inverter body, finned aluminium", X["inv"], C_ALU, "metal", 9, "internal", ei)
    add("Inverter end caps", X["inv_caps"], C_BLACK, "plastic", 9, "internal", ei)
    add("Inverter status LED", X["inv_led"], C_LIT_GREEN, "emissive", 9, "internal", ei)
    add("MPPT charge controller", X["mppt"], C_MPPT, "painted", 8, "internal", ei)
    add("MPPT heat sink", X["sink"], C_ALU, "metal", 8, "internal", ei)
    add("DIN rail and backplate", X["plate"], C_STEEL, "metal", 12, "internal", (380, 0, 560))
    add("DC breakers", X["breakers"], C_OFFWHITE, "plastic", 12, "internal", (380, 0, 560))
    add("Breaker toggles", X["toggles"], C_BLACK, "plastic", 12, "internal", (380, 0, 560))
    add("Class T fuse holder", X["fuse"], C_BLACK, "plastic", 12, "internal", (380, 0, 560))
    O = _outlet_face(P, D)
    eo = (720, 0, 200)
    add("DC outlet panel", O["dc_plate"], C_PANEL, "plastic", 10, "internal", eo)
    add("USB-C PD outlets", O["usb"], C_BLACK, "plastic", 10, "internal", eo)
    add("USB-C outlet rings (lit)", O["usb_ring"], C_LIT_TEAL, "emissive", 10, "internal", eo)
    add("12 V sockets", O["sockets"], C_BLACK, "plastic", 10, "internal", eo)
    add("12 V socket caps", O["socket_caps"], C_RUBBER, "rubber", 10, "internal", eo)
    add("Battery monitor", O["monitor"], C_BLACK, "plastic", 12, "internal", eo)
    add("Battery monitor display (lit)", O["monitor_screen"], C_LIT_TEAL, "emissive", 12, "internal", eo)
    add("Battery monitor keys", O["monitor_keys"], C_RUBBER, "rubber", 12, "internal", eo)
    add("GFCI duplex outlet", O["ac_face"], C_OFFWHITE, "plastic", 11, "internal", eo)
    add("GFCI test button", O["gfci_test"], C_BLACK, "plastic", 11, "internal", eo)
    add("GFCI reset button", O["gfci_reset"], C_RED, "plastic", 11, "internal", eo)
    add("In-use cover, clear", O["cover"], C_WINDOW, "clear", 11, "internal", (860, 0, 200))
    add("Battery isolator base", O["iso_base"], C_PANEL, "plastic", 12, "internal", eo)
    add("Battery isolator knob", O["iso_knob"], C_RED, "plastic", 12, "internal", eo)
    add("Inverter switch bezel", O["rocker_bezel"], C_PANEL, "plastic", 9, "internal", eo)
    add("Inverter switch rocker", O["rocker"], C_BLACK, "plastic", 9, "internal", eo)
    add("Inverter on indicator (lit)", O["inv_lamp"], C_LIT_GREEN, "emissive", 9, "internal", eo)
    cab, gl = _cables(P, D)
    add("Battery cables", cab, C_BLACK, "rubber", 17, "internal", (190, 0, 210))
    add("Cable glands", gl, C_RUBBER, "plastic", 17, "internal", (190, 0, 210))

    # ---- context: ground patch and the shared clay mannequin, standing beside the cart
    add("Ground patch", _ground(), C_GROUND, "rubber", None, "context", (0, 0, 0))
    from context_parts import mannequin
    person = Pos(PERSON_AT[0], PERSON_AT[1], 0) * Rot(0, 0, PERSON_ROT) * mannequin(1750, "stand")
    add("Person, 1.75 m (scale)", person, C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:45s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1e6:8.3f} dm3")
