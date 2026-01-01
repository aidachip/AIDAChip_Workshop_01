# Module 05: Layout with GenAI

**Duration**: ~30 minutes
**Prerequisites**: Module 00 (LLM Fundamentals)
**Tools Required**: KLayout (see [SETUP.md](../SETUP.md))
**Goal**: Learn to use LLMs for layout viewing, scripting, DRC/LVS, and automation

---

## Overview

This module demonstrates how GenAI can assist with layout tasks including:
- Writing KLayout Python/Ruby scripts for automation
- Understanding and fixing DRC violations
- LVS debugging strategies
- Layout manipulation and analysis
- Parameterized cell (PCell) development

---

## Tutorial: Layout Basics

> **For non-layout engineers**: This section provides essential background to follow the exercises.

### What is Layout?

Layout is the physical representation of a circuit as geometric shapes on different layers. Key concepts:

- **GDS/OASIS**: Standard file formats for layout data
- **Layers**: Different materials/processes (metal, poly, diffusion, etc.)
- **Cells**: Hierarchical building blocks
- **DRC**: Design Rule Checking - verifies manufacturing constraints
- **LVS**: Layout vs. Schematic - verifies layout matches circuit

### KLayout Overview

KLayout is a powerful open-source layout viewer and editor with:
- Python and Ruby scripting APIs
- Built-in DRC engine
- Cross-platform support (Windows, macOS, Linux)

### Key Layout Concepts

| Term | Description |
|------|-------------|
| **GDS/GDSII** | Graphic Database System - standard layout format |
| **OASIS** | Newer, more compact layout format |
| **Layer/Datatype** | Identifies geometry purpose (e.g., Metal1 = 31/0) |
| **Cell** | Reusable layout block (hierarchical) |
| **Instance** | Placement of a cell in another cell |
| **DRC** | Design Rule Check - spacing, width, enclosure rules |
| **LVS** | Layout vs Schematic - netlist extraction and comparison |

---

## Exercise 1: KLayout Scripting Basics (10 min)

### Objective
Use Claude to write KLayout Python scripts for layout automation.

### Step 0: Generate a Sample Layout

First, let's create a sample GDS file to work with. Ask Claude Code:

```
Run the generate_sample_gds.py script to create sample_layout.gds
```

This script creates a simple hierarchical layout with standard cells, metal layers, and instances that we'll analyze in the following steps.

> **Tip**: If you have your own GDS file, you can use that instead! Just replace `sample_layout.gds` with your file name in the exercises.

### Step 1: Generate a Layout Analysis Script

Now that we have a sample GDS file, ask Claude to write an analysis script:

```
Write a KLayout Python script that:
1. Opens the GDS file 'sample_layout.gds'
2. Lists all cells and their hierarchy
3. Reports total cell count and instance count
4. Calculates the bounding box of the top cell
5. Counts shapes per layer and reports statistics
6. Saves a summary report to 'layout_report.txt'

Save the script to analyze_layout.py
```

### Step 2: Run in KLayout

You can run the script in KLayout:

```bash
klayout -b -r analyze_layout.py
```

Or ask Claude Code:

```
Run the analyze_layout.py script with KLayout in batch mode and show me the results
```

> **Tip**: The `-b` flag runs KLayout in batch mode (no GUI). Use `-r` to run a script.

### Step 3: Extend the Script

```
Extend analyze_layout.py to also:
1. Find all cells that contain the text "VDD" or "VSS"
2. Report any cells with zero area (empty cells)
3. Identify the deepest hierarchy level
4. Export a cell hierarchy tree to JSON format

Update analyze_layout.py
```

### Reflection Questions
- What information would be most useful for your layout review process?
- How could you modify this script for your specific layer map?

---

## Exercise 2: DRC Scripting (10 min)

### Objective
Use Claude to write DRC rules and debug violations.

> **Note**: Keep things interactive! Ask Claude Code to run checks, visualize results, or explain rule syntax.

### Step 1: Write Basic DRC Rules

```
Write a KLayout DRC script for a simple process with these rules:

Metal1 (layer 31/0):
- Minimum width: 0.1 µm
- Minimum spacing: 0.1 µm

Metal2 (layer 32/0):
- Minimum width: 0.14 µm
- Minimum spacing: 0.14 µm

Via1 (layer 51/0):
- Must be enclosed by Metal1 by at least 0.02 µm
- Must be enclosed by Metal2 by at least 0.02 µm
- Minimum via spacing: 0.1 µm

Include comments explaining each rule.
Save to basic_drc.lydrc
```

### Step 2: Run DRC

```
Run basic_drc.lydrc on sample_layout.gds using KLayout and report any violations
```

Or manually:

```bash
klayout -b -r basic_drc.lydrc sample_layout.gds
```

### Step 3: Debug DRC Violations

If violations are found (or using the provided sample with intentional violations):

```
I have these DRC violations:
- 5 Metal1 minimum width violations
- 3 Via1 enclosure violations

Help me write a KLayout script that:
1. Highlights the violations in the layout
2. Exports violation locations to a CSV file
3. Suggests automated fixes where possible

Save to drc_debug.py
```

---

## Exercise 3: Layout Manipulation (10 min)

### Objective
Use Claude to generate scripts for layout modification and generation.

### Step 1: Create a Simple PCell

```
Write a KLayout Python PCell (parameterized cell) for a metal resistor with:

Parameters:
- width: metal width in µm (default 0.5)
- length: resistor length in µm (default 10)
- layer: metal layer number (default 31)

The PCell should:
1. Draw the resistor body
2. Add contact regions at both ends
3. Add a text label with the resistance value

Save to resistor_pcell.py
```

### Step 2: Generate a Via Array

```
Write a KLayout Python script that generates a via array:

Parameters:
- rows: number of rows
- cols: number of columns
- via_size: size of each via (µm)
- spacing: center-to-center spacing (µm)
- metal_top: top metal layer number
- metal_bot: bottom metal layer number
- via_layer: via layer number

The script should:
1. Create vias in a grid pattern
2. Add metal patches on top and bottom
3. Properly enclose all vias
4. Allow placement at a specified origin

Save to via_array_generator.py
```

### Step 3: Run and View

```
Run via_array_generator.py to create a 4x4 via array with 0.1µm vias
at 0.2µm spacing. Open the result in KLayout GUI to verify.
```

---

## Sample Files

This module includes sample files for hands-on practice:

| File | Description |
|------|-------------|
| `generate_sample_gds.py` | Script to generate sample layouts (run in Step 0) |
| `sample_layout.gds` | Generated - clean layout with hierarchy for analysis |
| `drc_test.gds` | Generated - layout with intentional DRC violations |
| `layer_map.txt` | Layer name to number mapping |
| `basic_drc.lydrc` | Starter DRC rule deck |

> **Note**: Run `generate_sample_gds.py` before starting the exercises to create the GDS files.

---

## Quick Reference: KLayout Python API

### Opening and Accessing Layout

```python
import klayout.db as db

# Load layout
layout = db.Layout()
layout.read("design.gds")

# Get top cell
top_cell = layout.top_cell()

# Iterate cells
for cell in layout.each_cell():
    print(cell.name)
```

### Working with Layers

```python
# Get layer index
layer_idx = layout.layer(31, 0)  # layer 31, datatype 0

# Iterate shapes
for shape in cell.shapes(layer_idx).each():
    print(shape.bbox())  # bounding box
```

### Creating Geometry

```python
# Create a new cell
new_cell = layout.create_cell("MY_CELL")

# Add a rectangle (in database units)
layer_idx = layout.layer(31, 0)
new_cell.shapes(layer_idx).insert(db.Box(0, 0, 1000, 500))

# Save layout
layout.write("output.gds")
```

### DRC Rule Syntax

```ruby
# In .lydrc file (Ruby-based)
metal1 = input(31, 0)
metal2 = input(32, 0)

# Width check
metal1.width(0.1.um).output("M1 min width")

# Spacing check
metal1.space(0.1.um).output("M1 min space")

# Enclosure check
via.enclosed(metal1, 0.02.um).output("Via M1 enclosure")
```

### Running KLayout

```bash
# GUI mode
klayout design.gds

# Batch mode with script
klayout -b -r script.py

# Run DRC
klayout -b -r rules.lydrc design.gds

# Export to different format
klayout -b -o output.oas input.gds
```

---

## Advanced Exercises

If you have more time, try these challenging exercises:

### Advanced 1: LVS Debug Helper

```
Write a Python script that helps debug LVS mismatches:

1. Parse an LVS report file (assume Calibre format)
2. Categorize mismatches: shorts, opens, device mismatches
3. For shorts: identify the nets involved and their locations
4. For opens: find the expected connection points
5. Generate a KLayout script that highlights problem areas

Save to lvs_debug.py
```

### Advanced 2: Automatic Density Fill

```
Write a KLayout script that adds metal density fill:

1. Read a layout with existing metal patterns
2. Identify empty regions that need fill
3. Add fill patterns (small squares) maintaining:
   - Minimum spacing from existing metal
   - Target density (e.g., 30% coverage)
   - Avoid filling over sensitive areas (marked by a "no fill" layer)
4. Report coverage statistics per region

Save to density_fill.py
```

### Advanced 3: Layout Comparison

```
Write a script to compare two GDS files:

1. Identify cells that exist in one but not the other
2. For matching cells, compare geometry differences
3. Report: added shapes, removed shapes, modified shapes
4. Export a diff visualization where differences are highlighted

Save to layout_diff.py
```

---

## Prompting Tips for Layout

### What Works Well
- Writing KLayout Python/Ruby scripts
- Explaining DRC rules and violations
- Generating parameterized cells (PCells)
- Creating utility scripts for layout analysis
- Debugging LVS issues from error reports

### What Requires Caution
- Process-specific rules (get from foundry documentation)
- Complex analog layout considerations
- Layer mapping (varies by foundry/technology)
- Antenna rule implementation

### Effective Context to Include
- Technology node and foundry
- Layer map (layer numbers and names)
- Specific DRC rules being addressed
- Error messages or violation reports

---

## Key Takeaways

1. **KLayout scripting is powerful** - automate repetitive layout tasks
2. **DRC rules are scriptable** - create reusable rule decks
3. **Layout analysis at scale** - scripts can process entire chips
4. **Debug systematically** - use scripts to categorize and locate issues
5. **PCells save time** - parameterized cells for common structures

---

## Keep Exploring

The exercises above are just starting points. Feel free to:

- **Automate your layout checks** - write scripts for your common review tasks
- **Build a PCell library** - create parameterized cells for resistors, capacitors, inductors
- **Create custom DRC rules** - extend the basic rules for your process
- **Generate layout reports** - build tools that extract key metrics from your designs
- **Explore Magic VLSI** - another open-source layout tool with different capabilities

The more you experiment, the better you'll understand how to leverage AI in your layout workflow.

---

## Share Your Feedback

We'd love to hear about your experience with this module!

- What worked well? What was frustrating?
- What improvements would you like to see in specialized **Layout agents** beyond what Claude Code can do?
- What layout tasks would benefit most from AI assistance?

**Send your feedback to: hello@aidachip.com**

Your insights will directly shape what we're building next - and we have some exciting launches coming soon that you won't want to miss!

---

## Next Module

Continue your workshop journey:
- [06_DFT](../06_DFT/) - Design for Test with AI
- [Back to Workshop Home](../README.md)

---

*Module 05 Complete - You've learned to use GenAI for layout tasks!*

---

**AIDAChip** - Follow us for more insights on AI-driven chip design automation.
