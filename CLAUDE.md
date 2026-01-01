# CLAUDE.md - Workshop Context for Claude Code

## Overview

This is the **AIDAChip GenAI Workshop for Silicon Engineers** - a self-guided workshop designed to teach semiconductor professionals how to leverage Large Language Models (LLMs) and Generative AI across various chip design disciplines.

## Workshop Structure

```
AIDAChip_Workshop_Si/
├── README.md                 # Start here - workshop overview and navigation
├── SETUP.md                  # Environment setup instructions
├── setup_check.py            # Run this to verify your environment
│
├── 00_LLM_Fundamentals/      # Educational: LLM concepts for silicon engineers
├── 01_Circuit_Design/        # Analog/mixed-signal design with AI assistance
├── 02_RTL_Development/       # Verilog/SystemVerilog development
├── 03_Design_Verification/   # Testbench, UVM, formal verification
├── 04_Physical_Design/       # Floorplanning, P&R, timing closure
├── 05_Layout/                # Layout generation and DRC/LVS
├── 06_DFT/                   # Design for Test automation
├── 07_STA/                   # Static Timing Analysis workflows
├── 08_Documentation/         # Spec writing, documentation generation
├── 09_Workflow_Automation/   # Scripts, flows, and automation
└── 10_Management/            # Project planning, reporting, communication
```

## Key Conventions

- **Each module is self-contained** with its own README.md containing exercises
- **Exercises are progressive**: Basic prompts → Follow-up tasks → Advanced challenges
- **~30 minutes per module** for core exercises; advanced sections are optional
- **Open-source tools** are used (ngspice, Yosys, OpenROAD, etc.) for accessibility
- **Cross-domain friendly**: Each module includes brief tutorials for non-experts

## How to Use This Workshop with Claude Code

1. Navigate to a module folder you want to explore
2. Read the module's README.md for context and exercises
3. Use Claude Code to help you:
   - Write and refine prompts for the exercises
   - Generate code, scripts, or documentation
   - Debug and iterate on solutions
   - Explore advanced use cases

## Tool Requirements

- **Python 3.8+** with standard scientific libraries
- **Claude Code** (this CLI tool)
- **Module-specific tools** listed in each module's README

Run `python3 setup_check.py` from the root directory to verify your environment.

## Target Audience

Silicon engineers across all disciplines:
- Circuit designers, RTL engineers, DV engineers
- Physical design, layout, DFT, STA engineers
- Technical writers, CAD engineers, engineering managers

Exercises assume domain expertise in the target area, with optional tutorials for cross-domain exploration.

## Workshop Goals

1. Understand LLM capabilities and limitations for silicon engineering
2. Learn effective prompting strategies for technical tasks
3. Gain hands-on experience with AI-assisted workflows
4. Identify opportunities to apply GenAI in your daily work

## Share Your Feedback

We'd love to hear about your experience with this workshop!

- Which modules were most valuable? Which need improvement?
- What improvements would you like to see in specialized **silicon engineering AI agents** (Circuit Design, RTL, DV, PD, DFT, STA, and more)?
- What tasks in your daily workflow would benefit most from AI assistance?

**Send your feedback to: hello@aidachip.com**

Your insights will directly shape what we're building next - and we have some exciting launches coming soon that you won't want to miss!

## About AIDAChip

This workshop is developed by **AIDAChip** - follow us for more insights, tools, and reports on AI-driven chip design automation.

---

*When assisting with this workshop, Claude should guide users through exercises progressively, explain concepts clearly, and encourage experimentation with prompts.*
