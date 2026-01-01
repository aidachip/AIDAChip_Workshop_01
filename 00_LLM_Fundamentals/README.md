# Module 00: LLM Fundamentals for Silicon Engineers

**Duration**: ~30 minutes
**Prerequisites**: None
**Goal**: Understand how LLMs work and learn effective prompting strategies for technical work

---

## Overview

Before diving into domain-specific applications, it's essential to understand what Large Language Models (LLMs) are, how they work, and what they're good (and not good) at. This module provides that foundation.

## What You'll Learn

1. How LLMs work (at a useful level of abstraction)
2. Effective prompting strategies for technical tasks
3. Common pitfalls and limitations
4. How to evaluate and iterate on AI-generated output

---

## Part 1: Understanding LLMs

### What is an LLM?

A Large Language Model is a neural network trained on vast amounts of text to predict the next token (word or sub-word) in a sequence. Through this training, LLMs develop:

- **Pattern recognition**: Understanding syntax, semantics, and structure
- **Knowledge compression**: Encoding facts, concepts, and relationships
- **Reasoning capabilities**: Following logical steps and making inferences

### Key Insight for Engineers

Think of an LLM as a highly capable **pattern matcher and synthesizer** that has "read" most publicly available technical documentation, code, papers, and discussions. It can:

- Recognize patterns in your input and generate contextually appropriate output
- Synthesize information from multiple sources
- Transform between representations (natural language ↔ code ↔ structured data)

### What LLMs Are NOT

- **Not a database**: They don't "look up" facts; they generate based on patterns
- **Not deterministic**: Same input can produce different outputs
- **Not a calculator**: They estimate numerical results, don't compute them
- **Not always current**: Knowledge has a training cutoff date

### Claude Code vs. Traditional Chat Interfaces

This workshop uses **Claude Code**, which is fundamentally different from typical LLM chat applications (like ChatGPT, Claude.ai, or Gemini web interfaces).

| Aspect | Traditional Chat Interface | Claude Code |
|--------|---------------------------|-------------|
| **Interaction** | You send messages, receive text responses | AI takes actions in your environment |
| **File Access** | Copy/paste code manually | Reads and writes files directly |
| **Commands** | Copy commands, run them yourself | Executes commands in your terminal |
| **Context** | Limited to conversation window | Navigates and understands your codebase |
| **Workflow** | One response at a time | Multi-step autonomous execution |

**Why this matters for engineers:**

With a traditional chat interface, you might:
1. Ask for a Verilog module → Copy the response → Create a file → Paste → Save
2. Ask for a testbench → Repeat the copy/paste process
3. Run simulation manually → Copy errors back → Ask for fixes

With Claude Code, you can:
1. Ask for a Verilog module → Claude Code writes the file
2. Ask to run simulation → Claude Code compiles and runs it
3. Claude Code sees errors and offers to fix them automatically

This **agentic** approach dramatically accelerates engineering workflows. Throughout this workshop, you'll experience this firsthand.

---

## Part 2: Effective Prompting Strategies

### The CRAFT Framework

Use this framework for technical prompts:

| Element | Description | Example |
|---------|-------------|---------|
| **C**ontext | Background information | "I'm designing a low-noise amplifier for a 2.4 GHz receiver..." |
| **R**ole | What perspective to take | "Act as a senior analog designer reviewing my circuit..." |
| **A**sk | Clear, specific request | "Identify potential issues with the biasing network..." |
| **F**ormat | Desired output structure | "Provide your analysis as a numbered list with severity ratings..." |
| **T**one | Level of detail/formality | "Be thorough but concise, focus on practical issues..." |

### Prompting Patterns for Silicon Engineers

#### 1. The Expert Reviewer Pattern
```
Review this [Verilog module / circuit / timing constraint] as an experienced
[DV engineer / circuit designer / STA engineer].

Identify:
1. Functional issues
2. Best practice violations
3. Potential improvements

[paste your code/design here]
```

#### 2. The Explainer Pattern
```
Explain [concept] as if teaching a junior engineer who understands
[prerequisite knowledge] but is new to [this specific area].

Use analogies where helpful and include a simple example.
```

#### 3. The Generator Pattern
```
Generate a [testbench / SPICE netlist / TCL script] that:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Follow [company/industry] coding conventions.
Include comments explaining key sections.
```

#### 4. The Debugger Pattern
```
I'm seeing [unexpected behavior/error].

Here's my [code/setup]:
[paste relevant content]

Here's what I expected:
[expected behavior]

Here's what actually happened:
[actual behavior]

Help me understand why and suggest fixes.
```

#### 5. The Toolmaker Pattern
```
Write a Python script that [parses / analyzes / processes] [file type].

The script should:
- [Specific requirement 1]
- [Specific requirement 2]
- [Output format]

Include command-line arguments for flexibility.
```

> **Why this pattern matters**: When you need to analyze files like timing reports, synthesis logs, or simulation outputs, ask Claude to write a script rather than parsing content directly. This gives you:
> - **Repeatability**: Run the same analysis on any file
> - **Robustness**: Code handles edge cases consistently
> - **Scalability**: Works on files larger than LLM context limits
> - **Version control**: Scripts can be tracked and shared

---

## Part 3: Hands-On Exercises

### Exercise 1: Basic Prompting (5 min)

Try this prompt with Claude:

```
Explain the difference between setup time and hold time violations
in digital circuits. Use a simple analogy and include what each
violation looks like in a timing report.
```

**Follow-up**: Ask Claude to generate a simple example timing report showing each type of violation.

---

### Exercise 2: Iterative Refinement (10 min)

Start with this basic prompt:

```
Write a Verilog counter.
```

Notice the output. Now iterate with more specific prompts:

**Iteration 1** - Add specifications:
```
Write a parameterizable N-bit synchronous counter in Verilog with:
- Configurable width (default 8 bits)
- Active-low synchronous reset
- Enable signal
- Terminal count output
```

**Iteration 2** - Add constraints:
```
Update the counter to:
- Follow [pick a coding style: Xilinx / Intel / generic synthesizable]
- Include proper header comments
- Use non-blocking assignments appropriately
```

**Iteration 3** - Request verification:
```
Now generate a simple testbench that:
- Tests reset functionality
- Tests counting with enable
- Verifies terminal count at rollover
- Uses $display for key events
```

**Reflect**: How did specificity change the output quality?

---

### Exercise 3: Context Matters (10 min)

Try these two prompts and compare the responses:

**Prompt A** (minimal context):
```
How do I fix a hold violation?
```

**Prompt B** (rich context):
```
I'm working on a 28nm digital design at 500 MHz. Post-layout STA shows
hold violations on paths from a high-speed clock domain crossing to a
slower peripheral domain.

The violations are -50ps on about 30 paths, all through the same
CDC synchronizer.

What are my options for fixing this, considering we're late in the
project and want to minimize ECO impact?
```

**Reflect**: How does context change the usefulness of the response?

---

### Exercise 4: Knowing the Limits (5 min)

Try these prompts to understand LLM limitations:

**Prompt 1** - Numerical precision:
```
Calculate the 3dB bandwidth of an RC filter with R=1.5kΩ and C=100pF.
```

**Prompt 2** - Recent information:
```
What's the latest version of the OpenROAD flow and its new features?
```

**Prompt 3** - Proprietary tools:
```
Write the exact commands to run Calibre DRC on my GDS file.
```

**Reflect**:
- For (1): Did Claude get the math right? Always verify calculations.
- For (2): Is the information current? Check dates and sources.
- For (3): How complete/accurate are tool-specific commands? Cross-reference with documentation.

---

## Part 4: Best Practices Summary

### Do's ✓

- **Be specific**: Include constraints, requirements, and context
- **Iterate**: Refine prompts based on output quality
- **Verify**: Always check generated code/calculations
- **Provide examples**: Show the format or style you want
- **Ask for explanations**: Request reasoning, not just answers
- **Ask for code, not direct parsing**: When analyzing files (timing reports, logs, synthesis reports), ask Claude to write a Python script instead of parsing content directly - this is repeatable, robust, and scalable

### Don'ts ✗

- **Don't trust blindly**: Verify all outputs, especially numerical results
- **Don't expect perfection**: Plan to review and refine
- **Don't share proprietary info**: Be mindful of confidential data
- **Don't skip fundamentals**: Use AI to accelerate, not replace understanding

### The 80/20 Rule

LLMs can often get you 80% of the way quickly. Your expertise is essential for:
- The final 20% refinement
- Verification and validation
- Judgment calls and trade-offs
- Context that can't be conveyed in a prompt

---

## Advanced Exploration

If you have extra time, try these advanced exercises:

### Advanced 1: Chain of Thought

Ask Claude to solve a complex problem step-by-step:

```
Walk me through the process of sizing a two-stage operational amplifier
for the following specifications:
- Gain > 60dB
- Unity gain bandwidth > 10 MHz
- Phase margin > 60°
- Load capacitance = 5pF
- Supply voltage = 1.8V
- Technology: 180nm CMOS

Think through each step, explaining your reasoning and trade-offs.
```

### Advanced 2: Self-Critique

Ask Claude to review its own output:

```
[After getting a response to a technical question]

Now critique your own response:
1. What assumptions did you make?
2. What might be wrong or oversimplified?
3. What would a senior engineer push back on?
4. What additional information would improve your answer?
```

### Advanced 3: Format Conversion

Practice using LLMs for format transformation:

```
Convert this timing constraint from SDC to the equivalent
Xilinx XDC format:

create_clock -name sys_clk -period 10 [get_ports clk]
set_input_delay -clock sys_clk -max 2.0 [get_ports data_in]
set_output_delay -clock sys_clk -max 1.5 [get_ports data_out]
```

---

## Key Takeaways

1. **LLMs are powerful pattern matchers** - leverage this for code generation, review, and transformation
2. **Context is king** - the more relevant context you provide, the better the output
3. **Iterate and refine** - rarely is the first output perfect
4. **Verify everything** - especially calculations, tool commands, and critical logic
5. **Know the limits** - use LLMs for what they're good at, your expertise for the rest

---

## Next Steps

You're now ready to explore domain-specific modules. Choose based on your role:

- **Circuit Designer**: [01_Circuit_Design](../01_Circuit_Design/)
- **RTL Engineer**: [02_RTL_Development](../02_RTL_Development/)
- **DV Engineer**: [03_Design_Verification](../03_Design_Verification/)
- **PD Engineer**: [04_Physical_Design](../04_Physical_Design/)
- **Layout Engineer**: [05_Layout](../05_Layout/)
- **DFT Engineer**: [06_DFT](../06_DFT/)
- **STA Engineer**: [07_STA](../07_STA/)
- **Anyone**: [08_Documentation](../08_Documentation/)

---

*Module 00 Complete - You've built the foundation for using GenAI effectively in silicon engineering!*

---

**AIDAChip** - Follow us for more insights on AI-driven chip design automation.
