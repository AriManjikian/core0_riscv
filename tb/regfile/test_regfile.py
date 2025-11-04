import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
import random


@cocotb.test()
async def random_write_test(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await RisingEdge(dut.clk)

    dut.rst_n.value = 0
    dut.w_en.value = 0
    dut.address1.value = 0
    dut.address2.value = 0
    dut.address3.value = 0
    dut.write_data.value = 0

    await RisingEdge(dut.clk)
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    print("[REG] [RST] Completed")

    regs = [0 for _ in range(32)]

    for i in range(1000):
        address1 = random.randint(1, 31)
        address2 = random.randint(1, 31)
        address3 = random.randint(1, 31)
        random_write = random.randint(0, 0xFFFFFFFF)

        await Timer(1, unit="ns")
        dut.address1.value = address1
        dut.address2.value = address2
        await Timer(1, unit="ns")

        read1 = int(dut.read_data1.value)
        read2 = int(dut.read_data2.value)
        assert (
            read1 == regs[address1]
        ), f"[REG][ITER={i}] read_data1 mismatch at addr {address1}: expected {regs[address1]:08X}, got {read1:08X}"
        assert (
            read2 == regs[address2]
        ), f"[REG][ITER={i}] read_data2 mismatch at addr {address2}: expected {regs[address2]:08X}, got {read2:08X}"

        dut.address3.value = address3
        dut.w_en.value = 1
        dut.write_data.value = random_write
        await RisingEdge(dut.clk)
        dut.w_en.value = 0

        regs[address3] = random_write
        await Timer(1, unit="ns")

    await Timer(1, unit="ns")
    dut.address3.value = 0
    dut.w_en.value = 1
    dut.write_data.value = 0xABABABAB
    await RisingEdge(dut.clk)
    dut.w_en.value = 0
    await Timer(1, unit="ns")

    dut.address1.value = 0
    await Timer(1, unit="ns")
    final_read = int(dut.read_data1.value)
    assert final_read == 0, f"[REG][ZERO] x0 register not zero! got {final_read:08X}"

    print("[REG] [TEST PASSED] Random write test completed successfully.")
