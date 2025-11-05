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
async def cpu_init_mem_test(dut):
    cocotb.start_soon(Clock(dut.clk, 1, unit="ns").start())
    await RisingEdge(dut.clk)
    await cpu_reset(dut)
    assert binary_to_hex(dut.pc.value) == "00000000"

    imem = []
    with open("test_imemory.hex", "r") as f:
        for line in f:
            line_content = line.split("//")[0].strip()
            if line_content:
                imem.append(hex_to_binary(line_content))
    for counter in range(5):
        expected_instr = imem[counter]
        assert dut.instr.value == expected_instr
        await RisingEdge(dut.clk)


@cocotb.test()
async def cpu_instr_test(dut):
    cocotb.start_soon(Clock(dut.clk, 1, unit="ns").start())
    await RisingEdge(dut.clk)
    await cpu_reset(dut)

    await RisingEdge(dut.clk)
    print(binary_to_hex(dut.regfile.registers[18].value))
    assert binary_to_hex(dut.regfile.registers[18].value) == "DEADBEEF"
