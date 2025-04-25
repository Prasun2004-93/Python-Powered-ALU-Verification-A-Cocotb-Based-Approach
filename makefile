TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(shell pwd)/16bit_alu.v
TOPLEVEL = alu
MODULE = test_alu

# Set simulator
SIM = icarus

include $(shell cocotb-config --makefiles)/Makefile.sim


