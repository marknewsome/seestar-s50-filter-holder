# Seestar-MarkOne-Kit
3D printable solar filter kit for Seestar telescope

This is a two-part, snapable design.

Steps:
1. run create_venv.sh to create a virtual environment with dependencies from requirements.txt
2. source ./activate_venv.sh
3. python ./create_solar_filter.py

It should generate these two files.  Use something like Meshlab to view them.

  seestar_s50_solar_filter.stl
  seestar_s50_solar_filter_retainer.stl


Assembly instructions:
1. Cut Baader film to 52mm diameter
2. Apply thin bead of RTV silicone in the groove on the top face
3. Lay film over the opening and press edges into the groove
4. Apply another thin bead of RTV on top of the film edge
5. Press retaining ring down over film to sandwich it in the groove
6. Allow to cure fully before use
7. Press nub into Seestar S50 front recess to mount

Print settings:
- Material: PETG or ABS (heat resistant)
- Layer height: 0.2mm
- Infill: 40%
- Supports: None needed
- Orientation: Flange-side down (nub pointing up during print)
