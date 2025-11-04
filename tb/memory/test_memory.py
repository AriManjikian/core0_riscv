import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
from mem_gen import generate_random_mem_file

MEM_WORDS = 64
MEM_FILE = "mem.hex"


async def reset(dut):
    await RisingEdge(dut.clk)
    dut.rst_n.value = 0
    dut.w_en.value = 0
    dut.address.value = 0
    dut.write_data.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    cocotb.log.info("[MEM] [RST] Completed")

    for addr in range(MEM_WORDS):
        dut.address.value = addr * 4
        await Timer(1, unit="ns")
        assert int(dut.read_data.value) == 0


@cocotb.test()
async def test_memory(dut):
    cocotb.start_soon(Clock(dut.clk, 1, unit="ns").start())
    await reset(dut)

    test_data = [(0, 0xDEADBEEF), (4, 0xCAFEBABE), (8, 0x12345678), (12, 0xA5A5A5A5)]
    dut.byte_en.value = 0b1111

    for addr, data in test_data:
        dut.address.value = addr
        dut.write_data.value = data
        dut.w_en.value = 1
        await RisingEdge(dut.clk)
        dut.w_en.value = 0
        dut.address.value = addr
        await RisingEdge(dut.clk)
        assert (
            dut.read_data.value == data
        ), f"[MEM] Error at address {addr}: expected {hex(data)}, got {hex(dut.read_data.value)}"

    for i in range(0, 40, 4):
        dut.address.value = i
        dut.write_data.value = i
        dut.w_en.value = 1
        await RisingEdge(dut.clk)
    dut.w_en.value = 0

    for i in range(0, 40, 4):
        dut.address.value = i
        await RisingEdge(dut.clk)
        read_val = int(dut.read_data.value)
        assert (
            read_val == i
        ), f"[MEM] Error at address {i}: expected {i}, got {hex(read_val)}"

    ref_mem = generate_random_mem_file(MEM_FILE, MEM_WORDS)

    for addr, data in enumerate(ref_mem):
        dut.address.value = addr * 4
        dut.write_data.value = data
        dut.w_en.value = 1
        await RisingEdge(dut.clk)
    dut.w_en.value = 0

    for addr, expected in enumerate(ref_mem):
        dut.address.value = addr * 4
        await RisingEdge(dut.clk)
        read_val = int(dut.read_data.value)
        assert (
            read_val == expected
        ), f"[MEM] Memory mismatch at {addr*4}: expected {hex(expected)}, got {hex(read_val)}"

    cocotb.log.info("[MEM] Random memory contents verified successfully!")
