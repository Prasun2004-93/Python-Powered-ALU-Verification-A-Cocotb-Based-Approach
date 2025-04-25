module alu (
    input wire [15:0] A,      // First 16-bit operand
    input wire [15:0] B,      // Second 16-bit operand
    input wire [2:0] Op,      // 3-bit operation select
    output reg [15:0] Y,      // 16-bit result
    output reg C,             // Carry/Borrow flag
    output reg V,             // Overflow flag
    output reg N,             // Negative flag
    output reg Z              // Zero flag
);

    reg [16:0] temp;          // Temporary 17-bit result for arithmetic ops

initial begin
$dumpfile("alu.vcd");
$dumpvars(0,alu);
end
    always @(*) begin
        case (Op)
            3'b000: begin // Addition
                temp = A + B;
                Y = temp[15:0];
                C = temp[16];              // Carry out
                V = (A[15] & B[15] & ~Y[15]) | (~A[15] & ~B[15] & Y[15]); // Overflow
            end
            3'b001: begin // Subtraction
                temp = A - B;
                Y = temp[15:0];
                C = (A < B);               // Borrow (1 if A < B)
                V = (A[15] & ~B[15] & ~Y[15]) | (~A[15] & B[15] & Y[15]); // Overflow
            end
            3'b010: begin // AND
                Y = A & B;
                C = 1'b0;
                V = 1'b0;
            end
            3'b011: begin // OR
                Y = A | B;
                C = 1'b0;
                V = 1'b0;
            end
            3'b100: begin // XOR
                Y = A ^ B;
                C = 1'b0;
                V = 1'b0;
            end
            3'b101: begin // NOT
                Y = ~A;
                C = 1'b0;
                V = 1'b0;
            end
            3'b110: begin // Left Shift by 1
                Y = A << 1;
                C = A[15];                 // Carry is MSB
                V = 1'b0;
            end
            3'b111: begin // Arithmetic Right Shift by 1
                Y = {A[15], A[15:1]};     // Sign-extended right shift
                C = A[0];                  // Carry is LSB
                V = 1'b0;
            end
            default: begin
                Y = 16'b0;
                C = 1'b0;
                V = 1'b0;
            end
        endcase
        N = Y[15];                         // Negative flag (sign bit)
        Z = (Y == 16'b0);                  // Zero flag
    end
endmodule
