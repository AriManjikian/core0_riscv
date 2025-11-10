module alu (
    input logic [ 3:0] alu_ctrl,
    input logic [31:0] src1,
    input logic [31:0] src2,

    output logic [31:0] alu_res,
    output logic zero
);

  always_comb begin
    case (alu_ctrl)
      4'b0000: alu_res = src1 + src2;
      4'b0010: alu_res = src1 & src2;
      4'b0011: alu_res = src1 | src2;
      4'b0001: alu_res = src1 + (~src2 + 1'b1);  // -a = (~a+1) 2's complement
      4'b0101: alu_res = {31'b0, $signed(src1) < $signed(src2)};
      4'b0111: alu_res = {31'b0, src1 < src2};
      4'b1000: alu_res = src1 ^ src2;
      4'b0100: alu_res = src1 << src2;  // SLL shift left logical
      default: alu_res = 32'd0;
    endcase
  end

  assign zero = alu_res == 32'd0;

endmodule
