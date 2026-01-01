# Module 01: Circuit Design with GenAI

**Duration**: ~30 minutes
**Prerequisites**: Module 00 (LLM Fundamentals)
**Tools Required**: ngspice (see [SETUP.md](../SETUP.md))
**Goal**: Learn to use LLMs for analog/mixed-signal circuit design tasks

---

## Overview

This module demonstrates how GenAI can assist with circuit design tasks including:
- Generating SPICE netlists
- Circuit analysis and explanation
- Design review and optimization
- Component sizing and calculations

---

## Tutorial: Circuit Design Basics

> **For non-circuit designers**: This section provides essential background to follow the exercises.

### What is SPICE?

SPICE (Simulation Program with Integrated Circuit Emphasis) is the industry-standard tool for simulating analog circuits. A SPICE netlist describes:

- **Components**: Resistors (R), Capacitors (C), Inductors (L), Transistors (M/Q), Voltage/Current sources (V/I)
- **Nodes**: Connection points between components
- **Analysis types**: DC operating point, AC frequency response, Transient time-domain

### Basic Netlist Structure

```spice
* Title line (comment)
* Component definitions: Name Node1 Node2 Value
R1 in out 1k
C1 out gnd 1p
V1 in gnd DC 1.8

* Analysis commands
.op
.tran 1n 100n
.ac dec 10 1 1G

.end
```

### Key Circuit Concepts

| Term | Description |
|------|-------------|
| **Bias point** | DC operating voltages/currents |
| **Gain** | Output/Input signal ratio |
| **Bandwidth** | Frequency range of operation |
| **Slew rate** | Maximum rate of output change |

---

## Exercise 1: Generate a SPICE Netlist (10 min)

### Objective
Use Claude to generate a complete SPICE netlist for an RC low-pass filter.

### Step 1: Generate and Save

Try this prompt with Claude Code:

```
Generate an ngspice netlist for a simple RC low-pass filter with:
- Cutoff frequency: 1 MHz
- Input: 1V AC source
- Include AC analysis from 100 Hz to 100 MHz

Calculate the required R and C values and explain your choices.

Save the netlist to rc_filter.sp
```

### Step 2: Run the Simulation

You can run the simulation yourself:

```bash
ngspice rc_filter.sp
```

In ngspice, type:
```
plot vdb(out)
```

**Or**, ask Claude Code to run it for you:

```
Run the ngspice simulation on rc_filter.sp and show me the results
```

> **Tip**: Simulation and plotting may not work perfectly on the first try depending on your setup. This is part of the learning experience! Observe the output and chat with Claude Code to troubleshoot. For example:
> - If plotting fails, ask Claude to plot the results using Python/matplotlib instead
> - If ngspice can't find gnuplot, you can install it (`brew install gnuplot` on macOS) or use the Python plotting approach
> - Share any errors with Claude Code and ask it to help resolve them
>
> This iterative problem-solving is a key skill when working with AI assistants.

### Step 3: Iterate

If the simulation doesn't work or results aren't as expected, share the error or output with Claude:

```
I ran your netlist and got this error:
[paste error]

Please fix the netlist.
```

### Reflection Questions
- Did Claude calculate R and C values correctly?
- Did the frequency response match the expected -3dB point at 1 MHz?
- What would you change to make the filter sharper?

---

## Exercise 2: Circuit Analysis (10 min)

### Objective
Use Claude to analyze and explain an existing circuit.

> **Note**: Keep things interactive! Feel free to ask Claude Code to save and simulate the netlist at any point. Claude Code may also proactively suggest ways to help - such as running simulations, plotting results, or modifying the circuit. Follow along with its suggestions to explore the workflow.

### Step 1: Present a Circuit

Give Claude this common-source amplifier netlist:

```
Analyze this MOSFET common-source amplifier:

* Common Source Amplifier
.include 'nmos.mod'

Vdd vdd gnd 1.8
Vin in gnd DC 0.6 AC 1

M1 out in gnd gnd nmos W=2u L=180n
Rd vdd out 5k

.op
.ac dec 20 1 1G

.end

Explain:
1. How does this circuit amplify signals?
2. What determines the gain?
3. What are the limitations of this topology?
4. Suggest improvements for better performance.
```

### Step 2: Follow-Up Questions

Ask deeper questions based on the response:

```
For the common-source amplifier:
1. How would I increase the gain without changing the supply voltage?
2. What's the trade-off between gain and bandwidth?
3. How do I calculate the output impedance?
```

### Step 3: Request Modifications

```
Modify the common-source amplifier to:
1. Add a source degeneration resistor for linearity
2. Explain how this affects gain and distortion
3. Provide the updated netlist
```

---

## Exercise 3: Design from Specifications (10 min)

### Objective
Use Claude to design a circuit from high-level specifications.

### The Task

```
Design a two-stage RC low-pass filter in ngspice with these specifications:
- Overall -3dB cutoff: approximately 10 kHz
- Attenuation at 100 kHz: at least -30 dB
- Input impedance: > 10 kΩ
- Use standard component values (E24 series)

Provide:
1. Circuit topology explanation
2. Component value calculations
3. Complete ngspice netlist
4. Expected frequency response

Save the netlist to two_stage_filter.sp
```

### Verify the Design

Run the generated netlist:

```bash
ngspice two_stage_filter.sp
```

Check:
- Does the -3dB point match the spec?
- Is the 100 kHz attenuation sufficient?

### Iterate if Needed

```
The simulation shows -3dB at 8 kHz instead of 10 kHz.
Adjust the component values to meet the spec.
```

---

## Quick Reference: ngspice Commands

| Command | Description |
|---------|-------------|
| `ngspice file.sp` | Run simulation |
| `plot v(node)` | Plot voltage at node |
| `plot vdb(node)` | Plot voltage in dB |
| `plot v(a)-v(b)` | Plot differential voltage |
| `print all` | Print all node voltages |
| `quit` | Exit ngspice |

### Analysis Types

| Analysis | Purpose | Example |
|----------|---------|---------|
| `.op` | DC operating point | `.op` |
| `.dc` | DC sweep | `.dc Vin 0 1.8 0.1` |
| `.ac` | Frequency response | `.ac dec 20 1 1G` |
| `.tran` | Time domain | `.tran 1n 100n` |

---

## Advanced Exercises

If you have more time, try these challenging exercises:

### Advanced 1: Op-Amp Design

```
Design a simple two-stage CMOS operational amplifier with:
- Open-loop gain > 60 dB
- Unity-gain bandwidth > 5 MHz
- Phase margin > 60°
- Supply: 1.8V
- Load: 5pF

Use a simple MOSFET model for 180nm technology.
Provide the complete ngspice netlist and explain each stage.
```

### Advanced 2: Circuit Debugging

```
This circuit isn't working as expected:

* Intended: Voltage buffer
M1 out in vdd vdd pmos W=10u L=180n
M2 out in gnd gnd nmos W=5u L=180n

Vin in gnd DC 0.9
Vdd vdd gnd 1.8

.op
.end

The output should follow the input, but simulation shows
out = 1.8V regardless of input. Debug this circuit.
```

### Advanced 3: Optimization

```
I have this bandgap reference circuit that generates 1.15V.
I need to reduce its temperature coefficient.

[paste circuit]

Suggest modifications to improve temperature stability
and explain the underlying physics.
```

---

## Prompting Tips for Circuit Design

### What Works Well
- Asking for explanations of circuit behavior
- Generating netlists from specifications
- Getting design equations and calculations
- Reviewing circuits for issues
- Suggesting topology alternatives

### What Requires Caution
- Exact component values (verify with simulation)
- Process-specific parameters (use actual PDK values)
- Performance claims (always simulate to verify)
- Complex optimization (better done with tools)

### Effective Context to Include
- Technology node and supply voltage
- Performance specifications
- Constraints (area, power, etc.)
- What you've already tried

---

## Key Takeaways

1. **LLMs excel at generating starter netlists** - but always simulate to verify
2. **Explanations are valuable** - use Claude to understand circuit behavior
3. **Iterate based on simulation results** - share actual errors/output for debugging
4. **Verify all calculations** - especially for critical specifications
5. **Context improves results** - include technology, specs, and constraints

---

## Keep Exploring

The exercises above are just starting points. Feel free to:

- **Tweak the prompts** to design circuits of your own choice
- **Explore other topologies** - ask Claude about different amplifier configurations, filter types, or reference circuits
- **Generate testbenches** - ask Claude Code to create comprehensive testbenches for your circuits, including corner cases and parametric sweeps

The more you experiment, the better you'll understand how to leverage AI in your circuit design workflow.

---

## Share Your Feedback

We'd love to hear about your experience with this module!

- What worked well? What was frustrating?
- What improvements would you like to see in specialized **Circuit Design agents** beyond what Claude Code can do?
- What circuit design tasks would benefit most from AI assistance?

**Send your feedback to: hello@aidachip.com**

Your insights will directly shape what we're building next - and we have some exciting launches coming soon that you won't want to miss!

---

## Next Module

Continue your workshop journey:
- [02_RTL_Development](../02_RTL_Development/) - Verilog/SystemVerilog with AI
- [Back to Workshop Home](../README.md)

---

*Module 01 Complete - You've learned to use GenAI for circuit design tasks!*

---

**AIDAChip** - Follow us for more insights on AI-driven chip design automation.
