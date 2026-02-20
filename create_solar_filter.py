
"""
Seestar S50 Solar Filter for Baader Film
Single-piece press-fit design — matches OEM form factor, ~2mm protrusion above scope face
"""

import cadquery as cq

# Dimensions (in mm)
MOUNT_DIAMETER    = 49.5  # Fits into 50mm Seestar recess (0.25mm clearance per side)
MOUNT_DEPTH       = 6.2   # Seestar recess is 7.04mm deep; 6.2mm seats without bottoming out
LENS_OPENING      = 46    # Clear aperture for Baader film
FLANGE_DIAMETER   = 56    # Outer lip that rests on scope face and provides grip
FLANGE_HEIGHT     = 2     # Protrusion above scope face (low-profile like OEM)
FILM_GROOVE_WIDTH = 3     # Width of annular groove on top face for gluing film
FILM_GROOVE_DEPTH = 1     # Groove depth; 1mm of solid remains below

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
)

RETAINING_RING_HEIGHT = 1.5  # Thin washer that sandwiches film into the groove

retaining_ring = (
    cq.Workplane("XY")
    .circle((LENS_OPENING + 2 * FILM_GROOVE_WIDTH) / 2)
    .circle(LENS_OPENING / 2)
    .extrude(RETAINING_RING_HEIGHT)
)

cq.exporters.export(filter_body,    "seestar_s50_solar_filter.stl")
cq.exporters.export(retaining_ring, "seestar_s50_solar_filter_retainer.stl")

film_diameter = LENS_OPENING + 2 * FILM_GROOVE_WIDTH

print("STL files generated:")
print("  seestar_s50_solar_filter.stl")
print("  seestar_s50_solar_filter_retainer.stl")
print(f"\nCut Baader film to {film_diameter}mm diameter circle")
print("\nAssembly instructions:")
print(f"1. Cut Baader film to {film_diameter}mm diameter")
print("2. Apply thin bead of RTV silicone in the groove on the top face")
print("3. Lay film over the opening and press edges into the groove")
print("4. Apply another thin bead of RTV on top of the film edge")
print("5. Press retaining ring down over film to sandwich it in the groove")
print("6. Allow to cure fully before use")
print("7. Press nub into Seestar S50 front recess to mount")
print("\nPrint settings:")
print("- Material: PETG or ABS (heat resistant)")
print("- Layer height: 0.2mm")
print("- Infill: 40%")
print("- Supports: None needed")
print("- Orientation: Flange-side down (nub pointing up during print)")
