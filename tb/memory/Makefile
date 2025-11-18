# Makefile 
SIM ?= verilator
TOPLEVEL_LANG ?= verilog
EXTRA_ARGS += --trace --trace-structs
WAVES = 1
VERILOG_SOURCES += $(PWD)/../../src/memory.sv
VERILOG_SOURCES += $(PWD)/../../packages/core0_pkg.sv
TOPLEVEL = memory
COCOTB_TEST_MODULES = test_memory
include $(shell cocotb-config  --makefiles)/Makefile.sim
