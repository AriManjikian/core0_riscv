module regfile #(
    parameter REGISTER_COUNT = 32
) (

    input logic clk,
    input logic rst_n,

    input logic [4:0] address1,
    input logic [4:0] address2,

    output logic [31:0] read_data1,
    output logic [31:0] read_data2,

    input logic w_en,
    input logic [31:0] write_data,
    input logic [4:0] address3
);

  (* public *) reg [31:0] registers[REGISTER_COUNT];

  always @(posedge clk) begin
    if (rst_n == 1'b0) begin
      for (int i = 0; i < REGISTER_COUNT; i++) begin
        registers[i] <= 32'b0;
      end
    end else if (w_en == 1'b1 && address3 != 0) begin
      registers[address3] <= write_data;
    end
  end

  always_comb begin : readLogic
    read_data1 = registers[address1];
    read_data2 = registers[address2];
  end

endmodule
