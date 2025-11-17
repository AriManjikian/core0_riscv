import cocotb
from cocotb.triggers import Timer
import random


@cocotb.test()
async def byte_en_test(dut):
    await Timer(1, unit="ns")
    word = 0x123ABC00

    # SW
    dut.func3.value = 0b010
    for _ in range(100):
        reg_data = random.randint(0, 0xFFFFFFFF)
        dut.reg_read.value = reg_data
        for offset in range(4):
            dut.alu_res_address.value = word | offset
            await Timer(1, unit="ns")
            assert dut.data.value == reg_data & 0xFFFFFFFF
            if offset == 0b00:
                assert dut.byte_en.value == 0b1111
            else:
                assert dut.byte_en.value == 0b0000

    await Timer(10, unit="ns")

    # SB
    dut.func3.value = 0b000
    for _ in range(100):
        reg_data = random.randint(0, 0xFFFFFFFF)
        dut.reg_read.value = reg_data
        for offset in range(4):
            dut.alu_res_address.value = word | offset
            await Timer(1, unit="ns")
            if offset == 0b00:
                assert dut.byte_en.value == 0b0001
                assert dut.data.value == (reg_data & 0x000000FF)
            elif offset == 0b01:
                assert dut.byte_en.value == 0b0010
                assert dut.data.value == (reg_data & 0x000000FF) << 8
            elif offset == 0b10:
                assert dut.byte_en.value == 0b0100
                assert dut.data.value == (reg_data & 0x000000FF) << 16
            elif offset == 0b11:
                assert dut.byte_en.value == 0b1000
                assert dut.data.value == (reg_data & 0x000000FF) << 24

    # SH
    await Timer(10, unit="ns")
    dut.func3.value = 0b001
    for _ in range(100):
        reg_data = random.randint(0, 0xFFFFFFFF)
        dut.reg_read.value = reg_data
        for offset in range(4):
            dut.alu_res_address.value = word | offset
            await Timer(1, unit="ns")
            if offset == 0b00:
                assert dut.byte_en.value == 0b0011
                assert dut.data.value == (reg_data & 0x0000FFFF)
            elif offset == 0b10:
                assert dut.byte_en.value == 0b1100
                assert dut.data.value == (reg_data & 0x0000FFFF) << 16
            else:
                assert dut.byte_en.value == 0b0000
