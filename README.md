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
| `seestar_s50_solar_filter_combined.stl`   | Both parts joined by thin sprues — **use this for print libraries with a one-file-per-week limit** |

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
| Orientation  | Flange-side down, nub pointing up |

---

## Assembly (combined print)

1. Cut Baader AstroSolar film to **52 mm diameter**.
2. Clip or knife the **3 sprues** at the gap line to free the retaining ring from the filter body.
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
- **Combined file:** The retaining ring floats 0.5 mm above the filter body (print-clearance gap) and is held by three 1.2 × 1.2 mm sprues at 60°, 180°, and 300° — offset from the 0° tab. Cut at the gap line with flush cutters or a hobby knife.
- **Font:** `Arial` (default). On Linux, change to `'DejaVu Sans'` in `create_solar_filter.py` if Arial is unavailable.
