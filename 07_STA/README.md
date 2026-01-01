# Module 07: Static Timing Analysis (STA) with GenAI

**Duration**: ~30 minutes
**Prerequisites**: Module 00 (LLM Fundamentals), Module 04 (Physical Design) helpful
**Tools Required**: Python for analysis scripts (see [SETUP.md](../SETUP.md))
**Goal**: Learn to use LLMs for timing constraint development, report analysis, and timing closure

> **Note**: This module's exercises are currently being verified. Some steps may require adjustment based on your environment. Please report any issues to hello@aidachip.com.

---

## Overview

This module demonstrates how GenAI can assist with STA tasks including:
- Writing and debugging SDC constraints
- Analyzing timing reports
- Understanding and fixing timing violations
- Clock domain crossing analysis
- Creating timing analysis automation scripts

---

## Tutorial: STA Basics

> **For non-STA engineers**: This section provides essential background to follow the exercises.

### What is Static Timing Analysis?

STA verifies that a design meets timing requirements without simulation:

- **Static**: Analyzes all paths mathematically, not with test vectors
- **Exhaustive**: Checks every timing path in the design
- **Fast**: Much faster than timing simulation

### Timing Path Fundamentals

```
       Launch Edge                    Capture Edge
            │                              │
            ▼                              ▼
    ┌───┐       ┌─────────┐        ┌───┐
────┤FF1├───────┤  Logic  ├────────┤FF2├────
    └───┘       └─────────┘        └───┘

    |←── Data Path Delay ──→|

Setup Check: Data must arrive BEFORE capture edge - setup time
Hold Check:  Data must be stable AFTER capture edge + hold time
```

### Key STA Concepts

| Term | Description |
|------|-------------|
| **Setup time** | Time data must be stable before clock edge |
| **Hold time** | Time data must be stable after clock edge |
| **Slack** | Timing margin (positive = pass, negative = fail) |
| **Critical path** | Path with worst (smallest) slack |
| **Clock skew** | Difference in clock arrival at different FFs |
| **Clock uncertainty** | Jitter + skew budget for timing analysis |
| **False path** | Path that doesn't need timing check |
| **Multicycle path** | Path that takes more than one clock cycle |

### Understanding Slack

```
Setup Slack = Data Required Time - Data Arrival Time

Data Arrival Time = Launch Clock + Clk-to-Q + Logic Delay
Data Required Time = Capture Clock + Clock Period - Setup Time

Positive slack → Timing met (margin available)
Zero slack → Timing exactly met (no margin)
Negative slack → Timing violated (must fix!)
```

---

## Exercise 1: SDC Constraint Development (10 min)

### Objective
Use Claude to develop and debug SDC constraints.

### Step 1: Create Constraints from Spec

We've provided a sample design spec. Ask Claude to generate SDC:

```
Based on the design specification in design_spec.md, create a complete
SDC file that includes:

1. All clock definitions with proper source latency
2. Generated clocks for any divided clocks
3. Clock groups for asynchronous domains
4. Clock uncertainty for different corners
5. Input and output delays for all ports
6. False paths where appropriate
7. Multicycle paths as specified

Follow best practices:
- Use meaningful constraint names
- Add comments explaining each section
- Group related constraints together

Save to constraints.sdc
```

### Step 2: SDC Lint Check

```
Review constraints.sdc for common SDC problems:

1. Missing constraints (unconstrained paths)
2. Over-constraints (unnecessarily tight)
3. Conflicting constraints
4. Clock domain crossing issues
5. Incorrect false paths

Provide a report of issues and fixes.
```

### Step 3: Debug a Constraint Issue

```
I'm seeing unexpected timing violations on paths between clk_a and clk_b,
even though I set them as false paths. Here's my constraint:

set_false_path -from clk_a -to clk_b

What's wrong? How should I fix it?
```

---

## Exercise 2: Timing Report Analysis (10 min)

### Objective
Use Claude to analyze timing reports and develop fix strategies.

> **Best Practice**: Use the Toolmaker pattern - ask Claude to write Python scripts for analyzing timing reports rather than parsing them directly.

### Step 1: Create a Timing Report Parser

We've provided a sample timing report. First, create a reusable parser:

```
Write a Python script to parse timing reports (PrimeTime format):

The script should:
1. Parse the timing report from sample_timing_report.txt
2. Extract path information:
   - Startpoint and endpoint
   - Path group
   - Slack value
   - Critical cells in path
3. Group violations by:
   - Clock domain
   - Path type (setup/hold)
   - Slack severity
4. Generate summary statistics
5. Output to CSV for spreadsheet analysis

Include command-line arguments for flexibility.
Save to parse_timing.py
```

### Step 2: Run the Parser

```
Run parse_timing.py on sample_timing_report.txt and show me:
1. Total number of violations
2. Worst 10 paths
3. Summary by clock domain
```

### Step 3: Develop Fix Strategies

Based on the parsed results:

```
For these timing violations:
[Paste summary from parser output]

Analyze each category and provide:
1. Root cause analysis
2. Specific fix recommendations
3. Priority order for fixes
4. Estimated effort and risk level

Consider both SDC and physical design fixes.
```

---

## Exercise 3: Clock Domain Crossing (10 min)

### Objective
Use Claude to understand and constrain clock domain crossings.

### Step 1: CDC Analysis

```
I have a design with these clock domains:

- clk_sys: 500 MHz system clock (main logic)
- clk_io: 100 MHz I/O clock (external interface)
- clk_mem: 333 MHz memory clock (DDR interface)
- clk_cpu: 1 GHz CPU clock (derived from PLL)

Domain relationships:
- clk_sys and clk_cpu are synchronous (common source PLL)
- clk_io is asynchronous to all others
- clk_mem is asynchronous but has fixed phase relationship to clk_sys

Explain:
1. Which crossings need special handling?
2. What synchronizer structures are appropriate?
3. How should I constrain each crossing type?
4. What are the potential metastability risks?
```

### Step 2: Generate CDC Constraints

```
Generate SDC constraints for the clock domains described above:

1. Clock definitions with realistic parameters
2. Clock groups (async vs sync relationships)
3. set_false_path or set_max_delay for CDC paths
4. Proper constraints for synchronizer chains
5. Comments explaining CDC timing requirements

Save to cdc_constraints.sdc
```

### Step 3: CDC Verification Script

```
Write a Python script that helps verify CDC handling:

1. Parse a timing report
2. Identify paths crossing between specified clock domains
3. Check that each CDC path has proper constraints
4. Flag any unconstrained CDC paths
5. Report synchronizer depth on CDC paths

Save to cdc_check.py
```

---

## Sample Files

This module includes sample files for exercises:

| File | Description |
|------|-------------|
| `design_spec.md` | Sample design specification for SDC exercise |
| `sample_timing_report.txt` | Sample timing report with violations |
| `cdc_constraints.sdc` | Example CDC constraint file |
| `parse_timing.py` | Starter timing parser script |

---

## Quick Reference: SDC Syntax

### Clock Definition

```tcl
# Primary clock
create_clock -name clk_sys -period 2.0 [get_ports clk]

# Clock with source latency
create_clock -name clk_sys -period 2.0 \
    -waveform {0 1.0} [get_ports clk]
set_clock_latency -source -max 0.3 [get_clocks clk_sys]
set_clock_latency -source -min 0.1 [get_clocks clk_sys]

# Generated clock (divide by 2)
create_generated_clock -name clk_div2 \
    -source [get_ports clk] \
    -divide_by 2 \
    [get_pins divider/clk_out]
```

### Timing Exceptions

```tcl
# False path - paths that don't need timing
set_false_path -from [get_clocks clk_a] -to [get_clocks clk_b]
set_false_path -through [get_pins mux/sel]

# Multicycle path - paths taking multiple cycles
set_multicycle_path 2 -setup -from [get_cells cfg_reg*]
set_multicycle_path 1 -hold  -from [get_cells cfg_reg*]

# Max delay (for CDC)
set_max_delay 2.0 -from [get_cells sync_reg1] -to [get_cells sync_reg2]
```

### Clock Relationships

```tcl
# Asynchronous clocks
set_clock_groups -asynchronous \
    -group [get_clocks clk_sys] \
    -group [get_clocks clk_io]

# Exclusive clocks (never active together)
set_clock_groups -logically_exclusive \
    -group [get_clocks clk_test] \
    -group [get_clocks clk_func]
```

### Slack Calculation

```
SETUP CHECK:
  Slack = (Capture_Clock + Period - Setup) - (Launch_Clock + Data_Path)

HOLD CHECK:
  Slack = (Launch_Clock + Data_Path) - (Capture_Clock + Hold)

For positive slack: PASS (timing met with margin)
For negative slack: FAIL (timing violated)
```

---

## Advanced Exercises

If you have more time, try these challenging exercises:

### Advanced 1: Multi-Corner Multi-Mode Analysis

```
Set up MCMM (Multi-Corner Multi-Mode) analysis:

Corners:
- ss_0p9v_125c (slow, setup-critical)
- ff_1p1v_m40c (fast, hold-critical)
- tt_1p0v_25c (nominal)

Modes:
- functional (normal operation)
- scan_shift (test mode at 100MHz)
- sleep (low power, minimal switching)

Create:
1. Library setup for each corner
2. SDC files for each mode
3. Analysis configuration file
4. Script to run all scenarios and merge results

Save to mcmm_setup/
```

### Advanced 2: Timing ECO Script

```
Write a Python script that:

1. Parses timing violations
2. Analyzes each violation for fix type:
   - Buffer insertion candidates
   - Cell sizing opportunities
   - Path restructuring needs
3. Generates ECO commands for common tools:
   - Innovus format
   - ICC2 format
4. Estimates timing improvement per fix
5. Prioritizes fixes by impact and risk

Save to timing_eco.py
```

### Advanced 3: Timing Correlation Analyzer

```
Write a script to analyze timing correlation:

1. Compare timing reports from two stages (e.g., synthesis vs P&R)
2. Identify paths with significant delta
3. Categorize differences:
   - Clock tree differences
   - Cell delay differences
   - Wire delay differences
4. Flag paths that were passing and are now failing
5. Generate correlation report

Save to timing_correlation.py
```

---

## Prompting Tips for STA

### What Works Well
- Generating SDC constraints from specifications
- Creating timing report parsers
- Explaining timing concepts and calculations
- Developing CDC constraint strategies
- Writing timing analysis automation

### What Requires Caution
- Exact delay values (library and tool dependent)
- Tool-specific report formats
- Clock tree analysis (needs actual data)
- Sign-off corner selection (process dependent)

### Effective Context to Include
- Target frequency and clock structure
- Technology node and corners
- Timing tool being used
- Specific path or violation details
- Design constraints and requirements

---

## Key Takeaways

1. **SDC generation is automatable** - constraints from specs
2. **Report parsing should be scripted** - use the Toolmaker pattern
3. **CDC requires careful constraints** - AI helps understand requirements
4. **Fix strategies are systematic** - categorize, prioritize, verify
5. **Correlation is essential** - track timing across flow stages

---

## Keep Exploring

The exercises above are just starting points. Feel free to:

- **Create custom parsers** - adapt to your tool's report format
- **Build timing dashboards** - visualize timing status across runs
- **Automate ECO generation** - script common timing fixes
- **Develop correlation flows** - track timing throughout your flow
- **Explore SI analysis** - signal integrity effects on timing

The more you experiment, the better you'll understand how to leverage AI in your STA workflow.

---

## Share Your Feedback

We'd love to hear about your experience with this module!

- What worked well? What was frustrating?
- What improvements would you like to see in specialized **STA agents** beyond what Claude Code can do?
- What timing analysis tasks would benefit most from AI assistance?

**Send your feedback to: hello@aidachip.com**

Your insights will directly shape what we're building next - and we have some exciting launches coming soon that you won't want to miss!

---

## Next Module

Continue your workshop journey:
- [08_Documentation](../08_Documentation/) - Technical documentation with AI
- [Back to Workshop Home](../README.md)

---

*Module 07 Complete - You've learned to use GenAI for STA tasks!*

---

**AIDAChip** - Follow us for more insights on AI-driven chip design automation.
