# Makefile 
SIM ?= verilator
TOPLEVEL_LANG ?= verilog
EXTRA_ARGS += --trace --trace-structs
WAVES = 1
VERILOG_SOURCES += $(PWD)/../../src/byte_enable_decoder.sv
VERILOG_SOURCES += $(PWD)/../../packages/core0_pkg.sv
TOPLEVEL = byte_enable_decoder
COCOTB_TEST_MODULES = test_byte_enable_decoder
include $(shell cocotb-config  --makefiles)/Makefile.sim
