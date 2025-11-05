module controller (
    input logic [6:0] op,
    input logic [2:0] func3,
    input logic [6:0] func7,
    input logic alu_zero,

    output logic [2:0] alu_ctrl,
    output logic [1:0] imm_src,
    output logic mem_write,
    output logic reg_write
);
  // OP DECODER
  logic [1:0] alu_op;
  always_comb begin
    case (op)
      // LW OP (0000011)
      7'b0000011: begin
        reg_write = 1'b1;
        imm_src = 2'b00;
        mem_write = 1'b0;
        alu_op = 2'b00;
      end
      default: begin
        reg_write = 1'b0;
        imm_src = 2'b00;
        mem_write = 1'b0;
        alu_op = 2'b00;
      end
    endcase
  end

  //ALU DECODER
  always_comb begin
    case (alu_op)
      2'b00:   alu_ctrl = 3'b000;
      default: alu_ctrl = 3'b111;
    endcase
  end

endmodule
