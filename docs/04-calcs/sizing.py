"""FieldCell sizing calculations for FCL-CAL-001 (docs/04-calcs/01-sizing.md).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number that FCL-CAL-001 quotes. Geometry comes from PARAMS in
cad/src/model.py, so the calc and the model share one set of dimensions.
First-principles estimates for a TRL 3 paper proof of concept; assumptions are
stated inline and in the note. Not a substitute for test.
"""
import csv
import sys
from math import radians, degrees, sin, cos, tan, atan, sqrt, pi, exp
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived  # noqa: E402

D = derived(P)
G = 9.81
RHO_AIR = 1.225
out = []


def say(tag, text):
    line = f"[{tag}] {text}"
    out.append(line)
    print(line)


# ============================================================ A. Energy storage (R1)
V_NOM, AH, DOD = 25.6, 50.0, 0.90           # 8S LiFePO4, 3.2 V per cell; usable depth of discharge
E_nom = V_NOM * AH                            # Wh
E_use = E_nom * DOD
say("A1", f"stored energy {E_nom:.0f} Wh nominal, {E_use:.0f} Wh usable at {DOD:.0%} depth of discharge")

# ============================================================ B. Electrical (R2)
P_AC, P_SURGE, ETA_INV_FULL = 1000.0, 2000.0, 0.90
V_LOW = 24.0                                  # pack near the low end of its discharge curve
P_DC = 2 * 100.0 + 12.0 * 20.0                # 2 x USB-C PD 100 W + 12 V 20 A converter
ETA_DC = 0.93
I_ac = P_AC / ETA_INV_FULL / V_LOW
I_surge = P_SURGE / 0.85 / V_LOW
I_dc = P_DC / ETA_DC / V_LOW
I_cont = I_ac + I_dc
say("B1", f"DC outlet capacity {P_DC:.0f} W (target 300 W)")
say("B2", f"battery current: 1 kW AC {I_ac:.1f} A, 2 kW surge {I_surge:.0f} A, full DC {I_dc:.1f} A, "
          f"AC plus DC continuous {I_cont:.1f} A ({I_cont / 100:.0%} of the 100 A fuse and BMS rating); "
          f"surge plus full DC {I_surge + I_dc:.0f} A for seconds")
RHO_CU, A_CABLE, L_LOOP = 0.0172, 16.0, 1.5   # ohm mm2/m, mm2, m of loop battery to inverter and back
R_cable = RHO_CU * L_LOOP / A_CABLE
dv = I_cont * R_cable
say("B3", f"16 mm2 cable, {L_LOOP} m loop: {R_cable * 1000:.2f} mohm, drop {dv:.2f} V ({dv / V_LOW:.1%}) at {I_cont:.0f} A, "
          f"{I_cont ** 2 * R_cable:.1f} W")
# PV string window: two panels in parallel into one MPPT
VMP, VOC, ISC = 36.0, 45.0, 6.0               # per panel at STC (24 V class, assumed datasheet values)
BETA_VOC, BETA_VMP = -0.0029, -0.0035         # per K
T_COLD, T_HOT = -10.0, 70.0                   # cell temperatures
voc_cold = VOC * (1 + BETA_VOC * (T_COLD - 25))
vmp_hot = VMP * (1 + BETA_VMP * (T_HOT - 25))
V_ABS = 28.4                                  # absorption voltage for 8S LiFePO4
say("B4", f"PV Voc at {T_COLD:.0f} C cell {voc_cold:.1f} V (MPPT limit 100 V); Vmp at {T_HOT:.0f} C cell {vmp_hot:.1f} V "
          f"against {V_ABS + 1:.1f} V needed (absorption + 1 V): headroom {vmp_hot - V_ABS - 1:.1f} V")
I_mppt_max = 2 * 200 * 0.96 / (V_NOM)
say("B5", f"PV input {2 * ISC:.0f} A short circuit (two in parallel); MPPT output at 400 W {I_mppt_max:.1f} A (20 A rating); "
          f"reverse current into one panel at most {ISC:.0f} A, so no per-panel fuse is needed for two in parallel")

# ============================================================ C. Irradiance and PV yield (R3)
# Clear-sky shape model, used only for transposition ratios (plane of array / global horizontal).
I_SC, B0_IAM, ALBEDO, K_DIFF = 1361.0, 0.05, 0.20, 0.12


def day_profile(lat, n, planes, step_min=5):
    """Daily irradiation (Wh/m2) on horizontal and on each plane (tilt, azimuth from south, + west)."""
    phi = radians(lat)
    dec = radians(23.45 * sin(radians(360 * (284 + n) / 365)))
    i0 = I_SC * (1 + 0.033 * cos(radians(360 * n / 365)))
    ghi_sum, sums, wsum, w2sum = 0.0, [0.0] * len(planes), 0.0, 0.0
    for k in range(int(24 * 60 / step_min)):
        w = radians((k * step_min / 60 - 12) * 15)
        sa = sin(phi) * sin(dec) + cos(phi) * cos(dec) * cos(w)
        if sa <= 0.02:
            continue
        alt = degrees(atan(sa / sqrt(max(1e-9, 1 - sa * sa))))
        am = 1 / (sa + 0.50572 * (alt + 6.07995) ** -1.6364)
        dni = i0 * 0.7 ** (am ** 0.678)
        dhi = K_DIFF * dni
        ghi = dni * sa + dhi
        s = (-cos(dec) * sin(w), cos(phi) * sin(dec) - sin(phi) * cos(dec) * cos(w), sa)   # east, north, up
        ghi_sum += ghi * step_min / 60
        for j, (tilt, az) in enumerate(planes):
            if tilt is None:   # two-axis tracking reference
                poa = dni + dhi
            else:
                b, a = radians(tilt), radians(az)
                nrm = (-sin(b) * sin(a), -sin(b) * cos(a), cos(b))   # azimuth from south, positive west
                ct = sum(p * q for p, q in zip(s, nrm))
                iam = max(0.0, 1 - B0_IAM * (1 / ct - 1)) if ct > 0.05 else 0.0
                poa = dni * max(0.0, ct) * iam + dhi * (1 + cos(b)) / 2 + ALBEDO * ghi * (1 - cos(b)) / 2
            sums[j] += poa * step_min / 60
            if j == 0:
                wsum += poa; w2sum += poa * poa
    return ghi_sum, sums, (w2sum / wsum if wsum else 0)


TILT = P["tilt"]
cases = [(15, "tropics 15 N"), (30, "subtropics 30 N"), (45, "mid-latitude 45 N")]
days = [(80, "equinox"), (172, "June solstice"), (355, "December solstice")]
ratios = []
say("C0", "transposition ratio, plane of array / global horizontal (IAM included); E-W = mean of the two wings")
for lat, lname in cases:
    for n, dname in days:
        planes = [(TILT, -90), (TILT, 90), (lat, 0), (None, 0)]
        ghi, s, g_w = day_profile(lat, n, planes)
        ew = (s[0] + s[1]) / 2 / ghi
        south = s[2] / ghi
        track = s[3] / ghi
        ratios.append((lat, n, ew, south, track, g_w, ghi))
        say("C0", f"  {lname:18s} {dname:17s} GHI {ghi / 1000:4.1f} kWh/m2  E-W {ew:.3f}  south at {lat} deg {south:.3f}  "
                  f"two-axis {track:.3f}  E-W/south {ew / south:.2f}  POA energy-weighted G {g_w:.0f} W/m2")
R_EW = sum(r[2] for r in ratios) / len(ratios)
R_EW_MIN = min(r[2] for r in ratios)
EW_VS_SOUTH = sum(r[2] / r[3] for r in ratios) / len(ratios)
G_W = sum(r[5] for r in ratios) / len(ratios)
say("C1", f"E-W wings: mean ratio {R_EW:.3f} (lowest {R_EW_MIN:.3f}); against a south panel at latitude tilt {EW_VS_SOUTH:.2f} "
          f"(penalty {1 - EW_VS_SOUTH:.0%}); energy-weighted POA irradiance {G_W:.0f} W/m2")

# Temperature derating: semi-flexible module bonded to a ventilated backing frame
NOCT, GAMMA = 48.0, -0.0038
def f_temp(t_amb):
    t_cell = t_amb + (NOCT - 20) / 800 * G_W
    return 1 + GAMMA * (t_cell - 25), t_cell
F_NAME, F_SOIL, F_MIS, F_WIRE, ETA_MPPT, ETA_CHG = 0.97, 0.97, 0.98, 0.98, 0.96, 0.97
P_STC = 2 * 200.0


def e_batt(psh, t_amb=25.0, ratio=R_EW):
    ft, _ = f_temp(t_amb)
    return psh * P_STC / 1000 * ratio * ft * F_NAME * F_SOIL * F_MIS * F_WIRE * ETA_MPPT * ETA_CHG


ft25, tc25 = f_temp(25); ft40, tc40 = f_temp(40)
PR = R_EW * ft25 * F_NAME * F_SOIL * F_MIS * F_WIRE
say("C2", f"cell temperature {tc25:.0f} C at 25 C ambient (factor {ft25:.3f}), {tc40:.0f} C at 40 C ambient (factor {ft40:.3f})")
say("C3", f"array factor PR (GHI to array DC) {PR:.3f}; to battery {PR * ETA_MPPT * ETA_CHG:.3f}")
for psh in (4.0, 4.5, 5.0):
    say("C4", f"  {psh} kWh/m2/day GHI: into battery {e_batt(psh):.2f} kWh/day at 25 C, {e_batt(psh, 40):.2f} at 40 C, "
              f"{e_batt(psh, 25, R_EW_MIN):.2f} at the lowest ratio")
E4, E45, E5 = e_batt(4.0), e_batt(4.5), e_batt(5.0)
E_full = E_nom * 0.90                           # 10 % to 100 %
say("C5", f"full recharge 10 to 100 % ({E_full:.0f} Wh): {E_full / 1000 / E5:.2f} day at 5 h, {E_full / 1000 / E4:.2f} day at 4 h")
P_peak = P_STC * max(r[2] for r in ratios) * 0.95 * ft25 * F_NAME * F_SOIL * F_MIS * F_WIRE * ETA_MPPT
say("C6", f"peak charge power at noon about {P_peak * 0.9:.0f} to {P_peak:.0f} W")

# ============================================================ D. Load and autonomy (R4)
LOADS = [  # name, W, h/day, path
    ("LED area lighting", 30, 8, "DC"), ("Radio, phone and messenger charging", 30, 8, "DC"),
    ("Laptop and Wi-Fi router", 50, 6, "AC"), ("Power tool or small pump", 700, 10 / 60, "AC")]
INV_P0, INV_ETA_M, INV_HOURS = 10.0, 0.92, 7.0    # inverter no-load draw while on, marginal efficiency, hours on
STANDBY, FAN = 12.0, 3.0 * 4                       # BMS, monitor, MPPT night, DC converter idle; filter fan 3 W x 4 h
e_dc = sum(p * h for _, p, h, path in LOADS if path == "DC")
e_ac = sum(p * h for _, p, h, path in LOADS if path == "AC")
b_dc = e_dc / ETA_DC
b_ac = e_ac / INV_ETA_M + INV_P0 * INV_HOURS
LOAD_OUT = e_dc + e_ac
LOAD_BATT = b_dc + b_ac + STANDBY + FAN
say("D1", f"reference load at outlets {LOAD_OUT:.0f} Wh/day (DC {e_dc:.0f}, AC {e_ac:.0f})")
say("D2", f"from battery: DC {b_dc:.0f}, AC incl. idle {b_ac:.0f} (idle {INV_P0 * INV_HOURS:.0f}), standby {STANDBY:.0f}, "
          f"fan {FAN:.0f}: total {LOAD_BATT:.0f} Wh/day, overall efficiency {LOAD_OUT / LOAD_BATT:.3f}")
AUTON = E_use / LOAD_BATT
say("D3", f"autonomy with no sun {AUTON:.2f} days")
for psh, e in ((4.0, E4), (4.5, E45), (5.0, E5)):
    say("D4", f"  {psh} h: energy balance {e * 1000 - LOAD_BATT:+.0f} Wh/day ({e * 1000 / LOAD_BATT - 1:+.0%})")
say("D5", f"break-even GHI {LOAD_BATT / 1000 / e_batt(1.0):.2f} kWh/m2/day at 25 C, {LOAD_BATT / 1000 / e_batt(1.0, 40):.2f} at 40 C")
say("D6", f"idle sensitivity: each 5 W of inverter no-load draw over 7 h costs {5 * 7:.0f} Wh/day "
          f"({5 * 7 / LOAD_BATT:.1%} of the load)")

# ============================================================ E. Mass, center of gravity, handle force (R6)
RHO_ST, RHO_AL = 7850e-9, 2700e-9    # kg/mm3
def sq_tube_kg_per_m(a, t, rho):
    return (a * a - (a - 2 * t) ** 2) * 1000 * rho
L, W_, R_ = P["deck_l"], P["deck_w"], P["rail"]
tube_len = 2 * L + 3 * (W_ - 2 * R_)
m_tubes = tube_len / 1000 * sq_tube_kg_per_m(R_, P["rail_wall"], RHO_ST)
m_deck = (L - 2 * R_) * (W_ - 2 * R_) * 1e-6 * 4.5          # expanded steel, 4.5 kg/m2 assumed
m_axle = pi * (P["axle_d"] / 2) ** 2 * 2 * P["wheel_y"] * RHO_ST
m_brk = 1.2                                                  # two axle brackets, welds, hinge mounts
m_frame = m_tubes + m_deck + m_axle + m_brk
m_frame_al = tube_len / 1000 * sq_tube_kg_per_m(R_, 2.0, RHO_AL) + m_deck * 0.4 + m_axle + m_brk * 0.5
say("E1", f"frame: tubes {tube_len / 1000:.2f} m x {sq_tube_kg_per_m(R_, P['rail_wall'], RHO_ST):.2f} kg/m = {m_tubes:.1f} kg, "
          f"deck {m_deck:.1f}, axle {m_axle:.1f}, brackets {m_brk:.1f}: {m_frame:.1f} kg steel "
          f"(bolted aluminium alternative about {m_frame_al:.1f} kg)")
hl = 2 * sqrt((P["grip_x"] - (L / 2 - 20)) ** 2 + (P["grip_z"] - D["rail_z"]) ** 2) + W_ + 40
m_handle = hl / 1000 * pi / 4 * (P["handle_d"] ** 2 - (P["handle_d"] - 3) ** 2) * 1000 * RHO_ST + 0.4
ax, ex, bx = P["axle_x"], D["ebox_x"], D["bin_x"]
MASS = [  # name, kg, x (mm from deck center, + toward handle), z (mm)
    ("Frame, deck and axle", m_frame, 0, 430),
    ("Wheels, flat-free (2 x 4.0 kg)", 8.0, ax, P["wheel_r"]),
    ("Handle", m_handle, 950, 700),
    ("Stand legs (4)", 1.8, 0, 230),
    ("Battery enclosure", 3.0, 0, 610),
    ("LiFePO4 pack", 12.0, 0, 576),
    ("Electronics enclosure, filter fan", 3.3, ex, 610),
    ("Inverter (high-frequency)", 4.0, ex, 521),
    ("MPPT, fusing, monitor, outlets", 4.0, ex, 580),
    ("Accessory bin and cables", 4.0, bx, 560),
    ("PV wings, stowed (2 x 6.5 kg)", 13.0, 0, P["hinge_z"] + P["pv_w"] / 2),
    ("Hinges, latches, outriggers, stakes", 3.0, 0, 780),
    ("Wiring and hardware", 2.0, 200, 600),
]
M = sum(m for _, m, _, _ in MASS)
cgx = sum(m * x for _, m, x, _ in MASS) / M
cgz = sum(m * z for _, m, _, z in MASS) / M
for name, m, x, z in MASS:
    say("E2", f"  {name:38s} {m:5.1f} kg  x {x:5.0f}  z {z:4.0f}")
say("E3", f"total {M:.1f} kg (limit 70 kg, margin {70 - M:+.1f} kg); CG x {cgx:.0f} mm, z {cgz:.0f} mm")
d_cg = cgx - ax
lever = P["grip_x"] - ax
W = M * G
F_h = W * d_cg / lever
dx5 = (cgz - P["wheel_r"]) * sin(radians(5))
say("E4", f"CG {d_cg:.0f} mm toward the handle from the axle; handle force {F_h:.0f} N level, "
          f"{W * (d_cg - dx5) / lever:.0f} to {W * (d_cg + dx5) / lever:.0f} N over +/-5 deg pitch")
say("E5", f"mass with the aluminium frame {M - m_frame + m_frame_al:.1f} kg; with pneumatic tyres (2 x 2.8 kg) "
          f"{M - 8.0 + 5.6:.1f} kg; with both {M - m_frame + m_frame_al - 2.4:.1f} kg")
say("E7", f"trim: moving 4 kg from the bin (x {bx:.0f}) to the electronics end (x {ex:.0f}) changes the handle force by "
          f"{4 * G * (ex - bx) / lever:.0f} N")
say("E6", f"heaviest removable module: LiFePO4 pack 12.0 kg (limit 25 kg)")

# ============================================================ F. Rough ground (R7)
th = atan(0.10)
for surf, crr in (("hard or packed", 0.04), ("gravel", 0.06), ("grass", 0.10)):
    say("F1", f"  pull on a 10 % grade, {surf} (Crr {crr}): {W * (sin(th) + crr * cos(th)):.0f} N (limit 150 N)")
F_grass = W * (sin(th) + 0.10 * cos(th))
h_step, r_w = 150.0, P["wheel_r"]
a_e = sqrt(h_step * (2 * r_w - h_step))          # horizontal distance axle to step edge at contact
arm_w = a_e - d_cg                                # CG behind the edge
F_step = W * arm_w / 1000 / ((P["grip_z"] - h_step) / 1000)
say("F2", f"150 mm step, handle first: edge {a_e:.0f} mm ahead of the axle, weight moment {W * arm_w / 1000:.0f} N m, "
          f"horizontal pull at the grip about {F_step:.0f} N (no vertical lift); a straight push at the axle would need "
          f"{W * a_e / (r_w - h_step):.0f} N")
clear = P["wheel_r"] - P["axle_d"] / 2
tip = degrees(atan(P["wheel_y"] / cgz))
say("F3", f"ground clearance under the axle {clear:.0f} mm; lateral static tip angle {tip:.1f} deg")
say("F4", f"deployed wing to tyre clearance {D['wing_tyre_gap']:.0f} mm")
# Frame and axle strength, 2 g bump
m_can = 30.0 * G * 2 * 0.40 / 2                    # 30 kg cantilevered 0.40 m on two rails at 2 g, per rail
I_r = (R_ ** 4 - (R_ - 2 * P["rail_wall"]) ** 4) / 12
sig_rail = m_can * 1000 / (I_r / (R_ / 2))
F_wh = W * 2 / 2
M_ax = F_wh * (P["wheel_y"] - P["bracket_y"]) / 1000
sig_ax = M_ax * 1000 / (pi * P["axle_d"] ** 3 / 32)
say("F5", f"side rail at 2 g: {m_can:.0f} N m, {sig_rail:.0f} MPa (S235 yield 235, factor {235 / sig_rail:.1f}); "
          f"axle at 2 g: {M_ax:.0f} N m, {sig_ax:.0f} MPa (bright mild steel yield about 350, factor {350 / sig_ax:.1f})")

# ============================================================ G. Thermal (R8, R9)
SIGMA, EPS = 5.67e-8, 0.9
def h_ext(dT, t_amb):
    tm = t_amb + 273.15 + dT / 2
    return 1.42 * (max(dT, 1) / 0.3) ** 0.25 + 4 * EPS * SIGMA * tm ** 3
eb = P["ebox"]
A_e = 2 * (eb[0] * eb[2] + eb[1] * eb[2]) * 1e-6 + eb[0] * eb[1] * 1e-6     # walls and top, bottom on the deck
def inv_loss(p):
    return p / (INV_ETA_M if p < 900 else ETA_INV_FULL) - p + INV_P0
Q_500 = inv_loss(500) + 10 + 5          # inverter, MPPT at about 250 W, DC converters light
Q_1k = inv_loss(1000) + 12 + 7          # inverter, MPPT at 300 W, DC 100 W
ALPHA_SOL, G_SUN = 0.4, 1000.0          # light grey enclosure, noon sun
Q_sun = ALPHA_SOL * G_SUN * (eb[0] * eb[1] + 0.5 * eb[1] * eb[2]) * 1e-6
def sealed_rise(q, t_amb):
    dT = 20.0
    for _ in range(30):
        dT = q / (h_ext(dT, t_amb) * A_e)
    return dT
FAN_M3H = 40.0
mcp = 1.2 * 1005 * FAN_M3H / 3600
def vented_rise(q, t_amb):
    return q / (mcp + h_ext(5, t_amb) * A_e)
say("G1", f"electronics box: walls and top {A_e:.2f} m2; losses {Q_500:.0f} W at 500 W AC, {Q_1k:.0f} W at 1 kW AC; "
          f"solar gain up to {Q_sun:.0f} W (absorptance {ALPHA_SOL})")
for label, q in (("500 W", Q_500), ("1 kW", Q_1k), ("1 kW + half solar", Q_1k + Q_sun / 2)):
    s45, v45 = sealed_rise(q, 45), vented_rise(q, 45)
    say("G2", f"  {label:18s} sealed rise {s45:4.1f} K (inside {45 + s45:.0f} C at 45 C); "
              f"{FAN_M3H:.0f} m3/h filter fan rise {v45:4.1f} K (inside {45 + v45:.0f} C)")
need = (Q_1k + Q_sun / 2) / (1.2 * 1005 * 10) * 3600
say("G3", f"airflow for a 10 K rise at 1 kW with sun: {need:.0f} m3/h")
bbx = P["batt_box"]
A_b = 2 * (bbx[0] * bbx[2] + bbx[1] * bbx[2]) * 1e-6 + bbx[0] * bbx[1] * 1e-6
Qb = ALPHA_SOL * G_SUN * bbx[0] * bbx[1] * 1e-6
dTb = Qb / (h_ext(10, 35) * A_b)
tau = (12.0 * 1100 + 3.0 * 1500) / (h_ext(10, 35) * A_b) / 3600
R_PACK = 0.010
say("G4", f"battery box in noon sun: {Qb:.0f} W absorbed, steady rise about {dTb:.0f} K, time constant about {tau:.1f} h; "
          f"pack I2R at 1 kW {I_ac ** 2 * R_PACK:.0f} W, at the reference load {(LOAD_BATT / 24 / V_NOM) ** 2 * R_PACK * 24:.1f} Wh/day")
say("G5", f"pack in sun reaches about {45 + dTb:.0f} C at 45 C ambient and {35 + dTb:.0f} C at 35 C; "
          f"typical LiFePO4 charge limit 45 C")

# ============================================================ H. Wind (R10)
pw_m = P["pv_w"] / 1000
A_w = P["pv_l"] * P["pv_w"] * 1e-6
CN, M_WING = 1.2, 6.5
t = radians(TILT)
arm_wt = pw_m / 2 * cos(t)
arm_out = (P["pv_w"] - 30) / 1000 * cos(t)
def lift_v():
    q = M_WING * G * arm_wt / (CN * A_w * pw_m / 2)
    return sqrt(2 * q / RHO_AIR)
v_lift = lift_v()
V_REQ = 15.0
q15 = 0.5 * RHO_AIR * V_REQ ** 2
F15 = CN * q15 * A_w
stake_wing = (F15 * pw_m / 2 - M_WING * G * arm_wt) / arm_out
stake_sf = (1.5 * F15 * pw_m / 2 - M_WING * G * arm_wt) / arm_out
say("H1", f"wing area {A_w:.2f} m2; unstaked wing lifts at about {v_lift:.1f} m/s")
say("H2", f"at {V_REQ:.0f} m/s: q {q15:.0f} Pa, normal force {F15:.0f} N per wing; stake pull-out {stake_wing / 2:.0f} N per foot "
          f"({stake_sf / 2:.0f} N with a 1.5 load factor)")
drag = 2 * F15 * sin(t) + 1.2 * q15 * (eb[1] * eb[2] + bbx[1] * bbx[2]) * 1e-6
normal = W - 2 * F15 * cos(t)
say("H3", f"whole cart at {V_REQ:.0f} m/s: uplift {2 * F15 * cos(t):.0f} N against weight {W:.0f} N; lateral load {drag:.0f} N "
          f"against friction {0.4 * normal:.0f} N (mu 0.4) unstaked; per staked foot {drag / 4:.0f} N lateral")
CD_S = 1.3
A_side = A_w
z_side = (P["hinge_z"] + P["pv_w"] / 2) / 1000
v_tip = sqrt(W * P["wheel_y"] / 1000 / (0.5 * RHO_AIR * CD_S * A_side * z_side))
say("H4", f"stowed cart, side wind on one wing wall: overturns at about {v_tip:.0f} m/s")

# ============================================================ I. Deploy (R5), noise (R11)
DEPLOY = [("Turn cart north to south, drop 4 stand legs", 1.0), ("Wing 1: unlatch, fold out, drop 2 outriggers", 1.5),
          ("Wing 2", 1.5), ("Stake 4 outrigger feet", 1.0), ("Isolator on, check monitor, inverter on, plug in", 1.0)]
STOW = [("Loads off, inverter off, isolator off", 0.5), ("Pull 4 stakes", 1.0), ("Wing 1: fold outriggers, raise, latch", 1.5),
        ("Wing 2", 1.5), ("Raise 4 stand legs", 0.5)]
say("I1", f"deploy {sum(t for _, t in DEPLOY):.1f} min, stow {sum(t for _, t in STOW):.1f} min (task analysis, limit 10 min)")
from math import log10
L_INV, L_FAN = 40.0, 35.0                       # dB(A) at 1 m, assumed, to confirm from datasheets
say("I2", f"noise at 1 m, 500 W: inverter fan {L_INV:.0f} + filter fan {L_FAN:.0f} dB(A) = "
          f"{10 * log10(10 ** (L_INV / 10) + 10 ** (L_FAN / 10)):.1f} dB(A) (assumed source levels)")

# ============================================================ J. Cost (R12)
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
top = sorted(rows, key=lambda r: -float(r["qty"]) * float(r["unit_cost_usd"]))[:3]
say("J1", f"BOM {len(rows)} lines, total ${total:,.0f} against budget $1,500: {total - 1500:+,.0f} ({total / 1500 - 1:+.0%})")
say("J2", "largest lines: " + ", ".join(f"{r['item']} ${float(r['qty']) * float(r['unit_cost_usd']):,.0f}" for r in top))

# ============================================================ K. Envelope
say("K1", f"deployed footprint {P['grip_x'] + P['pv_l'] / 2 + P['handle_d'] / 2:.0f} x {D['span']:.0f} mm; "
          f"stowed without handle {P['pv_l']:.0f} x {2 * (P['hinge_y'] + P['pv_t'] + P['out_d'] + 2):.0f} x "
          f"{P['hinge_z'] + P['pv_w']:.0f} mm")
