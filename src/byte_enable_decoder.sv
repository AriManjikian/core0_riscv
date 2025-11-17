`timescale 1ns / 1ps

module byte_enable_decoder (
    input logic [31:0] alu_res_address,
    input logic [ 2:0] func3,
    input logic [31:0] reg_read,

    output logic [ 3:0] byte_en,
    output logic [31:0] data
);
  logic [1:0] offset;


  assign offset = alu_res_address[1:0];

  always_comb begin
    case (func3)
      3'b000, 3'b100: begin
        case (offset)
          2'b00: begin
            byte_en = 4'b0001;
            data = reg_read & 32'h000000FF;
          end
          2'b01: begin
            byte_en = 4'b0010;
            data = (reg_read & 32'h000000FF) << 8;
          end
          2'b10: begin
            byte_en = 4'b0100;
            data = (reg_read & 32'h000000FF) << 16;
          end
          2'b11: begin
            byte_en = 4'b1000;
            data = (reg_read & 32'h000000FF) << 24;
          end
          default: begin
            byte_en = 4'b0000;
          end
        endcase
      end
      3'b010: begin
        byte_en = (offset == 2'b00) ? 4'b1111 : 4'b0000;
        data = reg_read;
      end
      3'b001, 3'b101: begin
        case (offset)
          2'b00: begin
            byte_en = 4'b0011;
            data = reg_read & 32'h0000FFFF;
          end
          2'b10: begin
            byte_en = 4'b1100;
            data = (reg_read & 32'h0000FFFF) << 16;
          end
          default: byte_en = 4'b0000;
        endcase
      end
      default: begin
        byte_en = 4'b0000;
      end
    endcase

  end

endmodule
