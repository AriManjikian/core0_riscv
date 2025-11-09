`timescale 1ns / 1ps

module sign_ext (
    input logic [24:0] raw_src,
    input logic [ 1:0] imm_src,

    output logic [31:0] imm
);

  always_comb begin
    case (imm_src)
      // I Type
      2'b00: imm = {{20{raw_src[24]}}, raw_src[24:13]};
      // S Type
      2'b01: imm = {{20{raw_src[24]}}, raw_src[24:18], raw_src[4:0]};
      // B-Type
      2'b10: imm = {{20{raw_src[24]}}, raw_src[0], raw_src[23:18], raw_src[4:1], 1'b0};

      // J-Ty  pe
      2'b11:   imm = {{12{raw_src[24]}}, raw_src[12:5], raw_src[13], raw_src[23:14], 1'b0};
      default: imm = 32'b0;
    endcase
  end
endmodule
