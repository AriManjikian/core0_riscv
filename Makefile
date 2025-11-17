.PHONY: all test clean alu controller cpu memory regfile sign_ext load_store_decoder reader

all: clean test

test:
	. .venv/bin/activate && $(MAKE) alu controller memory regfile sign_ext byte_enable_decoder reader cpu

alu:
	$(MAKE) -C tb/alu

byte_enable_decoder:
	$(MAKE) -C tb/byte_enable_decoder

memory:
	$(MAKE) -C tb/memory

reader:
	$(MAKE) -C tb/reader

regfile:
	$(MAKE) -C tb/regfile

controller:
	$(MAKE) -C tb/controller

sign_ext:
	$(MAKE) -C tb/sign_ext

cpu:
	$(MAKE) -C tb/cpu

view: 
	gtkwave tb/alu/dump.vcd &
	gtkwave tb/memory/dump.vcd &
	gtkwave tb/regfile/dump.vcd &
	gtkwave tb/sign_ext/dump.vcd &
	gtkwave tb/controller/dump.vcd &
	gtkwave tb/cpu/dump.vcd &

clean:
	@find ./tb -type d -name "__pycache__" -exec rm -rf {} +
	@find ./tb -type d -name "sim_build" -exec rm -rf {} +
	@find ./tb -type f -name "results.xml" -exec rm -f {} +
	@find ./tb -type f -name "*.None" -exec rm -f {} +
	@find ./tb -type d -name ".pytest_cache" -exec rm -rf {} +
	@find ./tb -type f -name "dump.vcd" -exec rm -f {} +
	@find ./tb -type f -name "dump.fst" -exec rm -f {} +
