`timescale 1ns / 1ps
module memory #(
    parameter WORDS = 64,
    parameter mem_init = ""
) (
    input logic clk,
    input logic rst_n,
    input logic [31:0] address,
    input logic [31:0] write_data,
    input logic w_en,

    output logic [31:0] read_data
);

  reg [31:0] mem[WORDS];

  initial begin
    if (mem_init != "") begin
      $readmemh(mem_init, mem);
    end
  end

  always @(posedge clk) begin
    if (rst_n == 1'b0) begin
      for (int i = 0; i < WORDS; i++) begin
        mem[i] <= 32'd0;
      end
    end else begin
      if (w_en) begin
        if (address[1:0] != 2'b00) begin
          $display("Misaligned write at address %h", address);
        end else begin
          mem[address[31:2]%WORDS] <= write_data;
        end
      end
    end
  end

  always_comb begin
    read_data = mem[address[31:2]%WORDS];
  end
endmodule
