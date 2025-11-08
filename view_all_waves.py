#!/usr/bin/env python3
import subprocess
import pathlib

# Root TB directory
tb_root = pathlib.Path("./tb")

# Find all dump.vcd files directly under each TB folder
vcd_files = [p for p in tb_root.glob("*/dump.vcd") if p.is_file()]

if not vcd_files:
    print("No VCD files found. Run your simulations first!")
    exit(1)

# GTKWave command
# Use -a to save/load session file
gtkwave_cmd = ["gtkwave", str(vcd_files[0]), "-a", "combined.gtkw"]

# Add remaining VCDs as merges
for vcd in vcd_files[1:]:
    gtkwave_cmd += ["-m", str(vcd)]

print("Opening GTKWave with the following VCDs:")
for vcd in vcd_files:
    print(f"  {vcd}")

# Launch GTKWave
subprocess.run(gtkwave_cmd)
