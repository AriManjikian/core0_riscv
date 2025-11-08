import cocotb
from cocotb.triggers import Timer
import random


@cocotb.test()
async def add_test(dut):
    await Timer(1, unit="ns")
    dut.alu_ctrl.value = 0b000
    for _ in range(1000):
        src1 = random.randint(0, 0xFFFFFFFF)
        src2 = random.randint(0, 0xFFFFFFFF)
        dut.src1.value = src1
        dut.src2.value = src2
        golden_add = (src1 + src2) & 0xFFFFFFFF
        await Timer(1, unit="ns")
    assert (
        int(dut.alu_res.value) == golden_add
    ), f"[ALU] Addition error src1: {src1}, src2: {src2}. Expected {golden_add}, but got {dut.alu_res.value}"


@cocotb.test()
async def and_test(dut):
    await Timer(1, unit="ns")
    dut.alu_ctrl.value = 0b010
    for _ in range(1000):
        src1 = random.randint(0, 0xFFFFFFFF)
        src2 = random.randint(0, 0xFFFFFFFF)
        dut.src1.value = src1
        dut.src2.value = src2
        golden_and = src1 & src2
        await Timer(1, unit="ns")
    assert (
        int(dut.alu_res.value) == golden_and
    ), f"[ALU] AND error src1: {src1}, src2: {src2}. Expected {golden_and}, but got {dut.alu_res.value}"


@cocotb.test()
async def or_test(dut):
    await Timer(1, unit="ns")
    dut.alu_ctrl.value = 0b011
    for _ in range(1000):
        src1 = random.randint(0, 0xFFFFFFFF)
        src2 = random.randint(0, 0xFFFFFFFF)
        dut.src1.value = src1
        dut.src2.value = src2
        golden_or = src1 | src2
        await Timer(1, unit="ns")
    assert (
        int(dut.alu_res.value) == golden_or
    ), f"[ALU] OR error src1: {src1}, src2: {src2}. Expected {golden_or}, but got {dut.alu_res.value}"


@cocotb.test()
async def sub_test(dut):
    await Timer(1, unit="ns")
    dut.alu_ctrl.value = 0b001
    for _ in range(1000):
        src1 = random.randint(0, 0xFFFFFFFF)
        src2 = random.randint(0, 0xFFFFFFFF)
        dut.src1.value = src1
        dut.src2.value = src2
        golden_sub = (src1 - src2) & 0xFFFFFFFF
        await Timer(1, unit="ns")
    assert (
        int(dut.alu_res.value) == golden_sub
    ), f"[ALU] SUB error src1: {src1}, src2: {src2}. Expected {golden_sub}, but got {dut.alu_res.value}"


@cocotb.test()
async def default_test(dut):
    await Timer(1, unit="ns")
    dut.alu_ctrl.value = 0b111
    src1 = random.randint(0, 0xFFFFFFFF)
    src2 = random.randint(0, 0xFFFFFFFF)
    dut.src1.value = src1
    dut.src2.value = src2
    expected = 0

    await Timer(1, unit="ns")
    assert (
        int(dut.alu_res.value) == expected
    ), "[ALU] Unexpected result during default test"


@cocotb.test()
async def zero_test(dut):
    await Timer(1, unit="ns")
    dut.alu_ctrl.value = 0b000
    dut.src1.value = 111
    dut.src2.value = -111
    await Timer(1, unit="ns")
    assert int(dut.zero.value) == 1
    assert (
        int(dut.alu_res.value) == 0
    ), f"[ALU] Addition error, zero_test: expected 0, but got {dut.alu_res.value}"
