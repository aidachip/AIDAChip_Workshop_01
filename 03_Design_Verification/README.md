# Module 03: Design Verification with GenAI

**Duration**: ~30 minutes
**Prerequisites**: Module 00 (LLM Fundamentals), familiarity with Verilog helpful
**Tools Required**: Icarus Verilog (`iverilog`) or Verilator (see [SETUP.md](../SETUP.md))
**Goal**: Learn to use LLMs for testbench development, assertions, and verification tasks

---

## Overview

This module demonstrates how GenAI can assist with design verification tasks including:
- Generating testbenches from specifications
- Writing SystemVerilog Assertions (SVA)
- Building scoreboards for output checking
- Creating coverage models
- Setting up regression suites
- Debugging failing tests

---

## Tutorial: Design Verification Basics

> **For non-DV engineers**: This section provides essential background to follow the exercises.

### What is Design Verification?

Design Verification (DV) ensures that an RTL design behaves correctly according to its specification. Key components include:

- **Testbench**: Code that stimulates the design and checks responses
- **Stimulus**: Input patterns applied to the design
- **Checking**: Comparison of actual vs. expected behavior
- **Coverage**: Metrics showing what has been tested

### Basic Testbench Structure

```systemverilog
module tb_example;
    // 1. Declare signals
    reg clk, rst_n;
    reg [7:0] data_in;
    wire [7:0] data_out;

    // 2. Instantiate DUT (Design Under Test)
    my_design dut (
        .clk(clk),
        .rst_n(rst_n),
        .data_in(data_in),
        .data_out(data_out)
    );

    // 3. Clock generation
    always #5 clk = ~clk;

    // 4. Test stimulus
    initial begin
        clk = 0; rst_n = 0; data_in = 0;
        #20 rst_n = 1;
        #10 data_in = 8'hAB;
        #10 data_in = 8'hCD;
        #100 $finish;
    end

    // 5. Checking / Assertions
    always @(posedge clk) begin
        if (rst_n && data_out !== expected_value)
            $error("Mismatch!");
    end
endmodule
```

### Key DV Concepts

| Term | Description |
|------|-------------|
| **DUT** | Design Under Test - the module being verified |
| **Stimulus** | Input patterns applied to test the design |
| **Scoreboard** | Component that collects, compares, and checks DUT outputs against expected values |
| **Golden model** | Reference implementation for comparison |
| **Assertion** | Property that must always be true |
| **Coverage** | Measure of what scenarios have been tested |
| **Regression** | Suite of tests run repeatedly to catch bugs introduced by changes |
| **Corner case** | Edge conditions that often reveal bugs |

---

## Exercise 1: Generate a Testbench (10 min)

### Objective
Use Claude to generate a comprehensive testbench for an existing design.

### Step 1: Create a Simple Design

First, let's create a design to verify:

```
Create a simple Verilog module for an 8-bit ALU with:
- Operations: ADD, SUB, AND, OR, XOR (selected by 3-bit opcode)
- Two 8-bit inputs (a, b)
- One 8-bit output (result)
- Carry/borrow output flag
- Zero flag (result == 0)

Save the module to alu.v
```

### Step 2: Generate a Testbench

Now ask Claude to create a testbench:

```
Generate a SystemVerilog testbench for alu.v that:
- Tests all 5 operations
- Includes corner cases (0x00, 0xFF, overflow conditions)
- Uses randomized inputs for at least 100 test vectors
- Compares against expected values calculated in the testbench
- Reports pass/fail for each test
- Generates a VCD waveform file
- Prints a summary at the end (total tests, passed, failed)

Save the testbench to alu_tb.sv
```

### Step 3: Run and Verify

```
Compile alu.v and alu_tb.sv and run the simulation. Show me the results.
```

> **Tip**: If tests fail, ask Claude to help debug. Share the failure messages and ask it to identify whether the issue is in the design or the testbench.

### Step 4: View Waveforms

If you want to examine signal behavior:

```
Open the VCD waveform file with Surfer
```

### Reflection Questions
- Did the testbench catch any bugs in the ALU design?
- What corner cases were tested?
- What additional tests would you add?

---

## Exercise 2: Write Assertions (10 min)

### Objective
Use Claude to write SystemVerilog Assertions (SVA) for property checking.

> **Note**: Keep things interactive! Feel free to ask Claude Code to add more assertions, run checks, or explain assertion syntax. Claude Code may proactively suggest improvements.

### Step 1: Learn Assertion Basics

Ask Claude to explain assertions:

```
Explain SystemVerilog Assertions (SVA) with examples relevant to
digital design. Cover:
1. Immediate assertions vs. concurrent assertions
2. Basic syntax for property and assert
3. Common temporal operators (##, |->. |=>)
4. When to use assertions vs. testbench checks
```

### Step 2: Add Assertions to a Design

```
Add SystemVerilog assertions to alu.v for:
1. Zero flag must be high when result is 0
2. Carry flag behavior for ADD operation
3. Result must be stable for at least one cycle after inputs are stable
4. Opcode must always be a valid operation (0-4)

Create a new file alu_with_sva.sv that includes these assertions.
```

### Step 3: Test the Assertions

```
Create a testbench that deliberately violates one of the assertions
to verify they're working. Run the simulation and show me the
assertion failure message.

Save as alu_assertion_test.sv
```

---

## Exercise 3: Coverage-Driven Verification (10 min)

### Objective
Use Claude to create functional coverage models.

### Step 1: Understand Coverage Concepts

```
Explain functional coverage in SystemVerilog:
1. Covergroups and coverpoints
2. Cross coverage
3. Bins (automatic and explicit)
4. Coverage goals and holes

Provide examples relevant to verifying an ALU.
```

### Step 2: Create a Coverage Model

```
Create a SystemVerilog covergroup for the ALU that covers:
1. All opcodes exercised
2. Input value ranges (low: 0-63, mid: 64-191, high: 192-255)
3. Cross coverage of opcode vs input ranges
4. Corner case bins (inputs = 0x00, 0xFF)
5. Overflow/underflow conditions for ADD/SUB

Add this to a new testbench file: alu_coverage_tb.sv
```

### Step 3: Run and Analyze Coverage

```
Run the coverage testbench and report the coverage results.
Identify any coverage holes and suggest additional test vectors
to fill them.
```

> **Note**: Full coverage support requires commercial tools, but the concepts and syntax you learn here apply directly. Icarus Verilog supports basic covergroups with limited reporting.

---

## Quick Reference: Verification Constructs

### Testbench Tasks

```systemverilog
// Reusable test task
task automatic apply_test(input [7:0] a, b, input [2:0] op);
    @(posedge clk);
    data_a <= a;
    data_b <= b;
    opcode <= op;
    @(posedge clk);
    check_result(a, b, op);
endtask
```

### Basic Assertions

```systemverilog
// Immediate assertion
always @(posedge clk)
    assert (!(read && write)) else $error("Simultaneous R/W!");

// Concurrent assertion
property p_req_ack;
    @(posedge clk) req |-> ##[1:3] ack;
endproperty
assert property (p_req_ack);
```

### Coverage Syntax

```systemverilog
covergroup cg_alu @(posedge clk);
    cp_opcode: coverpoint opcode {
        bins add = {3'b000};
        bins sub = {3'b001};
    }
    cp_input_a: coverpoint input_a {
        bins low = {[0:63]};
        bins high = {[192:255]};
    }
    cross cp_opcode, cp_input_a;
endgroup
```

---

## Advanced Exercises

If you have more time, try these challenging exercises:

### Advanced 1: Self-Checking Testbench with Golden Model

```
Create a self-checking testbench architecture for the ALU that:
1. Implements a behavioral golden model in SystemVerilog
2. Automatically compares DUT output against golden model
3. Uses constrained random stimulus
4. Runs until coverage goals are met OR max cycles reached
5. Reports detailed statistics at the end

Save to alu_selfcheck_tb.sv
```

### Advanced 2: Protocol Checker

```
Design a set of assertions for an AXI4-Lite interface that verify:
1. VALID must not depend on READY (no combinational loop)
2. Once VALID is asserted, it must stay high until READY
3. Data must be stable while VALID is high
4. No overlapping transactions on the same channel

Create a reusable checker module: axi_lite_checker.sv
```

### Advanced 3: Build a Scoreboard

```
Create a reusable scoreboard class for the ALU that:
1. Captures inputs when a transaction starts
2. Computes expected output using a reference model
3. Compares actual DUT output against expected
4. Tracks statistics (total, passed, failed, pending)
5. Reports mismatches with detailed context (inputs, expected, actual)
6. Supports out-of-order completion (use transaction IDs)

Implement in SystemVerilog using a class-based approach.
Save to alu_scoreboard.sv
```

### Advanced 4: Regression Suite Setup

```
Help me set up a regression infrastructure for the ALU:

1. Create 5 different testbenches targeting:
   - Basic operations (alu_test_basic.sv)
   - Corner cases (alu_test_corners.sv)
   - Random stress test (alu_test_random.sv)
   - Overflow conditions (alu_test_overflow.sv)
   - Back-to-back operations (alu_test_b2b.sv)

2. Create a shell script (run_regression.sh) that:
   - Compiles all tests
   - Runs each test and captures pass/fail
   - Generates a summary report
   - Returns non-zero exit code if any test fails

3. Create a simple Makefile with targets:
   - make compile
   - make run_all
   - make run TEST=<testname>
   - make clean
```

### Advanced 5: Debug a Failing Test

```
This testbench reports intermittent failures:

[Paste a testbench with a subtle bug - race condition,
timing issue, or incorrect expected value calculation]

Help me:
1. Identify the root cause of the intermittent failures
2. Explain why it only fails sometimes
3. Fix the issue
```

---

## Prompting Tips for Design Verification

### What Works Well
- Generating testbench structure and boilerplate
- Writing assertions for specific properties
- Building scoreboard architectures with reference models
- Explaining coverage concepts and syntax
- Creating regression scripts and Makefiles
- Creating test plans and checklists
- Suggesting corner cases and edge conditions

### What Requires Caution
- Complex UVM environments (start simple, build up)
- Timing-sensitive checks (verify clock relationships)
- Coverage closure strategies (tool-specific)
- Debug of subtle race conditions

### Effective Context to Include
- Design specification or behavior description
- Interface signals and protocols
- Known corner cases or previous bugs
- Target coverage goals
- Simulation tool being used

---

## Key Takeaways

1. **Testbench generation is a sweet spot** - LLMs excel at creating structured testbenches
2. **Assertions encode design intent** - use AI to help write properties from specs
3. **Coverage is about planning** - AI can suggest what to cover, you decide what matters
4. **Debug is collaborative** - share symptoms, let AI suggest hypotheses
5. **Start simple, add complexity** - don't ask for full UVM on day one

---

## Keep Exploring

The exercises above are just starting points. Feel free to:

- **Tweak the prompts** to verify your own designs
- **Build sophisticated scoreboards** - ask Claude to create scoreboards with queues, reference models, and out-of-order checking for your specific protocols
- **Set up full regression infrastructure** - ask Claude Code to create Makefiles, CI scripts, and test result parsers for your verification environment
- **Explore UVM** - ask Claude about UVM components, sequences, agents, and how scoreboards fit into the UVM architecture
- **Create assertion libraries** - build reusable protocol checkers for your common interfaces (AXI, APB, AHB, etc.)
- **Generate coverage-driven regressions** - ask Claude to analyze coverage holes and generate targeted tests to fill them

The more you experiment, the better you'll understand how to leverage AI in your verification workflow.

---

## Share Your Feedback

We'd love to hear about your experience with this module!

- What worked well? What was frustrating?
- What improvements would you like to see in specialized **Design Verification agents** beyond what Claude Code can do?
- What verification tasks would benefit most from AI assistance?

**Send your feedback to: hello@aidachip.com**

Your insights will directly shape what we're building next - and we have some exciting launches coming soon that you won't want to miss!

---

## Next Module

Continue your workshop journey:
- [04_Physical_Design](../04_Physical_Design/) - Floorplanning, P&R, and timing closure with AI
- [Back to Workshop Home](../README.md)

---

*Module 03 Complete - You've learned to use GenAI for design verification tasks!*

---

**AIDAChip** - Follow us for more insights on AI-driven chip design automation.
