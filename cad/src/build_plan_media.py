"""FieldCell prototype build plan pictures (FCL-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|layouts|wiring ...]
                         python cad/src/build_plan_media.py sheet 106     (one making sketch)
                         python cad/src/build_plan_media.py step 7        (one step picture)
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/FCL-DWG-101 to 111        making sketches for the made, cut and drilled components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/frame-layout.png    where every welded part sits on the frame (matplotlib)
    docs/05-build-plan/ebox-cutouts.png    cut-outs in the electronics box walls (matplotlib)
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model as m  # noqa: E402
from model import PARAMS as P, build_components, derived, box, FRAME_KEYS  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
_C = {}


def comps(deployed=True):
    if deployed not in _C:
        _C[deployed] = build_components(P, deployed)
    return _C[deployed]


def S(*ks, deployed=True):
    C = comps(deployed)
    return m._fuse([C[k].shape for k in ks])


COL = {"frame": "#4B5563", "axle": "#111827", "wheel": "#1F2937", "hw": "#B45309", "legs": "#0E7490",
       "angle": "#64748B", "case": "#57534E", "pack": "#C2410C", "fuse": "#B91C1C", "ebox": "#D1D5DB",
       "elec": "#0F766E", "inv": "#0E7490", "outlet": "#D4A017", "fan": "#475569", "gland": "#111827",
       "cable": "#B91C1C", "wframe": "#94A3B8", "module": "#1E3A8A", "hinge": "#7C3AED", "out": "#0F766E",
       "tie": "#7C3AED", "latch": "#B45309", "upright": "#A8A29E", "shade": "#E7E5E4", "handle": "#374151",
       "bin": "#65A30D", "strap": "#0F766E", "deck": "#9CA3AF"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(shape, x0, x1, y0, y1, z0, z1):
    return shape & box(x0, x1, y0, y1, z0, z1)


# ----------------------------------------------------------------- named components, in build order
def made():
    return {
        "frame": part("Frame (welded)", S("tubes", "deck", "brackets", "tabs", "sockets", "clevises", "up_tabs"), COL["frame"]),
        "axle": part("Axle", S("axle"), COL["axle"]),
        "wheels": part("Wheels, collars, linch pins", S("wheel_l", "wheel_r", "axle_hw"), COL["wheel"]),
        "legs": part("Stand legs (4)", S("legs", "leg_bolts"), COL["legs"]),
        "angles": part("Hinge spacer angles (2)", S("spacers"), COL["angle"]),
        "case": part("Battery case, drilled", S("batt_body", "batt_lid"), COL["case"]),
        "fuse": part("Class T fuse and holder", S("fuse_t"), COL["fuse"]),
        "pack": part("LiFePO4 pack", S("pack"), COL["pack"]),
        "ebox": part("Electronics box, cut", S("ebox_body", "ebox_lid"), COL["ebox"]),
        "elec": part("Inverter, MPPT, DIN rail", S("mplate", "inverter", "mppt", "fusing"), COL["elec"]),
        "outlets": part("Outlets, isolator, fan", S("dc_panel", "ac_outlet", "isolator", "fan"), COL["outlet"]),
        "glands": part("Glands, cables, cam straps", S("glands", "cables", "straps"), COL["gland"]),
        "wframes": part("Wing frames (2)", S("wing_frames"), COL["wframe"]),
        "modules": part("PV modules (2)", S("modules"), COL["module"]),
        "hinges": part("Hinges (2)", S("hinge_l"), COL["hinge"]),
        "outs": part("Outrigger legs and brackets (4)", S("outriggers", "out_brk", "out_bolts"), COL["out"]),
        "ties": part("Tie bars, latches, keepers", S("tie_bars", "tie_brk", "latches", "keepers"), COL["tie"]),
        "uprights": part("Shade uprights (4)", S("uprights"), COL["upright"]),
        "shade": part("Shade frame and fabric", S("shade_frame", "shade_fabric"), COL["shade"]),
        "handle": part("Handle", S("handle", "handle_pins"), COL["handle"]),
        "bin": part("Accessory bin and strap", S("bin", "bin_strap"), COL["bin"]),
    }


ORDER = ["frame", "axle", "wheels", "legs", "angles", "case", "fuse", "pack", "ebox", "elec", "outlets", "glands",
         "wframes", "modules", "hinges", "outs", "ties", "uprights", "shade", "handle", "bin"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"frame": (0, 0, 0), "axle": (0, 0, -300), "wheels": (0, 0, -520), "legs": (0, 0, -560),
           "angles": (0, 0, 160), "case": (-60, 0, 520), "fuse": (-60, 0, 1150), "pack": (-60, 0, 900),
           "ebox": (380, 0, 520), "elec": (380, 0, 880), "outlets": (760, 0, 620), "glands": (160, 0, 1250),
           "wframes": (-1900, 0, 500), "modules": (-1900, 0, 850), "hinges": (-1900, 0, 300), "outs": (-1900, 0, 120),
           "ties": (-1900, 0, 1150), "uprights": (60, 0, 1450), "shade": (60, 0, 1800), "handle": (650, 0, -80),
           "bin": (-350, 0, 650)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "FieldCell prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Parked pose, seen from the front right and above",
                       elev=24, azim=-58, size=(13, 9.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def _sheet(n):
    import build123d as b
    M = made()
    base = dict(project="FieldCell", date=DATE)
    a, d = D["sock_a"], D["sock_d"]
    if n == 101:
        fr = S("tubes", "deck", "brackets", "tabs", "sockets", "clevises", "up_tabs")
        return bv.component_sheet(
            Part("Frame", fr, COL["frame"]), [M["axle"], M["wheels"], M["legs"], M["angles"]],
            dwg_no="FCL-DWG-101", title="FieldCell frame weldment: making sketch",
            material="Steel square tube 40 x 40 x 1.5, S235; expanded steel sheet; 3 to 5 mm plate", inset_view=(24, -58),
            notes=["Rails: two 1,200 mm lengths of 40 x 40 x 1.5 tube. Cross tubes: three",
                   "  520 mm lengths, at both ends and the middle, between the rails.",
                   "Weld square on a flat table: diagonals equal within 2 mm. Tube tops",
                   "  are 455 mm above the ground when parked. Cap the four rail ends (3 mm).",
                   "Deck: expanded steel sheet 1,200 x 520 mm laid on the cross tubes",
                   "  between the rails, stitch welded 25 mm every 150 mm.",
                   "Axle brackets: 60 x 5 mm plate, 247 mm long, under each rail at 630 mm",
                   "  from the front end, 290 mm from the centre line; 20.5 mm axle hole",
                   "  35 mm above the bottom. Gusset 87 x 85 x 5 mm to the middle cross tube.",
                   "Hinge tabs: eight 30 x 3 mm, 75 mm long, on the rail outer faces at",
                   "  60, 420, 780 and 1,140 mm from the front end, 39 mm above the rail top.",
                   "Handle sockets, leg clevises, shade tabs: see the frame layout picture.",
                   "Check: deck flat within 3 mm; axle holes line up (20 mm bar slides through)."],
            **base)
    if n == 102:
        ax = S("axle")
        return bv.component_sheet(
            Part("Axle", ax, COL["axle"]), [M["frame"], M["wheels"]],
            dwg_no="FCL-DWG-102", title="FieldCell axle: making sketch", material="Bright mild steel bar 20 mm diameter",
            view_shape=b.Rot(0, 0, 90) * b.Pos(-P["axle_x"], 0, -P["wheel_r"]) * (ax - m.zcyl(P["wheel_r"] - 15, P["wheel_r"] + 15, P["axle_x"], P["axle_end"] - 10, 2.5) - m.zcyl(P["wheel_r"] - 15, P["wheel_r"] + 15, P["axle_x"], -P["axle_end"] + 10, 2.5)), inset_view=(20, -40),
            notes=["Cut 820 mm of 20 mm bright steel bar; chamfer both ends 1 mm.",
                   "Drill a 5 mm cross hole 10 mm from each end for the linch pins,",
                   "  both holes in the same plane.",
                   "Slide it through both bracket holes so 410 mm stands each side of",
                   "  the centre line; weld it to both brackets, all round, both faces.",
                   "Each end then takes, in order: a spacer collar 26 mm outside,",
                   "  20 mm bore, 37.5 mm long; the wheel hub (60 mm long);",
                   "  a 20 mm washer 3 mm thick; the linch pin.",
                   "Check: the wheels spin freely with 0.5 to 1 mm end float."],
            **base)
    if n == 103:
        x, y = P["leg_x"], P["leg_y"]
        lg = m.zcyl(P["foot"][1], P["leg_pivot_z"] + 12, x, y, P["leg_d"] / 2) + box(x - 30, x + 30, y - 30, y + 30, 0, P["foot"][1])
        return bv.component_sheet(
            Part("Stand leg", lg, COL["legs"]), [M["frame"], M["wheels"]],
            dwg_no="FCL-DWG-103", title="FieldCell stand leg (make 4): making sketch",
            material="Steel tube 25 x 2 mm; steel plate 5 mm", view_shape=b.Pos(-x, -y, 0) * lg, inset_view=(20, -35),
            notes=["Cut four 387 mm lengths of 25 x 2 mm tube; round the top end.",
                   "Drill 10.5 mm across the tube 12 mm from the top: the pivot.",
                   "Drill 6.5 mm across, 30 mm below the pivot hole: the detent hole",
                   "  that locks the leg down.",
                   "Weld a 60 x 60 x 5 mm foot plate square on the bottom end.",
                   "Fit: the top end goes between a pair of 3 mm clevis plates under",
                   "  the rail, 40 mm from the rail end; M10 pivot bolt, nyloc nut,",
                   "  snug so the leg swings. Spring detent pin through the clevis",
                   "  and the leg holds it down; a second clevis hole holds it folded.",
                   "The leg folds inward along the rail, foot toward the axle.",
                   "Check: with all four down the deck is level within 1 degree."],
            **base)
    if n == 104:
        hd = S("handle")
        return bv.component_sheet(
            Part("Handle", hd, COL["handle"]), [M["frame"], M["ebox"]],
            dwg_no="FCL-DWG-104", title="FieldCell handle: making sketch",
            material="Steel tube 28 x 1.5 mm (legs), 32 x 1.5 mm (grip)", view_shape=b.Pos(-P["socket_x"], 0, -D["tube_top"]) * hd,
            inset_view=(22, -40),
            notes=[f"Legs: two {D['handle_leg']:.0f} mm lengths of 28 x 1.5 mm tube.",
                   "Grip: 520 mm of 32 x 1.5 mm tube.",
                   "Lay out on the bench: leg feet 560 mm apart, leg tops 480 mm apart,",
                   "  meeting the grip 20 mm in from each grip end. Fish-mouth the leg",
                   "  tops to the grip and weld.",
                   "Each leg drops into a socket on the rail end, 30.5 degrees up from",
                   "  level; mark the leg 115 mm from its foot and drill 8.5 mm across it",
                   "  with the leg in the socket, through the socket's pin hole.",
                   "Quick-release pins hold the handle; pull them to take it off.",
                   "Grip 900 mm above the ground, 1,270 mm from the deck centre.",
                   "Check: the handle drops in and out of both sockets without forcing."],
            **base)
    if n == 105:
        ang = S("spacers") & box(-2000, 2000, 0, 2000, -10, 2000)
        flat_ang = b.Pos(0, -(P["deck_w"] / 2 + 3), -(D["angle_top"] - 20)) * ang
        holes = [m.ycyl(-1, 3, x, 9, 2.75) for x in P["tab_x"]] + \
                [m.zcyl(17, 21, -525 + 150 * k, 10, 2.25) for k in range(8)]
        flat_ang = flat_ang - m._fuse(holes)
        return bv.component_sheet(
            Part("Spacer angle", ang, COL["angle"]), [M["frame"], part("Right hinge", S("hinge_l") & box(-2000, 2000, 0, 2000, -10, 2000), COL["hinge"])],
            dwg_no="FCL-DWG-105", title="FieldCell hinge spacer angle (make 2): making sketch",
            material="Aluminium equal angle 20 x 20 x 2 mm, 6063", view_shape=flat_ang,
            inset_view=(30, -120),
            notes=["Cut two 1,200 mm lengths of 20 x 20 x 2 mm angle; deburr.",
                   "Upright leg: four 5.5 mm holes 11 mm down from the top, at 60,",
                   "  420, 780 and 1,140 mm from one end, to match the frame tabs.",
                   "Flat leg (top): 4.5 mm holes every 150 mm, 10 mm in from the",
                   "  outer edge, for the hinge screws; countersink from the top.",
                   "Fit: upright leg flat on the outside of the four tabs, top of the",
                   "  flat leg 494 mm above the ground, flat leg pointing outward.",
                   "  M5 bolts through the tabs, nyloc nuts inside.",
                   "The hinge's fixed leaf lies on the flat leg; its knuckle (the pin)",
                   "  overhangs the angle's edge by 7 mm.",
                   "Check: angle top level and straight within 1 mm along its length."],
            **base)
    if n == 106:
        W = m._wing_local_parts(P, D)
        wf = W["frame"]
        return bv.component_sheet(
            Part("Wing frame", m._local(P, D, wf), COL["wframe"]), [M["frame"], M["angles"], M["outs"], M["wheels"]],
            dwg_no="FCL-DWG-106", title="FieldCell PV wing frame (make 2): making sketch",
            material="Aluminium rectangular tube 30 x 20 x 1.5 mm, 6063", view_shape=wf, inset_view=(32, -40),
            notes=["Long members: two 1,400 mm lengths. End members and ribs: five",
                   "  660 mm lengths. All 30 x 20 x 1.5 tube, 30 mm side upright.",
                   "Ribs at 350, 700 and 1,050 mm from one end, square to the long members.",
                   "Join every butt with an aluminium corner cleat inside the tubes and",
                   "  four 4.8 mm blind rivets (or TIG weld). Frame 1,400 x 700 mm.",
                   "Face (top): flat within 2 mm; the module is bonded to it.",
                   "Inner long member (hinge side): M4 rivet nuts every 150 mm in its",
                   "  inner face, 10 mm below the top, for the hinge's moving leaf.",
                   "Outer long member: outrigger brackets underneath at 80 mm from each",
                   "  end; tie bar bracket (left wing) or keeper (right wing) at each end.",
                   "Check: diagonals equal within 2 mm; frame does not rock on a table."],
            **base)
    if n == 107:
        x, py = P["out_x"], D["out_y"]
        lg = m.zcyl(P["out_foot"][1], D["out_pz"] + 10, x, py, P["out_d"] / 2) + box(x - 25, x + 25, py - 25, py + 25, 0, 4) \
            + (box(x + 25, x + 53, py - 15, py + 15, 0, 4) - m.zcyl(-1, 5, x + 40, py, 5.5))
        return bv.component_sheet(
            Part("Outrigger leg", lg, COL["out"]), [M["wframes"], M["modules"], M["frame"]],
            dwg_no="FCL-DWG-107", title="FieldCell outrigger leg and bracket (make 4): making sketch",
            material="Steel tube 25 x 2 mm, steel plate 4 mm; aluminium strip 3 mm (bracket)",
            view_shape=b.Pos(-x, -py, 0) * lg, inset_view=(18, -30),
            notes=["Leg: cut 269 mm of 25 x 2 mm tube; round the top end; drill 8.5 mm",
                   "  across, 10 mm from the top (pivot), and 6.5 mm 30 mm below it (detent).",
                   "Foot: 50 x 50 x 4 mm plate with a 28 x 30 mm stake tab on one side",
                   "  (11 mm hole, 15 mm from the plate edge); weld square to the leg.",
                   "  The tab points toward the nearer end of the cart.",
                   "Bracket: bend a 3 mm aluminium strip into a U, 26 mm inside,",
                   "  legs 29 mm, web 45 mm long; 8.5 mm pivot hole through both legs.",
                   "Fit: rivet the web under the wing's outer long member, 80 mm from",
                   "  the frame end; M8 pivot bolt, nyloc nut, snug.",
                   "Leg down: vertical with the wing at 15 degrees. Folded: flat under",
                   "  the wing, 7 mm clear of the frame.",
                   "Check: the wing's outer edge sits 309 mm above the ground."],
            **base)
    if n == 108:
        L = comps(False)["tie_bars"].shape.bounding_box().size.Y
        tb_ = (box(0, L, 0, 20, 0, 20) - m.ycyl(-1, 21, 10, 10, 3.25)) + box(L, L + 12, 0, 20, 0, 20)
        return bv.component_sheet(
            Part("Tie bar", S("tie_bars", "latches", deployed=False), COL["tie"]),
            [part("Wings", S("wing_frames", "modules", deployed=False), COL["wframe"])],
            dwg_no="FCL-DWG-108", title="FieldCell tie bar (make 2): making sketch",
            material="Aluminium square tube 20 x 20 x 1.5 mm, 6063", view_shape=tb_, inset_view=(24, -25),
            notes=[f"Cut two {L:.0f} mm lengths of 20 x 20 x 1.5 mm square tube; deburr",
                   f"  ({L + 12:.0f} mm overall with the latch body on the end).",
                   "Drill 6.5 mm across, 10 mm from one end: the pivot.",
                   "Rivet the over-centre latch body to the other end, hook outward.",
                   "Pivot bracket: 3 mm aluminium angle, ear 35 mm tall beside the bar,",
                   "  riveted to the top corner of the left wing's frame, on its back.",
                   "Keeper: screwed to the top of the right wing's outer member,",
                   "  12 mm in from its back face, opposite the latch.",
                   "Travel: the bar lies across the tops of both stowed wings and the",
                   "  latch pulls the right wing in against it.",
                   "Parked: the bar folds down the back of the left wing, held by a clip.",
                   "Check: latched, neither wing moves when pushed outward at the top."],
            **base)
    if n == 109:
        sh = S("uprights", "shade_frame")
        return bv.component_sheet(
            Part("Shade frame and uprights", sh, COL["upright"]), [M["frame"], M["case"], M["ebox"]],
            dwg_no="FCL-DWG-109", title="FieldCell sun shade frame and uprights: making sketch",
            material="Aluminium square tube 20 x 20 x 1.5 mm; aluminized fabric",
            view_shape=b.Pos(0, 0, -D["tube_top"]) * sh, inset_view=(26, -55),
            notes=["Frame: two 830 mm long sides, three 540 mm cross tubes (ends and",
                   "  middle), 20 x 20 x 1.5 mm; corner cleats and rivets. 830 x 580 mm.",
                   "Fabric: reflective aluminized fabric, 830 x 580 mm, eyelets every",
                   "  100 mm, laced round the frame, shiny side up.",
                   "Uprights: four 355 mm lengths of the same tube. 6.5 mm hole across",
                   "  each, 30 mm from the bottom, for the M6 bolt into the frame tab.",
                   "Uprights stand on the rail tops at 400 and 1,100 mm from the front end,",
                   "  280 mm each side of the centre line.",
                   "The frame's long sides rest on the upright tops 810 mm above the ground,",
                   "  50 mm over both boxes; an angle clip and M6 wing bolt at each upright.",
                   "Undo four wing bolts to lift the shade off and open the battery lid.",
                   "Check: 50 mm air gap over both boxes; shade level within 5 mm."],
            **base)
    if n == 110:
        eb = S("ebox_body")
        return bv.component_sheet(
            Part("Electronics box", eb, COL["ebox"]), [M["frame"], M["case"], M["outlets"]],
            dwg_no="FCL-DWG-110", title="FieldCell electronics box: cutting sketch",
            material="Bought IP54 polycarbonate box 320 x 460 x 300 mm", view_shape=b.Pos(-D["ebox_x"], 0, -P["deck_z"]) * eb,
            inset_view=(24, -40),
            notes=["Sizes are from the box's outside bottom edge and its centre line.",
                   "Outlet end (toward the handle): DC panel 150 x 160 mm, 40 to 190 mm",
                   "  right of centre, 80 to 240 mm up; AC outlet 60 x 110 mm, 90 to 150",
                   "  mm left, 130 to 240 mm up; isolator 40 x 40 mm, 15 to 55 mm left,",
                   "  160 to 200 mm up. (Right and left as seen facing that end.)",
                   "Right side wall: fan 115 x 115 mm, 35 to 150 mm from the battery end,",
                   "  35 to 150 mm up. Left wall: exhaust 115 x 115 mm, 155 to 270 mm",
                   "  from the battery end, 130 to 245 mm up.",
                   "Battery end: two 25.5 mm gland holes, 40 mm each side, 150 mm up.",
                   "Both side walls: a 16.5 mm PV gland hole 30 mm from the outlet end,",
                   "  30 mm up. Floor: four 6.5 mm holes for the deck bolts.",
                   "Cut with a step drill and a fine jigsaw; tape first; no solvents."],
            **base)
    if n == 111:
        cb = S("batt_body")
        return bv.component_sheet(
            Part("Battery case", cb, COL["case"]), [M["frame"], M["ebox"], M["glands"]],
            dwg_no="FCL-DWG-111", title="FieldCell battery case: drilling sketch",
            material="Bought IP65 polypropylene case about 420 x 360 x 300 mm", view_shape=b.Pos(0, 0, -P["deck_z"]) * cb,
            inset_view=(24, -40),
            notes=["Only the end facing the electronics box is drilled.",
                   "Two 25.5 mm holes for M25 glands, 40 mm each side of the centre",
                   "  line, 150 mm up from the outside bottom: they line up with the",
                   "  gland holes in the electronics box, 60 mm away.",
                   "Tape, pilot 3 mm, open with a step drill; deburr; no solvents.",
                   "Keep the case's own pressure vent; do not block it.",
                   "Inside: the pack sits in the middle of the floor on a 3 mm rubber mat",
                   "  with foam blocks round it; the class T fuse holder is screwed to",
                   "  the floor beside the pack at the gland end, so the positive lead",
                   "  from the pack to the fuse is under 150 mm.",
                   "Two cam straps hold the case and lid down through the deck.",
                   "Check: glands seat flat; lid closes on its seal with the cables in."],
            **base)
    raise ValueError(n)


def sheets(nums=None):
    return [_sheet(n) for n in (nums or range(101, 112))]


# ----------------------------------------------------------------- joints
def joint(n):
    C = comps(True)
    X = lambda k: C[k].shape  # noqa: E731
    if n == 1:
        bx = (-40, P["axle_x"], 200, 425, 140, 440)      # cut through the axle centre line
        parts = [part("Rail (cut through)", win(X("tubes"), *bx), COL["frame"]),
                 part("Axle bracket and gusset, welded", win(X("brackets"), *bx), "#6B7280"),
                 part("Axle, welded to the brackets", win(X("axle"), *bx), COL["axle"]),
                 part("Spacer collar, washer, linch pin", win(X("axle_hw"), *bx), COL["hw"]),
                 part("Wheel hub on its bearings (tyre cut away)", win(X("wheel_r"), *bx) & box(-60, 110, 200, 425, 140, 262), "#475569")]
        return bv.joint(parts, OUT / "joint-01.png", "Joint 1: axle, bracket, collar and wheel hub (right side, cut open)",
                        subtitle="Cut through the axle, seen from the handle end. Collar between bracket and hub; washer and linch pin outside",
                        elev=12, azim=8, size=(8, 6))
    if n == 2:
        bx = (500, 620, 230, 330, 250, 460)
        parts = [part("Rail", win(X("tubes"), *bx), COL["frame"]),
                 part("Clevis plates, welded under the rail", win(X("clevises"), *bx), "#6B7280"),
                 part("Stand leg", win(X("legs"), *bx), COL["legs"]),
                 part("M10 pivot bolt, nyloc nut", win(X("leg_bolts"), *bx), COL["axle"])]
        return bv.joint(parts, OUT / "joint-02.png", "Joint 2: stand leg on its clevis (handle end, right side)",
                        subtitle="The leg swings on the pivot bolt; a detent pin through the plates locks it down or folded",
                        elev=12, azim=-35, size=(8, 6))
    if n == 3:
        bx = (500, 720, 230, 330, 400, 600)
        parts = [part("Rail and end cap", win(X("tubes"), *bx), COL["frame"]),
                 part("Socket and gusset, welded", win(X("sockets"), *bx), "#6B7280"),
                 part("Handle leg, in the socket", win(X("handle"), *bx), COL["handle"]),
                 part("Quick-release pin", win(X("handle_pins"), *bx), COL["hw"])]
        return bv.joint(parts, OUT / "joint-03.png", "Joint 3: handle leg in its socket (right side)",
                        subtitle="Socket welded on the rail end at 30.5 degrees, gusset under it; one pin holds the leg",
                        elev=14, azim=-60, size=(8, 6))
    if n == 4:
        bx = (165, 195, 250, 372, 405, 515)
        parts = [part("Rail (cut through)", win(X("tubes"), *bx), COL["frame"]),
                 part("Hinge tab, welded to the rail", win(X("tabs"), *bx), "#6B7280"),
                 part("Spacer angle, bolted to the tab", win(X("spacers"), *bx), COL["angle"]),
                 part("Hinge: fixed leaf, knuckle, moving leaf", win(X("hinge_l"), *bx), COL["hinge"]),
                 part("Wing frame inner member", win(X("wing_frames"), *bx), COL["wframe"]),
                 part("PV module", win(X("modules"), *bx), COL["module"])]
        return bv.joint(parts, OUT / "joint-04.png", "Joint 4: hinge line, cut through a tab (right side, wing folded out)",
                        subtitle="Seen from the handle end. The pin sits 4.5 mm above the panel face so the panel clears the knuckle",
                        elev=4, azim=0, size=(8, 6))
    if n == 5:
        x = P["out_x"]
        bx = (x - 60, x + 60, D["out_y"] - 90, D["out_y"] + 80, D["out_pz"] - 120, D["out_pz"] + 110)
        parts = [part("Wing frame outer member", win(X("wing_frames"), *bx), COL["wframe"]),
                 part("PV module", win(X("modules"), *bx), COL["module"]),
                 part("U bracket, riveted under the member", win(X("out_brk"), *bx), "#6B7280"),
                 part("Outrigger leg", win(X("outriggers"), *bx), COL["out"]),
                 part("M8 pivot bolt", win(X("out_bolts"), *bx), COL["axle"])]
        return bv.joint(parts, OUT / "joint-05.png", "Joint 5: outrigger leg on its bracket (right wing, handle end)",
                        subtitle="Seen from below and outside. The leg stands vertical; it folds back flat under the wing for travel",
                        elev=-20, azim=-30, size=(8, 6))
    if n in (6, 9):
        Cs = comps(False)
        Y = lambda k: Cs[k].shape  # noqa: E731
        x = P["tie_x"]
        if n == 6:
            bx = (x - 50, x + 50, 290, 400, 1110, 1240)
            parts = [part("Right wing frame (stowed)", win(Y("wing_frames"), *bx), COL["wframe"]),
                     part("Tie bar end", win(Y("tie_bars"), *bx), COL["tie"]),
                     part("Over-centre latch, riveted to the bar", win(Y("latches"), *bx), COL["latch"]),
                     part("Keeper, screwed to the wing top", win(Y("keepers"), *bx), COL["axle"])]
            return bv.joint(parts, OUT / "joint-06.png", "Joint 6: tie bar latch on the right wing (handle end, travel)",
                            subtitle="Seen from the handle end and above. The bar rests on the wing top; the latch hooks the keeper and pulls in",
                            elev=22, azim=-35, size=(8, 6))
        bx = (x - 50, x + 50, -420, -300, 1110, 1240)
        parts = [part("Left wing frame (stowed)", win(Y("wing_frames"), *bx), COL["wframe"]),
                 part("Tie bar, pivot end", win(Y("tie_bars"), *bx), COL["tie"]),
                 part("Pivot bracket, riveted to the frame back", win(Y("tie_brk"), *bx), "#6B7280")]
        return bv.joint(parts, OUT / "joint-09.png", "Joint 9: tie bar pivot on the left wing (handle end, travel)",
                        subtitle="Seen from the handle end. The bar sits on the wing top and turns on an M6 bolt through the bracket ear and folds down the back",
                        elev=12, azim=170, size=(8, 6))
    if n == 7:
        x = P["up_x"][1]
        bx = (x - 50, x + 50, 220, 330, 400, 860)
        parts = [part("Rail", win(X("tubes"), *bx), COL["frame"]),
                 part("Upright tab, welded on the rail", win(X("up_tabs"), *bx), "#6B7280"),
                 part("Shade upright, M6 bolt into the tab", win(X("uprights"), *bx), COL["upright"]),
                 part("Shade frame, resting on the upright", win(X("shade_frame"), *bx), "#A8A29E"),
                 part("Fabric", win(X("shade_fabric"), *bx), "#D6D3D1")]
        return bv.joint(parts, OUT / "joint-07.png", "Joint 7: shade upright, rail and shade frame (right side)",
                        subtitle="Seen from outside. The upright is bolted to its tab; the frame sits on the upright's top",
                        elev=14, azim=60, size=(8, 6))
    if n == 8:
        bx = (150, 330, -110, 0, 520, 700)
        parts = [part("Battery case wall (cut open)", win(X("batt_body"), *bx), COL["case"]),
                 part("Electronics box wall (cut open)", win(X("ebox_body"), *bx), "#9CA3AF"),
                 part("M25 glands, nut inside", win(X("glands"), *bx), COL["gland"]),
                 part("Battery cable, 16 mm2", win(X("cables"), *bx), COL["cable"]),
                 part("Inverter", win(X("inverter"), *bx), COL["inv"])]
        return bv.joint(parts, OUT / "joint-08.png", "Joint 8: battery cables between the boxes (cut through the left gland)",
                        subtitle="Seen from the left. 60 mm between the boxes: two gland domes and 16 mm of cable",
                        elev=10, azim=-100, size=(8, 6))
    raise ValueError(n)


def joints(nums=None):
    return [joint(n) for n in (nums or range(1, 10))]


# ----------------------------------------------------------------- assembly steps
def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def step(n):
    M = made()
    F = M["frame"]
    st = lambda done, new, title, sub, **kw: bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}",  # noqa: E731
                                                       subtitle=sub, **kw)
    rolling = [F, M["axle"], M["wheels"], M["legs"]]
    if n == 1:
        return st([F], [mv(M["axle"], (0, -700, 0))], "axle through the brackets",
                  "Slide it in from one side, 410 mm each side of the centre line; weld to both brackets",
                  elev=20, azim=-60)
    if n == 2:
        left = S("wheel_l") + (S("axle_hw") & box(-999, 999, -999, 0, -9, 999))
        right = S("wheel_r") + (S("axle_hw") & box(-999, 999, 0, 999, -9, 999))
        return st([F, M["axle"]], [mv(part("Left wheel, collar, washer, pin", left, COL["wheel"]), (0, -250, 0)),
                                   mv(part("Right wheel, collar, washer, pin", right, COL["wheel"]), (0, 250, 0))],
                  "wheels onto the axle", "Collar, wheel, washer, then the linch pin; each side the same",
                  elev=18, azim=-60, label_done=False)
    if n == 3:
        return st([F, M["axle"], M["wheels"]], [mv(M["legs"], (0, 0, -200))], "stand legs into their clevises",
                  "M10 pivot bolt each, nyloc nut snug; detent pin in the down hole",
                  elev=14, azim=-55, label_done=False)
    if n == 4:
        return st(rolling, [mv(M["angles"], (0, 0, 150))], "hinge spacer angles onto the tabs",
                  "Upright leg on the outside of the four tabs, flat leg outward; four M5 bolts per side",
                  elev=24, azim=-60, label_done=False)
    base = rolling + [M["angles"]]
    if n == 5:
        return st(base, [mv(part("Battery case, glands fitted", S("batt_body", "batt_lid") + (S("glands") & box(-999, 240, -999, 999, -9, 999)), COL["case"]), (0, 0, 350)),
                         mv(part("Two cam straps, through the deck", S("straps"), COL["strap"]), (0, 0, 700))],
                  "battery case onto the deck", "Centred on the middle cross tube, gland end toward the handle; straps loose for now",
                  elev=24, azim=-60, label_done=False)
    if n == 6:
        return st([part("Battery case", S("batt_body"), COL["case"])],
                  [mv(M["pack"], (0, 0, 350)), mv(M["fuse"], (0, 0, 250))], "pack and class T fuse into the case",
                  "Pack on its mat in the middle; fuse holder beside it at the gland end; fuse OUT",
                  elev=40, azim=-55, label_done=True)
    if n == 7:
        return st([part("Electronics box", S("ebox_body"), COL["ebox"])],
                  [mv(part("Mounting plate", S("mplate"), "#94A3B8"), (0, 0, 300)),
                   mv(part("Inverter", S("inverter"), COL["inv"]), (0, -60, 520)),
                   mv(part("MPPT charge controller", S("mppt"), COL["elec"]), (-40, 60, 520)),
                   mv(part("DIN rail: breakers and shunt", S("fusing"), COL["fuse"]), (60, 60, 520))],
                  "inverter, MPPT and DIN rail on the mounting plate", "All screwed to the plate on the bench; then the plate goes in on its bosses",
                  elev=32, azim=-50, label_done=True)
    if n == 8:
        return st([part("Electronics box", S("ebox_body", "mplate", "inverter", "mppt", "fusing"), COL["ebox"])],
                  [mv(part("DC outlet panel", S("dc_panel"), COL["outlet"]), (150, 0, 0)),
                   mv(part("AC outlet, GFCI, in-use cover", S("ac_outlet"), "#F59E0B"), (150, 0, 0)),
                   mv(part("Battery isolator", S("isolator"), COL["fuse"]), (150, 0, 0)),
                   mv(part("Filter fan (right wall)", S("fan") & box(-999, 999, 0, 999, -9, 999), COL["fan"]), (0, 150, 0)),
                   mv(part("Exhaust filter (left wall)", S("fan") & box(-999, 999, -999, 0, -9, 999), COL["fan"]), (0, -150, 0))],
                  "outlets, isolator, fan and exhaust filter", "Each through its cut-out from outside, sealed with its gasket, fixed inside",
                  elev=24, azim=-35, label_done=False)
    if n == 9:
        return st(base + [part("Battery case", S("batt_body", "batt_lid", "straps"), COL["case"])],
                  [mv(part("Electronics box, fitted out", S("ebox_body", "mplate", "inverter", "mppt", "fusing", "dc_panel", "ac_outlet", "isolator", "fan"), COL["ebox"]), (0, 0, 400))],
                  "electronics box onto the deck", "Outlet end 10 mm in from the frame end; four M6 bolts through the floor, large washers under the deck",
                  elev=24, azim=-60, label_done=False)
    boxes = base + [part("Boxes", S("batt_body", "batt_lid", "straps", "ebox_body", "dc_panel", "ac_outlet", "isolator", "fan", "ebox_lid"), COL["case"])]
    if n == 10:
        return st(base + [part("Battery case", S("batt_body", "straps"), COL["case"]), part("Electronics box", S("ebox_body", "dc_panel", "ac_outlet", "isolator", "fan", "mplate", "inverter", "mppt", "fusing"), COL["ebox"])],
                  [mv(part("Battery cables and glands", S("glands", "cables"), COL["cable"]), (0, -330, 0)),
                   mv(part("Battery case lid", S("batt_lid"), COL["case"]), (0, 0, 250)),
                   mv(part("Electronics box lid", S("ebox_lid"), COL["ebox"]), (0, 0, 250))],
                  "battery cables, then the lids", "Cables through both glands, lugs on; fuse still out. Close both lids; tighten the cam straps",
                  elev=26, azim=-60, label_done=False)
    if n == 11:
        wf = S("wing_frames") & box(-999, 999, 0, 2000, -9, 2000)
        md = S("modules") & box(-999, 999, 0, 2000, -9, 2000)
        return st([part("Wing frame", wf, COL["wframe"])], [mv(part("PV module, bonded on", md, COL["module"]), (0, 70, 260))],
                  "module onto the wing frame (on the bench)", "Structural tape on every member's face; lay the module on from one end, roll it down",
                  elev=35, azim=-60, label_done=True)
    if n == 12:
        wf = S("wing_frames", "modules") & box(-999, 999, 0, 2000, -9, 2000)
        ob = S("outriggers", "out_brk", "out_bolts") & box(-999, 999, 0, 2000, -9, 2000)
        return st([part("Right wing", wf, COL["wframe"])],
                  [mv(part("Outrigger brackets and legs (2 per wing)", ob, COL["out"]), (0, 0, -200))],
                  "outriggers onto the wings", "Seen from below. U brackets riveted under the outer member, 80 mm from each end; legs on M8 pivot bolts",
                  elev=-25, azim=-50, label_done=False)
    wings = part("Wings", S("wing_frames", "modules", "outriggers", "out_brk", "keepers", "tie_brk", "tie_bars", "latches", "hinge_l"), COL["wframe"])
    if n == 13:
        return st(boxes, [mv(part("Right wing with its hinge", S("wing_frames", "modules", "outriggers", "out_brk", "keepers", "hinge_l") & box(-999, 999, 0, 2000, -9, 2000), COL["module"]), (0, 200, 120)),
                          mv(part("Left wing with its hinge and tie bars", S("wing_frames", "modules", "outriggers", "out_brk", "tie_brk", "tie_bars", "latches", "hinge_l") & box(-999, 999, -2000, 0, -9, 2000), COL["module"]), (0, -200, 120))],
                  "wings onto the hinge angles", "Wings folded out on their legs; fixed leaf on the angle, M4 countersunk screws every 150 mm",
                  elev=26, azim=-60, label_done=False)
    if n == 14:
        return st(boxes + [wings], [mv(M["uprights"], (0, 0, 250)), mv(M["shade"], (0, 0, 500))], "shade uprights, then the shade",
                  "M6 bolt through each upright into its tab; frame on the uprights, a wing bolt at each",
                  elev=28, azim=-60, label_done=False)
    if n == 15:
        return st(boxes + [wings, M["uprights"], M["shade"]], [mv(M["handle"], (260, 0, 150))], "handle into its sockets",
                  "Both legs into the sockets; a quick-release pin through each",
                  elev=22, azim=-55, label_done=False)
    if n == 16:
        return st(boxes + [wings, M["uprights"], M["shade"], M["handle"]], [mv(M["bin"], (0, 0, 350))], "accessory bin and strap",
                  "Bin at the front end, strap over it and through the deck",
                  elev=24, azim=-60, label_done=False)
    if n == 17:
        Cs = comps(False)
        done = [part("Cart, travel pose", m._fuse([c.shape for k, c in Cs.items() if k not in ("tie_bars", "latches")]), "#D1D5DB")]
        return st(done, [mv(part("Tie bars, swung over and latched", S("tie_bars", "latches", deployed=False), COL["tie"]), (0, -250, 120))],
                  "fold for travel and tie the wings", "Legs folded under each wing, both wings up; each tie bar over the tops, latch closed",
                  elev=24, azim=-60, label_done=False)
    raise ValueError(n)


def steps(nums=None):
    return [step(n) for n in (nums or range(1, 18))]


# ----------------------------------------------------------------- layouts (matplotlib)
def _fig(w, h):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt, plt.figure(figsize=(w, h), dpi=150)


INK, MUT, AC, WARN = "#111827", "#4B5563", "#0F766E", "#B45309"


def _footer(fig):
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color=WARN)
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/fieldcell", fontsize=7, color=AC, ha="right", family="monospace")


def frame_layout():
    from matplotlib.patches import Rectangle, Polygon
    plt, fig = _fig(12, 7.4)
    ax = fig.add_axes([0.03, 0.08, 0.67, 0.8]); ax.set_aspect("equal"); ax.set_axis_off()
    L, Wd, R = P["deck_l"], P["deck_w"], P["rail"]
    X = lambda x: x + L / 2  # noqa: E731   distance from the front end
    for s in (-1, 1):
        ax.add_patch(Rectangle((0, s * (Wd / 2 - R / 2) - R / 2), L, R, fc="#E5E7EB", ec=INK, lw=1))
    for x in (-L / 2 + R / 2, 0, L / 2 - R / 2):
        ax.add_patch(Rectangle((X(x) - R / 2, -Wd / 2 + R), R, Wd - 2 * R, fc="#E5E7EB", ec=INK, lw=1))
    ax.axhline(0, color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    items = []
    for s in (-1, 1):
        for x in P["tab_x"]:
            ax.add_patch(Rectangle((X(x) - 15, s * Wd / 2 + (0 if s > 0 else -10)), 30, 10, fc="#7C3AED", ec="none"))
        ax.add_patch(Rectangle((X(P["axle_x"]) - 30, s * P["bracket_y"] - 2.5), 60, 5, fc="#B91C1C", ec="none"))
        for sx in (-1, 1):
            ax.add_patch(Rectangle((X(sx * P["leg_x"]) - 20, s * P["leg_y"] - 16), 40, 32, fc="none", ec="#0E7490", lw=1.2))
        for x in P["up_x"]:
            ax.add_patch(Rectangle((X(x) - 10, s * P["up_y"] - 10), 20, 20, fc="#A8A29E", ec=INK, lw=0.6))
        ax.add_patch(Polygon([(X(P["socket_x"]) - 30, s * 280 - 17), (X(P["socket_x"]) + 110, s * 274 - 17),
                              (X(P["socket_x"]) + 110, s * 274 + 17), (X(P["socket_x"]) - 30, s * 280 + 17)],
                             fc="#D4A017", ec=INK, lw=0.6, alpha=0.9))
    ax.add_patch(Rectangle((X(4), P["bracket_y"] - 90), 5, 87, fc="#B91C1C", ec="none", alpha=0.6))
    ax.add_patch(Rectangle((X(4), -P["bracket_y"] + 3), 5, 87, fc="#B91C1C", ec="none", alpha=0.6))
    # dimension rows below
    marks = [(X(x), "tab") for x in P["tab_x"]] + [(X(sx * P["leg_x"]), "leg") for sx in (-1, 1)] + \
            [(X(x), "up") for x in P["up_x"]] + [(X(P["axle_x"]), "axle"), (X(P["socket_x"]), "sock"), (0, ""), (L, "")]
    ys = {"tab": -360, "leg": -395, "up": -430, "axle": -465, "sock": -465, "": -500}
    col = {"tab": "#7C3AED", "leg": "#0E7490", "up": "#57534E", "axle": "#B91C1C", "sock": "#B45309", "": INK}
    for xv, k in marks:
        y = ys[k]
        ax.plot([xv, xv], [-Wd / 2 - 5, y + 12], color=col[k], lw=0.4, ls=":")
        ax.text(xv, y, f"{xv:.0f}", ha="center", va="center", fontsize=7.5, color=col[k],
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    ax.text(L / 2, -540, "distances from the front end of the frame, mm", ha="center", fontsize=8, color=MUT)
    ax.text(-30, 0, "centre line", ha="right", va="center", fontsize=7.5, color=MUT)
    ax.annotate("", xy=(L + 60, 0), xytext=(L + 10, 0), arrowprops=dict(arrowstyle="-|>", color=MUT))
    ax.text(L + 65, 0, "handle\nend", va="center", fontsize=7.5, color=MUT)
    ax.set_xlim(-140, L + 140); ax.set_ylim(-560, Wd / 2 + 40)
    fig.text(0.03, 0.965, "Frame: where each welded part sits (seen from above)", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.925, "Rails 1,200 mm, cross tubes 520 mm, 40 x 40 x 1.5 mm. Each part is the same on both rails, mirrored about the centre line.",
             fontsize=8.5, color=MUT, va="top")
    key = [("#7C3AED", "Hinge tabs 30 x 3 x 75, on the rail", "outer faces (drawn thicker)"),
           ("#B91C1C", "Axle brackets 60 x 5 under the rails,", "290 out; 5 mm gussets inboard"),
           ("#0E7490", "Stand leg clevis pairs, 3 mm plates", "40 x 55, 26 apart, under the rails"),
           ("#57534E", "Shade upright tabs 20 x 3 x 60 on", "the rail tops, outside each upright"),
           ("#D4A017", "Handle sockets 33.7 x 2.6 on the", "rail tops, 30.5 deg, gusset to cap")]
    fig.text(0.735, 0.86, "Key (all welded, mm)", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, (c, t1, t2) in enumerate(key):
        y = 0.82 - i * 0.085
        fig.patches.append(Rectangle((0.735, y - 0.018), 0.012, 0.02, transform=fig.transFigure, fc=c, ec=INK, lw=0.4))
        fig.text(0.752, y, t1, fontsize=7.8, color=INK, va="top"); fig.text(0.752, y - 0.027, t2, fontsize=7.8, color=INK, va="top")
    _footer(fig)
    out = OUT / "frame-layout.png"; OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def ebox_cutouts():
    """Each wall seen from outside; horizontal positions measured from that view's left edge."""
    from matplotlib.patches import Rectangle, Circle
    plt, fig = _fig(12, 4.6)
    eb, H = P["ebox"], P["ebox"][2]
    W1, W2 = eb[1], eb[0]
    # outlet end seen from the handle: +y on the right; left edge is y = -230
    oe = lambda y: y + W1 / 2  # noqa: E731
    # right side wall (+y) seen from outside: the outlet end is on the left
    rw = lambda d_batt: W2 - d_batt  # noqa: E731
    panels = [("Outlet end, from the handle", W1,
               [("DC panel", oe(40), oe(190), 80, 240, "in"), ("AC outlet", oe(-150), oe(-90), 130, 240, "below"),
                ("Isolator", oe(-55), oe(-15), 160, 200, "above")], [], "left edge = left side wall"),
              ("Right side wall, from outside", W2,
               [("Fan", rw(150), rw(35), 35, 150, "above")], [("PV gland 16.5", rw(290), 30, 8.25)], "outlet end on the left"),
              ("Left side wall, from outside", W2,
               [("Exhaust", 155, 270, 130, 245, "below")], [("PV gland 16.5", 290, 30, 8.25)], "battery end on the left"),
              ("Battery end, from outside", W1, [], [("Two M25 gland holes 25.5", W1 / 2, 150, 0)],
               "glands line up with the battery case")]
    xs = [0.03, 0.29, 0.51, 0.73]
    ws = [0.24, 0.2, 0.2, 0.24]
    for (title, w, rects, holes, sub), x0, wf in zip(panels, xs, ws):
        ax = fig.add_axes([x0, 0.07, wf, 0.76]); ax.set_aspect("equal"); ax.set_axis_off()
        ax.add_patch(Rectangle((0, 0), w, H, fc="#F3F4F6", ec=INK, lw=1))
        ax.add_patch(Rectangle((0, H - P["lid_h"]), w, P["lid_h"], fc="white", ec=MUT, lw=0.6, ls="--"))
        ax.text(w / 2, H - P["lid_h"] / 2, "lid", ha="center", va="center", fontsize=7, color=MUT)
        for name, a0, a1, z0, z1, where in rects:
            ax.add_patch(Rectangle((a0, z0), a1 - a0, z1 - z0, fc="white", ec=AC, lw=1.2))
            txt = f"{name}\n{a1 - a0:.0f} x {z1 - z0:.0f}\n{a0:.0f} to {a1:.0f} across\n{z0:.0f} to {z1:.0f} up"
            if where == "in":
                ax.text((a0 + a1) / 2, (z0 + z1) / 2, txt, ha="center", va="center", fontsize=6.6, color=INK, linespacing=1.15)
            elif where == "below":
                ax.text((a0 + a1) / 2, z0 - 4, txt, ha="center", va="top", fontsize=6.4, color=INK, linespacing=1.15)
            else:
                ax.text((a0 + a1) / 2, z1 + 4, txt.replace("\n", ", ", 1), ha="center", va="bottom", fontsize=6.4, color=INK, linespacing=1.15)
        for name, a, z, r in holes:
            if r == 0:
                for da in (-40, 40):
                    ax.add_patch(Circle((a + da, z), 12.75, fc="white", ec=AC, lw=1.2))
                ax.text(a, z - 22, "Two M25 gland holes, 25.5 mm\n190 and 270 across, 150 up", ha="center", va="top",
                        fontsize=6.6, color=INK, linespacing=1.15)
                continue
            ax.add_patch(Circle((a, z), r, fc="white", ec=AC, lw=1.2))
            ax.text(a, z + r + 4, f"{name}\n{a:.0f} across, {z:.0f} up" if name else f"{a:.0f} across\n{z:.0f} up",
                    ha="center", va="bottom", fontsize=6.4, color=INK, linespacing=1.15)
        ax.set_xlim(-10, w + 10); ax.set_ylim(-46, H + 8)
        ax.text(w / 2, -14, title, ha="center", va="center", fontsize=8.2, fontweight="bold", color=INK)
        ax.text(w / 2, -34, sub, ha="center", va="center", fontsize=7, color=MUT)
    fig.text(0.03, 0.965, "Electronics box: cut-outs, each wall seen from outside", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.905, "mm. Across: from the left edge of the wall as you look at it. Up: from the outside bottom. "
             "Check each part's own cut-out template before cutting. Floor: four 6.5 mm holes for the deck bolts.",
             fontsize=8.3, color=MUT, va="top")
    _footer(fig)
    out = OUT / "ebox-cutouts.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def layouts():
    return [frame_layout(), ebox_cutouts()]


# ----------------------------------------------------------------- wiring
def wiring():
    from matplotlib.patches import FancyBboxPatch
    plt, fig = _fig(12.5, 7.6)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 125); ax.set_ylim(0, 82); ax.set_axis_off()
    DY = 4
    ax.text(2, 80, "FieldCell prototype: block-level wiring", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 76.6, "Bought parts wired at block level; no circuit board. Stranded copper; crimped lugs or ferrules on every terminal; "
            "every circuit fused where it leaves its source.", fontsize=8.5, color=MUT, va="top")
    _footer(fig)

    def blk(x, y, w, h, title, sub, color):
        y += DY
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=8.6, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.1, sub, ha="center", va="top", fontsize=7, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ys = [v + DY for v in ys]
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        y += DY
        ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, AMB = "#B91C1C", "#1D4ED8", "#6B7280", "#B45309"
    ax.add_patch(FancyBboxPatch((3, 7 + DY), 30, 52, boxstyle="round,pad=0.4", fc="#FFF7ED", ec="#C2410C", lw=1, ls="--"))
    ax.text(4.5, 58 + DY, "In the battery case", fontsize=8, color="#C2410C", va="top")
    ax.add_patch(FancyBboxPatch((44, 7 + DY), 78, 52, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(45.5, 58 + DY, "In the electronics box", fontsize=8, color=MUT, va="top")
    blk(6, 12, 22, 14, "LiFePO4 pack", "25.6 V 50 Ah,\n100 A BMS with\ncharge temperature cut-off", "#C2410C")
    blk(6, 38, 22, 11, "Class T fuse 100 A", "in its holder,\nunder 150 mm from +", RED)
    blk(48, 38, 15, 11, "Isolator", "on the outlet face,\nno tools", RED)
    blk(48, 12, 15, 11, "Shunt", "battery monitor,\nnegative side", GRY)
    blk(70, 38, 20, 13, "DIN rail breakers", "inverter 63 A, MPPT 25 A,\nDC panel 32 A, PV 20 A", RED)
    blk(98, 44, 21, 11, "Inverter 1 kW", "24 V in, 120 V out", "#0E7490")
    blk(98, 28, 21, 11, "GFCI outlet", "in-use cover", "#F59E0B")
    blk(70, 14, 20, 12, "MPPT 100 V 20 A", "LiFePO4 profile", "#0F766E")
    blk(98, 12, 21, 12, "DC panel", "24 to 12 V converter,\nUSB-C PD, 12 V sockets", "#D4A017")
    blk(98, 62, 21, 7, "PV wings (2)", "in parallel, via PV glands", "#1E3A8A")
    blk(70, 62, 20, 7, "Fan thermostat", "24 V filter fan", GRY)
    wire([(17, 26), (17, 38)], RED); lab(17.6, 32, "+ 16 mm2", RED)
    wire([(28, 43.5), (48, 43.5)], RED); lab(35, 45.6, "+ 16 mm2 through gland", RED, "left")
    wire([(63, 43.5), (70, 43.5)], RED); lab(66.5, 45.6, "16 mm2", RED, "center")
    wire([(90, 49.5), (98, 49.5)], RED); lab(94, 51.6, "16 mm2", RED, "center")
    wire([(108.5, 44), (108.5, 39)], AMB); lab(109.2, 41.5, "120 V, 2.5 mm2", AMB)
    wire([(28, 18), (48, 18)], BLU); lab(35, 20, "- 16 mm2 through gland", BLU)
    wire([(63, 17.5), (66, 17.5), (66, 10), (95, 10), (95, 46), (98, 46)], BLU, 1.6); lab(80, 8.3, "negative bus, 16 mm2: inverter, MPPT and DC panel negatives to the shunt load side", BLU, "center")
    wire([(80, 38), (80, 26)], RED); lab(80.6, 32, "MPPT out, 6 mm2", RED)
    wire([(90, 41), (94, 41), (94, 21), (98, 21)], RED, 1.6); lab(93.4, 30, "DC panel,\n6 mm2", RED, "right")
    wire([(108.5, 62), (108.5, 57), (92, 57), (92, 23), (90, 23)], "#1E3A8A", 1.6); lab(100, 59.4, "PV +/-, 4 mm2, via the PV breaker", "#1E3A8A", "center")
    wire([(80, 62), (80, 51)], GRY, 1.2); lab(80.6, 56, "fan, 0.75 mm2", GRY)
    ax.text(3, 7.0, "Safety: class T fuse OUT until the stops in section 6 of the plan are passed. Never connect FieldCell to building wiring. "
            "PV leads are live whenever lit.", fontsize=7.6, color=WARN, fontweight="bold")
    ax.text(3, 4.2, "Red: positive DC. Blue: negative DC. Amber: 120 V AC. Breaker ratings are a starting point: set them from the chosen parts' datasheets.",
            fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["sheet"]:
        print(sheets([int(a) for a in args[1:]]))
    elif args[:1] == ["step"]:
        print(steps([int(a) for a in args[1:]]))
    elif args[:1] == ["joint"]:
        print(joints([int(a) for a in args[1:]]))
    else:
        what = args or ["layouts", "wiring", "overview", "sheets", "joints", "steps"]
        fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
        for w in what:
            print(w, "->", fns[w]())
