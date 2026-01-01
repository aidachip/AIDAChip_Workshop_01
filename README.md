# AIDAChip GenAI Workshop for Silicon Engineers

Welcome to the **AIDAChip GenAI Workshop** - a hands-on, self-guided workshop designed to demonstrate the power of Large Language Models (LLMs) and Generative AI for semiconductor professionals.

## Who Is This For?

This workshop is designed for **silicon engineers** across all disciplines:

| Role | Relevant Modules |
|------|------------------|
| Circuit Designer | 00, 01, 05 |
| RTL Engineer | 00, 02, 03 |
| DV Engineer | 00, 03, 02 |
| Physical Design Engineer | 00, 04, 07 |
| Layout Engineer | 00, 05, 01 |
| DFT Engineer | 00, 06, 02 |
| STA Engineer | 00, 07, 04 |
| CAD Engineer | 00, 09, 08 |
| Engineering Manager | 00, 10, 08 |

## Getting Started

### Step 1: Setup Your Environment

Follow the instructions in [SETUP.md](SETUP.md) to configure your environment.

```bash
# Quick verification
python3 setup_check.py
```

### Step 2: Start with the Fundamentals

Begin with **Module 00** to understand LLM concepts tailored for silicon engineers:

```bash
cd 00_LLM_Fundamentals
# Read the README.md and follow the exercises
```

### Step 3: Explore Your Domain

Navigate to the module(s) relevant to your expertise and interests.

## Workshop Modules

| Module | Topic | Duration | Description |
|--------|-------|----------|-------------|
| [00](00_LLM_Fundamentals/) | LLM Fundamentals | 30 min | How LLMs work, prompting strategies, limitations |
| [01](01_Circuit_Design/) | Circuit Design | 30 min | Analog/mixed-signal design assistance |
| [02](02_RTL_Development/) | RTL Development | 30 min | Verilog/SystemVerilog coding with AI |
| [03](03_Design_Verification/) | Design Verification | 30 min | Testbenches, UVM, coverage analysis |
| [04](04_Physical_Design/) | Physical Design | 30 min | Floorplanning, P&R, timing closure |
| [05](05_Layout/) | Layout | 30 min | Layout generation, DRC/LVS |
| [06](06_DFT/) | DFT | 30 min | Scan insertion, ATPG, BIST |
| [07](07_STA/) | STA | 30 min | Timing analysis, constraint writing |
| [08](08_Documentation/) | Documentation | 30 min | Specs, reports, documentation |
| [09](09_Workflow_Automation/) | Workflow Automation | 30 min | Scripts, flows, CAD automation |
| [10](10_Management/) | Management | 30 min | Planning, communication, reporting |

## How to Use This Workshop

This workshop is designed to be used with **Claude Code** - Anthropic's agentic coding tool that runs in your terminal.

### What is Claude Code?

Unlike a typical chat interface where you send messages and receive responses, Claude Code is an **agentic AI assistant** that can:

- **Read and write files** directly in your project
- **Run commands** in your terminal (compile, simulate, run tests)
- **Navigate your codebase** to understand context
- **Take multi-step actions** to complete tasks autonomously

This makes it ideal for engineering workflows where you need AI to not just suggest code, but actually create files, run simulations, and iterate based on results.

### Claude Code Gets Proactive

As you work with Claude Code, it becomes increasingly proactive. It may automatically:
- Generate a testbench after you create a Verilog module
- Run simulations without being explicitly asked
- Suggest next steps or improvements
- Fix errors it encounters along the way

**This is a feature, not a bug.** Watch what Claude Code does at each step. If you like the proactivity, let it continue. If you prefer more control, give it feedback and direction. This back-and-forth is how you develop an effective working relationship with AI assistants.

### Module Structure

Each module contains:
- **Overview**: Background and objectives
- **Tutorial**: Brief introduction for non-experts
- **Core Exercises**: Guided prompts and tasks (~30 min)
- **Advanced Challenges**: Deeper exploration for those who want more

### Workflow

1. Read the module's README.md
2. Follow the exercises using Claude Code
3. Experiment with your own variations
4. Try the advanced challenges if time permits

## A Note on Tools

This workshop uses **open-source tools** to ensure accessibility:
- **ngspice** for circuit simulation
- **Yosys** for synthesis
- **OpenROAD** for physical design
- **Magic/KLayout** for layout
- Standard Python libraries

> **Note**: The techniques and prompts demonstrated here apply equally to commercial EDA tools (Cadence, Synopsys, Siemens). If you have access to vendor tools, feel free to adapt the exercises accordingly.

## Workshop Philosophy

This workshop aims to:

1. **Demonstrate practical value** - Real tasks you do every day
2. **Build intuition** - Understand what LLMs can and cannot do well
3. **Encourage experimentation** - Try different prompts, see what works
4. **Inspire adoption** - Identify opportunities in your workflow

GenAI won't replace silicon engineers - but engineers who leverage AI effectively will have a significant advantage.

---

## Share Your Feedback

We'd love to hear about your experience with this workshop!

- Which modules were most valuable? Which need improvement?
- What improvements would you like to see in specialized **silicon engineering AI agents** (Circuit Design, RTL, DV, PD, DFT, STA, and more)?
- What tasks in your daily workflow would benefit most from AI assistance?

**Send your feedback to: hello@aidachip.com**

Your insights will directly shape what we're building next - and we have some exciting launches coming soon that you won't want to miss!

---

## About AIDAChip

This workshop is developed by **AIDAChip**.

Follow us for more insights, tools, and reports on AI-driven chip design automation:
- Website: [AIDAChip.com](https://aidachip.com)
- LinkedIn: [AIDAChip](https://linkedin.com/company/aidachip)

---

*Ready to begin? Start with [SETUP.md](SETUP.md) to configure your environment.*
