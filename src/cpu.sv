module cpu (
    input logic clk,
    input logic rst_n
);

  reg   [31:0] pc;
  logic [31:0] pc_next;

  always_comb begin : pcSelect
    pc_next = pc + 4;
  end

  always @(posedge clk) begin
    if (rst_n == 0) begin
      pc <= 32'b0;
    end else begin
      pc <= pc_next;
    end
  end

  wire [31:0] instr;

  memory #(
      .mem_init("./test_imemory.hex")
  ) instruction_memory (
      .clk(clk),
      .address(pc),
      .write_data(32'b0),
      .w_en(1'b0),
      .byte_en(4'b0),
      .rst_n(1'b1),

      .read_data(instr)
  );

  logic [6:0] op;
  assign op = instr[6:0];
  logic [2:0] func3;
  assign func3 = instr[14:12];
  wire alu_zero;

  wire [2:0] alu_ctrl;
  wire [1:0] imm_src;
  wire mem_write;
  wire reg_write;

  controller controller_unit (
      .op(op),
      .func3(func3),
      .func7(7'b0),
      .alu_zero(alu_zero),

      .alu_ctrl (alu_ctrl),
      .imm_src  (imm_src),
      .mem_write(mem_write),
      .reg_write(reg_write)
  );

  logic [4:0] source_reg1;
  assign source_reg1 = instr[19:15];
  logic [4:0] source_reg2;
  assign source_reg2 = instr[24:20];
  logic [4:0] dest_reg;
  assign dest_reg = instr[11:7];
  wire  [31:0] data_reg1;
  wire  [31:0] data_reg2;

  logic [31:0] write_back_data;
  always_comb begin : wbSelect
    write_back_data = mem_read;
  end

  regfile regfile (
      .clk  (clk),
      .rst_n(rst_n),

      .address1(source_reg1),
      .address2(source_reg2),
      .read_data1(data_reg1),
      .read_data2(data_reg2),
      .w_en(reg_write),
      .write_data(write_back_data),
      .address3(dest_reg)
  );

  logic [24:0] raw_imm;
  assign raw_imm = instr[31:7];
  wire [31:0] imm;
  sign_ext sign_extender (
      .raw_src(raw_imm),
      .imm_src(imm_src),
      .imm(imm)
  );

  wire  [31:0] alu_res;
  logic [31:0] alu_src2;
  always_comb begin : srcBSelect
    alu_src2 = imm;
  end

  alu alu_inst (
      .alu_ctrl(alu_ctrl),
      .src1(data_reg1),
      .src2(alu_src2),

      .alu_res(alu_res),
      .zero(alu_zero)
  );

  wire [31:0] mem_read;
  memory #(
      .mem_init("./test_dmemory.hex")
  ) data_memory (
      .clk(clk),
      .address(alu_res),
      .write_data(32'b0),
      .w_en(1'b0),
      .byte_en(4'b0),
      .rst_n(1'b1),

      .read_data(mem_read)
  );

endmodule
