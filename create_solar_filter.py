"""
Seestar S50 Solar Filter for Baader Film
Single-piece press-fit design — matches OEM form factor, ~2mm protrusion above scope face

Combined print: filter body + retaining ring lay flat side-by-side, joined by two
thin sacrificial bridges (0.8 mm tall).  Snap or cut the bridges before assembly.
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

# ── Combined single-file print (flat layout with sacrificial bridges) ──────────
# Retaining ring sits to the LEFT of the filter body (opposite the 0° tab).
# Two ultra-thin bridges (0.4 mm = 2 layers) connect their facing edges —
# snap cleanly by hand or score with a fingernail.
BRIDGE_GAP    = 2.0  # mm between the two parts — room for a hobby knife blade
BRIDGE_WIDTH  = 3.0  # mm (Y extent per bridge)
BRIDGE_HEIGHT = 0.4  # mm tall — 2 × 0.2 mm layers; snaps with finger pressure

_ring_outer_r  = (LENS_OPENING + 2 * FILM_GROOVE_WIDTH) / 2    # 26 mm
_ring_offset_x = -(FLANGE_DIAMETER / 2 + BRIDGE_GAP + _ring_outer_r)  # -56 mm

# Retaining ring placed to the LEFT of the filter body (flat, same Z=0 base)
retaining_ring_flat = retaining_ring.translate((_ring_offset_x, 0, 0))

# Bridge geometry: spans the gap on the left side
_bridge_x1  = _ring_offset_x + _ring_outer_r   # right edge of retaining ring: -30 mm
_bridge_x2  = -FLANGE_DIAMETER / 2             # left edge of filter body:     -28 mm
_bridge_cx  = (_bridge_x1 + _bridge_x2) / 2    # centre of gap:                -29 mm
_bridge_len = _bridge_x2 - _bridge_x1          # == BRIDGE_GAP (2 mm)

# Two bridges symmetrically offset in Y
_bridge_y_spacing = BRIDGE_WIDTH + 3.0          # centre-to-centre: 6 mm

def _make_bridge(y_pos):
    return (
        cq.Workplane("XY")
        .center(_bridge_cx, y_pos)
        .rect(_bridge_len, BRIDGE_WIDTH)
        .extrude(BRIDGE_HEIGHT)
    )

combined_body = filter_body.union(retaining_ring_flat)
for y in (-_bridge_y_spacing / 2, _bridge_y_spacing / 2):
    combined_body = combined_body.union(_make_bridge(y))

cq.exporters.export(filter_body,    "output/seestar_s50_solar_filter.stl")
cq.exporters.export(retaining_ring, "output/seestar_s50_solar_filter_retainer.stl")
cq.exporters.export(combined_body,  "output/seestar_s50_solar_filter_combined.stl")

film_diameter = LENS_OPENING + 2 * FILM_GROOVE_WIDTH

print("STL files generated:")
print("  output/seestar_s50_solar_filter.stl")
print("  output/seestar_s50_solar_filter_retainer.stl")
print("  output/seestar_s50_solar_filter_combined.stl  ← single file for print libraries")
print(f"\nCut Baader film to {film_diameter}mm diameter circle")
print("\nAssembly instructions (combined print):")
print(f"1. Cut Baader film to {film_diameter}mm diameter")
print("2. Snap or knife the 2 flat bridges to separate the retaining ring")
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
print("- Orientation: Flat — both pieces print face-down on the bed")
print(f"- Layout: filter body at centre, retaining ring {abs(_ring_offset_x):.0f} mm to the left")
print(f"- Total footprint: ~{FLANGE_DIAMETER + BRIDGE_GAP + 2*_ring_outer_r:.0f} mm × {FLANGE_DIAMETER:.0f} mm")
