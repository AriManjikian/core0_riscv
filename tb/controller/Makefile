# Makefile 
SIM ?= verilator
TOPLEVEL_LANG ?= verilog
EXTRA_ARGS += --trace --trace-structs
WAVES = 1
VERILOG_SOURCES += $(PWD)/../../src/controller.sv
TOPLEVEL = controller
COCOTB_TEST_MODULES = test_controller
include $(shell cocotb-config  --makefiles)/Makefile.sim
