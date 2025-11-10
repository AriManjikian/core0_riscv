file_path = "./tb/cpu/test_imemory.hex"

with open(file_path, "r") as f:
    lines = f.readlines()

formatted_lines = []
for line in lines:
    line = line.strip()
    if not line:
        continue

    parts = line.split("//")
    hex_val = parts[0].strip()
    comment = parts[1].strip() if len(parts) > 1 else ""

    if "|" in comment:
        instr_part, result_part = comment.split("|", 1)
    else:
        instr_part, result_part = comment, ""

    instr_part = instr_part.strip()
    result_part = result_part.strip()

    formatted_line = f"{hex_val:<10} // {instr_part:<20} | {result_part}"
    formatted_lines.append(formatted_line)

with open(file_path, "w") as f:
    for line in formatted_lines:
        f.write(line + "\n")

print("Formatted test_imemory.hex")
