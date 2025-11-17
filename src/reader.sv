module reader (

    input logic [31:0] mem_data,
    input logic [ 3:0] be_mask,
    input logic [ 2:0] func3,

    output logic [31:0] wb_data,
    output logic valid
);

  logic sign_ext;
  assign sign_ext = ~func3[2];

  logic [31:0] masked_data;
  logic [31:0] raw_data;

  always_comb begin : mask_apply
    for (int i = 0; i < 4; i++) begin
      if (be_mask[i]) begin
        masked_data[(i*8)+:8] = mem_data[(i*8)+:8];
      end else begin
        masked_data[(i*8)+:8] = 8'h00;
      end
    end
  end

  always_comb begin : shift_data
    case (func3)
      3'b010:  raw_data = masked_data;
      3'b000, 3'b100: begin
        case (be_mask)
          4'b0001: raw_data = masked_data;
          4'b0010: raw_data = masked_data >> 8;
          4'b0100: raw_data = masked_data >> 16;
          4'b1000: raw_data = masked_data >> 24;
          default: raw_data = 32'd0;
        endcase
      end
      3'b001, 3'b101: begin
        case (be_mask)
          4'b0011: raw_data = masked_data;
          4'b1100: raw_data = masked_data >> 16;
          default: raw_data = 32'd0;
        endcase
      end
      default: raw_data = 32'd0;
    endcase
  end

  always_comb begin : sign_ext_logic
    case (func3)
      3'b010: wb_data = raw_data;
      3'b000, 3'b100: wb_data = sign_ext ? {{24{raw_data[7]}}, raw_data[7:0]} : raw_data;
      3'b001, 3'b101: wb_data = sign_ext ? {{16{raw_data[15]}}, raw_data[15:0]} : raw_data;
      default: wb_data = 32'd0;
    endcase
    valid = |be_mask;
  end
endmodule
