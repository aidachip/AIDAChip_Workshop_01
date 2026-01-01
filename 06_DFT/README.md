# Module 06: Design for Test (DFT) with GenAI

**Duration**: ~30 minutes
**Prerequisites**: Module 00 (LLM Fundamentals), Module 02 (RTL) helpful
**Tools Required**: Icarus Verilog for RTL exercises (see [SETUP.md](../SETUP.md))
**Goal**: Learn to use LLMs for DFT planning, scan insertion, test pattern concepts, and automation

---

## Overview

This module demonstrates how GenAI can assist with DFT tasks including:
- Understanding scan chain architecture
- Generating scan insertion scripts
- ATPG pattern analysis and debugging
- BIST implementation concepts
- Test coverage analysis
- DFT rule checking

---

## Tutorial: DFT Basics

> **For non-DFT engineers**: This section provides essential background to follow the exercises.

### Why DFT?

Manufacturing defects can cause circuit failures. DFT adds structures that make chips testable:

- **Without DFT**: Only primary inputs/outputs accessible → low test coverage
- **With DFT**: Internal states controllable and observable → high test coverage

### Key DFT Concepts

| Term | Description |
|------|-------------|
| **Scan chain** | Flip-flops connected in series for shift-based testing |
| **Scan mode** | Test mode where flip-flops act as a shift register |
| **ATPG** | Automatic Test Pattern Generation - creates test vectors |
| **Fault coverage** | Percentage of faults detected by test patterns |
| **Stuck-at fault** | Fault model where a signal is stuck at 0 or 1 |
| **BIST** | Built-In Self-Test - on-chip test generation/checking |
| **Controllability** | Ease of setting internal nodes to desired values |
| **Observability** | Ease of propagating internal values to outputs |

### Scan Chain Basics

```
Normal Mode:    D → [FF] → Q    (functional operation)

Scan Mode:      SI → [FF] → SO   (shift operation)
                     ↑
                    SE (scan enable)
```

A scan flip-flop has:
- **SI** (Scan In): Serial input for test data
- **SE** (Scan Enable): Switches between normal and scan mode
- **SO** (Scan Out): Usually connected to Q, chains to next FF's SI

---

## Exercise 1: Scan Architecture Design (10 min)

### Objective
Use Claude to design a scan chain architecture for a given design.

### Step 1: Analyze Design for Scan

Provide Claude with a design description:

```
I have a digital design with these characteristics:

- 5,000 flip-flops total
- 4 clock domains: clk_core (500MHz), clk_io (100MHz), clk_mem (200MHz), clk_test (50MHz)
- Maximum scan chain length allowed: 200 FFs
- Scan shift frequency: 50 MHz
- Constraints:
  - Keep clock domains separate in scan chains
  - Memory interface FFs should be in dedicated chains

Design a scan architecture that:
1. Determines the number of scan chains needed
2. Assigns FFs to chains by clock domain
3. Estimates total scan shift time
4. Identifies potential issues or recommendations

Save the analysis to scan_architecture.md
```

### Step 2: Generate Scan Insertion Script

```
Generate a TCL script for scan insertion (Synopsys DFT Compiler style) that:

1. Defines scan configuration
2. Sets up clock domains for scan
3. Specifies scan chain count and max length
4. Identifies scan enable and test mode signals
5. Runs DRC and reports results

Include comments explaining each section.
Save to scan_insert.tcl
```

### Step 3: Review and Iterate

```
Review the scan architecture for these concerns:
1. Are there any clock crossing issues during scan shift?
2. What's the total test time for a full scan?
3. Are there any FFs that should NOT be in scan chains?
4. Recommendations for reducing test time?
```

---

## Exercise 2: ATPG and Test Patterns (10 min)

### Objective
Use Claude to understand and analyze ATPG patterns.

> **Note**: Keep things interactive! Ask Claude to explain pattern generation concepts, analyze coverage reports, or suggest improvements.

### Step 1: Understand ATPG Concepts

```
Explain how ATPG works for stuck-at faults:

1. How does a pattern detect a stuck-at-0 fault?
2. What is fault activation and propagation?
3. What makes a fault "undetectable"?
4. Explain ATPG controllability and observability

Use a simple example circuit (AND gate, OR gate, FF) to illustrate.
```

### Step 2: Analyze Coverage Report

We've provided a sample coverage report. Ask Claude to analyze it:

```
Analyze this ATPG coverage report and provide recommendations:

[Contents of sample_atpg_report.txt]

Identify:
1. Overall stuck-at coverage and whether it meets typical targets
2. Categories of undetected faults
3. Most common reasons for low coverage
4. Specific recommendations to improve coverage
```

### Step 3: Create Coverage Analysis Script

```
Write a Python script that parses ATPG coverage reports:

1. Extract coverage numbers by fault type
2. List modules with coverage below threshold
3. Categorize untestable faults by reason
4. Generate a summary with actionable recommendations

Include command-line arguments for:
- Input report file
- Target coverage threshold
- Output format (text, csv, json)

Save to analyze_coverage.py
```

---

## Exercise 3: BIST Implementation (10 min)

### Objective
Use Claude to generate BIST (Built-In Self-Test) components.

### Step 1: Generate an LFSR

```
Generate a Verilog module for a 16-bit LFSR (Linear Feedback Shift Register)
for use in BIST:

Requirements:
- Parameterizable width
- Maximum-length sequence polynomial
- Seed loading capability
- Enable signal for controlled stepping

Include comments explaining:
- The polynomial used and why
- How to calculate the sequence length
- Typical BIST applications

Save to lfsr.v
```

### Step 2: Generate a MISR

```
Generate a Verilog module for a Multiple-Input Signature Register (MISR):

Requirements:
- Parameterizable width (default 32 bits)
- Compresses multiple inputs into a single signature
- Signature comparison output
- Expected signature register

Explain how MISR compaction works and potential aliasing issues.

Save to misr.v
```

### Step 3: Create a Simple BIST Controller

```
Create a simple BIST controller that:

1. Generates patterns using the LFSR
2. Applies patterns to a device under test (DUT)
3. Compresses responses with MISR
4. Compares final signature to expected value
5. Reports pass/fail status

Interface:
- clk, rst_n
- bist_start (input) - starts BIST sequence
- bist_done (output) - BIST complete
- bist_pass (output) - test passed

Parameters:
- PATTERN_COUNT - number of patterns to apply

Save to bist_controller.v
```

### Step 4: Simulate BIST

```
Create a testbench that:
1. Instantiates the BIST controller with a simple DUT (use an ALU or counter)
2. Runs the BIST sequence
3. Verifies pass/fail output
4. Displays pattern count and signature

Save to bist_tb.v and run the simulation.
```

---

## Sample Files

This module includes sample files for exercises:

| File | Description |
|------|-------------|
| `sample_atpg_report.txt` | Sample ATPG coverage report for analysis |
| `scan_rules.txt` | Common DFT design rules |
| `lfsr.v` | Starter LFSR implementation |
| `misr.v` | Starter MISR implementation |

---

## Quick Reference: DFT Concepts

### Scan Flip-Flop Structure

```verilog
// Scan FF behavior
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        q <= 1'b0;
    else if (scan_enable)
        q <= scan_in;    // Scan mode: shift
    else
        q <= d;          // Normal mode: capture
end
assign scan_out = q;
```

### Common LFSR Polynomials

| Width | Polynomial | Max Length |
|-------|------------|------------|
| 8-bit | x⁸ + x⁶ + x⁵ + x⁴ + 1 | 255 |
| 16-bit | x¹⁶ + x¹⁵ + x¹³ + x⁴ + 1 | 65,535 |
| 32-bit | x³² + x²² + x² + x¹ + 1 | 4,294,967,295 |

### DFT Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Stuck-at coverage | % of stuck-at faults detected | > 95% |
| Transition coverage | % of transition faults detected | > 90% |
| Test pattern count | Number of patterns needed | Minimize |
| Scan chain balance | Variation in chain lengths | < 5% |

---

## Advanced Exercises

If you have more time, try these challenging exercises:

### Advanced 1: Compression Architecture

```
Design a test compression architecture:

1. Explain how EDT/DFTMAX compression works
2. Design a simple XOR-based decompressor
3. Design a corresponding compressor for outputs
4. Calculate the compression ratio achieved
5. Discuss trade-offs: compression vs. pattern count

Provide Verilog implementations of decompressor and compressor.
```

### Advanced 2: Memory BIST

```
Design a March-C memory BIST for an SRAM:

1. Explain the March-C algorithm
2. Implement a BIST controller for:
   - 1K x 32 single-port SRAM
   - March-C pattern sequence
   - Address generator
   - Data checker
3. Calculate test time for the memory
4. Discuss fault coverage for stuck-at, coupling, and address decoder faults
```

### Advanced 3: DFT Rule Checker

```
Write a Python script that checks Verilog for common DFT rule violations:

1. Combinational feedback loops
2. Asynchronous set/reset usage
3. Gated clocks without DFT bypass
4. Multi-cycle path flip-flops
5. Tri-state buses

Parse the Verilog, identify violations, and report with file/line numbers.

Save to dft_rule_check.py
```

---

## Prompting Tips for DFT

### What Works Well
- Explaining DFT concepts and architectures
- Generating BIST components (LFSR, MISR, controllers)
- Creating scan insertion scripts
- Analyzing coverage reports (with the Toolmaker pattern)
- Writing DFT rule checkers

### What Requires Caution
- Tool-specific ATPG flows (verify against documentation)
- Compression architectures (proprietary algorithms)
- Fault simulation accuracy (use actual tools)
- Silicon-proven patterns (always validate)

### Effective Context to Include
- Design size (FF count, gate count)
- Clock domains and frequencies
- Target fault coverage
- Test time constraints
- DFT tools being used

---

## Key Takeaways

1. **Scan architecture is plannable** - AI can help design chain assignments
2. **BIST is RTL-based** - LLMs excel at generating LFSR, MISR, controllers
3. **Coverage analysis is data parsing** - use the Toolmaker pattern
4. **DFT rules are checkable** - create scripts to catch issues early
5. **Concepts transfer to tools** - understanding helps with any ATPG tool

---

## Keep Exploring

The exercises above are just starting points. Feel free to:

- **Design BIST for your blocks** - memory BIST, logic BIST, pattern generators
- **Automate coverage analysis** - create scripts for your specific report formats
- **Build DFT linters** - check RTL for DFT rule violations before synthesis
- **Explore at-speed testing** - launch-capture, transition faults
- **Study compression** - how tools like EDT and DFTMAX work

The more you experiment, the better you'll understand how to leverage AI in your DFT workflow.

---

## Share Your Feedback

We'd love to hear about your experience with this module!

- What worked well? What was frustrating?
- What improvements would you like to see in specialized **DFT agents** beyond what Claude Code can do?
- What DFT tasks would benefit most from AI assistance?

**Send your feedback to: hello@aidachip.com**

Your insights will directly shape what we're building next - and we have some exciting launches coming soon that you won't want to miss!

---

## Next Module

Continue your workshop journey:
- [07_STA](../07_STA/) - Static Timing Analysis with AI
- [Back to Workshop Home](../README.md)

---

*Module 06 Complete - You've learned to use GenAI for DFT tasks!*

---

**AIDAChip** - Follow us for more insights on AI-driven chip design automation.
