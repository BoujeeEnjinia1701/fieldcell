"""FieldCell parametric model (build123d), TRL 3, constructable design (FCL-DDR-003).

Run from the repo root:  python cad/src/model.py            exports STEP and STL, prints key figures
                         python cad/src/model.py --check    prints the constructability checks only
Exports into cad/step and cad/stl:
    fieldcell-deployed.step / .stl   whole cart, parked, wings folded out on their outriggers
    fieldcell-stowed.step / .stl     whole cart, wings up as the cart sides and tied together (travel)
    frame.step, pv-wing.step, battery-enclosure.step, electronics-enclosure.step (and .stl)

Rev for DDR-002 (2026-09-25): hinge line raised on a 20 mm spacer angle; reflective sun shade.
Rev for DDR-003 (2026-09-30, design for construction): every part is now something that can be
cut, bent, welded, drilled or bought, and every part touches and is fixed to its neighbours:
    deck sheet on top of the cross tubes (tubes 5 mm lower, deck top unchanged at 460 mm);
    rail end caps; axle brackets stop at the rail and are braced by gussets; a longer axle with
    spacer collars, washers and linch pins, wheels with a 20 mm bore;
    stand legs under the rails on welded clevises with pivot bolts, folding inward;
    handle sockets welded on the rail ends with gussets, handle legs pinned in them;
    hinge spacer angle bolted to steel tabs welded on the rails; real hinge leaves and knuckle,
    pin 4.5 mm above the panel face so the panel sits where the concept put it;
    PV wing as a module bonded on a frame of aluminium rectangular tube with three ribs;
    outrigger legs on clevis brackets under the wing's outer edge, folding under the wing;
    two tie bars that hold the stowed wings together at the top (over-centre latch and keeper);
    sun shade on four uprights bolted to tabs on the rails (it lifts off to open the battery case);
    electronics box moved 30 mm toward the handle (60 mm between the boxes for the cable glands),
    contents on its mounting plate, outlets, isolator, filter fan and exhaust filter through
    cut-outs; class T fuse inside the battery case; battery case and bin strapped to the deck.

Axes: X along the cart (handle toward +X), Y across the cart, Z up, ground at Z = 0.
The same PARAMS feed docs/04-calcs/sizing.py (FCL-CAL-001).
"""
import math
import sys
from math import radians, sin, cos
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # cart frame (welded steel square tube, decided 2026-09-25)
    "deck_l": 1200.0, "deck_w": 600.0,       # frame footprint (outside of the rails)
    "rail": 40.0, "rail_wall": 1.5,          # 40 x 40 x 1.5 mm square tube
    "deck_z": 460.0,                         # deck top when parked level on the stand legs
    "deck_t": 5.0,                           # expanded-metal deck sheet, laid on the cross tubes between the rails
    "cap_t": 3.0,                            # steel end cap on each rail end
    # wheels and axle
    "wheel_r": 203.0, "wheel_w": 90.0,       # 16 in (406 mm) flat-free tyre
    "wheel_y": 360.0,                        # wheel center from cart center line (track 720 mm)
    "hub_w": 60.0, "rim_r": 148.0,           # hub length and rim radius
    "axle_x": 30.0, "axle_d": 20.0,          # axle position from deck center, solid axle diameter
    "bracket_y": 290.0,                      # axle bracket plane from center line
    "brk": (60.0, 5.0, 35.0),                # axle bracket plate width, thickness, depth below the axle centre
    "gusset": (87.0, 85.0, 5.0),             # bracket gusset legs (across, down) and thickness
    "axle_end": 410.0,                       # axle end from center line (washer and linch pin outside the hub)
    # handle (detachable, in sockets on the rail ends)
    "grip_x": 1270.0, "grip_z": 900.0, "handle_d": 28.0, "grip_d": 32.0,
    "socket": (33.7, 2.6, 120.0),            # socket tube OD, wall, length along the handle leg
    "socket_x": 545.0,                       # where the socket axis meets the rail top (one radius up)
    # stand legs and outriggers
    "leg_d": 25.0, "leg_x": 560.0, "leg_y": 280.0,   # under the rail centre line
    "leg_pivot_z": 380.0, "foot": (60.0, 5.0),       # pivot height; foot plate side and thickness
    "clevis_t": 3.0,                                 # stand leg clevis plate thickness
    "out_d": 25.0, "out_x": 620.0, "out_pivot": (670.0, -55.0),   # outrigger pivot in the wing frame (u, v)
    "out_foot": (50.0, 4.0),
    # PV wings (2 x 200 W semi-flexible module bonded on an aluminium frame)
    "pv_l": 1400.0, "pv_w": 700.0, "pv_t": 35.0,
    "pv_tube": (30.0, 20.0, 1.5),            # frame tube depth, width, wall
    "rib_x": (-350.0, 0.0, 350.0),           # cross ribs
    "module_t": 5.0, "module_inset": 10.0,   # module plus bonding tape; rim left round the module
    "hinge_y": 330.0, "hinge_z": 490.0,      # inner top edge of the deployed wing (as in the concept)
    "pin": (-0.75, 4.5),                      # hinge pin from that edge, in the wing frame (u, v)
    "hinge_l": 1200.0, "leaf": (26.0, 1.5), "knuckle_r": 4.0,
    "spacer": 20.0, "spacer_t": 2.0,         # 20 x 20 x 2 mm aluminium angle (DDR-002)
    "tab": (30.0, 3.0), "tab_x": (-540.0, -180.0, 180.0, 540.0),   # steel tabs that carry the angle
    "tilt": 15.0,                            # deployed wing tilt below horizontal
    # tie bars that hold the stowed wings together
    "tie": 20.0, "tie_x": 665.0, "tie_pivot": (710.0, -45.0),
    # enclosures and main parts (outer envelopes)
    "batt_box": (420.0, 360.0, 300.0),       # IP65 battery case, centered over the deck center
    "batt_x": 0.0,
    "pack": (330.0, 175.0, 220.0),           # 25.6 V 50 Ah LiFePO4 pack
    "ebox": (320.0, 460.0, 300.0),           # IP54 electronics enclosure, outlet face toward the handle
    "ebox_margin": -10.0,                    # box end this far from the frame end (concept had -20, DDR-003)
    "lid_h": 40.0,
    "bin": (320.0, 460.0, 240.0),            # accessory and cable bin at the far end
    "wall": 6.0,                             # wall thickness of enclosures
    "fan": (125.0, 125.0, 20.0),             # IP54 filter fan (intake, +Y wall) and exhaust filter (-Y wall)
    "gland_y": 40.0, "gland_h": 150.0,       # battery cable glands: either side of centre, height above the deck
    # reflective sun shade over both enclosures (DDR-002): x from, x to, width, gap above the enclosure tops
    "shade": (-230.0, 600.0, 580.0, 50.0), "shade_t": 1.0, "shade_tube": 20.0,
    "up_x": (-200.0, 500.0), "up_y": 280.0,  # shade uprights on the rails
    "strap": (25.0, 1.5), "strap_x": (-120.0, 120.0),
}


# ------------------------------------------------------------------ geometry helpers
def _b():
    import build123d as b
    return b


def _tube(p1, p2, r):
    from build123d import Solid, Plane, Vector
    v = Vector(*p2) - Vector(*p1)
    return Solid.make_cylinder(r, v.length, Plane(origin=p1, z_dir=v))


def _hollow(p1, p2, ro, ri):
    return _tube(p1, p2, ro) - _tube(p1, p2, ri)


def box(x0, x1, y0, y1, z0, z1):
    b = _b()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)


def xcyl(x0, x1, y, z, r):
    return _tube((x0, y, z), (x1, y, z), r)


def ycyl(y0, y1, x, z, r):
    return _tube((x, y0, z), (x, y1, z), r)


def zcyl(z0, z1, x, y, r):
    return _tube((x, y, z0), (x, y, z1), r)


def _shell(lx, ly, lz, t, open_top=False):
    from build123d import Box, Pos
    outer = Box(lx, ly, lz)
    inner = Pos(0, 0, t if open_top else 0) * Box(lx - 2 * t, ly - 2 * t, lz - (t if open_top else 2 * t))
    return outer - inner


def _comp(*shapes):
    from build123d import Compound
    return Compound(children=[s for s in shapes if s is not None])


def _fuse(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def _face_yz(pts):
    b = _b()
    return b.Face(b.Wire.make_polygon([b.Vector(0, y, z) for y, z in pts], close=True))


def _face_xz(pts, y):
    b = _b()
    return b.Face(b.Wire.make_polygon([b.Vector(x, y, z) for x, z in pts], close=True))


def _prism_xz(pts, y0, y1):
    b = _b()
    return b.extrude(_face_xz(pts, y0), amount=y1 - y0, dir=(0, 1, 0))


def _prism_yz(pts, x0, x1):
    b = _b()
    f = _face_yz(pts)
    return b.Pos(x0, 0, 0) * b.extrude(f, amount=x1 - x0, dir=(1, 0, 0))


def rot_x(shape, deg, y, z):
    """Rotate about a line parallel to X through (y, z); +deg turns +Y toward +Z."""
    b = _b()
    return b.Pos(0, y, z) * b.Rot(deg, 0, 0) * b.Pos(0, -y, -z) * shape


def rot_y(shape, deg, x, z):
    """Rotate about a line parallel to Y through (x, z); +deg turns +Z toward +X."""
    b = _b()
    return b.Pos(x, 0, z) * b.Rot(0, deg, 0) * b.Pos(-x, 0, -z) * shape


def mirror_y(shape):
    b = _b()
    return shape.mirror(b.Plane.XZ)


def mirror_x(shape):
    b = _b()
    return shape.mirror(b.Plane.YZ)


# ------------------------------------------------------------------ derived positions
def derived(P=PARAMS):
    """Positions that other parts and the calc note depend on."""
    d = {}
    d["tube_top"] = P["deck_z"] - P["deck_t"]                 # rails and cross tubes sit under the deck sheet
    d["rail_z"] = d["tube_top"] - P["rail"] / 2
    d["rail_bot"] = d["tube_top"] - P["rail"]
    d["ebox_x"] = P["deck_l"] / 2 + P["ebox_margin"] - P["ebox"][0] / 2
    d["bin_x"] = -P["deck_l"] / 2 + 20 + P["bin"][0] / 2
    t = radians(P["tilt"])
    d["t"] = (cos(t), -sin(t))          # wing frame u axis in (y, z), right wing, deployed
    d["n"] = (sin(t), cos(t))           # wing frame v axis
    pu, pv = P["pin"]
    d["pin_y"] = P["hinge_y"] + pu * d["t"][0] + pv * d["n"][0]
    d["pin_z"] = P["hinge_z"] + pu * d["t"][1] + pv * d["n"][1]
    d["stow_deg"] = 90.0 + P["tilt"]   # wing turns this far about the pin from deployed to stowed
    ou, ov = P["out_pivot"]
    d["out_y"] = P["hinge_y"] + ou * d["t"][0] + ov * d["n"][0]
    d["out_pz"] = P["hinge_z"] + ou * d["t"][1] + ov * d["n"][1]
    d["out_top"] = d["out_pz"]                                   # outrigger pivot height, deployed
    d["out_len"] = d["out_pz"] - P["out_foot"][1] + 10.0        # leg tube: foot plate to 10 mm past the pivot
    d["span"] = 2 * (P["hinge_y"] + P["pv_w"] * cos(t))
    d["edge_z"] = P["hinge_z"] - P["pv_w"] * sin(t)
    # clearance between the deployed wing underside and the tyre top, at the tyre outer edge
    y_out = P["wheel_y"] + P["wheel_w"] / 2
    s = (y_out - P["hinge_y"]) / cos(t)
    d["wing_tyre_gap"] = (P["hinge_z"] - s * sin(t) - P["pv_t"] / cos(t)) - 2 * P["wheel_r"]
    # spacer angle and tabs
    d["angle_top"] = d["pin_z"] - P["leaf"][1] / 2
    # socket axis
    sx, so = P["socket_x"], P["socket"][0] / 2
    a = (sx, P["leg_y"], d["tube_top"] + so)
    g = (P["grip_x"], P["leg_y"] - 40.0, P["grip_z"])
    v = [g[i] - a[i] for i in range(3)]
    L = math.sqrt(sum(c * c for c in v))
    d["sock_a"], d["sock_d"] = a, tuple(c / L for c in v)
    d["sock_slope"] = math.degrees(math.atan2(v[2], math.hypot(v[0], v[1])))
    d["handle_leg"] = L
    return d


# ------------------------------------------------------------------ the wing frame (right wing, deployed)
def _wing_plane(P, D):
    from build123d import Plane
    return Plane(origin=(0, P["hinge_y"], P["hinge_z"]), x_dir=(1, 0, 0), z_dir=(0, D["n"][0], D["n"][1]))


def _local(P, D, shape):
    """Wing-frame (x, u, v) solid to world, right wing deployed."""
    return _wing_plane(P, D).from_local_coords(shape)


def _wing_local_parts(P, D):
    """Right wing in its own frame: x along the cart, u across the panel from its inner edge, v up
    from the panel face (the frame is below, v < 0)."""
    L, W, T = P["pv_l"], P["pv_w"], P["pv_t"]
    td, tw, _ = P["pv_tube"]
    mt, mi = P["module_t"], P["module_inset"]
    v0, v1 = -T, -T + td                     # frame tube depth band (-35 to -5)
    frame = _fuse([
        box(-L / 2, L / 2, 0, tw, v0, v1),                 # inner long member (hinge side)
        box(-L / 2, L / 2, W - tw, W, v0, v1),             # outer long member
        box(-L / 2, -L / 2 + tw, tw, W - tw, v0, v1),      # end members
        box(L / 2 - tw, L / 2, tw, W - tw, v0, v1),
        *[box(x - tw / 2, x + tw / 2, tw, W - tw, v0, v1) for x in P["rib_x"]],
    ])
    module = box(-L / 2 + mi, L / 2 - mi, mi, W - mi, -mt, 0)
    # hinge leaf on the inner face of the inner member, knuckle round the pin
    pu, pv = P["pin"]
    lw, lt = P["leaf"]
    hl = P["hinge_l"]
    leaf_b = box(-hl / 2, hl / 2, pu - lt / 2, pu + lt / 2, pv - lw, pv)
    knuckle = xcyl(-hl / 2, hl / 2, pu, pv, P["knuckle_r"])
    # outrigger clevis brackets under the outer member
    ou, ov = P["out_pivot"]
    r = P["out_d"] / 2
    brk, bolts = [], []
    for x in (-P["out_x"], P["out_x"]):
        brk.append(box(x - r - 3.5, x + r + 3.5, ou - 15, W, v0 - 3, v0))      # U bracket: web under the member
        for s in (-1, 1):
            c0 = x + s * (r + 0.5)
            brk.append(box(min(c0, c0 + 3 * s), max(c0, c0 + 3 * s), ou - 15, ou + 15, ov - 12, v0 - 3))
        bolts.append(xcyl(x - r - 6, x + r + 6, ou, ov, 4.0))
    # tie bar pivot brackets (used on the left wing) and latch keepers (right wing)
    tu, tv = P["tie_pivot"]
    tie_brk, keepers = [], []
    for s in (-1, 1):
        x = s * P["tie_x"]
        e0 = x + s * P["tie"] / 2
        tie_brk.append(box(min(e0, e0 + 3 * s), max(e0, e0 + 3 * s), tu - 20, tu + 15, tv - 15, v0))   # ear
        b0 = e0 + 3 * s
        tie_brk.append(box(min(b0, s * L / 2), max(b0, s * L / 2), W - tw, W, v0 - 3, v0))            # base on the back face
        keepers.append(box(x - P["tie"] / 2, x + P["tie"] / 2, W, W + 8, -32, -18))
    return dict(frame=frame, module=module, leaf_b=leaf_b, knuckle=knuckle, out_brk=_fuse(brk),
                out_bolts=_fuse(bolts), tie_brk=_fuse(tie_brk), keepers=_fuse(keepers))


def _outrigger_world(P, D, folded):
    """Right wing outrigger legs and feet in world coordinates, wing deployed. folded: legs swung
    under the wing (the way they travel)."""
    r = P["out_d"] / 2
    fs, ft = P["out_foot"]
    py, pz = D["out_y"], D["out_pz"]
    legs = []
    for x in (-P["out_x"], P["out_x"]):
        leg = zcyl(ft, pz + 10.0, x, py, r)
        foot = box(x - fs / 2, x + fs / 2, py - fs / 2, py + fs / 2, 0, ft)
        sx = 1 if x > 0 else -1          # stake loop points along the cart, so the folded leg lies flat
        lx0, lx1 = sorted((x + sx * fs / 2, x + sx * (fs / 2 + 28)))
        loop = box(lx0, lx1, py - 15, py + 15, 0, ft) - zcyl(-1, ft + 1, x + sx * (fs / 2 + 15), py, 5.5)
        legs.append(leg + foot + loop)
    out = _fuse(legs)
    if folded:
        out = rot_x(out, -(90.0 + P["tilt"]), py, pz)
    return out


def _tie_bar_world(P, D, across):
    """Right-built tie bar (mirrored onto the left wing) with its latch body, wing deployed.
    across=False: folded under the wing; True: the pose it takes once the wing is stowed."""
    tu, tv = P["tie_pivot"]
    a = P["tie"]
    # bar length from the stowed geometry: pivot to just short of the other wing's keeper
    ys = _stowed_face_y(P, D)
    yp = _stowed_point(P, D, tu, tv)[0]
    L = (yp + 10.0) + (ys + 6.0)
    bars, latches = [], []
    for s in (-1, 1):
        x = s * P["tie_x"]
        bar = box(x - a / 2, x + a / 2, tu + 10.0 - L, tu + 10.0, tv - a / 2, tv + a / 2)
        latch = box(x - a / 2, x + a / 2, tu + 10.0 - L - 12.0, tu + 10.0 - L, tv - a / 2, tv + a / 2)
        bars.append(bar)
        latches.append(latch)
    bar, latch = _local(P, D, _fuse(bars)), _local(P, D, _fuse(latches))
    if across:
        py, pz = _local_pt(P, D, tu, tv)
        bar, latch = rot_x(bar, -90.0, py, pz), rot_x(latch, -90.0, py, pz)
    return bar, latch


def _local_pt(P, D, u, v):
    return (P["hinge_y"] + u * D["t"][0] + v * D["n"][0], P["hinge_z"] + u * D["t"][1] + v * D["n"][1])


def _stowed_point(P, D, u, v):
    """World (y, z) of wing point (u, v) once the right wing is stowed."""
    y, z = _local_pt(P, D, u, v)
    a = radians(D["stow_deg"])
    dy, dz = y - D["pin_y"], z - D["pin_z"]
    return (D["pin_y"] + dy * cos(a) - dz * sin(a), D["pin_z"] + dy * sin(a) + dz * cos(a))


def _stowed_face_y(P, D):
    """World y of the stowed right wing's module face (its inside face)."""
    return _stowed_point(P, D, 300.0, 0.0)[0]


# ------------------------------------------------------------------ components
class Comp:
    def __init__(self, key, name, shape, bom, group=None):
        self.key, self.name, self.shape, self.bom, self.group = key, name, shape, bom, group


def build_components(P=PARAMS, deployed=True):
    """Every component as {key: Comp}, in build order. deployed=False gives the travel pose."""
    from build123d import Box, Cylinder, Pos, Rot
    D = derived(P)
    C = {}

    def add(key, name, shape, bom, group=None):
        C[key] = Comp(key, name, shape, bom, group)

    L, Wd, R, rt = P["deck_l"], P["deck_w"], P["rail"], P["rail_wall"]
    tt, rb, rz = D["tube_top"], D["rail_bot"], D["rail_z"]
    yr = Wd / 2 - R / 2                       # rail centre line

    # ---- 1 frame weldment
    def sq_tube(x0, x1, y0, y1):
        o = box(x0, x1, y0, y1, rb, tt)
        if x1 - x0 > y1 - y0:
            i = box(x0 - 1, x1 + 1, y0 + rt, y1 - rt, rb + rt, tt - rt)
        else:
            i = box(x0 + rt, x1 - rt, y0 - 1, y1 + 1, rb + rt, tt - rt)
        return o - i
    rails = [sq_tube(-L / 2, L / 2, s * yr - R / 2, s * yr + R / 2) for s in (-1, 1)]
    cross = [sq_tube(x - R / 2, x + R / 2, -Wd / 2 + R, Wd / 2 - R) for x in (-L / 2 + R / 2, 0, L / 2 - R / 2)]
    ct = P["cap_t"]
    caps = [box(*sorted((sx * L / 2, sx * (L / 2 + ct))), s * yr - R / 2, s * yr + R / 2, rb, tt)
            for s in (-1, 1) for sx in (-1, 1)]
    add("tubes", "Frame tubes and end caps", _fuse(rails + cross + caps), 1, "frame")
    add("deck", "Deck sheet", box(-L / 2, L / 2, -Wd / 2 + R, Wd / 2 - R, tt, P["deck_z"]), 1, "frame")
    # axle brackets and gussets
    bw, bt, bd = P["brk"]
    ax, ar, wr = P["axle_x"], P["axle_d"] / 2, P["wheel_r"]
    by = P["bracket_y"]
    brks, gus = [], []
    for s in (-1, 1):
        y0, y1 = sorted((s * (by - bt / 2), s * (by + bt / 2)))
        brks.append(box(ax - bw / 2, ax + bw / 2, y0, y1, wr - bd, rb) - ycyl(y0 - 1, y1 + 1, ax, wr, ar))
        ga, gb, gt = P["gusset"]
        yi = s * (by - bt / 2)
        pts = [(yi, rb), (yi - s * ga, rb), (yi, rb - gb)]
        gus.append(_prism_yz(pts, 4.0, 4.0 + gt))
    add("brackets", "Axle brackets and gussets", _fuse(brks + gus), 1, "frame")
    # hinge tabs
    tw_, tth = P["tab"]
    tabs = []
    for s in (-1, 1):
        for x in P["tab_x"]:
            y0, y1 = sorted((s * Wd / 2, s * (Wd / 2 + tth)))
            tabs.append(box(x - tw_ / 2, x + tw_ / 2, y0, y1, rb + 4.0, D["angle_top"]))
    add("tabs", "Hinge tabs (8)", _fuse(tabs), 1, "frame")
    # handle sockets and gussets
    so, sw, sl = P["socket"]
    a, d = D["sock_a"], D["sock_d"]
    sockets, sg = [], []
    for s in (-1, 1):
        a_ = (a[0], s * a[1], a[2])
        d_ = (d[0], s * d[1], d[2])
        p0 = tuple(a_[i] - 25.0 * d_[i] for i in range(3))
        p1 = tuple(a_[i] + sl * d_[i] for i in range(3))
        tube = _hollow(p0, p1, so / 2, so / 2 - sw) & box(a_[0] - 200, a_[0] + 300, s * a[1] - 60, s * a[1] + 60, tt, tt + 400)
        sockets.append(tube)
        x0 = L / 2 + ct
        k = d[2] / d[0]
        zt = lambda x: a[2] + (x - a[0]) * k - (so / 2) / (d[0] / math.hypot(d[0], d[2]))  # noqa: E731
        pts = [(x0, rb), (x0, zt(x0) + 1.0), (x0 + 40.0, zt(x0 + 40.0) + 1.0)]
        g = _prism_xz(pts, s * a[1] - 2.0, s * a[1] + 2.0)
        g = g - _tube(p0, p1, so / 2)
        sg.append(g)
    add("sockets", "Handle sockets and gussets", _fuse(sockets + sg), 1, "frame")
    # stand leg clevises
    lr = P["leg_d"] / 2
    clev = []
    for sx in (-1, 1):
        for s in (-1, 1):
            for e in (-1, 1):
                c0 = s * P["leg_y"] + e * (lr + 0.5)
                y0, y1 = sorted((c0, c0 + e * P["clevis_t"]))
                clev.append(box(sx * P["leg_x"] - 20, sx * P["leg_x"] + 20, y0, y1, P["leg_pivot_z"] - 20, rb))
    add("clevises", "Stand leg clevises (4 pairs)", _fuse(clev), 1, "frame")
    # shade upright tabs
    ub = []
    for x in P["up_x"]:
        for s in (-1, 1):
            y0 = s * (P["up_y"] + P["shade_tube"] / 2)
            ub.append(box(x - 10, x + 10, min(y0, y0 + 3 * s), max(y0, y0 + 3 * s), tt, tt + 60))
    add("up_tabs", "Shade upright tabs (4)", _fuse(ub), 1, "frame")

    # ---- axle, wheels and their hardware
    ae = P["axle_end"]
    add("axle", "Axle", ycyl(-ae, ae, ax, wr, ar), 1, "frame")
    hub0, hub1 = P["wheel_y"] - P["hub_w"] / 2, P["wheel_y"] + P["hub_w"] / 2
    hw = []
    for s in (-1, 1):
        y_in = by + bt / 2
        hw.append(ycyl(min(s * y_in, s * hub0), max(s * y_in, s * hub0), ax, wr, 13.0) - ycyl(-ae, ae, ax, wr, ar))
        hw.append(ycyl(min(s * hub1, s * (hub1 + 3)), max(s * hub1, s * (hub1 + 3)), ax, wr, 18.0) - ycyl(-ae, ae, ax, wr, ar))
        hw.append(zcyl(wr - 25, wr + 25, ax, s * (hub1 + 10), 2.25))
    add("axle_hw", "Spacer collars, washers, linch pins", _fuse(hw), 2)

    def wheel(s):
        y0, y1 = sorted((s * (P["wheel_y"] - P["wheel_w"] / 2), s * (P["wheel_y"] + P["wheel_w"] / 2)))
        h0, h1 = sorted((s * hub0, s * hub1))
        tyre = ycyl(y0, y1, ax, wr, wr) - ycyl(y0 - 1, y1 + 1, ax, wr, P["rim_r"])
        hub = ycyl(h0, h1, ax, wr, P["rim_r"]) - ycyl(h0 - 1, h1 + 1, ax, wr, ar)
        return tyre + hub
    add("wheel_l", "Wheel", wheel(-1), 2)
    add("wheel_r", "Wheel, far side", wheel(1), 2)

    # ---- 4 stand legs (down when parked, folded inward under the rails in travel)
    fs, ft = P["foot"]
    pz = P["leg_pivot_z"]
    legs, lbolts = [], []
    for sx in (-1, 1):
        for s in (-1, 1):
            x, y = sx * P["leg_x"], s * P["leg_y"]
            leg = zcyl(ft, pz + 12.0, x, y, lr) + box(x - fs / 2, x + fs / 2, y - fs / 2, y + fs / 2, 0, ft)
            if not deployed:
                leg = rot_y(leg, sx * 90.0, x, pz)
            legs.append(leg)
            lbolts.append(ycyl(y - lr - 9, y + lr + 9, x, pz, 5.0))
    add("legs", "Stand legs (4)", _fuse(legs), 4)
    add("leg_bolts", "Stand leg pivot bolts", _fuse(lbolts), 4)

    # ---- 3 handle
    hr = P["handle_d"] / 2
    hl = []
    for s in (-1, 1):
        a_ = (a[0], s * a[1], a[2])
        d_ = (d[0], s * d[1], d[2])
        p0 = tuple(a_[i] + 5.0 * d_[i] for i in range(3))     # leg end sits 5 mm up the socket, clear of the rail
        g = (P["grip_x"], s * (P["leg_y"] - 40.0), P["grip_z"])
        hl.append(_tube(p0, g, hr))
    hl.append(ycyl(-(P["leg_y"] - 20), P["leg_y"] - 20, P["grip_x"], P["grip_z"], P["grip_d"] / 2))
    add("handle", "Handle", _fuse(hl), 3)
    pins = []
    for s in (-1, 1):
        c = tuple((a[0], s * a[1], a[2])[i] + 120.0 * (d[0], s * d[1], d[2])[i] for i in range(3))
        pins.append(ycyl(c[1] - 25, c[1] + 25, c[0], c[2], 3.0))
    add("handle_pins", "Handle quick-release pins", _fuse(pins), 3)

    # ---- 14 hinge spacer angles, fixed leaves and knuckles
    sp, st = P["spacer"], P["spacer_t"]
    at = D["angle_top"]
    ang = []
    for s in (-1, 1):
        y0 = Wd / 2 + tth
        h = box(-L / 2, L / 2, y0, y0 + sp, at - st, at)
        v = box(-L / 2, L / 2, y0, y0 + st, at - sp, at)
        sh = h + v
        ang.append(sh if s > 0 else mirror_y(sh))
    add("spacers", "Hinge spacer angles (2)", _fuse(ang), 14)

    # ---- wings (right built, left mirrored)
    W = _wing_local_parts(P, D)
    lw, lt = P["leaf"]
    hlen = P["hinge_l"]
    leaf_a = box(-hlen / 2, hlen / 2, D["pin_y"] - lw, D["pin_y"] - P["knuckle_r"], at, at + lt)

    def wing_state(shape_world):
        return shape_world if deployed else rot_x(shape_world, D["stow_deg"], D["pin_y"], D["pin_z"])

    def both(shape_right, left=True, right=True):
        out = []
        if right:
            out.append(shape_right)
        if left:
            out.append(mirror_y(shape_right))
        return _fuse(out)

    wf = wing_state(_local(P, D, W["frame"]))
    md = wing_state(_local(P, D, W["module"]))
    lb = wing_state(_local(P, D, W["leaf_b"] + W["knuckle"]))
    add("hinge_l", "Hinges (2), fixed and moving leaves", both(leaf_a + lb), 14)
    add("wing_frames", "Wing frames (2)", both(wf), 13)
    add("modules", "PV modules, 200 W (2)", both(md), 13)
    ob = wing_state(_local(P, D, W["out_brk"]))
    add("out_brk", "Outrigger brackets (4)", both(ob), 15)
    add("out_bolts", "Outrigger pivot bolts", both(wing_state(_local(P, D, W["out_bolts"]))), 15)
    add("outriggers", "Outrigger legs (4)", both(wing_state(_outrigger_world(P, D, folded=not deployed))), 15)
    add("tie_brk", "Tie bar pivot brackets (2)", mirror_y(wing_state(_local(P, D, W["tie_brk"]))), 19)
    add("keepers", "Latch keepers (2)", wing_state(_local(P, D, W["keepers"])), 14)
    bar, latch = _tie_bar_world(P, D, across=not deployed)
    add("tie_bars", "Tie bars (2)", mirror_y(wing_state(bar)), 19)
    add("latches", "Over-centre latches (2)", mirror_y(wing_state(latch)), 14)

    # ---- 5, 6 battery case, pack and class T fuse
    bb, pk, t = P["batt_box"], P["pack"], P["wall"]
    bx0 = P["batt_x"]
    z0 = P["deck_z"]
    lh = P["lid_h"]
    gy, gh = P["gland_y"], P["gland_h"]
    bxa, bxb = bx0 - bb[0] / 2, bx0 + bb[0] / 2
    case = Pos(bx0, 0, z0 + bb[2] / 2) * _shell(*bb, t)
    holes = _fuse([xcyl(bxb - t - 1, bxb + 1, s * gy, z0 + gh, 12.75) for s in (-1, 1)])
    body = (case & box(bxa - 1, bxb + 1, -bb[1], bb[1], z0, z0 + bb[2] - lh)) - holes
    lid = case & box(bxa - 1, bxb + 1, -bb[1], bb[1], z0 + bb[2] - lh, z0 + bb[2])
    add("batt_body", "Battery case", body, 5)
    add("batt_lid", "Battery case lid", lid, 5)
    add("pack", "LiFePO4 pack, 25.6 V 50 Ah", box(bx0 - pk[0] / 2, bx0 + pk[0] / 2, -pk[1] / 2, pk[1] / 2, z0 + t, z0 + t + pk[2]), 6)
    # class T fuse beside the pack at the gland end, within 150 mm of the positive terminal
    add("fuse_t", "Class T fuse and holder", box(bxb - t - 10 - 60, bxb - t - 10, pk[1] / 2 + 8, pk[1] / 2 + 58, z0 + t, z0 + t + 45), 12)
    sw_, stt = P["strap"]
    straps = []
    hw2 = bb[1] / 2
    for x in P["strap_x"]:
        xa, xb = bx0 + x - sw_ / 2, bx0 + x + sw_ / 2
        straps += [box(xa, xb, -hw2 - stt, hw2 + stt, z0 + bb[2], z0 + bb[2] + stt),
                   box(xa, xb, hw2, hw2 + stt, tt - stt, z0 + bb[2] + stt),
                   box(xa, xb, -hw2 - stt, -hw2, tt - stt, z0 + bb[2] + stt),
                   box(xa, xb, -hw2 - stt, hw2 + stt, tt - stt, tt)]
    add("straps", "Cam straps (2)", _fuse(straps), 17)

    # ---- 7 to 12 electronics box and contents
    eb, ex = P["ebox"], D["ebox_x"]
    exa, exb = ex - eb[0] / 2, ex + eb[0] / 2
    ey = eb[1] / 2
    fx, fy, fz = P["fan"]
    ebox_shell = Pos(ex, 0, z0 + eb[2] / 2) * _shell(*eb, t)
    # outlet face parts (outside x exb..), bodies pass through cut-outs in the wall
    dc_body = box(exb - 60, exb, 40, 190, z0 + 80, z0 + 240)
    dc = dc_body + box(exb, exb + 6, 30, 200, z0 + 70, z0 + 250)
    ac_body = box(exb - 60, exb, -150, -90, z0 + 130, z0 + 240)
    ac = ac_body + box(exb, exb + 38, -165, -75, z0 + 120, z0 + 250)
    iso_body = box(exb - 45, exb, -55, -15, z0 + 160, z0 + 200)
    iso = iso_body + xcyl(exb, exb + 30, -35, z0 + 180, 20)
    fin_body = box(exa + 35, exa + 150, ey - 56, ey, z0 + 35, z0 + 150)
    fan_in = fin_body + box(exa + 30, exa + 155, ey, ey + 12, z0 + 30, z0 + 155)
    fout_body = box(exa + 155, exa + 270, -ey, -ey + 30, z0 + 130, z0 + 245)
    fan_out = fout_body + box(exa + 150, exa + 275, -ey - 12, -ey, z0 + 125, z0 + 250)
    gl_holes = _fuse([xcyl(exa - 1, exa + t + 1, s * gy, z0 + gh, 12.75) for s in (-1, 1)])
    pv_holes = _fuse([ycyl(s * (ey - t - 1), s * (ey + 1), exb - 30, z0 + 30, 8.25) for s in (-1, 1)])
    cut = _fuse([dc_body, ac_body, iso_body, fin_body, fout_body]) + gl_holes + pv_holes
    shell_cut = ebox_shell - cut
    ebody = shell_cut & box(exa - 1, exb + 1, -ey - 1, ey + 1, z0, z0 + eb[2] - lh)
    elid = shell_cut & box(exa - 1, exb + 1, -ey - 1, ey + 1, z0 + eb[2] - lh, z0 + eb[2])
    add("ebox_body", "Electronics box", ebody, 7)
    add("ebox_lid", "Electronics box lid", elid, 7)
    add("fan", "Filter fan and exhaust filter", fan_in + fan_out, 7)
    zi = z0 + t
    add("mplate", "Mounting plate", box(exa + t, exb - t, -ey + t, ey - t, zi, zi + 3), 7)
    zp = zi + 3
    add("inverter", "Inverter, 1 kW", box(exa + 20, exa + 290, -212, -2, zp, zp + 110), 9)
    add("mppt", "MPPT charge controller", box(exa + 20, exa + 170, 14, 154, zp, zp + 70), 8)
    add("fusing", "DIN rail: breakers and shunt", box(exa + 180, exa + 250, 14, 154, zp, zp + 90), 12)
    add("dc_panel", "DC outlet panel", dc, 10)
    add("ac_outlet", "AC outlet with GFCI and in-use cover", ac, 11)
    add("isolator", "Battery isolator", iso, 12)

    # glands and battery cables between the boxes, PV glands on the electronics box
    gl = []
    for s in (-1, 1):
        y = s * gy
        gl += [xcyl(bxb - t - 8, bxb - t, y, z0 + gh, 18.0), xcyl(bxb - t, bxb, y, z0 + gh, 12.75),
               xcyl(bxb, bxb + 22, y, z0 + gh, 16.0),
               xcyl(exa - 22, exa, y, z0 + gh, 16.0), xcyl(exa, exa + t, y, z0 + gh, 12.75),
               xcyl(exa + t, exa + t + 8, y, z0 + gh, 18.0)]
        yo = s * ey
        gl += [ycyl(min(yo, yo + 15 * s), max(yo, yo + 15 * s), exb - 30, z0 + 30, 11.0),
               ycyl(min(yo, yo - t * s), max(yo, yo - t * s), exb - 30, z0 + 30, 8.25),
               ycyl(min(yo - t * s, yo - (t + 8) * s), max(yo - t * s, yo - (t + 8) * s), exb - 30, z0 + 30, 12.0)]
    cables = _fuse([xcyl(bxb - 30, exa + 18, s * gy, z0 + gh, 5.5) for s in (-1, 1)])
    add("glands", "Cable glands", _fuse(gl) - cables, 17)
    add("cables", "Battery cables, 16 mm2", cables, 17)

    # ---- 18 sun shade on four uprights
    sx0, sx1, swd, gap = P["shade"]
    top = z0 + max(bb[2], eb[2])
    zs = top + gap
    st_ = P["shade_tube"]
    ups = []
    for x in P["up_x"]:
        for s in (-1, 1):
            yc = s * P["up_y"]
            o = box(x - st_ / 2, x + st_ / 2, yc - st_ / 2, yc + st_ / 2, tt, zs)
            i = box(x - st_ / 2 + 1.5, x + st_ / 2 - 1.5, yc - st_ / 2 + 1.5, yc + st_ / 2 - 1.5, tt - 1, zs + 1)
            ups.append(o - i)
    add("uprights", "Shade uprights (4)", _fuse(ups), 18)
    yo = swd / 2
    sframe = _fuse([box(sx0, sx1, yo - st_, yo, zs, zs + st_), box(sx0, sx1, -yo, -yo + st_, zs, zs + st_),
                    box(sx0, sx0 + st_, -yo + st_, yo - st_, zs, zs + st_), box(sx1 - st_, sx1, -yo + st_, yo - st_, zs, zs + st_),
                    box((sx0 + sx1) / 2 - st_ / 2, (sx0 + sx1) / 2 + st_ / 2, -yo + st_, yo - st_, zs, zs + st_)])
    add("shade_frame", "Shade frame", sframe, 18)
    add("shade_fabric", "Shade fabric", box(sx0, sx1, -yo, yo, zs + st_, zs + st_ + P["shade_t"]), 18)

    # ---- 16 accessory bin and its strap
    bn = P["bin"]
    bxc = D["bin_x"]
    add("bin", "Accessory and cable bin", Pos(bxc, 0, z0 + bn[2] / 2) * _shell(*bn, t, open_top=True), 16)
    hb = bn[1] / 2
    xa, xb = bxc - sw_ / 2, bxc + sw_ / 2
    add("bin_strap", "Bin strap", _fuse([box(xa, xb, -hb - stt, hb + stt, z0 + bn[2], z0 + bn[2] + stt),
                                         box(xa, xb, hb, hb + stt, tt - stt, z0 + bn[2] + stt),
                                         box(xa, xb, -hb - stt, -hb, tt - stt, z0 + bn[2] + stt),
                                         box(xa, xb, -hb - stt, hb + stt, tt - stt, tt)]), 16)
    return C


FRAME_KEYS = ("tubes", "deck", "brackets", "tabs", "sockets", "clevises", "up_tabs", "axle")

# Concept media groups: (key, name, member components, BOM number)
GROUPS = [
    ("frame", "Cart frame and axle", FRAME_KEYS, 1),
    ("wheels", "Wheels, 16 in (2)", ("wheel_l", "wheel_r", "axle_hw"), 2),
    ("handle", "Handle", ("handle", "handle_pins"), 3),
    ("legs", "Stand legs (4)", ("legs", "leg_bolts"), 4),
    ("batt_box", "Battery enclosure", ("batt_body", "batt_lid"), 5),
    ("pack", "LiFePO4 pack, 25.6 V 50 Ah", ("pack",), 6),
    ("ebox", "Electronics enclosure with filter fan", ("ebox_body", "ebox_lid", "fan", "mplate"), 7),
    ("mppt", "MPPT charge controller", ("mppt",), 8),
    ("inverter", "Inverter, 1 kW", ("inverter",), 9),
    ("dc_panel", "DC outlet panel", ("dc_panel",), 10),
    ("ac_outlet", "AC outlet with GFCI", ("ac_outlet",), 11),
    ("fusing", "Fusing and disconnect", ("fusing", "isolator", "fuse_t"), 12),
    ("wings", "PV wings, 200 W (2)", ("wing_frames", "modules"), 13),
    ("hinges", "Hinges, spacers and latches", ("spacers", "hinge_l", "keepers", "latches"), 14),
    ("outriggers", "Outrigger legs (4)", ("outriggers", "out_brk", "out_bolts"), 15),
    ("bin", "Accessory and cable bin", ("bin", "bin_strap"), 16),
    ("wiring", "Cables, glands and straps", ("glands", "cables", "straps"), 17),
    ("shade", "Sun shade", ("uprights", "shade_frame", "shade_fabric"), 18),
    ("tie_bars", "Wing tie bars (2)", ("tie_bars", "tie_brk"), 19),
]


def build_parts(P=PARAMS, deployed=True):
    """[(key, name, shape, bom_no)] by BOM group, for the concept media."""
    C = build_components(P, deployed)
    return [(k, n, _comp(*[C[m].shape for m in mem]), bom) for k, n, mem, bom in GROUPS]


def build(P=PARAMS, deployed=True):
    """Whole assembly as one Compound."""
    C = build_components(P, deployed)
    return _comp(*[c.shape for c in C.values()])


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(P=PARAMS):
    """Pairs that must touch, or must stay apart by a clearance. Both poses are checked.
    Returns (description, overlap mm3, gap mm, expectation, ok)."""
    rows = []

    def chk(desc, a, b_, expect, tol=0.3):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1.0 and (gp <= tol if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    D = derived(P)
    for deployed in (True, False):
        C = build_components(P, deployed)
        S = lambda *ks: _fuse([C[k].shape for k in ks])  # noqa: E731
        tag = "parked" if deployed else "travel"
        if deployed:
            chk("Deck sheet on the cross tubes", S("deck"), S("tubes"), "touch")
            chk("Axle brackets under the rails", S("brackets"), S("tubes"), "touch")
            chk("Axle through the brackets", S("axle"), S("brackets"), "touch")
            chk("Hinge tabs on the rails", S("tabs"), S("tubes"), "touch")
            chk("Handle sockets on the rails", S("sockets"), S("tubes"), "touch")
            chk("Stand leg clevises under the rails", S("clevises"), S("tubes"), "touch")
            chk("Shade upright tabs on the rails", S("up_tabs"), S("tubes"), "touch")
            chk("Wheels on the axle (20 mm bore)", S("wheel_l", "wheel_r"), S("axle"), "touch")
            chk("Spacer collars between bracket and hub", S("axle_hw"), S("brackets"), "touch")
            chk("Wheels clear of the frame", S("wheel_l", "wheel_r"), S(*FRAME_KEYS[:-1]), 10.0)
            chk("Handle legs in their sockets (sliding fit)", S("handle"), S("sockets"), "touch")
            chk("Handle legs clear of the rails", S("handle"), S("tubes", "deck"), 2.0)
            chk("Handle clear of the electronics box", S("handle"), S("ebox_body", "ebox_lid", "ac_outlet", "dc_panel", "isolator"), 20.0)
            chk("Spacer angles on the hinge tabs", S("spacers"), S("tabs"), "touch")
            chk("Spacer angles clear of the rails", S("spacers"), S("tubes"), 0.5)
            chk("Hinge fixed leaves on the spacer angles", S("hinge_l"), S("spacers"), "touch")
            chk("Battery case on the deck", S("batt_body"), S("deck"), "touch")
            chk("Battery lid on the case", S("batt_lid"), S("batt_body"), "touch")
            chk("Pack on the case floor", S("pack"), S("batt_body"), "touch")
            chk("Class T fuse on the case floor", S("fuse_t"), S("batt_body"), "touch")
            chk("Class T fuse clear of the pack", S("fuse_t"), S("pack"), 5.0)
            chk("Electronics box on the deck", S("ebox_body"), S("deck"), "touch")
            chk("Electronics lid on the box", S("ebox_lid"), S("ebox_body"), "touch")
            chk("Mounting plate on the box floor", S("mplate"), S("ebox_body"), "touch")
            for k in ("inverter", "mppt", "fusing"):
                chk(f"{C[k].name} on the mounting plate", S(k), S("mplate"), "touch")
            inside = ("inverter", "mppt", "fusing", "dc_panel", "ac_outlet", "isolator", "fan")
            for i, k1 in enumerate(inside):
                for k2 in inside[i + 1:]:
                    chk(f"{C[k1].name} clear of {C[k2].name}", S(k1), S(k2), 4.0)
            for k in ("dc_panel", "ac_outlet", "isolator", "fan"):
                chk(f"{C[k].name} in its cut-out", S(k), S("ebox_body"), "touch")
            chk("Glands seated in both boxes", S("glands"), S("batt_body", "ebox_body"), "touch")
            mid = (P["batt_x"] + P["batt_box"][0] / 2 + D["ebox_x"] - P["ebox"][0] / 2) / 2
            chk("Gland domes clear of each other between the boxes", S("glands") & box(-500, mid, -300, 300, 0, 900),
                S("glands") & box(mid, 900, -300, 300, 0, 900), 12.0)
            chk("Battery case clear of the electronics box", S("batt_body", "batt_lid"), S("ebox_body", "ebox_lid"), 55.0)
            chk("Glands clear of the inverter", S("glands"), S("inverter"), 1.0)
            chk("Straps over the battery case", S("straps"), S("batt_lid"), "touch")
            chk("Shade uprights on the rails", S("uprights"), S("tubes"), "touch")
            chk("Shade uprights against their tabs", S("uprights"), S("up_tabs"), "touch")
            chk("Shade frame on the uprights", S("shade_frame"), S("uprights"), "touch")
            chk("Shade clear of the enclosures (air gap)", S("shade_frame", "shade_fabric"), S("batt_lid", "ebox_lid"), 45.0)
            chk("Shade uprights clear of the enclosures", S("uprights"), S("batt_body", "batt_lid", "ebox_body", "ebox_lid", "fan", "glands"), 15.0)
            chk("Bin on the deck", S("bin"), S("deck"), "touch")
            chk("Bin clear of the battery case", S("bin"), S("batt_body"), 10.0)
            chk("Deployed wing clear of the tyre (concept 28 mm)", S("wing_frames", "modules"), S("wheel_l", "wheel_r"), 25.0)
            chk("Outrigger feet on the ground", S("outriggers") & box(-2000, 2000, -2000, 2000, -1, 0.5), box(-2000, 2000, -2000, 2000, -10, 0), "touch")
            chk("Stand leg feet on the ground", S("legs") & box(-2000, 2000, -2000, 2000, -1, 0.5), box(-2000, 2000, -2000, 2000, -10, 0), "touch")
            chk("Folded tie bars clear of the frame and handle", S("tie_bars", "latches"), S(*FRAME_KEYS, "handle"), 3.0)
        chk(f"Moving leaves on the wing frames ({tag})", S("hinge_l"), S("wing_frames"), "touch")
        chk(f"Wings clear of the spacer angles ({tag})", S("wing_frames", "modules"), S("spacers", "tabs", "tubes"), 0.5)
        chk(f"Modules on the wing frames ({tag})", S("modules"), S("wing_frames"), "touch")
        chk(f"Outrigger brackets under the wing frames ({tag})", S("out_brk"), S("wing_frames"), "touch")
        chk(f"Outrigger legs clear of the wing frames ({tag})", S("outriggers"), S("wing_frames", "modules"), 2.0)
        chk(f"Tie bar brackets on the wing frame ({tag})", S("tie_brk"), S("wing_frames"), "touch")
        chk(f"Tie bars against their brackets ({tag})", S("tie_bars"), S("tie_brk"), "touch")
        chk(f"Tie bars clear of the outrigger legs ({tag})", S("tie_bars", "latches"), S("outriggers"), 2.0)
        chk(f"Wings clear of the shade ({tag})", S("wing_frames", "modules"), S("uprights", "shade_frame", "shade_fabric"), 30.0)
        chk(f"Wings clear of the wheels ({tag})", S("wing_frames", "modules", "outriggers"), S("wheel_l", "wheel_r"), 20.0)
        chk(f"Stand legs clear of the wheels and brackets ({tag})", S("legs"), S("wheel_l", "wheel_r", "brackets", "axle_hw"), 4.0)
        chk(f"Stand legs clear of the rails ({tag})", S("legs"), S("tubes"), 3.0)
        if not deployed:
            chk("Tie bars resting on both stowed wings", S("tie_bars"), S("wing_frames"), "touch")
            chk("Latches against the keepers", S("latches"), S("keepers"), "touch")
            chk("Keepers on the wing frame", S("keepers"), S("wing_frames"), "touch")
            chk("Stowed wings clear of the handle", S("wing_frames", "modules", "outriggers"), S("handle"), 15.0)
    return rows


def print_checks(P=PARAMS):
    rows = checks(P)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:62s} overlap {v:9.1f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


def key_figures(P=PARAMS):
    D = derived(P)
    Cs = build_components(P, deployed=False)
    stow = _comp(*[c.shape for k, c in Cs.items() if k not in ("handle", "handle_pins")]).bounding_box()
    return D, stow


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    D = derived()
    for name, dep in (("fieldcell-deployed", True), ("fieldcell-stowed", False)):
        asm = build(deployed=dep)
        export_step(asm, str(out / "step" / f"{name}.step"))
        export_stl(asm, str(out / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
        bb = asm.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm (L x W x H)")
    C = build_components()
    sets = {"frame": FRAME_KEYS, "pv-wing": ("wing_frames", "modules"),
            "battery-enclosure": ("batt_body", "batt_lid"), "electronics-enclosure": ("ebox_body", "ebox_lid", "fan")}
    for fname, keys in sets.items():
        shp = _comp(*[C[k].shape for k in keys])
        if fname == "pv-wing":
            shp = _comp(*[C[k].shape & box(-1000, 1000, 0, 2000, -10, 2000) for k in keys])
        export_step(shp, str(out / "step" / f"{fname}.step"))
        export_stl(shp, str(out / "stl" / f"{fname}.stl"), tolerance=0.5, angular_tolerance=0.3)
    _, sb = key_figures()
    print(f"wingspan {D['span']:.0f} mm, wing outer edge {D['edge_z']:.0f} mm above ground, "
          f"wing to tyre clearance {D['wing_tyre_gap']:.0f} mm; hinge pin at y {D['pin_y']:.1f}, z {D['pin_z']:.1f}")
    print(f"stowed without handle {sb.size.X:.0f} x {sb.size.Y:.0f} x {sb.size.Z:.0f} mm; "
          f"handle socket slope {D['sock_slope']:.1f} deg; outrigger leg {D['out_len']:.0f} mm")
    print("exported STEP and STL to cad/step and cad/stl")
    print_checks()
