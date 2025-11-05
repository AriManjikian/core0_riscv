module sign_ext (
    input logic [24:0] raw_src,
    input logic imm_src,

    output logic [31:0] imm
);

  logic [11:0] gathered_imm;
  always_comb begin
    case (imm_src)
      1'b00:   gathered_imm = raw_src[24:13];
      default: gathered_imm = 12'b0;
    endcase
  end
  assign imm = {{20{gathered_imm[11]}}, gathered_imm};
endmodule
