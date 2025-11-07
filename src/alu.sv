module alu (
    input logic [ 2:0] alu_ctrl,
    input logic [31:0] src1,
    input logic [31:0] src2,

    output logic [31:0] alu_res,
    output logic zero
);

  always_comb begin
    case (alu_ctrl)
      3'b000:  alu_res = src1 + src2;
      3'b010:  alu_res = src1 & src2;
      3'b011:  alu_res = src1 | src2;
      default: alu_res = 32'b0;
    endcase
  end

  assign zero = alu_res == 32'b0;

endmodule
