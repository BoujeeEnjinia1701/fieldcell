"""FieldCell general arrangement sheet FCL-DWG-002, Rev P2 (TRL 3).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/FCL-DWG-002.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Overall dimensions are drawn from the model
bounding box and PARAMS, so they follow any parameter change.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, project_views, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, build, derived  # noqa: E402
import contextlib, io  # noqa: E402
sys.path.insert(0, str(ROOT / "docs" / "04-calcs"))
with contextlib.redirect_stdout(io.StringIO()):
    import sizing as C  # noqa: E402

DATE = "2026-09-25"


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h, scale)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    """Horizontal dimension line with arrowheads and centered text above."""
    a = 1.4
    g = [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
         f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
         f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
         _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]
    return g


def dim_v(x, y1, y2, text):
    """Vertical dimension line with arrowheads and text rotated along it."""
    a = 1.4
    cx, cy = x - 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    dep, stow = build(deployed=True), build(deployed=False)
    views = project_views(dep, work / "deployed")
    views["iso"] = project_views(stow, work / "stowed")["iso"]
    bb = dep.bounding_box()
    s = Sheet(project="FieldCell", title="General arrangement", dwg_no="FCL-DWG-002", rev="P2",
              author="Amish Chadha", date=DATE, scale=None, theme="technical",
              material="Welded steel frame, IP65 and IP54 enclosures; see bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "Hinge spacer +20 mm, sun shade added (DDR-002)", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    # top view: overall length above, overall width at left
    x, y, w, h = c["top"]
    L += dim_h(x, x + w, y - 3.5, f"{bb.size.X:,.0f} overall")
    L += dim_v(x - 4, y, y + h, f"{bb.size.Y:,.0f} over outrigger feet")
    # front view (from -Y): overall height, deck height and hinge line, at left
    x, y, w, h = c["front"]
    zb = y + h                                   # ground line on the sheet
    L += [ext(x - 13, zb, x, zb)]
    L += dim_v(x - 4, y, zb, f"{bb.size.Z:,.0f}")
    L += dim_v(x - 10, zb - P["deck_z"] * k, zb, f"{P['deck_z']:.0f} deck")
    L += [ext(x - 11, zb - P["deck_z"] * k, x + (-P["deck_l"] / 2 - bb.min.X) * k, zb - P["deck_z"] * k)]
    # right view (from +X, +Y to the right): wheel track above, wing edge height at right
    x, y, w, h = c["right"]
    yc = x + w / 2
    wl, wr = yc - P["wheel_y"] * k, yc + P["wheel_y"] * k
    L += [ext(wl, y - 6, wl, y + h - P["wheel_r"] * k), ext(wr, y - 6, wr, y + h - P["wheel_r"] * k)]
    L += dim_h(wl, wr, y - 4, f"{2 * P['wheel_y']:.0f} track")
    ez = y + h - D["edge_z"] * k
    L += [ext(x + w - 4, ez, x + w + 6, ez)]
    L += dim_v(x + w + 5, ez, y + h, f"{D['edge_z']:.0f}")
    s._layers += L
    s.add_svg(views["iso"], 276, 32, 140, 106, label="Isometric view, stowed for travel", sublabel="Not to scale")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Deployed {bb.size.X:,.0f} L x {bb.size.Y:,.0f} W x {bb.size.Z:,.0f} H; wingspan {D['span']:,.0f}",
        f"Stowed, handle off: {P['pv_l']:,.0f} x {2 * (P['hinge_y'] + P['pv_t'] + P['out_d'] + 2):.0f} x {P['hinge_z'] + P['pv_w']:,.0f}",
        f"Frame {P['deck_l']:,.0f} x {P['deck_w']:.0f}, 40 x 40 x 1.5 steel tube; deck {P['deck_z']:.0f} parked",
        f"Wheels {2 * P['wheel_r']:.0f} dia., track {2 * P['wheel_y']:.0f}; axle {P['axle_x']:.0f} toward handle",
        f"Hinge line Y +/-{P['hinge_y']:.0f}, Z {P['hinge_z']:.0f}; wings {P['tilt']:.0f} deg below horizontal",
        f"Hinge on 20 spacer; wing to tyre clearance {D['wing_tyre_gap']:.0f}",
        "Reflective sun shade over both enclosures (item 18)",
        f"Outlet face toward handle; grip at Z {P['grip_z']:.0f}",
        f"Mass about {C.M:.1f} kg (FCL-CAL-001); 2 x 200 W PV, 1.28 kWh",
        "Third-angle; front view from -Y, right view from +X",
    ], x=276, y=160, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "FCL-DWG-002")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
