# Makefile 
SIM ?= verilator
TOPLEVEL_LANG ?= verilog
EXTRA_ARGS += --trace --trace-structs
WAVES = 1
VERILOG_SOURCES += $(PWD)/../../src/reader.sv
TOPLEVEL = reader
COCOTB_TEST_MODULES = test_reader
include $(shell cocotb-config  --makefiles)/Makefile.sim
