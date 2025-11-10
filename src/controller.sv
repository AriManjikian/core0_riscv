`timescale 1ns / 1ps
module controller (
    input logic [6:0] op,
    input logic [2:0] func3,
    input logic [6:0] func7,
    input logic alu_zero,

    output logic [3:0] alu_ctrl,
    output logic [2:0] imm_src,
    output logic mem_write,
    output logic reg_write,
    output logic alu_src,
    output logic [1:0] write_back_src,
    output logic pc_src,
    output logic second_add_src
);
  // OP DECODER
  logic [1:0] alu_op;
  logic branch;
  logic jump;

  always_comb begin
    case (op)
      // I-Type
      7'b0000011: begin
        reg_write = 1'b1;
        imm_src = 3'b000;
        mem_write = 1'b0;
        alu_op = 2'b00;
        alu_src = 1'b1;
        write_back_src = 2'b01;
        branch = 1'b0;
        jump = 1'b0;
      end
      // ALU I-Type
      7'b0010011: begin
        reg_write = 1'b1;
        imm_src = 3'b000;
        mem_write = 1'b0;
        alu_op = 2'b10;
        alu_src = 1'b1;
        write_back_src = 2'b00;
        branch = 1'b0;
        jump = 1'b0;
      end
      // S-Type
      7'b0100011: begin
        reg_write = 1'b0;
        imm_src = 3'b001;
        mem_write = 1'b1;
        alu_op = 2'b00;
        alu_src = 1'b1;
        branch = 1'b0;
        jump = 1'b0;
      end
      // R-Type
      7'b0110011: begin
        reg_write = 1'b1;
        mem_write = 1'b0;
        alu_op = 2'b10;
        alu_src = 1'b0;
        write_back_src = 2'b00;
        branch = 1'b0;
        jump = 1'b0;
      end
      // B-Type
      7'b1100011: begin
        reg_write = 1'b0;
        imm_src = 3'b010;
        alu_src = 1'b0;
        mem_write = 1'b0;
        alu_op = 2'b01;
        branch = 1'b1;
        jump = 1'b0;
      end
      // J-Type
      7'b1101111: begin
        reg_write = 1'b1;
        imm_src = 3'b011;
        mem_write = 1'b0;
        write_back_src = 2'b10;
        branch = 1'b0;
        jump = 1'b1;
      end
      // U-Type
      7'b0110111, 7'b0010111: begin
        reg_write = 1'b1;
        imm_src = 3'b100;
        mem_write = 1'b0;
        write_back_src = 2'b11;
        branch = 1'b0;
        jump = 1'b0;
        unique case (op[5])
          1'b1: second_add_src = 1'b1;  //lui
          1'b0: second_add_src = 1'b0;  // auipc
        endcase
      end
      default: begin
        reg_write = 1'b0;
        mem_write = 1'b0;
        jump = 1'b0;
        branch = 1'b0;
      end
    endcase
  end

  //ALU DECODER
  always_comb begin
    case (alu_op)
      // LW SW
      2'b00:   alu_ctrl = 4'b0000;
      // R-Types
      2'b10: begin
        case (func3)
          // ADD
          3'b000:  alu_ctrl = 4'b0000;
          // AND
          3'b111:  alu_ctrl = 4'b0010;
          // OR
          3'b110:  alu_ctrl = 4'b0011;
          // SLTI
          3'b010:  alu_ctrl = 4'b0101;
          // SLTIU
          3'b011:  alu_ctrl = 4'b0111;
          // XOR
          3'b100:  alu_ctrl = 4'b1000;
          // SLL
          3'b001:  alu_ctrl = 4'b0100;
          default: alu_ctrl = 4'b0111;
        endcase
      end
      // B-Type
      2'b01:   alu_ctrl = 4'b0001;
      default: alu_ctrl = 4'b0111;
    endcase
  end
  assign pc_src = (alu_zero & branch) | jump;

endmodule
