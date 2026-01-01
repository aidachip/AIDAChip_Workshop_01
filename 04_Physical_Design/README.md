# Module 04: Physical Design with GenAI

**Duration**: ~30 minutes
**Prerequisites**: Module 00 (LLM Fundamentals), basic understanding of digital design helpful
**Tools Required**: Yosys (synthesis), OpenROAD (P&R) - see [SETUP.md](../SETUP.md), Python for analysis scripts
**Goal**: Learn to use LLMs for floorplanning, constraints, timing closure, and PD automation

---

## Overview

This module demonstrates how GenAI can assist with physical design tasks including:
- Generating SDC timing constraints
- Creating floorplan strategies and scripts
- Analyzing and interpreting timing reports
- Writing TCL scripts for PD automation
- Power intent specification (UPF basics)
- Debugging timing and congestion issues

---

## Tutorial: Physical Design Basics

> **For non-PD engineers**: This section provides essential background to follow the exercises.

### What is Physical Design?

Physical Design (PD) transforms an RTL netlist into a manufacturable layout. The main stages are:

```
Synthesis → Floorplanning → Placement → CTS → Routing → Signoff
```

- **Synthesis**: Convert RTL to gate-level netlist
- **Floorplanning**: Define chip/block dimensions, place macros, create power grid
- **Placement**: Position standard cells
- **CTS (Clock Tree Synthesis)**: Build balanced clock distribution network
- **Routing**: Connect all signals with metal wires
- **Signoff**: Final verification (timing, DRC, LVS, power)

### Key PD Concepts

| Term | Description |
|------|-------------|
| **SDC** | Synopsys Design Constraints - timing constraints file format |
| **Floorplan** | Physical arrangement of blocks, macros, and IO |
| **Utilization** | Percentage of area used by cells (typically 60-80%) |
| **Clock tree** | Network distributing clock with balanced delays |
| **Setup time** | Data must be stable before clock edge |
| **Hold time** | Data must be stable after clock edge |
| **Slack** | Timing margin (positive = passing, negative = violation) |
| **Congestion** | Routing resource shortage in an area |

### SDC Basics

```tcl
# Define clocks
create_clock -name clk -period 2.0 [get_ports clk]

# Input/output delays
set_input_delay -clock clk -max 0.5 [get_ports data_in]
set_output_delay -clock clk -max 0.3 [get_ports data_out]

# False paths and multicycle paths
set_false_path -from [get_clocks clk_a] -to [get_clocks clk_b]
set_multicycle_path 2 -setup -from [get_pins reg_a/Q] -to [get_pins reg_b/D]
```

---

## Exercise 1: Generate SDC Constraints (10 min)

### Objective
Use Claude to generate timing constraints from a design specification.

### Step 1: Describe Your Design

Provide Claude with a design specification:

```
I have a digital design with the following characteristics:

Clocks:
- Main clock: 500 MHz (2ns period), input port "clk"
- Slow clock: 100 MHz (10ns period), input port "clk_slow"
- The clocks are asynchronous to each other

Interfaces:
- Input bus "data_in[31:0]" synchronized to clk, arrives 0.3ns after clock edge
- Output bus "data_out[31:0]" synchronized to clk, must be valid 0.4ns before capture
- SPI interface on clk_slow domain: spi_clk, spi_mosi, spi_miso, spi_cs_n

Special paths:
- Configuration registers (cfg_*) are written once at startup, can be multicycle (3 cycles)
- Reset "rst_n" is asynchronous

Generate a complete SDC file with:
1. Clock definitions with realistic source latency and jitter
2. Clock groups for async domains
3. Input/output delays for all interfaces
4. False paths for reset
5. Multicycle paths for config registers
6. Comments explaining each constraint

Save to design.sdc
```

### Step 2: Review and Refine

Ask Claude to explain the constraints:

```
Explain each constraint in design.sdc and why it's needed.
Are there any potential issues or missing constraints?
```

### Step 3: Add Clock Domain Crossing Constraints

```
Add constraints for safe clock domain crossing between clk and clk_slow:
- Assume we use a 2-FF synchronizer
- Add appropriate set_max_delay or set_false_path constraints
- Explain the timing implications

Update design.sdc with these additions.
```

> **Tip**: SDC syntax is highly standardized across tools. Constraints generated here will work with Synopsys, Cadence, Siemens, and OpenROAD with minimal modifications.

---

## Exercise 2: Floorplan and Run OpenROAD (10 min)

### Objective
Use Claude to plan a floorplan, generate scripts, and run them in OpenROAD.

> **Note**: Keep things interactive! Ask Claude Code to generate scripts, run OpenROAD commands, and help you iterate on the results.

### Prerequisites: Synthesis Before Physical Design

OpenROAD requires a **synthesized gate-level netlist** - it cannot work directly from RTL. The typical open-source flow is:

```
RTL (Verilog) → Yosys (Synthesis) → Netlist → OpenROAD (Floorplan → Place → CTS → Route)
```

First, let's set up a working environment. Ask Claude:

```
Help me set up a complete OpenROAD flow from RTL:

1. Create a minimal Verilog design (simple counter or ALU)
2. Create a Yosys synthesis script that:
   - Reads the Verilog
   - Synthesizes to a target library (use Nangate45 or Sky130)
   - Outputs a gate-level netlist for OpenROAD
3. Show me how to obtain the necessary PDK files (LEF/LIB)
4. Create a basic OpenROAD script that reads the netlist
5. Show me how to run both Yosys and OpenROAD

Save all files to a pd_workshop/ directory.
```

> **Tip**: If full setup is complex, Claude can help you use OpenROAD-flow-scripts or the built-in test designs. Alternatively, you can focus on script generation and concepts, then run them on your own environment.

### Step 1: Describe Your Block

```
I'm floorplanning a block with these characteristics:

Die/Block size: 2mm x 2mm
Target utilization: 70%

Macros:
- 2x SRAM blocks (256KB each): ~0.4mm x 0.3mm each
- 1x PLL: 0.15mm x 0.15mm
- 1x ADC: 0.2mm x 0.1mm

IO requirements:
- North edge: 64 data IOs
- South edge: Power/ground, 32 control IOs
- East edge: High-speed SerDes (sensitive to routing)
- West edge: Analog signals for ADC (need guard ring)

Critical paths:
- SRAM to datapath logic (timing critical)
- PLL to clock distribution (minimize skew)

Provide:
1. A floorplan strategy with macro placement recommendations
2. Rationale for each placement decision
3. Potential congestion hotspots to watch
4. Power grid considerations
```

### Step 2: Generate Floorplan Script

```
Generate an OpenROAD TCL script that implements this floorplan:
1. Initialize the floorplan with the given dimensions
2. Place macros according to your recommendations
3. Create placement blockages around macros with appropriate halos
4. Add placement guides for critical logic near SRAMs

Save to floorplan.tcl
```

### Step 3: Run in OpenROAD

Ask Claude Code to run the script:

```
Run the floorplan.tcl script in OpenROAD and show me the results.
If using Docker: docker run -it -v $(pwd):/work openroad/openroad
Then source the script and display the floorplan.
```

Or manually:

```bash
# Direct install
openroad -gui
source floorplan.tcl

# Or via Docker
docker run -it -v $(pwd):/work openroad/openroad openroad -gui /work/floorplan.tcl
```

> **Tip**: OpenROAD's GUI can display the floorplan visually. Use `gui::show` in the TCL script or run with `-gui` flag. If running headless, ask Claude to add commands that report macro locations and utilization statistics.

### Step 4: Iterate on Placement

```
The SRAMs have high pin density on their east side.
How should I adjust the placement to avoid routing congestion
between the two SRAMs?

Update the floorplan script, run it in OpenROAD, and show me the
utilization and placement report.
```

---

## Exercise 3: Timing Report Analysis (10 min)

### Objective
Use Claude to analyze timing reports and create reusable analysis tools.

> **Best Practice**: When analyzing structured files like timing reports, logs, or synthesis reports, ask Claude to **write a Python script** rather than parsing the content directly. This approach is:
> - **Repeatable**: Run the same script on any timing report
> - **Robust**: Code handles edge cases consistently
> - **Scalable**: Works on large files without LLM context limits
> - **Auditable**: You can review, modify, and version control the script

### Step 1: Understand a Timing Report

First, let's understand what we're looking at. Ask Claude to explain:

```
Analyze this timing report and identify the issues:

Startpoint: input_reg/Q (rising edge-triggered flip-flop clocked by clk)
Endpoint: output_reg/D (rising edge-triggered flip-flop clocked by clk)
Path Group: clk
Path Type: max

Point                                    Incr       Path
-----------------------------------------------------------
clock clk (rise edge)                   0.000      0.000
clock network delay (ideal)             0.100      0.100
input_reg/Q (CK->Q)                     0.150      0.250
u_mult/A[0] (input)                     0.020      0.270
u_mult/Z[31] (output)                   1.450      1.720
u_add/A[31] (input)                     0.030      1.750
u_add/Z[31] (output)                    0.280      2.030
output_reg/D (D)                        0.015      2.045
data arrival time                                  2.045

clock clk (rise edge)                   2.000      2.000
clock network delay (ideal)             0.100      2.100
clock uncertainty                      -0.050      2.050
output_reg/D (D)
library setup time                     -0.040      2.010
data required time                                 2.010
-----------------------------------------------------------
slack (VIOLATED)                                  -0.035

Explain:
1. What is causing this timing violation?
2. What are my options to fix it?
3. Which fix would you recommend and why?
```

### Step 2: Generate Fix Strategies

```
For the timing violation above, generate:

1. SDC changes that might help (if any)
2. Synthesis directives to consider
3. Physical design techniques (placement, routing priority)
4. A prioritized action plan

Consider that we're late in the project and want minimal risk changes.
```

### Step 3: Create a Reusable Timing Analysis Script

Now, instead of having Claude parse reports directly each time, create a reusable tool:

```
Write a Python script that I can use repeatedly to analyze timing reports:

1. Parses a timing report file (assume Synopsys PrimeTime format)
2. Extracts all violating paths
3. Groups violations by endpoint clock
4. Calculates statistics (worst slack, total negative slack, # violations)
5. Identifies common cells in critical paths (potential optimization targets)
6. Outputs a summary report

Include command-line arguments for:
- Input file path
- Output format (text, csv, json)
- Slack threshold filter

Save to analyze_timing.py
```

### Step 4: Run the Script

```
Run analyze_timing.py on a sample timing report and show me the results.
If we don't have a real report, generate a sample timing report file first.
```

This script now becomes part of your toolkit - run it on any project, any number of times, with consistent results.

---

## Quick Reference: SDC Commands

### Clock Definition

```tcl
# Basic clock
create_clock -name clk -period 10.0 [get_ports clk]

# Generated clock (divided)
create_generated_clock -name clk_div2 -source [get_ports clk] \
    -divide_by 2 [get_pins divider/Q]

# Clock with jitter/uncertainty
set_clock_uncertainty -setup 0.1 [get_clocks clk]
set_clock_latency -source 0.2 [get_clocks clk]
```

### Timing Exceptions

```tcl
# False path
set_false_path -from [get_clocks clkA] -to [get_clocks clkB]

# Multicycle path
set_multicycle_path 2 -setup -from [get_cells cfg_reg*]
set_multicycle_path 1 -hold -from [get_cells cfg_reg*]

# Max delay (for CDC)
set_max_delay 1.5 -from [get_cells sync_reg1] -to [get_cells sync_reg2]
```

### I/O Constraints

```tcl
# Input delay
set_input_delay -clock clk -max 0.5 [get_ports data_in*]
set_input_delay -clock clk -min 0.1 [get_ports data_in*]

# Output delay
set_output_delay -clock clk -max 0.4 [get_ports data_out*]

# Driving cell and load
set_driving_cell -lib_cell BUF_X4 [get_ports data_in*]
set_load 0.05 [get_ports data_out*]
```

### OpenROAD Commands

```tcl
# Floorplan initialization
initialize_floorplan -die_area {0 0 2000 2000} \
    -core_area {50 50 1950 1950} -site FreePDK45_38x28_10R_NP_162NW_34O

# Macro placement
place_cell -inst_name sram_0 -origin {100 100} -orient R0

# Placement
global_placement -density 0.7
detailed_placement

# Clock tree synthesis
clock_tree_synthesis -root_buf CLKBUF_X3 -buf_list {CLKBUF_X2 CLKBUF_X3}

# Routing
global_route -guide_file route.guide
detailed_route

# Reports
report_design_area
report_timing -path_delay max -max_paths 10
report_power
```

### Running OpenROAD

```bash
# Interactive mode
openroad

# With GUI
openroad -gui

# Run script
openroad -exit script.tcl

# Via Docker
docker run -it -v $(pwd):/work openroad/openroad openroad /work/script.tcl
```

---

## Advanced Exercises

If you have more time, try these challenging exercises:

### Advanced 1: Power Intent (UPF)

```
Create a UPF (Unified Power Format) file for a design with:
- Always-on domain (AON) for critical control logic
- Switchable domain (PD1) for main datapath, can be powered down
- Retention registers in PD1 that preserve state during power-down
- Level shifters between domains
- Isolation cells at domain boundaries

Explain each construct and its purpose.
Save to power_intent.upf
```

### Advanced 2: Congestion Analysis and Fixes

```
I'm seeing routing congestion in my design with these symptoms:
- DRC violations concentrated in the center of the block
- 15% of GCells showing >90% utilization
- Timing degradation after detailed routing
- Long detours on critical nets

My current utilization is 75% with 3 large macros.

Provide:
1. Diagnostic questions to narrow down the root cause
2. Floorplan adjustments to consider
3. Placement strategies to reduce congestion
4. Routing options (NDR, shielding, layer assignment)
5. A systematic approach to debug and fix
```

### Advanced 3: Multi-Mode Multi-Corner (MMMC)

```
Set up an MMMC analysis for a design that must work across:

Modes:
- Functional mode (normal operation)
- Test mode (scan shift at reduced frequency)
- Sleep mode (retention, minimal switching)

Corners:
- SS/0.9V/-40C (slow, setup critical)
- FF/1.1V/125C (fast, hold critical)
- TT/1.0V/25C (nominal)

Generate:
1. SDC files for each mode (func.sdc, test.sdc, sleep.sdc)
2. A library setup script that defines all corners
3. An analysis configuration that checks setup at slow corner and hold at fast corner
```

### Advanced 4: ECO Script Generation

```
I need to make an ECO (Engineering Change Order) to fix a timing violation.

The fix requires:
1. Upsize cell u_buffer_1 from BUF_X1 to BUF_X4
2. Add a buffer (BUF_X2) on net net_critical between u_and/Z and u_reg/D
3. Swap cell u_mux from MUX2_X1 to MUX2_X2

Generate TCL scripts for:
1. Innovus ECO commands
2. ICC2 ECO commands
3. OpenROAD ECO commands

Include before/after timing checks.
```

---

## Prompting Tips for Physical Design

### What Works Well
- Generating SDC constraints from specifications
- Creating TCL scripts for PD flows
- Analyzing and explaining timing reports
- Suggesting floorplan strategies
- Writing utility scripts for report parsing
- Explaining PD concepts and trade-offs

### What Requires Caution
- Exact timing numbers (tool and library dependent)
- Congestion predictions (need actual design data)
- Power grid design (IR drop is complex)
- Antenna and electromigration rules (process specific)

### Effective Context to Include
- Target frequency and clock structure
- Technology node (affects constraints)
- Tool being used (syntax variations)
- Design size and macro count
- Known problem areas or constraints

---

## Key Takeaways

1. **SDC generation is highly automatable** - describe your design, get constraints
2. **Timing reports are ideal for AI analysis** - pattern recognition at scale
3. **Floorplanning benefits from experience** - AI can suggest strategies based on common patterns
4. **Scripts save significant time** - TCL and Python automation for repetitive tasks
5. **Context matters enormously** - always specify your tool, node, and constraints

---

## Keep Exploring

The exercises above are just starting points. Feel free to:

- **Generate constraints for your own designs** - describe your clock architecture and interfaces
- **Create timing report parsers** - automate your timing closure debug flow
- **Build floorplan templates** - ask Claude to create reusable scripts for common block types
- **Explore power optimization** - ask about clock gating, multi-Vt strategies, and power grid design
- **Automate ECO flows** - generate scripts for common late-stage fixes

The more you experiment, the better you'll understand how to leverage AI in your physical design workflow.

---

## Share Your Feedback

We'd love to hear about your experience with this module!

- What worked well? What was frustrating?
- What improvements would you like to see in specialized **Physical Design agents** beyond what Claude Code can do?
- What PD tasks would benefit most from AI assistance?

**Send your feedback to: hello@aidachip.com**

Your insights will directly shape what we're building next - and we have some exciting launches coming soon that you won't want to miss!

---

## Next Module

Continue your workshop journey:
- [05_Layout](../05_Layout/) - Layout generation and DRC/LVS with AI
- [07_STA](../07_STA/) - Deep dive into Static Timing Analysis
- [Back to Workshop Home](../README.md)

---

*Module 04 Complete - You've learned to use GenAI for physical design tasks!*

---

**AIDAChip** - Follow us for more insights on AI-driven chip design automation.
