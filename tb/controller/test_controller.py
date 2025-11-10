import cocotb
from cocotb.triggers import Timer
from cocotb.types import LogicArray


async def set_unknown(dut):
    await Timer(1, unit="ns")
    dut.op.value = LogicArray("XXXXXXX")
    dut.func3.value = LogicArray("XXX")
    dut.func7.value = LogicArray("XXXXXXX")
    dut.alu_zero.value = LogicArray("X")
    dut.write_back_src.value = LogicArray("XX")

    await Timer(1, unit="ns")


@cocotb.test()
async def lw_datapath_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0000011
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "0000"
    assert dut.imm_src.value == "000"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"

    assert dut.alu_src.value == "1"
    assert dut.write_back_src.value == "01"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def sw_datapath_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0100011
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "0000"
    assert dut.imm_src.value == "001"
    assert dut.mem_write.value == "1"
    assert dut.reg_write.value == "0"

    assert dut.alu_src.value == "1"

    assert dut.pc_src.value == "0"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def add_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0110011
    dut.func3.value = 0b000
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "0000"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"
    assert dut.alu_src.value == "0"
    assert dut.write_back_src.value == "00"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def addi_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0010011
    dut.func3.value = 0b000
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "0000"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"
    assert dut.imm_src.value == "000"
    assert dut.alu_src.value == "1"
    assert dut.write_back_src.value == "00"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def and_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0110011
    dut.func3.value = 0b111
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "0010"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"

    assert dut.alu_src.value == "0"
    assert dut.write_back_src.value == "00"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def andi_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0010011
    dut.func3.value = 0b111
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "0010"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"

    assert dut.alu_src.value == "1"
    assert dut.write_back_src.value == "00"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def or_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0110011
    dut.func3.value = 0b110
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "0011"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"

    assert dut.alu_src.value == "0"
    assert dut.write_back_src.value == "00"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def ori_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0010011
    dut.func3.value = 0b110
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "0011"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"

    assert dut.alu_src.value == "1"
    assert dut.write_back_src.value == "00"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def xori_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0010011
    dut.func3.value = 0b100
    await Timer(1, unit="ns")

    assert dut.alu_ctrl.value == "1000"
    assert dut.imm_src.value == "000"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"

    assert dut.alu_src.value == "1"
    assert dut.write_back_src.value == "00"
    assert dut.pc_src.value == "0"


@cocotb.test()
async def slti_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0010011
    dut.func3.value = 0b010
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "0101"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"
    assert dut.imm_src.value == "000"
    assert dut.alu_src.value == "1"
    assert dut.write_back_src.value == "00"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def sltu_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0010011
    dut.func3.value = 0b011
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "0111"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"
    assert dut.imm_src.value == "000"
    assert dut.alu_src.value == "1"
    assert dut.write_back_src.value == "00"

    assert dut.pc_src.value == "0"


@cocotb.test()
async def beq_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b1100011
    dut.func3.value = 0b000
    dut.alu_zero.value = 0b0
    await Timer(1, unit="ns")
    assert dut.alu_ctrl.value == "0001"
    assert dut.imm_src.value == "010"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "0"
    assert dut.alu_src.value == "0"
    assert dut.branch.value == "1"
    assert dut.pc_src.value == "0"

    await Timer(3, unit="ns")
    dut.alu_zero.value = 0b1
    await Timer(1, unit="ns")
    assert dut.pc_src.value == "1"


@cocotb.test()
async def jal_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b1101111
    await Timer(1, unit="ns")
    assert dut.imm_src.value == "011"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"
    assert dut.branch.value == "0"
    assert dut.pc_src.value == "1"
    assert dut.jump.value == "1"
    assert dut.write_back_src.value == "10"


@cocotb.test()
async def lui_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0110111
    await Timer(1, unit="ns")
    assert dut.imm_src.value == "100"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"
    assert dut.write_back_src.value == "11"
    assert dut.branch.value == "0"
    assert dut.jump.value == "0"
    assert dut.second_add_src.value == "1"


@cocotb.test()
async def auipc_test(dut):
    await set_unknown(dut)
    await Timer(10, unit="ns")
    dut.op.value = 0b0010111
    await Timer(1, unit="ns")
    assert dut.imm_src.value == "100"
    assert dut.mem_write.value == "0"
    assert dut.reg_write.value == "1"
    assert dut.write_back_src.value == "11"
    assert dut.branch.value == "0"
    assert dut.jump.value == "0"
    assert dut.second_add_src.value == "0"
