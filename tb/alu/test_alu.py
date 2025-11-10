import cocotb
from cocotb.triggers import Timer
import random


@cocotb.test()
async def add_test(dut):
    await Timer(1, unit="ns")
    dut.alu_ctrl.value = 0b0000
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
    dut.alu_ctrl.value = 0b0010
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
    dut.alu_ctrl.value = 0b0011
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
    dut.alu_ctrl.value = 0b0001
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
async def slt_test(dut):
    await Timer(1, unit="ns")
    dut.alu_ctrl.value = 0b0101
    for _ in range(1000):
        src1 = random.randint(0, 0xFFFFFFFF)
        src2 = random.randint(0, 0xFFFFFFFF)
        dut.src1.value = src1
        dut.src2.value = src2
        await Timer(1, unit="ns")
        if src1 >> 31 == 0 and src2 >> 31 == 0:
            golden_slt = int(src1 < src2)
        elif src1 >> 31 == 0 and src2 >> 31 == 1:
            golden_slt = int(src1 < (src2 - (1 << 32)))
        elif src1 >> 31 == 1 and src2 >> 31 == 0:
            golden_slt = int((src1 - (1 << 32)) < src2)
        elif src1 >> 31 == 1 and src2 >> 31 == 1:
            golden_slt = int((src1 - (1 << 32)) < (src2 - (1 << 32)))
    assert (
        int(dut.alu_res.value) == golden_slt
    ), f"[ALU] SLT error src1: {src1}, src2: {src2}. Expected {golden_slt}, but got {dut.alu_res.value}"
    assert dut.alu_res.value == 31 * "0" + str(int(dut.alu_res.value))


@cocotb.test()
async def sltu_test(dut):
    await Timer(1, unit="ns")
    dut.alu_ctrl.value = 0b0111
    for _ in range(1000):
        src1 = random.randint(0, 0xFFFFFFFF)
        src2 = random.randint(0, 0xFFFFFFFF)
        dut.src1.value = src1
        dut.src2.value = src2
        await Timer(1, unit="ns")
        golden_slt = int(src1 < src2)
    assert (
        int(dut.alu_res.value) == golden_slt
    ), f"[ALU] SLTU error src1: {src1}, src2: {src2}. Expected {golden_slt}, but got {dut.alu_res.value}"
    assert dut.alu_res.value == 31 * "0" + str(int(dut.alu_res.value))


@cocotb.test()
async def sll_test(dut):
    await Timer(1, unit="ns")
    dut.alu_ctrl.value = 0b0100
    for _ in range(1000):
        src1 = random.randint(0, 0xFFFFFFFF)
        src2 = random.randint(0, 0xFFFFFFFF)
        dut.src1.value = src1
        shamt = src2 & 0b11111
        dut.src2.value = shamt

        await Timer(1, unit="ns")
        golden_sll = (src1 << shamt) & 0xFFFFFFFF

        assert int(dut.alu_res.value) == int(
            golden_sll
        ), f"[ALU] SLL error src1: {src1}, src2: {src2}, shamt: {shamt}. Expected {golden_sll}, but got {dut.alu_res.value}"


@cocotb.test()
async def srl_test(dut):
    await Timer(1, unit="ns")
    dut.alu_ctrl.value = 0b0110
    for _ in range(1000):
        src1 = random.randint(0, 0xFFFFFFFF)
        src2 = random.randint(0, 0xFFFFFFFF)
        dut.src1.value = src1
        shamt = src2 & 0b11111
        dut.src2.value = shamt

        await Timer(1, unit="ns")
        golden_srl = (src1 >> shamt) & 0xFFFFFFFF

        assert int(dut.alu_res.value) == int(
            golden_srl
        ), f"[ALU] SLL error src1: {src1}, src2: {src2}, shamt: {shamt}. Expected {golden_srl}, but got {dut.alu_res.value}"


@cocotb.test()
async def xor_test(dut):
    await Timer(1, unit="ns")
    dut.alu_ctrl.value = 0b1000
    for _ in range(1000):
        src1 = random.randint(0, 0xFFFFFFFF)
        src2 = random.randint(0, 0xFFFFFFFF)
        dut.src1.value = src1
        dut.src2.value = src2
        await Timer(1, unit="ns")
        golden_xor = src1 ^ src2
        assert int(dut.alu_res.value) == int(
            golden_xor
        ), f"[ALU] XOR error src1: {src1}, src2: {src2}. Expected {golden_xor}, but got {dut.alu_res.value}"


@cocotb.test()
async def default_test(dut):
    await Timer(1, unit="ns")
    dut.alu_ctrl.value = 0b1111
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
    dut.alu_ctrl.value = 0b0000
    dut.src1.value = 111
    dut.src2.value = -111
    await Timer(1, unit="ns")
    assert int(dut.zero.value) == 1
    assert (
        int(dut.alu_res.value) == 0
    ), f"[ALU] Addition error, zero_test: expected 0, but got {dut.alu_res.value}"
