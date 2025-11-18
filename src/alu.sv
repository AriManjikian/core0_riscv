`timescale 1ns / 1ps

module alu (
    input logic [ 3:0] alu_ctrl,
    input logic [31:0] src1,
    input logic [31:0] src2,

    output logic [31:0] alu_res,
    output logic zero,
    output logic last_bit
);
  import core0_pkg::*;

  wire [4:0] shamt = src2[4:0];

  always_comb begin
    case (alu_ctrl)
      ALU_ADD:  alu_res = src1 + src2;
      ALU_AND:  alu_res = src1 & src2;
      ALU_OR:   alu_res = src1 | src2;
      ALU_SUB:  alu_res = src1 + (~src2 + 1'b1);  // -a = (~a+1) 2's complement
      ALU_SLT:  alu_res = {31'b0, $signed(src1) < $signed(src2)};
      ALU_SLTU: alu_res = {31'b0, src1 < src2};
      ALU_XOR:  alu_res = src1 ^ src2;
      ALU_SLL:  alu_res = src1 << shamt;
      ALU_SRL:  alu_res = src1 >> shamt;
      ALU_SRA:  alu_res = $signed(src1) >>> shamt;
      default:  alu_res = 32'd0;
    endcase
  end

  assign zero = alu_res == 32'd0;
  assign last_bit = alu_res[0];
endmodule
