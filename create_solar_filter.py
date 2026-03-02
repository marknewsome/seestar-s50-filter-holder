"""
Seestar S50 Solar Filter for Baader Film
Single-piece press-fit design — matches OEM form factor, ~2mm protrusion above scope face
"""

import cadquery as cq
import math

# Dimensions (in mm)
MOUNT_DIAMETER    = 49.5  # Fits into 50mm Seestar recess (0.25mm clearance per side)
MOUNT_DEPTH       = 6.2   # Seestar recess is 7.04mm deep; 6.2mm seats without bottoming out
LENS_OPENING      = 46    # Clear aperture for Baader film
FLANGE_DIAMETER   = 56    # Outer lip that rests on scope face and provides grip
FLANGE_HEIGHT     = 2     # Protrusion above scope face (low-profile like OEM)
FILM_GROOVE_WIDTH = 3     # Width of annular groove on top face for gluing film
FILM_GROOVE_DEPTH = 1     # Groove depth; 1mm of solid remains below

# OEM-style curved tab — annular sector flush with flange top
TAB_INNER_RADIUS = FLANGE_DIAMETER / 2        # 28mm — starts at flange outer edge
TAB_OUTER_RADIUS = FLANGE_DIAMETER / 2 + 10   # 38mm — extends 10mm radially
TAB_ANGLE_SPAN   = 30                          # degrees of arc span (~16mm at outer edge)
TAB_HEIGHT       = FLANGE_HEIGHT               # coplanar with flange (no extra protrusion)
TAB_CENTER_ANGLE = 0                           # degrees; 0° = "3 o'clock"
HOLE_DIAMETER    = 4                           # mm; lanyard/safety-cord hole

# Tab arc geometry
_ha  = TAB_ANGLE_SPAN / 2
_s   = math.radians(TAB_CENTER_ANGLE - _ha)
_m   = math.radians(TAB_CENTER_ANGLE)
_e   = math.radians(TAB_CENTER_ANGLE + _ha)
ri, ro = TAB_INNER_RADIUS, TAB_OUTER_RADIUS

inner_start = (ri * math.cos(_s), ri * math.sin(_s))
inner_mid   = (ri * math.cos(_m), ri * math.sin(_m))
inner_end   = (ri * math.cos(_e), ri * math.sin(_e))
outer_start = (ro * math.cos(_s), ro * math.sin(_s))
outer_mid   = (ro * math.cos(_m), ro * math.sin(_m))
outer_end   = (ro * math.cos(_e), ro * math.sin(_e))

# Annular-sector profile: inner arc CCW → radial line → outer arc CW → close
tab = (
    cq.Workplane("XY")
    .moveTo(*inner_start)
    .threePointArc(inner_mid, inner_end)
    .lineTo(*outer_end)
    .threePointArc(outer_mid, outer_start)
    .close()
    .extrude(TAB_HEIGHT)
)

# Lanyard hole — centred radially and angularly in the tab
_hole_r = (ri + ro) / 2
hole_x  = _hole_r * math.cos(_m)
hole_y  = _hole_r * math.sin(_m)

hole_cutter = (
    cq.Workplane("XY")
    .center(hole_x, hole_y)
    .circle(HOLE_DIAMETER / 2)
    .extrude(TAB_HEIGHT)
)

filter_body = (
    cq.Workplane("XY")
    # Flange — sits on scope face (Z=0 to Z=FLANGE_HEIGHT)
    .circle(FLANGE_DIAMETER / 2)
    .circle(LENS_OPENING / 2)
    .extrude(FLANGE_HEIGHT)
    # Grip ridges on flange underside — add BEFORE nub so faces("<Z") = Z=0 (flange bottom)
    .faces("<Z")
    .workplane()
    .polarArray((FLANGE_DIAMETER - 4) / 2, 0, 360, 16)
    .rect(2, 3)
    .cutBlind(-1.5)
    # Press-fit nub — presses into Seestar recess (extends down from Z=0)
    .faces("<Z")
    .circle(MOUNT_DIAMETER / 2)
    .circle(LENS_OPENING / 2)
    .extrude(MOUNT_DEPTH)
    # Film seating groove on top face — annular pocket for gluing Baader film
    .faces(">Z")
    .workplane()
    .circle((LENS_OPENING + 2 * FILM_GROOVE_WIDTH) / 2)
    .circle(LENS_OPENING / 2)
    .cutBlind(-FILM_GROOVE_DEPTH)
    # OEM-style curved tab
    .union(tab)
    # Lanyard hole through tab
    .cut(hole_cutter)
)

# ── Text engraving on tab top face ────────────────────────────────────────────
# Two lines centred on the tab.  rotate=(0,0,90+TAB_CENTER_ANGLE) makes the text
# read along the arc rather than radially.  Lines sit 4 mm inset from each edge.
_engrave_depth     = 0.4   # mm deep — visible on 0.2 mm layer-height prints
_engrave_font_size = 1.5   # mm  — fits "Seestar S50 filter" (~16 mm) in 17 mm arc
_text_rotate_z     = TAB_CENTER_ANGLE + 90

# Place each line one font-height clear of the hole edge so the hole doesn't
# cut through the text.  Hole centre = _hole_r (33 mm), radius = HOLE_DIAMETER/2.
_tab_r1 = _hole_r - HOLE_DIAMETER / 2 - _engrave_font_size  # 29.5 mm — inside the hole
_tab_r2 = _hole_r + HOLE_DIAMETER / 2 + _engrave_font_size  # 36.5 mm — outside the hole

_text_line1 = (
    cq.Workplane("XY")
    .transformed(
        offset=(_tab_r1 * math.cos(_m), _tab_r1 * math.sin(_m),
                FLANGE_HEIGHT - _engrave_depth),
        rotate=(0, 0, _text_rotate_z),
    )
    .text("Seestar S50 filter", fontsize=_engrave_font_size, distance=_engrave_depth,
          halign='center', valign='center', font='Arial')
)
_text_line2 = (
    cq.Workplane("XY")
    .transformed(
        offset=(_tab_r2 * math.cos(_m), _tab_r2 * math.sin(_m),
                FLANGE_HEIGHT - _engrave_depth),
        rotate=(0, 0, _text_rotate_z),
    )
    .text("by AstroMark", fontsize=_engrave_font_size, distance=_engrave_depth,
          halign='center', valign='center', font='Arial')
)
filter_body = filter_body.cut(_text_line1).cut(_text_line2)

RETAINING_RING_HEIGHT = 1.5  # Thin washer that sandwiches film into the groove

retaining_ring = (
    cq.Workplane("XY")
    .circle((LENS_OPENING + 2 * FILM_GROOVE_WIDTH) / 2)
    .circle(LENS_OPENING / 2)
    .extrude(RETAINING_RING_HEIGHT)
)

# ── Combined single-file print ─────────────────────────────────────────────────
# Retaining ring floats above filter body with a print-clearance gap, held by
# three thin sprues that are easily cut with flush cutters or a hobby knife.
SPRUE_GAP        = 0.5   # mm gap between parts — enough for a thin blade
SPRUE_SIZE       = 1.2   # mm square cross-section — small enough to cut by hand
SPRUE_BITE       = 0.4   # mm the sprue penetrates each part for a solid union
SPRUE_COUNT      = 3
SPRUE_START_ANGLE = 60   # degrees — offset so sprues avoid the 0° tab

# Retaining ring lifted by the print gap
_ring_z = FLANGE_HEIGHT + SPRUE_GAP
retaining_ring_lifted = retaining_ring.translate((0, 0, _ring_z))

# Sprue radial position: midpoint of retaining ring width (r = 23–26 mm)
_sprue_r = (LENS_OPENING / 2 + (LENS_OPENING + 2 * FILM_GROOVE_WIDTH) / 2) / 2
_sprue_z = FLANGE_HEIGHT - SPRUE_BITE                           # start (inside flange top)
_sprue_h = SPRUE_BITE + SPRUE_GAP + RETAINING_RING_HEIGHT + SPRUE_BITE  # total height

def _make_sprue(angle_deg):
    a = math.radians(angle_deg)
    x = _sprue_r * math.cos(a)
    y = _sprue_r * math.sin(a)
    return (
        cq.Workplane("XY")
        .center(x, y)
        .rect(SPRUE_SIZE, SPRUE_SIZE)
        .extrude(_sprue_h)
        .translate((0, 0, _sprue_z))
    )

combined_body = filter_body.union(retaining_ring_lifted)
for i in range(SPRUE_COUNT):
    combined_body = combined_body.union(
        _make_sprue(SPRUE_START_ANGLE + i * (360 / SPRUE_COUNT))
    )

cq.exporters.export(filter_body,    "seestar_s50_solar_filter.stl")
cq.exporters.export(retaining_ring, "seestar_s50_solar_filter_retainer.stl")
cq.exporters.export(combined_body,  "seestar_s50_solar_filter_combined.stl")

film_diameter = LENS_OPENING + 2 * FILM_GROOVE_WIDTH

print("STL files generated:")
print("  seestar_s50_solar_filter.stl")
print("  seestar_s50_solar_filter_retainer.stl")
print("  seestar_s50_solar_filter_combined.stl  ← single file for print libraries")
print(f"\nCut Baader film to {film_diameter}mm diameter circle")
print("\nAssembly instructions (combined print):")
print(f"1. Cut Baader film to {film_diameter}mm diameter")
print("2. Clip or knife the 3 sprues at the gap line to free the retaining ring")
print("3. Apply thin bead of RTV silicone in the groove on the top face")
print("4. Lay film over the opening and press edges into the groove")
print("5. Apply another thin bead of RTV on top of the film edge")
print("6. Press retaining ring down over film to sandwich it in the groove")
print("7. Allow to cure fully before use")
print("8. Press nub into Seestar S50 front recess to mount")
print("\nPrint settings:")
print("- Material: PETG or ABS (heat resistant)")
print("- Layer height: 0.2mm")
print("- Infill: 40%")
print("- Supports: None needed")
print("- Orientation: Flange-side down (nub pointing up during print)")
