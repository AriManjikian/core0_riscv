# Makefile 
SIM ?= verilator
TOPLEVEL_LANG ?= verilog
EXTRA_ARGS += --trace --trace-structs
WAVES = 1
VERILOG_SOURCES += $(PWD)/../../src/sign_ext.sv
TOPLEVEL = sign_ext
MODULE = test_sign_ext
include $(shell cocotb-config  --makefiles)/Makefile.sim
