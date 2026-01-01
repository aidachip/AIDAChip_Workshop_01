# Module 08: Documentation with GenAI

**Duration**: ~30 minutes
**Prerequisites**: Module 00 (LLM Fundamentals)
**Tools Required**: Markdown editor, optional: Pandoc for format conversion
**Goal**: Learn to use LLMs for technical documentation, specifications, and reports

---

## Overview

This module demonstrates how GenAI can assist with documentation tasks including:
- Writing design specifications from notes or code
- Generating API documentation
- Creating user guides and README files
- Converting documentation between formats
- Reviewing and improving existing documentation

---

## Tutorial: Technical Documentation Basics

> **For all engineers**: Good documentation is a multiplier - it helps your team, future you, and your project succeed.

### Why Documentation Matters in Silicon Engineering

- **Specs define the target**: Ambiguous specs lead to design bugs
- **Reviews need context**: Reviewers can't find issues without understanding intent
- **Knowledge transfer**: People leave, documentation stays
- **Reuse enables speed**: Good docs make IP reusable

### Common Documentation Types

| Type | Purpose | Audience |
|------|---------|----------|
| **Design Spec** | Define requirements and architecture | Designers, reviewers |
| **Micro-architecture** | Detailed implementation description | RTL designers |
| **Interface Spec** | Signal definitions and protocols | Integration teams |
| **Verification Plan** | Test strategy and coverage goals | DV engineers |
| **User Guide** | How to use an IP or tool | End users |
| **Release Notes** | What changed and why | All stakeholders |

### Documentation Best Practices

1. **Start with the reader**: What do they need to know?
2. **Be specific**: "Fast" is meaningless; "< 10 cycles" is useful
3. **Use examples**: Show, don't just tell
4. **Keep it current**: Outdated docs are worse than none
5. **Review docs like code**: They're just as important

---

## Exercise 1: Generate a Design Spec (10 min)

### Objective
Use Claude to transform notes and requirements into a formal specification.

### Step 1: From Notes to Spec

We've provided rough notes from a design discussion. Ask Claude to formalize them:

```
Transform the rough notes in design_notes.txt into a formal design specification.

The spec should include:
1. Document header (title, version, author, date)
2. Overview and purpose
3. Feature list with detailed descriptions
4. Block diagram description
5. Interface specifications (signals, protocols)
6. Register map (if applicable)
7. Timing requirements
8. Power considerations
9. Test requirements
10. Open issues and TODOs

Use proper technical writing style:
- Active voice where possible
- Specific, quantified requirements
- Consistent terminology
- Clear section numbering

Save to design_spec.md
```

### Step 2: Generate Interface Documentation

```
From design_spec.md, extract and expand the interface section into a
standalone interface control document (ICD):

1. Signal table with name, direction, width, description
2. Timing diagrams in ASCII art or Wavedrom format
3. Protocol state machines
4. Example transactions
5. Error handling

Save to interface_spec.md
```

### Step 3: Create a Quick Reference

```
Create a one-page quick reference card for design_spec.md that includes:
1. Block diagram (ASCII art)
2. Key parameters table
3. Essential signals
4. Common use cases
5. Gotchas and tips

This should fit on a single page when printed.
Save to quick_reference.md
```

---

## Exercise 2: API and Code Documentation (10 min)

### Objective
Use Claude to generate documentation from code.

> **Note**: Keep things interactive! Ask Claude to generate different documentation styles, add examples, or clarify sections.

### Step 1: Document a Verilog Module

Use your own Verilog module, or ask Claude to generate one first:

```
Generate a simple AXI-Lite register interface module in Verilog with:
- 4 read/write registers
- APB-like timing
- Parameterizable data width

Save to sample_module.v
```

Then ask Claude to document it:

```
Generate comprehensive documentation for sample_module.v:

1. Module overview and purpose
2. Parameter descriptions with valid ranges
3. Port descriptions with timing requirements
4. Functional description
5. Usage examples (instantiation)
6. Integration notes
7. Known limitations

Output as a Markdown file suitable for inclusion in a project wiki.
Save to sample_module_doc.md
```

> **Tip**: If you have your own RTL, use that instead! Documenting real code is more valuable practice.

### Step 2: Generate Wavedrom Timing Diagrams

```
Based on sample_module.v, create Wavedrom timing diagrams showing:

1. Basic read transaction
2. Basic write transaction
3. Back-to-back operations
4. Error handling case

Provide the Wavedrom JSON for each diagram.
Save to timing_diagrams.md
```

### Step 3: Create Register Documentation

```
Given this register definition:

[Paste register RTL or description]

Generate a register map document with:
1. Register summary table
2. Individual register descriptions
3. Bit field tables with access type (RW, RO, W1C, etc.)
4. Reset values
5. Programming sequence examples

Format suitable for both HTML and PDF generation.
Save to register_map.md
```

---

## Exercise 3: Documentation Review and Improvement (10 min)

### Objective
Use Claude to review and improve existing documentation.

### Step 1: Review for Completeness

Use the `design_spec.md` you generated in Exercise 1, or provide your own spec:

```
Review design_spec.md and identify:

1. Missing sections that a reader would expect
2. Ambiguous requirements that need clarification
3. Inconsistent terminology
4. Outdated information (based on common patterns)
5. Gaps between what's described and what's typical for this type of design

Provide a prioritized list of improvements needed.
```

### Step 2: Improve Clarity

```
Rewrite the following unclear specification text to be specific and testable:

"The module should process data quickly and handle errors gracefully.
Performance should be good enough for most applications.
The interface should be easy to use."

Transform each vague statement into concrete, measurable requirements.
```

### Step 3: Generate Missing Sections

```
Based on the review from Step 1, generate any missing sections for design_spec.md:

1. Test plan outline
2. Performance metrics and targets
3. Power estimation methodology
4. Integration checklist

Save the improved version to improved_spec.md
```

---

## Sample Files

This module includes sample files for exercises:

| File | Description |
|------|-------------|
| `design_notes.txt` | Rough notes from design meeting |

---

## Quick Reference: Documentation Formats

### Markdown Basics

```markdown
# Heading 1
## Heading 2

**Bold** and *italic* text

- Bullet list
- Another item

1. Numbered list
2. Second item

| Column 1 | Column 2 |
|----------|----------|
| Data     | Data     |

`inline code` and:

​```verilog
// Code block
module example();
endmodule
​```

> Block quote for notes
```

### Wavedrom Timing Diagram

```json
{ "signal": [
  { "name": "clk",  "wave": "p......." },
  { "name": "valid","wave": "0.1..0.." },
  { "name": "data", "wave": "x.====x.", "data": ["A", "B", "C", "D"] },
  { "name": "ready","wave": "1...0.1." }
]}
```

### Document Templates

You can ask Claude to generate a specification template for your projects:

```
Create a reusable design specification template with placeholders for:
- Project info, version, authors
- Requirements, architecture, interfaces
- Test plan, open issues

Save to template_spec.md
```

---

## Advanced Exercises

If you have more time, try these challenging exercises:

### Advanced 1: Multi-Format Generation

```
From design_spec.md, generate outputs in multiple formats:

1. HTML page with navigation
2. PDF-ready LaTeX source
3. Confluence wiki format
4. Word document outline

Explain the conversion process and any limitations.
```

### Advanced 2: Documentation Automation

```
Create a Python script that:

1. Scans a Verilog file for modules
2. Extracts port definitions and comments
3. Generates a documentation template
4. Identifies undocumented parameters/ports
5. Outputs Markdown documentation

Save to generate_docs.py
```

### Advanced 3: Release Notes Generator

```
Given these git commit messages and bug tracker IDs:

[Paste sample commits]

Generate professional release notes that:
1. Group changes by category (features, fixes, improvements)
2. Summarize technical changes in user-friendly language
3. List known issues and workarounds
4. Include upgrade instructions

Format for both internal and customer-facing versions.
```

---

## Prompting Tips for Documentation

### What Works Well
- Transforming notes into structured documents
- Generating documentation from code
- Creating templates and outlines
- Improving clarity of existing text
- Format conversion

### What Requires Caution
- Accuracy of technical details (verify against source)
- Specific numerical values (may need correction)
- Company-specific terminology
- Proprietary information handling

### Effective Context to Include
- Document purpose and audience
- Existing documentation or code
- Company style guide preferences
- Required sections or format

---

## Key Takeaways

1. **AI accelerates first drafts** - get structure quickly, refine details
2. **Code is a documentation source** - extract and format systematically
3. **Review is still essential** - AI helps write, you verify accuracy
4. **Templates save time** - create once, reuse often
5. **Multiple formats from one source** - maintain consistency

---

## Keep Exploring

The exercises above are just starting points. Feel free to:

- **Create your own templates** - design specs, interface docs, test plans
- **Automate documentation extraction** - from RTL, constraints, or scripts
- **Build a documentation pipeline** - generate, review, publish
- **Explore diagram generation** - Wavedrom, Mermaid, ASCII art
- **Document your own blocks** - practice on real project needs

The more you experiment, the better you'll understand how to leverage AI in your documentation workflow.

---

## Share Your Feedback

We'd love to hear about your experience with this module!

- What worked well? What was frustrating?
- What improvements would you like to see in specialized **Documentation agents** beyond what Claude Code can do?
- What documentation tasks would benefit most from AI assistance?

**Send your feedback to: hello@aidachip.com**

Your insights will directly shape what we're building next - and we have some exciting launches coming soon that you won't want to miss!

---

## Next Module

Continue your workshop journey:
- [09_Workflow_Automation](../09_Workflow_Automation/) - Scripts and automation with AI
- [Back to Workshop Home](../README.md)

---

*Module 08 Complete - You've learned to use GenAI for documentation tasks!*

---

**AIDAChip** - Follow us for more insights on AI-driven chip design automation.
