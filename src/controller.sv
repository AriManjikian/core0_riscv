module controller (
    input logic [6:0] op,
    input logic [2:0] func3,
    input logic [6:0] func7,
    input logic alu_zero,

    output logic [2:0] alu_ctrl,
    output logic [1:0] imm_src,
    output logic mem_write,
    output logic reg_write,
    output logic alu_src,
    output logic write_back_src,
    output logic pc_src
);
  // OP DECODER
  logic [1:0] alu_op;
  logic branch;

  /* verilator lint_off LATCH */
  always_comb begin
    case (op)
      // I-Type
      7'b0000011: begin
        reg_write = 1'b1;
        imm_src = 2'b00;
        mem_write = 1'b0;
        alu_op = 2'b00;
        alu_src = 1'b1;
        write_back_src = 1'b1;
        branch = 1'b0;
      end
      // S-Type
      7'b0100011: begin
        reg_write = 1'b0;
        imm_src = 2'b01;
        mem_write = 1'b1;
        alu_op = 2'b00;
        alu_src = 1'b1;
        branch = 1'b0;
      end
      // R-Type
      7'b0110011: begin
        reg_write = 1'b1;
        mem_write = 1'b0;
        alu_op = 2'b10;
        alu_src = 1'b0;
        write_back_src = 1'b0;
        branch = 1'b0;
      end
      7'b1100011: begin
        reg_write = 1'b0;
        imm_src = 2'b10;
        alu_src = 1'b0;
        mem_write = 1'b0;
        alu_op = 2'b01;
        branch = 1'b1;
      end
      default: begin
        reg_write = 1'b0;
        imm_src = 2'b00;
        mem_write = 1'b0;
        alu_op = 2'b00;
      end
    endcase
  end
  /* verilator lint_on LATCH */

  //ALU DECODER
  always_comb begin
    case (alu_op)
      // LW SW
      2'b00:   alu_ctrl = 3'b000;
      // R-Types
      2'b10: begin
        case (func3)
          // ADD
          3'b000:  alu_ctrl = 3'b000;
          // AND
          3'b111:  alu_ctrl = 3'b010;
          // OR
          3'b110:  alu_ctrl = 3'b011;
          default: alu_ctrl = 3'b111;
        endcase
      end
      // B-Type
      2'b01:   alu_ctrl = 3'b001;
      default: alu_ctrl = 3'b111;
    endcase
  end
  assign pc_src = branch & alu_zero;
endmodule
