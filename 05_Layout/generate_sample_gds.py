#!/usr/bin/env python3
"""
Generate sample GDS files for the Layout module exercises.

This script creates:
1. sample_layout.gds - A clean layout with hierarchy for analysis
2. drc_test.gds - A layout with intentional DRC violations

Usage:
    python3 generate_sample_gds.py

Requires: klayout package (pip install klayout)
"""

try:
    import klayout.db as db
except ImportError:
    print("Error: klayout package not found.")
    print("Install with: pip install klayout")
    print("Or run KLayout GUI and use the built-in Python console.")
    exit(1)

def create_sample_layout():
    """Create a sample layout with hierarchy for analysis exercises."""

    layout = db.Layout()
    layout.dbu = 0.001  # 1nm database units

    # Define layers
    M1 = layout.layer(31, 0)
    M2 = layout.layer(32, 0)
    VIA1 = layout.layer(51, 0)
    TEXT = layout.layer(100, 0)

    # Create a via cell
    via_cell = layout.create_cell("VIA1_1X")
    # Via: 0.1um x 0.1um
    via_cell.shapes(VIA1).insert(db.Box(0, 0, 100, 100))
    # M1 enclosure: 0.02um each side
    via_cell.shapes(M1).insert(db.Box(-20, -20, 120, 120))
    # M2 enclosure: 0.02um each side
    via_cell.shapes(M2).insert(db.Box(-20, -20, 120, 120))

    # Create a wire cell
    wire_cell = layout.create_cell("M1_WIRE")
    # Horizontal wire: 0.2um wide, 5um long
    wire_cell.shapes(M1).insert(db.Box(0, 0, 5000, 200))

    # Create a resistor cell
    res_cell = layout.create_cell("RESISTOR")
    # Resistor body: 0.5um wide, 10um long
    res_cell.shapes(M1).insert(db.Box(0, 0, 10000, 500))
    # End caps
    res_cell.shapes(M1).insert(db.Box(-200, -200, 200, 700))
    res_cell.shapes(M1).insert(db.Box(9800, -200, 10200, 700))
    # Label
    res_cell.shapes(TEXT).insert(db.Text("RES_1K", db.Trans(5000, 250)))

    # Create a sub-block cell
    sub_block = layout.create_cell("SUB_BLOCK")
    # Place some wires
    sub_block.insert(db.CellInstArray(wire_cell.cell_index(), db.Trans(0, 0)))
    sub_block.insert(db.CellInstArray(wire_cell.cell_index(), db.Trans(0, 500)))
    sub_block.insert(db.CellInstArray(wire_cell.cell_index(), db.Trans(0, 1000)))
    # Add vias
    for i in range(3):
        sub_block.insert(db.CellInstArray(via_cell.cell_index(), db.Trans(4500, i * 500 + 50)))

    # Create top cell
    top_cell = layout.create_cell("TOP")
    # Place sub-blocks
    top_cell.insert(db.CellInstArray(sub_block.cell_index(), db.Trans(0, 0)))
    top_cell.insert(db.CellInstArray(sub_block.cell_index(), db.Trans(6000, 0)))
    top_cell.insert(db.CellInstArray(sub_block.cell_index(), db.Trans(0, 2000)))
    top_cell.insert(db.CellInstArray(sub_block.cell_index(), db.Trans(6000, 2000)))
    # Add resistor
    top_cell.insert(db.CellInstArray(res_cell.cell_index(), db.Trans(1000, 4500)))
    # Add power labels
    top_cell.shapes(TEXT).insert(db.Text("VDD", db.Trans(0, 5500)))
    top_cell.shapes(TEXT).insert(db.Text("VSS", db.Trans(0, -500)))

    # M2 power straps
    top_cell.shapes(M2).insert(db.Box(-500, 5200, 12000, 5800))  # VDD
    top_cell.shapes(M2).insert(db.Box(-500, -800, 12000, -200))  # VSS

    layout.write("sample_layout.gds")
    print("Created: sample_layout.gds")
    print(f"  - {layout.cells()} cells")
    print(f"  - Top cell: {top_cell.name}")

    return layout


def create_drc_test_layout():
    """Create a layout with intentional DRC violations for testing."""

    layout = db.Layout()
    layout.dbu = 0.001  # 1nm database units

    # Define layers
    M1 = layout.layer(31, 0)
    M2 = layout.layer(32, 0)
    VIA1 = layout.layer(51, 0)
    TEXT = layout.layer(100, 0)

    top_cell = layout.create_cell("DRC_TEST")

    # ===== Metal1 width violations =====
    # Good: 0.1um width
    top_cell.shapes(M1).insert(db.Box(0, 0, 1000, 100))
    top_cell.shapes(TEXT).insert(db.Text("M1 OK width", db.Trans(500, 150)))

    # Bad: 0.08um width (violation!)
    top_cell.shapes(M1).insert(db.Box(0, 500, 1000, 580))
    top_cell.shapes(TEXT).insert(db.Text("M1 BAD width", db.Trans(500, 650)))

    # Bad: 0.05um width (violation!)
    top_cell.shapes(M1).insert(db.Box(0, 1000, 1000, 1050))
    top_cell.shapes(TEXT).insert(db.Text("M1 BAD width", db.Trans(500, 1150)))

    # ===== Metal1 spacing violations =====
    # Good: 0.1um spacing
    top_cell.shapes(M1).insert(db.Box(2000, 0, 2500, 200))
    top_cell.shapes(M1).insert(db.Box(2600, 0, 3100, 200))
    top_cell.shapes(TEXT).insert(db.Text("M1 OK space", db.Trans(2500, 250)))

    # Bad: 0.05um spacing (violation!)
    top_cell.shapes(M1).insert(db.Box(2000, 500, 2500, 700))
    top_cell.shapes(M1).insert(db.Box(2550, 500, 3050, 700))
    top_cell.shapes(TEXT).insert(db.Text("M1 BAD space", db.Trans(2500, 750)))

    # ===== Via enclosure violations =====
    # Good: proper enclosure
    top_cell.shapes(VIA1).insert(db.Box(4000, 0, 4100, 100))
    top_cell.shapes(M1).insert(db.Box(3980, -20, 4120, 120))
    top_cell.shapes(M2).insert(db.Box(3980, -20, 4120, 120))
    top_cell.shapes(TEXT).insert(db.Text("VIA OK", db.Trans(4050, 180)))

    # Bad: M1 enclosure violation
    top_cell.shapes(VIA1).insert(db.Box(4000, 500, 4100, 600))
    top_cell.shapes(M1).insert(db.Box(4000, 500, 4100, 600))  # No enclosure!
    top_cell.shapes(M2).insert(db.Box(3980, 480, 4120, 620))
    top_cell.shapes(TEXT).insert(db.Text("VIA BAD M1 enc", db.Trans(4050, 680)))

    # Bad: M2 enclosure violation
    top_cell.shapes(VIA1).insert(db.Box(4000, 1000, 4100, 1100))
    top_cell.shapes(M1).insert(db.Box(3980, 980, 4120, 1120))
    top_cell.shapes(M2).insert(db.Box(4000, 1000, 4100, 1100))  # No enclosure!
    top_cell.shapes(TEXT).insert(db.Text("VIA BAD M2 enc", db.Trans(4050, 1180)))

    # ===== Via spacing violation =====
    # Bad: vias too close
    top_cell.shapes(VIA1).insert(db.Box(5000, 0, 5100, 100))
    top_cell.shapes(VIA1).insert(db.Box(5050, 0, 5150, 100))  # Overlapping!
    top_cell.shapes(M1).insert(db.Box(4950, -50, 5200, 150))
    top_cell.shapes(M2).insert(db.Box(4950, -50, 5200, 150))
    top_cell.shapes(TEXT).insert(db.Text("VIA BAD space", db.Trans(5050, 200)))

    layout.write("drc_test.gds")
    print("Created: drc_test.gds")
    print("  - Contains intentional DRC violations for testing")

    return layout


if __name__ == "__main__":
    print("Generating sample GDS files for Layout module...\n")
    create_sample_layout()
    print()
    create_drc_test_layout()
    print("\nDone! You can now use these files with the exercises.")
