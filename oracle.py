#!/usr/bin/env python3
"""Independent oracle for Trellis math. Mirrors engine.js float ops exactly."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10

def num(x):
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return repr(x)

def slat_grid(w_cm, h_cm, gap_cm):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (w_cm, h_cm)):
        return {"error": "trellis dimensions must be positive"}
    if not (isinstance(gap_cm, (int, float)) and math.isfinite(gap_cm) and gap_cm > 0):
        return {"error": "gap must be positive"}
    v_slats = math.floor(w_cm / gap_cm) + 1
    h_slats = math.floor(h_cm / gap_cm) + 1
    if v_slats < 2 or h_slats < 2:
        return {"error": "gap is wider than the trellis"}
    real_gap_w = r1(w_cm / (v_slats - 1))
    real_gap_h = r1(h_cm / (h_slats - 1))
    lumber_m = r1((v_slats * h_cm + h_slats * w_cm) / 100)
    return {"wCm": r1(w_cm), "hCm": r1(h_cm), "vSlats": v_slats, "hSlats": h_slats,
            "realGapW": real_gap_w, "realGapH": real_gap_h, "lumberM": lumber_m}

def render_slat(r):
    if "error" in r: return r["error"]
    return (f"A {num(r['wCm'])} x {num(r['hCm'])} cm trellis takes {r['vSlats']} vertical and {r['hSlats']}"
            f" horizontal slats at a real {num(r['realGapW'])} x {num(r['realGapH'])} cm gap - about {num(r['lumberM'])}"
            " m of slat in total (labeled 15 cm grid).")

def twine_grid(w_cm, h_cm, grid_cm):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (w_cm, h_cm)):
        return {"error": "trellis dimensions must be positive"}
    if not (isinstance(grid_cm, (int, float)) and math.isfinite(grid_cm) and grid_cm > 0):
        return {"error": "grid size must be positive"}
    v_lines = math.floor(w_cm / grid_cm) + 1
    h_lines = math.floor(h_cm / grid_cm) + 1
    if v_lines < 2 or h_lines < 2:
        return {"error": "grid is wider than the trellis"}
    twine_m = r1((v_lines * h_cm + h_lines * w_cm) / 100 * 1.1)
    return {"wCm": r1(w_cm), "hCm": r1(h_cm), "vLines": v_lines, "hLines": h_lines, "twineM": twine_m}

def render_twine(r):
    if "error" in r: return r["error"]
    return (f"A {num(r['wCm'])} x {num(r['hCm'])} cm grid is {r['vLines']} vertical and {r['hLines']}"
            f" horizontal lines - about {num(r['twineM'])} m of twine with the labeled 10% for knots and tie-offs.")

def espalier_wire(w_cm, h_cm, row_gap_cm, anchor_gap_cm):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (w_cm, h_cm)):
        return {"error": "wall dimensions must be positive"}
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (row_gap_cm, anchor_gap_cm)):
        return {"error": "gaps must be positive"}
    rows = math.floor(h_cm / row_gap_cm)
    if rows < 1:
        return {"error": "wall is shorter than one labeled wire row"}
    anchors_per_row = math.floor(w_cm / anchor_gap_cm) + 1
    anchors = rows * anchors_per_row
    wire_m = r1(rows * w_cm / 100 * 1.05)
    return {"wCm": r1(w_cm), "hCm": r1(h_cm), "rows": rows, "anchorsPerRow": anchors_per_row,
            "anchors": anchors, "wireM": wire_m}

def render_espalier(r):
    if "error" in r: return r["error"]
    return (f"A {num(r['wCm'])} x {num(r['hCm'])} cm wall takes {r['rows']} wire rows at the labeled 40 cm spacing, "
            f"{r['anchorsPerRow']} anchors per row ({r['anchors']} vine eyes in total) and about {num(r['wireM'])}"
            " m of wire with the labeled 5% for tensioning.")

cases = []
for w, h, g in [(180, 180, 15), (120, 180, 15), (100, 100, 10), (200, 150, 20), (90, 90, 30),
                (180, 180, 12.5), (10, 180, 15), (180, 10, 15), (0, 180, 15), (180, -5, 15),
                (180, 180, 0), (250, 200, 15), (33, 44, 15)]:
    res = slat_grid(w, h, g)
    cases.append({"fn": "slatGrid", "args": [w, h, g], "result": res, "render": render_slat(res)})
for w, h, g in [(180, 180, 15), (120, 180, 10), (100, 100, 20), (200, 150, 15), (90, 90, 7.5),
                (10, 180, 15), (180, 10, 15), (0, 180, 15), (180, -5, 15), (180, 180, 0), (33, 44, 15)]:
    res = twine_grid(w, h, g)
    cases.append({"fn": "twineGrid", "args": [w, h, g], "result": res, "render": render_twine(res)})
for w, h, rg, ag in [(300, 200, 40, 60), (200, 160, 40, 60), (400, 240, 40, 60), (150, 100, 30, 50),
                     (300, 30, 40, 60), (100, 39, 40, 60), (0, 200, 40, 60), (300, -5, 40, 60),
                     (300, 200, 0, 60), (300, 200, 40, 0), (55, 80, 40, 60), (600, 300, 45, 75)]:
    res = espalier_wire(w, h, rg, ag)
    cases.append({"fn": "espalierWire", "args": [w, h, rg, ag], "result": res, "render": render_espalier(res)})

with open("expected.json", "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print(len(cases), "cases written")
