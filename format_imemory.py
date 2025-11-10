input_file = "tb/cpu/test_imemory.hex"
output_file = "tb/cpu/test_imemory.hex"

with open(input_file, "r") as f:
    lines = f.readlines()

non_empty_lines = [line.strip() for line in lines if line.strip()]

formatted_lines = []
pc = 0x00000000

for line in non_empty_lines:
    parts = line.split("//", 1)
    hex_code = parts[0].strip()
    comment = parts[1].strip() if len(parts) > 1 else ""
    comment_parts = [part.strip() for part in comment.split("|")]

    formatted_line = f"{hex_code:<12} // {comment_parts[0]:<25} | {comment_parts[1]:<55} | PC:0x{pc:08X}"
    formatted_lines.append(formatted_line)

    pc += 0x4

result = "\n".join(formatted_lines)

if output_file:
    with open(output_file, "w") as f:
        f.write(result)
        print(f"Formatted output written to {output_file}")
else:
    print(result)
