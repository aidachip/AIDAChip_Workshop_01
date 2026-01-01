// =============================================================================
// LFSR (Linear Feedback Shift Register) for BIST Pattern Generation
// =============================================================================
//
// This module implements a parameterizable LFSR for generating pseudo-random
// test patterns in Built-In Self-Test (BIST) applications.
//
// Features:
// - Parameterizable width (8, 16, 32 bits)
// - Maximum-length polynomial for full sequence coverage
// - Seed loading for deterministic sequences
// - Enable control for stepping
//
// =============================================================================

module lfsr #(
    parameter WIDTH = 16,           // LFSR width
    parameter SEED  = 16'hACE1     // Initial seed (non-zero)
)(
    input  wire             clk,        // Clock
    input  wire             rst_n,      // Active-low reset
    input  wire             enable,     // Enable LFSR stepping
    input  wire             load,       // Load seed value
    input  wire [WIDTH-1:0] seed_val,   // Seed value to load
    output wire [WIDTH-1:0] lfsr_out,   // LFSR output
    output wire             lfsr_bit    // Single-bit output (LSB)
);

    reg [WIDTH-1:0] lfsr_reg;
    wire feedback;

    // =========================================================================
    // Polynomial Selection
    // =========================================================================
    // Maximum-length polynomials ensure the LFSR cycles through all 2^N - 1
    // non-zero states before repeating.
    //
    // Common polynomials (taps listed are XORed with MSB for feedback):
    // 8-bit:  x^8 + x^6 + x^5 + x^4 + 1         (taps: 8,6,5,4)
    // 16-bit: x^16 + x^15 + x^13 + x^4 + 1      (taps: 16,15,13,4)
    // 32-bit: x^32 + x^22 + x^2 + x^1 + 1       (taps: 32,22,2,1)
    // =========================================================================

    generate
        if (WIDTH == 8) begin : gen_lfsr8
            // 8-bit: x^8 + x^6 + x^5 + x^4 + 1
            assign feedback = lfsr_reg[7] ^ lfsr_reg[5] ^ lfsr_reg[4] ^ lfsr_reg[3];
        end
        else if (WIDTH == 16) begin : gen_lfsr16
            // 16-bit: x^16 + x^15 + x^13 + x^4 + 1
            assign feedback = lfsr_reg[15] ^ lfsr_reg[14] ^ lfsr_reg[12] ^ lfsr_reg[3];
        end
        else if (WIDTH == 32) begin : gen_lfsr32
            // 32-bit: x^32 + x^22 + x^2 + x^1 + 1
            assign feedback = lfsr_reg[31] ^ lfsr_reg[21] ^ lfsr_reg[1] ^ lfsr_reg[0];
        end
        else begin : gen_lfsr_default
            // Default: simple XOR of two MSBs (not maximum length!)
            assign feedback = lfsr_reg[WIDTH-1] ^ lfsr_reg[WIDTH-2];
        end
    endgenerate

    // =========================================================================
    // LFSR Register
    // =========================================================================

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            lfsr_reg <= SEED;
        end
        else if (load) begin
            // Load a specific seed value
            lfsr_reg <= (seed_val == {WIDTH{1'b0}}) ? SEED : seed_val;
        end
        else if (enable) begin
            // Shift left and insert feedback at LSB
            lfsr_reg <= {lfsr_reg[WIDTH-2:0], feedback};
        end
    end

    // =========================================================================
    // Outputs
    // =========================================================================

    assign lfsr_out = lfsr_reg;
    assign lfsr_bit = lfsr_reg[0];

endmodule

// =============================================================================
// Usage Example:
// =============================================================================
//
// lfsr #(
//     .WIDTH(16),
//     .SEED(16'hACE1)
// ) pattern_gen (
//     .clk(clk),
//     .rst_n(rst_n),
//     .enable(bist_active),
//     .load(load_seed),
//     .seed_val(16'h1234),
//     .lfsr_out(test_pattern),
//     .lfsr_bit(random_bit)
// );
//
// =============================================================================
