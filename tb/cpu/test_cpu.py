import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


def binary_to_hex(binnum):
    hexnum = hex(int(binnum))[2:].zfill(8)
    return hexnum.upper()


def hex_to_binary(hexnum):
    binnum = bin(int(hexnum.value), 16)[2:]
    binnum = binnum.zfill(32)
    return binnum.upper()


async def cpu_reset(dut):
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)


@cocotb.test()
async def cpu_instr_test(dut):
    cocotb.start_soon(Clock(dut.clk, 1, unit="ns").start())
    await RisingEdge(dut.clk)
    await cpu_reset(dut)
    # LW
    await RisingEdge(dut.clk)
    assert (
        binary_to_hex(dut.regfile.registers[18].value) == "DEADBEEF"
    ), "[CPU] LW datapath failed"

    # SW
    test_addr = int(0xC / 4)
    assert (
        binary_to_hex(dut.data_memory.mem[test_addr].value) == "F2F2F2F2"
    ), "[CPU] SW datapath failed 1"

    await RisingEdge(dut.clk)

    assert (
        binary_to_hex(dut.data_memory.mem[test_addr].value) == "DEADBEEF"
    ), f"[CPU] SW datapath failed 2, expected DEADBEEF but got {binary_to_hex(dut.data_memory.mem[test_addr].value)}"

    # ADD
    expected = (0xDEADBEEF + 0x00000AAA) & 0xFFFFFFFF
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[19].value) == "00000AAA"
    await RisingEdge(dut.clk)
    assert (
        binary_to_hex(dut.regfile.registers[20].value) == hex(expected)[2:].upper()
    ), f"[CPU] Unexpected result during ADD, expected {expected}, but got {binary_to_hex(dut.regfile.registers[20].value)}"

    # AND
    expected = expected & 0xDEADBEEF
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[21].value) == "DEAD8889"
    assert (
        binary_to_hex(dut.regfile.registers[21].value) == hex(expected)[2:].upper()
    ), f"[CPU] Unexpected result during AND, expected {expected}, but got {binary_to_hex(dut.regfile.registers[21].value)}"

    # OR
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[5].value) == "125F552D"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[6].value) == "7F4FD46A"
    await RisingEdge(dut.clk)
    assert (
        binary_to_hex(dut.regfile.registers[7].value) == "7F5FD56F"
    ), f"[CPU] Unexpected result during OR, expected 7F5FD56F, but got {binary_to_hex(dut.regfile.registers[7].value)}"

    # BEQ
    assert binary_to_hex(dut.instr.value) == "00730663"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.instr.value) == "00802B03"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[22].value) == "DEADBEEF"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.instr.value) == "00002B03"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[22].value) == "AEAEAEAE"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.instr.value) == "00000663"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.instr.value) == "00000013"
    await RisingEdge(dut.clk)

    # JAL
    assert binary_to_hex(dut.instr.value) == "00C000EF"
    assert binary_to_hex(dut.pc.value) == "00000044"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.instr.value) == "FFDFF0EF"
    assert binary_to_hex(dut.pc.value) == "00000050"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.instr.value) == "00C000EF"
    assert binary_to_hex(dut.pc.value) == "0000004C"
    assert binary_to_hex(dut.regfile.registers[1].value) == "00000054"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.instr.value) == "00C02383"
    assert binary_to_hex(dut.pc.value) == "00000058"
    assert binary_to_hex(dut.regfile.registers[1].value) == "00000050"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[7].value) == "DEADBEEF"

    # ADDI
    assert binary_to_hex(dut.instr.value) == "1AB38D13"
    assert not binary_to_hex(dut.regfile.registers[26].value) == "DEADC09A"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.instr.value) == "F2130C93"
    assert binary_to_hex(dut.regfile.registers[26].value) == "DEADC09A"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[25].value) == "7F4FD38B"

    # AUIPC
    assert binary_to_hex(dut.instr.value) == "1F1FA297"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[5].value) == "1F1FA064"

    # LUI
    assert binary_to_hex(dut.instr.value) == "2F2FA2B7"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[5].value) == "2F2FA000"

    # SLTI
    assert binary_to_hex(dut.regfile.registers[19].value) == "00000AAA"
    assert binary_to_hex(dut.instr.value) == "FFF9AB93"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[23].value) == "00000000"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[23].value) == "00000001"

    # SLTU
    assert binary_to_hex(dut.instr.value) == "FFF9BB13"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[22].value) == "00000001"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[22].value) == "00000000"

    # XOR
    assert binary_to_hex(dut.instr.value) == "AAA94913"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[18].value) == "21524445"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[19].value) == binary_to_hex(
        dut.regfile.registers[18].value
    )

    # ORI
    assert binary_to_hex(dut.instr.value) == "AAA9EA13"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[20].value) == "FFFFFEEF"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[21].value) == binary_to_hex(
        dut.regfile.registers[20].value
    )

    # ANDI
    assert binary_to_hex(dut.instr.value) == "7FFA7913"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[18].value) == "000006EF"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[19].value) == binary_to_hex(
        dut.regfile.registers[21].value
    )
    assert binary_to_hex(dut.regfile.registers[19].value) == "FFFFFEEF"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[20].value) == "00000000"

    # SLLI
    assert binary_to_hex(dut.instr.value) == "00499993"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[19].value) == "FFFFEEF0"
    assert dut.reg_write.value == "0"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[19].value) == "FFFFEEF0"

    # SRLI
    assert binary_to_hex(dut.instr.value) == "0049DA13"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[20]) == "0FFFFEEF"
    assert dut.reg_write.value == "0"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[20]) == "0FFFFEEF"

    # SRAI
    assert binary_to_hex(dut.instr.value) == "404ADA93"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[21].value) == "FFFFFFEE"
    assert dut.reg_write.value == "0"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[21].value) == "FFFFFFEE"

    # SUB
    assert binary_to_hex(dut.instr.value) == "412A8933"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[18].value) == "FFFFF8FF"

    # ADDI
    assert binary_to_hex(dut.instr.value) == "00800393"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[7].value) == "00000008"

    # SLL
    assert binary_to_hex(dut.instr.value) == "00791933"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[18].value) == "FFF8FF00"

    # SLT
    assert binary_to_hex(dut.instr.value) == "013928B3"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[17].value) == "00000001"

    # SLTU
    assert binary_to_hex(dut.instr.value) == "013938B3"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[17].value) == "00000001"

    # XOR
    assert binary_to_hex(dut.instr.value) == "013948B3"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[17].value) == "000711F0"

    # SRL
    assert binary_to_hex(dut.instr.value) == "0079D433"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[8].value) == "00FFFFEE"

    # SRA
    assert binary_to_hex(dut.instr.value) == "4079D433"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.regfile.registers[8].value) == "FFFFFFEE"

    # BLT
    assert binary_to_hex(dut.pc.value) == "000000D0"
    assert binary_to_hex(dut.instr.value) == "0088C463"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.pc.value) == "000000D4"

    assert binary_to_hex(dut.instr.value) == "01144463"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.pc.value) == "000000DC"

    # BNE
    assert binary_to_hex(dut.instr.value) == "00841463"
    assert binary_to_hex(dut.regfile.registers[8].value) == "FFFFFFEE"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.pc.value) == "000000E0"

    assert binary_to_hex(dut.instr.value) == "01141463"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.pc.value) == "000000E8"

    # BGE
    assert binary_to_hex(dut.instr.value) == "01145463"
    assert binary_to_hex(dut.regfile.registers[8].value) == "FFFFFFEE"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.pc.value) == "000000EC"

    assert binary_to_hex(dut.instr.value) == "00845463"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.pc.value) == "000000F4"
    assert binary_to_hex(dut.regfile.registers[8].value) == "FFFFFFEE"

    # BLTU
    assert binary_to_hex(dut.instr.value) == "01146463"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.pc.value) == "000000F8"

    assert binary_to_hex(dut.instr.value) == "0088E463"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.pc.value) == "00000100"
    assert binary_to_hex(dut.regfile.registers[8].value) == "FFFFFFEE"

    # BGEU
    assert binary_to_hex(dut.instr.value) == "0088F463"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.pc.value) == "00000104"

    assert binary_to_hex(dut.instr.value) == "01147463"
    await RisingEdge(dut.clk)
    assert binary_to_hex(dut.pc.value) == "0000010C"
    assert binary_to_hex(dut.regfile.registers[8].value) == "FFFFFFEE"

    # JALR
