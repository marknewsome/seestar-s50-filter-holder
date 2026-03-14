# Seestar S50 Solar Filter

3D-printable solar filter kit for the ZWO Seestar S50 smart telescope.
Uses Baader AstroSolar film in a two-part press-fit design that matches the OEM form factor.

> **Status:** Awaiting first print result (submitted 29 Feb 2026)

---

## Parts

| File                                      | Description                                                                        |
|-------------------------------------------|------------------------------------------------------------------------------------|
| `seestar_s50_solar_filter.stl`            | Main filter body — OEM-style curved tab with lanyard hole and engraved label       |
| `seestar_s50_solar_filter_retainer.stl`   | Retaining ring — sandwiches Baader film into the groove                            |
| `seestar_s50_solar_filter_combined.stl`   | Both parts flat side-by-side, joined by two sacrificial bridges — **use this for print libraries with a one-file-per-week limit** |

---

## Building the STL files

### First-time setup

```bash
./create_venv.sh        # create virtualenv and install dependencies
```

### Generate STLs

```bash
./build.sh
```

The script activates the virtualenv, runs `create_solar_filter.py`, and moves the three STL files into the `output/` folder.

Alternatively, run the Python script manually:

```bash
source ./activate_venv.sh
python ./create_solar_filter.py
```

Use a tool such as [MeshLab](https://www.meshlab.net/) or [PrusaSlicer](https://www.prusa3d.com/prusaslicer/) to inspect the STLs before printing.

---

## Print settings

| Setting      | Value                             |
|--------------|-----------------------------------|
| Material     | PETG or ABS (heat-resistant)      |
| Layer height | 0.2 mm                            |
| Infill       | 40 %                              |
| Supports     | None needed                       |
| Orientation  | Flat — both pieces print face-down on the bed |
| Layout       | Filter body at centre; retaining ring 56 mm to the left |
| Footprint    | ~110 × 56 mm (fits any standard printer bed) |

---

## Assembly (combined print)

1. Cut Baader AstroSolar film to **52 mm diameter**.
2. Snap or knife the **2 flat bridges** along the 2 mm gap to separate the retaining ring from the filter body.
3. Apply a thin bead of RTV silicone in the annular groove on the top face of the filter body.
4. Lay the film over the opening and press the edges into the groove.
5. Apply another thin bead of RTV on top of the film edge.
6. Press the retaining ring down over the film to sandwich it in the groove.
7. Allow to cure fully before use.
8. Press the nub into the Seestar S50 front recess to mount.

---

## Design notes

- **Tab:** OEM-style annular-sector tab (curved inner and outer arcs, true `threePointArc` geometry) with a 4 mm lanyard hole centred in it.
- **Label:** "Seestar S50 filter / by AstroMark" engraved 0.4 mm deep on the tab top face, offset radially to avoid the lanyard hole.
- **Combined file:** Both parts lay flat on the print bed, side-by-side (filter body centred, retaining ring 56 mm to the left). Two sacrificial bridges (2 mm long × 3 mm wide × 0.4 mm tall — 2 print layers) connect their facing edges. They snap cleanly with finger pressure before assembly.
- **Font:** `Arial` (default). On Linux, change to `'DejaVu Sans'` in `create_solar_filter.py` if Arial is unavailable.
