module sign_ext (
    input logic [24:0] raw_src,
    input logic [ 1:0] imm_src,

    output logic [31:0] imm
);

  logic [11:0] gathered_imm;
  always_comb begin
    case (imm_src)
      // I Type
      2'b00:   gathered_imm = raw_src[24:13];
      // S Type
      2'b01:   gathered_imm = {raw_src[24:18], raw_src[4:0]};
      // B-Type
      2'b10:   gathered_imm = {raw_src[0], raw_src[23:18], raw_src[4:1], 1'b0};
      default: gathered_imm = 12'b0;
    endcase
  end
  assign imm = (imm_src == 2'b10) ? {{20{raw_src[24]}}, gathered_imm} : {{20{gathered_imm[11]}}, gathered_imm};
endmodule
