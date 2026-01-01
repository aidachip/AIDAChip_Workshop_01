# Module 02: RTL Development with GenAI

**Duration**: ~30 minutes
**Prerequisites**: Module 00 (LLM Fundamentals)
**Tools Required**: Icarus Verilog (`iverilog`) or Verilator (see [SETUP.md](../SETUP.md))
**Goal**: Learn to use LLMs for Verilog/SystemVerilog development tasks

---

## Overview

This module demonstrates how GenAI can assist with RTL development tasks including:
- Generating Verilog/SystemVerilog modules from specifications
- Code review and best practices
- Debugging and fixing syntax/logic errors
- Converting between coding styles and formats

---

## Tutorial: RTL Development Basics

> **For non-RTL engineers**: This section provides essential background to follow the exercises.

### What is RTL?

RTL (Register Transfer Level) is a design abstraction that describes digital circuits in terms of:
- **Registers**: Storage elements (flip-flops) that hold state
- **Combinational logic**: Logic that computes outputs from inputs
- **Data flow**: How data moves between registers through logic

### Verilog Basics

```verilog
module example (
    input  wire       clk,
    input  wire       rst_n,
    input  wire [7:0] data_in,
    output reg  [7:0] data_out
);

    // Sequential logic (registers)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            data_out <= 8'b0;
        else
            data_out <= data_in;
    end

endmodule
```

### Key RTL Concepts

| Term | Description |
|------|-------------|
| **Module** | Basic building block, like a function |
| **Wire** | Combinational signal (no storage) |
| **Reg** | Can hold a value (may or may not be a register) |
| **Always block** | Describes behavior (sequential or combinational) |
| **Blocking (=)** | Executes in order, used for combinational logic |
| **Non-blocking (<=)** | Executes in parallel, used for sequential logic |

---

## Exercise 1: Generate an RTL Module (10 min)

### Objective
Use Claude to generate a complete Verilog module from specifications.

### Step 1: Generate and Save

Try this prompt with Claude Code:

```
Generate a Verilog module for an 8-bit synchronous FIFO with:
- Configurable depth (parameter, default 16)
- Write enable and read enable signals
- Full and empty status flags
- Active-low synchronous reset
- Use synthesizable RTL style

Include clear comments explaining each section.

Save the module to fifo.v
```

### Step 2: Compile and Check

You can compile manually:

```bash
iverilog -o fifo_check fifo.v
```

**Or**, ask Claude Code to compile it for you:

```
Compile fifo.v with Icarus Verilog and show me any errors or warnings
```

> **Tip**: If compilation fails or you see warnings, share them with Claude Code. This iterative troubleshooting is a key part of working with AI assistants.

### Step 3: Generate a Testbench

Now ask Claude to create a testbench:

```
Generate a Verilog testbench for fifo.v that:
- Tests reset behavior
- Writes several values to the FIFO
- Reads them back and verifies order
- Tests the full and empty flags
- Generates a VCD waveform file

Save the testbench to fifo_tb.v
```

### Step 4: Run the Simulation

Ask Claude Code to run the simulation:

```
Compile fifo.v and fifo_tb.v together and run the simulation
```

Or manually:

```bash
iverilog -o fifo_sim fifo.v fifo_tb.v
vvp fifo_sim
```

### Step 5: View Waveforms with Surfer

If the testbench generated a VCD file, view the waveforms:

```bash
surfer waves.vcd
```

**Or**, ask Claude Code:

```
Open the generated VCD waveform file with Surfer
```

> **Tip**: Surfer is an open-source waveform viewer. If it's not installed, see [SETUP.md](../SETUP.md) for installation instructions, or ask Claude to help you install it. You can also use GTKWave as an alternative (`gtkwave waves.vcd`).

### Step 6: Iterate

If there are issues at any step, share them with Claude:

```
I got this error when running the simulation:
[paste error]

Please help me debug this.
```

### Reflection Questions
- Is the code synthesizable (no delays, proper reset)?
- Are the pointer widths correct for the depth parameter?
- How would you modify it for an asynchronous FIFO?

---

## Exercise 2: Code Review and Improvement (10 min)

### Objective
Use Claude to review existing RTL code and suggest improvements.

> **Note**: Keep things interactive! Feel free to ask Claude Code to save files, run simulations, or generate testbenches at any point. Claude Code may also proactively suggest ways to help - follow along with its suggestions to explore the workflow.

### Step 1: Present Code for Review

Give Claude this code with issues:

```
Review this Verilog module and identify all issues:

module counter(
    input clk,
    input reset,
    input enable,
    output [7:0] count
);

reg [7:0] count;

always @(posedge clk)
begin
    if (reset)
        count = 0;
    else if (enable)
        count = count + 1;
end

endmodule

Look for:
1. Synthesis issues
2. Coding style problems
3. Potential simulation/synthesis mismatches
4. Best practice violations
```

### Step 2: Request Fixes

```
Fix all the issues you identified and provide the corrected Verilog code.
Explain each change you made.

Save the corrected module to counter_fixed.v
```

### Step 3: Compare Approaches

```
Show me three different ways to implement this counter:
1. Using always_ff (SystemVerilog)
2. Using continuous assignments where possible
3. Using a generate block for parameterized width

Which approach would you recommend for a production design and why?
```

---

## Exercise 3: Generate a Testbench (10 min)

### Objective
Use Claude to generate a comprehensive testbench for verification.

### The Task

```
Generate a SystemVerilog testbench for the FIFO module in fifo.v that:
- Tests reset behavior
- Writes data until full
- Reads data until empty
- Verifies data integrity (FIFO ordering)
- Tests simultaneous read/write
- Uses $display to show test progress
- Reports PASS/FAIL status

Save the testbench to fifo_tb.sv
```

### Run the Simulation

```
Run the testbench with Icarus Verilog and show me the results
```

Or manually:

```bash
iverilog -g2012 -o fifo_sim fifo.v fifo_tb.sv
vvp fifo_sim
```

### Iterate if Needed

```
The testbench shows a failure at the simultaneous read/write test.
Help me debug this - is it a testbench issue or a design issue?
```

---

## Quick Reference: Icarus Verilog Commands

| Command | Description |
|---------|-------------|
| `iverilog -o out file.v` | Compile Verilog |
| `iverilog -g2012 -o out file.sv` | Compile SystemVerilog |
| `vvp out` | Run simulation |
| `iverilog -t null file.v` | Syntax check only |

### Common Flags

| Flag | Description |
|------|-------------|
| `-g2012` | Enable SystemVerilog (IEEE 1800-2012) |
| `-Wall` | Enable all warnings |
| `-o <name>` | Output file name |
| `-I <dir>` | Include directory |
| `-D<macro>` | Define macro |

### Waveform Viewing

Add to your testbench for waveform generation:
```verilog
initial begin
    $dumpfile("waves.vcd");
    $dumpvars(0, fifo_tb);
end
```

View with Surfer (recommended): `surfer waves.vcd`

Or with GTKWave: `gtkwave waves.vcd`

---

## Advanced Exercises

If you have more time, try these challenging exercises:

### Advanced 1: FSM Generation

```
Design a Verilog FSM for a traffic light controller with:
- States: GREEN, YELLOW, RED for main road
- States: GREEN, YELLOW, RED for side road
- Configurable timing for each state
- Pedestrian crossing request input
- Emergency vehicle preemption input

Use one-hot encoding for states.
Include a state diagram in comments.

Save to traffic_light.v
```

### Advanced 2: Code Conversion

```
Convert this Verilog-95 style code to modern SystemVerilog:

module old_style (a, b, c, clk, rst, out);
    input a, b, c;
    input clk, rst;
    output out;
    reg out;
    reg [1:0] state;

    parameter IDLE = 0, RUN = 1, DONE = 2;

    always @(posedge clk or posedge rst)
        if (rst) begin
            state = IDLE;
            out = 0;
        end
        else case (state)
            IDLE: if (a) state = RUN;
            RUN: if (b) state = DONE;
            DONE: begin out = c; state = IDLE; end
        endcase
endmodule

Use:
- ANSI-style ports
- logic instead of reg/wire
- always_ff and always_comb
- Enumerated types for states
- Proper non-blocking assignments
```

### Advanced 3: Interface Design

```
Create a SystemVerilog interface for an AXI4-Lite bus with:
- All required signals (AWADDR, AWVALID, AWREADY, etc.)
- Modports for master and slave
- Clocking blocks for verification
- Helper tasks for read/write transactions

Then create a simple register file slave that uses this interface.

Save the interface to axi_lite_if.sv
Save the register file to axi_lite_regs.sv
```

---

## Prompting Tips for RTL Development

### What Works Well
- Generating modules from clear specifications
- Code review and identifying issues
- Converting between coding styles
- Generating testbenches
- Explaining complex RTL constructs

### What Requires Caution
- Complex timing requirements (verify with STA)
- CDC (clock domain crossing) - always review carefully
- Area/power optimization claims (use synthesis tools)
- Tool-specific pragmas and attributes

### Effective Context to Include
- Target technology/FPGA family
- Coding standards (company or industry)
- Synthesis tool being used
- Clock frequency and timing requirements
- Reset strategy (sync/async, active high/low)

---

## Key Takeaways

1. **LLMs excel at generating boilerplate RTL** - FIFOs, FSMs, interfaces
2. **Code review is valuable** - catch issues before synthesis
3. **Testbench generation saves time** - but verify coverage
4. **Specify coding style explicitly** - Verilog-95 vs SystemVerilog
5. **Always simulate and synthesize** - AI-generated code needs verification

---

## Keep Exploring

The exercises above are just starting points. Feel free to:

- **Tweak the prompts** to generate modules for your own projects
- **Explore other architectures** - ask Claude about pipelining, arbitration schemes, or protocol implementations
- **Generate comprehensive testbenches** - ask Claude Code to create UVM environments, coverage collectors, or assertion-based verification

The more you experiment, the better you'll understand how to leverage AI in your RTL development workflow.

---

## Share Your Feedback

We'd love to hear about your experience with this module!

- What worked well? What was frustrating?
- What improvements would you like to see in specialized **RTL Development agents** beyond what Claude Code can do?
- What RTL tasks would benefit most from AI assistance?

**Send your feedback to: hello@aidachip.com**

Your insights will directly shape what we're building next - and we have some exciting launches coming soon that you won't want to miss!

---

## Next Module

Continue your workshop journey:
- [03_Design_Verification](../03_Design_Verification/) - Testbenches, UVM, and coverage with AI
- [Back to Workshop Home](../README.md)

---

*Module 02 Complete - You've learned to use GenAI for RTL development tasks!*

---

**AIDAChip** - Follow us for more insights on AI-driven chip design automation.
