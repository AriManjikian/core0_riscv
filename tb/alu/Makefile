# Makefile 
SIM ?= verilator
TOPLEVEL_LANG ?= verilog
EXTRA_ARGS += --trace --trace-structs
WAVES = 1
VERILOG_SOURCES += $(PWD)/../../src/alu.sv
VERILOG_SOURCES += $(PWD)/../../packages/core0_pkg.sv
TOPLEVEL = alu
MODULE = test_alu
include $(shell cocotb-config  --makefiles)/Makefile.sim
