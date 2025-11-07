.PHONY: all test clean alu controller cpu memory regfile sign_ext load_store_decoder reader

all: clean test

test:
	. .venv/bin/activate && $(MAKE) alu controller memory regfile sign_ext load_store_decoder reader cpu

alu:
	$(MAKE) -C tb/alu

memory:
	$(MAKE) -C tb/memory

regfile:
	$(MAKE) -C tb/regfile

controller:
	$(MAKE) -C tb/controller

sign_ext:
	$(MAKE) -C tb/sign_ext

cpu:
	$(MAKE) -C tb/cpu


clean:
	@find ./tb -type d -name "__pycache__" -exec rm -rf {} +
	@find ./tb -type d -name "sim_build" -exec rm -rf {} +
	@find ./tb -type f -name "results.xml" -exec rm -f {} +
	@find ./tb -type f -name "*.None" -exec rm -f {} +
	@find ./tb -type d -name ".pytest_cache" -exec rm -rf {} +
	@find ./tb -type f -name "dump.vcd" -exec rm -f {} +
