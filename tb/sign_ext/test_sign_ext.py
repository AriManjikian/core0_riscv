import cocotb
from cocotb.triggers import Timer
import random


@cocotb.test()
async def sign_ext_i_type_test(dut):
    imm = 0b000001111011
    imm <<= 13
    src = 0b000
    irrelevant_bits = 0b000000000000_1100101011010
    raw_data = irrelevant_bits | imm
    await Timer(1, unit="ns")
    dut.raw_src.value = raw_data
    dut.imm_src.value = src
    expected = "00000000000000000000000001111011"
    await Timer(1, unit="ns")
    assert (
        dut.imm.value == expected
    ), f"[SIGN] I-Pos Mismatch, expected {expected} but got {int(dut.imm.value)}"
    assert int(dut.imm.value) == 123

    imm = 0b111110000101
    imm <<= 13
    src = 0b000
    irrelevant_bits = 0b000000000000_1100101011010
    raw_data = irrelevant_bits | imm
    await Timer(1, unit="ns")
    dut.raw_src.value = raw_data
    dut.imm_src.value = src
    expected = "11111111111111111111111110000101"
    await Timer(1, unit="ns")
    assert (
        dut.imm.value == expected
    ), f"[SIGN] I-Neg Mismatch, expected {expected} but got {int(dut.imm.value)}"
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
        ), f"[SIGN] S-Pos Mismatch, expected {imm} but got {int(dut.imm.value)}"

        imm = random.randint(0b100000000000, 0b111111111111) - (1 << 12)
        imm_11_5 = imm >> 5
        imm_4_0 = imm & 0b000000011111
        raw_data = (imm_11_5 << 18) | (imm_4_0)  # the 25 bits of data
        source = 0b001
        await Timer(1, unit="ns")
        dut.raw_src.value = raw_data
        dut.imm_src.value = source
        await Timer(1, unit="ns")
        assert (
            int(dut.imm.value) - (1 << 32) == imm
        ), f"[SIGN] S-Neg Mismatch, expected {imm} but got {int(dut.imm.value)}"


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
        source = 0b010
        await Timer(1, unit="ns")
        dut.raw_src.value = raw_data
        dut.imm_src.value = source
        await Timer(1, unit="ns")
        assert (
            int(dut.imm.value) == imm
        ), f"[SIGN] B-Pos Mismatch, expected {imm} but got {int(dut.imm.value)}"

        await Timer(100, unit="ns")
        imm = random.randint(0b100000000000, 0b111111111111)
        imm <<= 1
        imm_12 = (imm & 0b1000000000000) >> 12
        imm_11 = (imm & 0b0100000000000) >> 11
        imm_10_5 = (imm & 0b0011111100000) >> 5
        imm_4_1 = (imm & 0b0000000011110) >> 1
        raw_data = (imm_12 << 24) | (imm_11 << 0) | (imm_10_5 << 18) | (imm_4_1 << 1)
        source = 0b010
        await Timer(1, unit="ns")
        dut.raw_src.value = raw_data
        dut.imm_src.value = source
        await Timer(1, unit="ns")
        assert int(dut.imm.value) - (1 << 32) == imm - (
            1 << 13
        ), f"[SIGN] B-Neg Mismatch, expected {imm} but got {int(dut.imm.value)}"


@cocotb.test()
async def sign_ext_j_type_test(dut):
    for _ in range(100):
        await Timer(100, unit="ns")
        imm = random.randint(0, 0b01111111111111111111)
        imm <<= 1
        imm_20 = (imm & 0b100000000000000000000) >> 20
        imm_19_12 = (imm & 0b011111111000000000000) >> 12
        imm_11 = (imm & 0b000000000100000000000) >> 11
        imm_10_1 = (imm & 0b000000000011111111110) >> 1
        raw_data = (imm_20 << 24) | (imm_19_12 << 5) | (imm_11 << 13) | (imm_10_1 << 14)
        source = 0b011
        await Timer(1, unit="ns")
        dut.raw_src.value = raw_data
        dut.imm_src.value = source
        await Timer(1, unit="ns")
        assert (
            int(dut.imm.value) == imm
        ), f"[SIGN] J-Pos Mismatch, expected {imm} but got {int(dut.imm.value)}"

        await Timer(100, unit="ns")
        imm = random.randint(0b10000000000000000000, 0b11111111111111111111)
        imm <<= 1
        imm_20 = (imm & 0b100000000000000000000) >> 20
        imm_19_12 = (imm & 0b011111111000000000000) >> 12
        imm_11 = (imm & 0b000000000100000000000) >> 11
        imm_10_1 = (imm & 0b000000000011111111110) >> 1
        raw_data = (imm_20 << 24) | (imm_19_12 << 5) | (imm_11 << 13) | (imm_10_1 << 14)
        source = 0b011
        await Timer(1, unit="ns")
        dut.raw_src.value = raw_data
        dut.imm_src.value = source
        await Timer(1, unit="ns")
        assert int(dut.imm.value) - (1 << 32) == imm - (
            1 << 21
        ), f"[SIGN] J-Neg Mismatch, expected {imm} but got {int(dut.imm.value)}"


@cocotb.test()
async def sign_ext_u_type_test(dut):
    for _ in range(100):
        await Timer(100, unit="ns")
        imm_31_12 = random.randint(0, 0b11111111111111111111)
        raw_data = imm_31_12 << 5
        irrelevant_bits = random.randint(0, 0b11111)
        raw_data = raw_data | irrelevant_bits
        source = 0b100
        await Timer(1, unit="ns")
        dut.raw_src.value = raw_data
        dut.imm_src.value = source
        await Timer(1, unit="ns")
        assert (
            int(dut.imm.value) == imm_31_12 << 12
        ), f"[SIGN] U Mismatch, expected {imm_31_12 << 12} but got {int(dut.imm.value)}"
