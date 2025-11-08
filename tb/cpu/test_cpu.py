import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


def binary_to_hex(binnum):
    hexnum = hex(int(str(binnum), 2))[2:]
    hexnum = hexnum.zfill(8)
    return hexnum.upper()


def hex_to_binary(hexnum):
    binnum = bin(int(str(hexnum), 16))[2:]
    binnum = binnum.zfill(32)
    return binnum.upper()


async def cpu_reset(dut):
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)


@cocotb.test()
async def cpu_instr_test(dut):
    cocotb.start_soon(Clock(dut.clk, 1, unit="ns").start())
    await RisingEdge(dut.clk)
    await cpu_reset(dut)
    # LW
    await RisingEdge(dut.clk)
    assert (
        binary_to_hex(dut.regfile.registers[18].value) == "DEADBEEF"
    ), "[CPU] LW datapath failed"

    # SW
    test_addr = int(0xC / 4)
    assert (
        binary_to_hex(dut.data_memory.mem[test_addr].value) == "F2F2F2F2"
    ), "[CPU] SW datapath failed 1"

    await RisingEdge(dut.clk)

    assert (
        binary_to_hex(dut.data_memory.mem[test_addr].value) == "DEADBEEF"
    ), f"[CPU] SW datapath failed 2, expected DEADBEEF but got {binary_to_hex(dut.data_memory.mem[test_addr].value)}"

    # ADD
    expected = (0xDEADBEEF + 0x00000AAA) & 0xFFFFFFFF
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[19].value) == "00000AAA"
    await RisingEdge(dut.clk)
    assert (
        binary_to_hex(dut.regfile.registers[20].value) == hex(expected)[2:].upper()
    ), f"[CPU] Unexpected result during ADD, expected {expected}, but got {binary_to_hex(dut.regfile.registers[20].value)}"

    # AND
    expected = expected & 0xDEADBEEF
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[21].value) == "DEAD8889"
    assert (
        binary_to_hex(dut.regfile.registers[21].value) == hex(expected)[2:].upper()
    ), f"[CPU] Unexpected result during AND, expected {expected}, but got {binary_to_hex(dut.regfile.registers[21].value)}"

    # OR
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[5].value) == "125F552D"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[6].value) == "7F4FD46A"
    await RisingEdge(dut.clk)
    assert (
        binary_to_hex(dut.regfile.registers[7].value) == "7F5FD56F"
    ), f"[CPU] Unexpected result during OR, expected 7F5FD56F, but got {binary_to_hex(dut.regfile.registers[7].value)}"

    # BEQ
    assert binary_to_hex(dut.instr.value) == "00730663"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.instr.value) == "00802B03"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[22].value) == "DEADBEEF"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.instr.value) == "00002B03"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[22].value) == "AEAEAEAE"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.instr.value) == "00000663"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.instr.value) == "00000013"
