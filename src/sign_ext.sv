`timescale 1ns / 1ps

module sign_ext (
    input logic [24:0] raw_src,
    input logic [ 2:0] imm_src,

    output logic [31:0] imm
);

  always_comb begin
    case (imm_src)
      // I Type
      3'b000:  imm = {{20{raw_src[24]}}, raw_src[24:13]};
      // S Type
      3'b001:  imm = {{20{raw_src[24]}}, raw_src[24:18], raw_src[4:0]};
      // B-Type
      3'b010:  imm = {{20{raw_src[24]}}, raw_src[0], raw_src[23:18], raw_src[4:1], 1'b0};
      // J-Type
      3'b011:  imm = {{12{raw_src[24]}}, raw_src[12:5], raw_src[13], raw_src[23:14], 1'b0};
      // U-Type
      3'b100:  imm = {raw_src[24:5], 12'b000000000000};
      default: imm = 32'b0;
    endcase
  end
endmodule
