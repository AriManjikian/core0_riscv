import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock
import random


@cocotb.test()
async def sign_ext_i_type_test(dut):
    imm = 0b000001111011
    imm <<= 13
    src = 0b00
    irrelevant_bits = 0b000000000000_1100101011010
    raw_data = irrelevant_bits | imm
    await Timer(1, unit="ns")
    dut.raw_src.value = raw_data
    dut.imm_src.value = src
    expected = "00000000000000000000000001111011"
    await Timer(1, unit="ns")
    assert (
        dut.imm.value == expected
    ), f"[SIGN] I-Pos Mismatch, expected {expected} but got {dut.imm.value}"
    assert int(dut.imm.value) == 123

    imm = 0b111110000101
    imm <<= 13
    src = 0b00
    irrelevant_bits = 0b000000000000_1100101011010
    raw_data = irrelevant_bits | imm
    await Timer(1, unit="ns")
    dut.raw_src.value = raw_data
    dut.imm_src.value = src
    expected = "11111111111111111111111110000101"
    await Timer(1, unit="ns")
    assert (
        dut.imm.value == expected
    ), f"[SIGN] I-Neg Mismatch, expected {expected} but got {dut.imm.value}"
    assert int(dut.imm.value) - (1 << 32) == -123


@cocotb.test()
async def sign_ext_s_type_test(dut):
    for _ in range(100):
        await Timer(100, unit="ns")
        imm = random.randint(0, 0b01111111111)
        imm_11_5 = imm >> 5
        imm_4_0 = imm & 0b000000011111
        raw_data = (imm_11_5 << 18) | (imm_4_0)
        source = 0b001
        dut.raw_src.value = raw_data
        dut.imm_src.value = source
        await Timer(1, unit="ns")
        assert (
            int(dut.imm.value) == imm
        ), f"[SIGN] S-Pos Mismatch, expected {imm} but got {dut.imm.value}"

        imm = random.randint(0b100000000000, 0b111111111111) - (1 << 12)
        imm_11_5 = imm >> 5
        imm_4_0 = imm & 0b000000011111
        raw_data = (imm_11_5 << 18) | (imm_4_0)  # the 25 bits of data
        source = 0b01
        await Timer(1, unit="ns")
        dut.raw_src.value = raw_data
        dut.imm_src.value = source
        await Timer(1, unit="ns")
        assert (
            int(dut.imm.value) - (1 << 32) == imm
        ), f"[SIGN] S-Neg Mismatch, expected {imm} but got {dut.imm.value}"


@cocotb.test()
async def sign_ext_b_type_test(dut):
    for _ in range(100):
        await Timer(100, unit="ns")
        imm = random.randint(0, 0b01111111111)
        imm <<= 1
        imm_12 = (imm & 0b1000000000000) >> 12
        imm_11 = (imm & 0b0100000000000) >> 11
        imm_10_5 = (imm & 0b0011111100000) >> 5
        imm_4_1 = (imm & 0b0000000011110) >> 1
        raw_data = (imm_12 << 24) | (imm_11 << 0) | (imm_10_5 << 18) | (imm_4_1 << 1)
        source = 0b10
        await Timer(1, unit="ns")
        dut.raw_src.value = raw_data
        dut.imm_src.value = source
        await Timer(1, unit="ns")
        assert (
            int(dut.imm.value) == imm
        ), f"[SIGN] B-Pos Mismatch, expected {imm} but got {dut.imm.value}"

        await Timer(100, unit="ns")
        imm = random.randint(0b100000000000, 0b111111111111)
        imm <<= 1
        imm_12 = (imm & 0b1000000000000) >> 12
        imm_11 = (imm & 0b0100000000000) >> 11
        imm_10_5 = (imm & 0b0011111100000) >> 5
        imm_4_1 = (imm & 0b0000000011110) >> 1
        raw_data = (imm_12 << 24) | (imm_11 << 0) | (imm_10_5 << 18) | (imm_4_1 << 1)
        source = 0b10
        await Timer(1, unit="ns")
        dut.raw_src.value = raw_data
        dut.imm_src.value = source
        await Timer(1, unit="ns")
        assert int(dut.imm.value) - (1 << 32) == imm - (
            1 << 13
        ), f"[SIGN] B-Neg Mismatch, expected {imm} but got {dut.imm.value}"
