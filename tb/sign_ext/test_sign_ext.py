import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock


@cocotb.test()
async def possitive_imm_test(dut):
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
    ), f"[SIGN] Mismatch, expected {expected} but got {dut.imm.value}"
    assert int(dut.imm.value) == 123


@cocotb.test()
async def negative_imm_test(dut):
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
    ), f"[SIGN] Mismatch, expected {expected} but got {dut.imm.value}"
    assert int(dut.imm.value) - (1 << 32) == -123
