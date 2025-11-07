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
