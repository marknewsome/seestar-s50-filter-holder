#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/venv"
OUTPUT="$SCRIPT_DIR/output"

if [ ! -d "$VENV" ]; then
    echo "ERROR: virtual environment not found at $VENV"
    echo "Run create_venv.sh first."
    exit 1
fi

source "$VENV/bin/activate"

mkdir -p "$OUTPUT"

echo "Generating STL files..."
cd "$SCRIPT_DIR"
python create_solar_filter.py

mv -f seestar_s50_solar_filter.stl         "$OUTPUT/"
mv -f seestar_s50_solar_filter_retainer.stl "$OUTPUT/"
mv -f seestar_s50_solar_filter_combined.stl "$OUTPUT/"

echo ""
echo "STL files written to: $OUTPUT/"
ls -lh "$OUTPUT/"*.stl
