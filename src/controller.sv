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
  import core0_pkg::*;

  // OP DECODER
  logic [1:0] alu_op;
  logic branch;
  logic jump;

  always_comb begin
    case (op)
      // I-Type
      OPCODE_I_TYPE_LOAD: begin
        reg_write = 1'b1;
        imm_src = 3'b000;
        mem_write = 1'b0;
        alu_op = 2'b00;
        alu_src = 1'b1;
        write_back_src = 2'b01;
        branch = 1'b0;
        jump = 1'b0;
      end
      OPCODE_I_TYPE_ALU: begin
        imm_src = 3'b000;
        mem_write = 1'b0;
        alu_op = 2'b10;
        alu_src = 1'b1;
        write_back_src = 2'b00;
        branch = 1'b0;
        jump = 1'b0;
        if (func3 == F3_SLL) begin
          reg_write = (func7 == F7_SLL_SRL) ? 1'b1 : 1'b0;
        end else if (func3 == F3_SRL_SRA) begin
          reg_write = (func7 == F7_SLL_SRL | func7 == F7_SRA) ? 1'b1 : 1'b0;
        end else begin
          reg_write = 1'b1;
        end
      end
      OPCODE_S_TYPE: begin
        reg_write = 1'b0;
        imm_src = 3'b001;
        mem_write = 1'b1;
        alu_op = 2'b00;
        alu_src = 1'b1;
        branch = 1'b0;
        jump = 1'b0;
      end
      OPCODE_R_TYPE: begin
        reg_write = 1'b1;
        mem_write = 1'b0;
        alu_op = 2'b10;
        alu_src = 1'b0;
        write_back_src = 2'b00;
        branch = 1'b0;
        jump = 1'b0;
      end
      OPCODE_B_TYPE: begin
        reg_write = 1'b0;
        imm_src = 3'b010;
        alu_src = 1'b0;
        mem_write = 1'b0;
        alu_op = 2'b01;
        branch = 1'b1;
        jump = 1'b0;
        second_add_src = 2'b00;
      end
      OPCODE_J_TYPE, OPCODE_J_TYPE_JALR: begin
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
      OPCODE_U_TYPE_LUI, OPCODE_U_TYPE_AUIPC: begin
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
      ALU_OP_LOAD_STORE: alu_ctrl = ALU_ADD;
      ALU_OP_MATH: begin
        unique case (func3)
          F3_ADD_SUB: begin
            if (op == 7'b0110011) begin
              alu_ctrl = (func7 == F7_SUB) ? ALU_SUB : ALU_ADD;
            end else begin
              alu_ctrl = ALU_ADD;
            end
          end
          F3_AND:  alu_ctrl = ALU_AND;
          F3_OR:   alu_ctrl = ALU_OR;
          F3_SLT:  alu_ctrl = ALU_SLT;
          F3_SLTU: alu_ctrl = ALU_SLTU;
          F3_XOR:  alu_ctrl = ALU_XOR;
          F3_SLL:  alu_ctrl = ALU_SLL;
          F3_SRL_SRA: begin
            if (func7 == F7_SLL_SRL) begin
              alu_ctrl = ALU_SRL;
            end else if (func7 == F7_SRA) begin
              alu_ctrl = ALU_SRA;
            end
          end
        endcase
      end
      // B-Type
      ALU_OP_BRANCHES: begin
        case (func3)
          // BEQ, BNE
          F3_BEQ, F3_BNE: alu_ctrl = 4'b0001;
          // BLT, BGE
          F3_BLT, F3_BGE: alu_ctrl = 4'b0101;
          // BLTU, BGEU
          F3_BLTU, F3_BGEU: alu_ctrl = 4'b0111;
          default: alu_ctrl = 4'b1111;
        endcase
      end
      default: alu_ctrl = 4'b1111;
    endcase
  end

  logic assert_branch;
  always_comb begin : branch_logic_decode
    case (func3)
      // BEQ
      F3_BEQ: assert_branch = alu_zero & branch;
      // BLT, BLTU
      F3_BLT, F3_BLTU: assert_branch = alu_last_bit & branch;
      // BNE
      F3_BNE: assert_branch = ~alu_zero & branch;
      // BGE, BGEU
      F3_BGE, F3_BGEU: assert_branch = ~alu_last_bit & branch;
      default: assert_branch = 1'b0;
    endcase
  end

  assign pc_src = assert_branch | jump;

endmodule
