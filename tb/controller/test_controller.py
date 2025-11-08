import cocotb
from cocotb.triggers import Timer
from cocotb.types import LogicArray


async def set_unknown(dut):
    await Timer(1, unit="ns")
    dut.op.value = LogicArray("XXXXXXX")
    dut.func3.value = LogicArray("XXX")
    dut.func7.value = LogicArray("XXXXXXX")
    dut.alu_zero.value = LogicArray("X")

    await Timer(1, unit="ns")


@cocotb.test()
async def lw_datapath_test(dut):
    set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0000011
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "000"
    assert dut.imm_src.value == "00"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"

    assert dut.alu_src.value == "1"
    assert dut.write_back_src.value == "1"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def sw_datapath_test(dut):
    set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0100011
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "000"
    assert dut.imm_src.value == "01"
    assert dut.mem_write.value == "1"
    assert dut.reg_write.value == "0"

    assert dut.alu_src.value == "1"

    assert dut.pc_src.value == "0"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def add_test(dut):
    set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0110011
    dut.func3.value = 0b000
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "000"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"
    assert dut.alu_src.value == "0"
    assert dut.write_back_src.value == "0"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def and_test(dut):
    set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0110011
    dut.func3.value = 0b111
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "010"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"

    assert dut.alu_src.value == "0"
    assert dut.write_back_src.value == "0"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def or_test(dut):
    set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0110011
    dut.func3.value = 0b110
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "011"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"

    assert dut.alu_src.value == "0"
    assert dut.write_back_src.value == "0"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def beq_test(dut):
    set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b1100011
    dut.func3.value = 0b000
    dut.alu_zero.value = 0b0
    await Timer(1, unit="ns")
    assert dut.imm_src.value == "10"
    assert dut.alu_ctrl.value == "001"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "0"
    assert dut.alu_src.value == "0"
    assert dut.branch.value == "1"
    assert dut.pc_src.value == "0"

    await Timer(3, unit="ns")
    dut.alu_zero.value = 0b1
    await Timer(1, unit="ns")
    assert dut.pc_src.value == "1"
