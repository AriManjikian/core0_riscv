`timescale 1ns / 1ps
module controller (
    input logic [6:0] op,
    input logic [2:0] func3,
    input logic [6:0] func7,
    input logic alu_zero,
    input logic alu_last_bit,

    output logic [3:0] alu_ctrl,
    output logic [2:0] imm_src,
    output logic mem_write,
    output logic reg_write,
    output logic alu_src,
    output logic [1:0] write_back_src,
    output logic pc_src,
    output logic [1:0] second_add_src
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
        imm_src = 3'b000;
        mem_write = 1'b0;
        alu_op = 2'b10;
        alu_src = 1'b1;
        write_back_src = 2'b00;
        branch = 1'b0;
        jump = 1'b0;
        if (func3 == 3'b001) begin
          reg_write = (func7 == 7'b0000000) ? 1'b1 : 1'b0;
        end else if (func3 == 3'b101) begin
          reg_write = (func7 == 7'b0000000 | func7 == 7'b0100000) ? 1'b1 : 1'b0;
        end else begin
          reg_write = 1'b1;
        end
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
        second_add_src = 2'b00;
      end
      // J-Type
      7'b1101111, 7'b1100111: begin
        reg_write = 1'b1;
        mem_write = 1'b0;
        write_back_src = 2'b10;
        branch = 1'b0;
        jump = 1'b1;
        if (op[3]) begin
          second_add_src = 2'b00;
          imm_src = 3'b011;
        end else if (~op[3]) begin
          second_add_src = 2'b10;
          imm_src = 3'b000;
        end
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
          1'b1: second_add_src = 2'b01;  //lui
          1'b0: second_add_src = 2'b00;  // auipc
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
          // ADD, SUB
          3'b000: begin
            if (op == 7'b0110011) begin
              alu_ctrl = func7[5] ? 4'b0001 : 4'b0000;
            end else begin
              alu_ctrl = 4'b0000;
            end
          end
          // AND
          3'b111: alu_ctrl = 4'b0010;
          // OR
          3'b110: alu_ctrl = 4'b0011;
          // SLT, SLTI
          3'b010: alu_ctrl = 4'b0101;
          // SLTU, SLTIU
          3'b011: alu_ctrl = 4'b0111;
          // XOR
          3'b100: alu_ctrl = 4'b1000;
          // SLL
          3'b001: alu_ctrl = 4'b0100;
          // SRL, SRA
          3'b101: begin
            if (func7 == 7'b0000000) begin
              alu_ctrl = 4'b0110;  // srl
            end else if (func7 == 7'b0100000) begin
              alu_ctrl = 4'b1001;  // sra
            end
          end

          default: alu_ctrl = 4'b0111;
        endcase
      end
      // B-Type
      2'b01: begin
        case (func3)
          // BEQ, BNE
          3'b000, 3'b001: alu_ctrl = 4'b0001;
          // BLT, BGE
          3'b100, 3'b101: alu_ctrl = 4'b0101;
          // BLTU, BGEU
          3'b110, 3'b111: alu_ctrl = 4'b0111;
          default: alu_ctrl = 4'b1111;
        endcase
      end
      default: alu_ctrl = 4'b0111;
    endcase
  end

  logic assert_branch;
  always_comb begin : branch_logic_decode
    case (func3)
      // BEQ
      3'b000: assert_branch = alu_zero & branch;
      // BLT, BLTU
      3'b100, 3'b110: assert_branch = alu_last_bit & branch;
      // BNE
      3'b001: assert_branch = ~alu_zero & branch;
      // BGE, BGEU
      3'b101, 3'b111: assert_branch = ~alu_last_bit & branch;
      default: assert_branch = 1'b0;
    endcase
  end

  assign pc_src = assert_branch | jump;

endmodule
