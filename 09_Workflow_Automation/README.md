# Module 09: Workflow Automation with GenAI

**Duration**: ~30 minutes
**Prerequisites**: Module 00 (LLM Fundamentals), basic scripting knowledge helpful
**Tools Required**: Python 3, Bash shell
**Goal**: Learn to use LLMs for scripting, automation, and workflow optimization

> **Note**: This module's exercises are currently being verified. Some steps may require adjustment based on your environment. Please report any issues to hello@aidachip.com.

---

## Overview

This module demonstrates how GenAI can assist with workflow automation including:
- Creating build and run scripts
- Automating repetitive tasks
- Parsing and processing log files
- Building CI/CD pipelines for hardware
- Creating Makefiles and flow managers

---

## Tutorial: Workflow Automation Basics

> **For all engineers**: Automation is the key to reproducibility, efficiency, and sanity.

### Why Automate?

- **Reproducibility**: Same commands, same results
- **Efficiency**: Run overnight, review in morning
- **Quality**: Never forget a step
- **Scalability**: Handle more designs without more effort
- **Documentation**: Scripts document your process

### Common Automation Targets in Silicon

| Area | What to Automate |
|------|------------------|
| **Simulation** | Compile, run, check results |
| **Synthesis** | Run flow, parse reports |
| **P&R** | Stage progression, timing checks |
| **Verification** | Regression, coverage merge |
| **Release** | Packaging, version tagging |
| **Reporting** | Status dashboards, email alerts |

### Scripting Languages

| Language | Best For |
|----------|----------|
| **Bash** | Quick tasks, tool invocation, file manipulation |
| **Python** | Complex logic, data processing, report generation |
| **Makefile** | Dependency-based builds, parallel execution |
| **TCL** | EDA tool automation (synthesis, P&R) |
| **Perl** | Text processing (legacy, but still used) |

---

## Exercise 1: Build and Run Scripts (10 min)

### Objective
Use Claude to create a complete build and run flow.

### Step 1: Generate a Simulation Makefile

```
Create a Makefile for a Verilog simulation environment:

Features:
- Compile all .v files in src/ and .sv files in tb/
- Support Icarus Verilog and Verilator (selectable)
- Run simulation with waveform generation
- Clean build artifacts
- Support for test selection: make run TEST=test_name
- Parallel compilation where possible

Include:
- Variable definitions at top for easy customization
- Help target that lists available commands
- Color-coded output for pass/fail

Save to Makefile
```

### Step 2: Create a Test Runner Script

```
Write a Python test runner script that:

1. Discovers all tests in a tb/ directory
2. Runs each test and captures output
3. Parses output for PASS/FAIL status
4. Generates a summary report with:
   - Total tests run
   - Pass/fail counts
   - Execution time per test
   - Failure details
5. Returns non-zero exit code if any test fails
6. Supports parallel execution with -j option

Save to run_tests.py
```

### Step 3: Add Email Notification

```
Extend run_tests.py to optionally send email on completion:

1. Add --email option to specify recipients
2. Send summary on any failures
3. Include:
   - Subject line with PASS/FAIL and counts
   - HTML formatted body with test table
   - Log attachments for failures
4. Support SMTP configuration via environment variables

Update run_tests.py
```

---

## Exercise 2: Log Parsing and Analysis (10 min)

### Objective
Use Claude to create log analysis tools.

> **Best Practice**: Use the Toolmaker pattern - create reusable scripts rather than one-off parsing.

### Step 1: Create a Generic Log Parser

```
Write a Python log parser framework that:

1. Defines a parser base class with:
   - Pattern registration (regex → handler)
   - State machine support
   - Error/warning collection
2. Includes parsers for:
   - Simulation logs (errors, warnings, assertions)
   - Synthesis logs (area, timing, resource usage)
   - Lint logs (violations by severity)
3. Outputs structured data (JSON)
4. Generates summary statistics

Save to log_parser.py
```

### Step 2: Build a Synthesis Flow Monitor

```
Create a script that monitors a synthesis run:

1. Watches log file in real-time
2. Extracts key metrics as they appear:
   - Current stage (elaborate, compile, optimize)
   - Area estimates
   - Timing estimates
   - Error/warning counts
3. Displays progress with live updates
4. Saves final summary to JSON

Save to synth_monitor.py
```

### Step 3: Create a Trend Analyzer

```
Write a script that tracks metrics across runs:

1. Reads JSON outputs from multiple runs
2. Tracks trends for:
   - Area growth
   - Timing slack changes
   - Warning count changes
3. Alerts on significant regressions
4. Generates trend charts (ASCII or matplotlib)
5. Outputs markdown summary

Save to trend_analysis.py
```

---

## Exercise 3: CI/CD for Hardware (10 min)

### Objective
Use Claude to set up continuous integration for RTL.

### Step 1: Create GitHub Actions Workflow

```
Create a GitHub Actions workflow for RTL CI:

Triggers:
- Push to main branch
- Pull request to main
- Manual dispatch

Jobs:
1. Lint (Verilator lint, or custom lint script)
2. Compile (Icarus Verilog compile check)
3. Unit tests (run small tests, < 5 min total)
4. Full regression (on main branch only, up to 1 hour)

Features:
- Cache compiled objects
- Parallel job execution where possible
- Artifact upload for logs and reports
- Status badges for README
- Slack/email notification on failure

Save to .github/workflows/rtl_ci.yml
```

### Step 2: Create Pre-commit Hooks

```
Create Git pre-commit hooks for RTL development:

1. Verilog/SystemVerilog formatting check
2. Lint for common issues:
   - Blocking assignments in sequential blocks
   - Missing default in case statements
   - Unused signals
3. Commit message format validation
4. Check for debug code (e.g., $display left in)
5. Verify all files have headers

Provide:
- Pre-commit hook script
- Installation instructions
- Bypass instructions for emergency

Save to hooks/pre-commit
```

### Step 3: Create a Release Script

```
Create a release automation script:

1. Validates all tests pass
2. Updates version number in:
   - RTL parameters
   - Documentation
   - Changelog
3. Generates release notes from commits
4. Creates signed git tag
5. Packages release artifacts:
   - Synthesizable RTL
   - Testbench (optional)
   - Documentation
   - Reports
6. Uploads to internal repository

Save to scripts/release.py
```

---

## Sample Files

This module includes sample files for exercises:

| File | Description |
|------|-------------|
| `sample_sim_log.txt` | Sample simulation log for parsing |
| `sample_synth_log.txt` | Sample synthesis log for parsing |
| `Makefile.template` | Starter Makefile template |
| `run_tests.py` | Starter test runner |

---

## Quick Reference: Scripting Patterns

### Bash Best Practices

```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined var, pipe fail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'  # No Color

# Function with error handling
run_step() {
    local name=$1
    shift
    echo "Running: $name"
    if "$@"; then
        echo -e "${GREEN}PASS${NC}: $name"
    else
        echo -e "${RED}FAIL${NC}: $name"
        return 1
    fi
}

# Trap for cleanup
cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT
```

### Python Argument Parsing

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description='Run tests')
    parser.add_argument('--test', '-t', help='Specific test to run')
    parser.add_argument('--parallel', '-j', type=int, default=1,
                        help='Parallel jobs')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')
    args = parser.parse_args()

if __name__ == '__main__':
    main()
```

### Makefile Patterns

```makefile
# Variables at top
SRC_DIR := src
TB_DIR := tb
BUILD_DIR := build

# Phony targets
.PHONY: all clean test help

# Default target
all: compile

# Pattern rules
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.v
	@mkdir -p $(@D)
	iverilog -c $< -o $@

# Help target
help:
	@echo "Available targets:"
	@echo "  all     - Build everything"
	@echo "  test    - Run tests"
	@echo "  clean   - Remove build artifacts"
```

---

## Advanced Exercises

If you have more time, try these challenging exercises:

### Advanced 1: Flow Manager

```
Create a Python-based flow manager that:

1. Reads a flow definition from YAML:
   - Stages with dependencies
   - Commands for each stage
   - Retry policies
2. Executes stages respecting dependencies
3. Supports:
   - Stage restart from failure point
   - Parallel execution of independent stages
   - Resource limits (max parallel jobs)
   - Timeout per stage
4. Generates execution report with timing

Save to flow_manager.py
```

### Advanced 2: Smart Test Selector

```
Create a test selection tool that:

1. Analyzes git diff to find changed files
2. Maps RTL files to relevant tests
3. Generates minimal test list for changes
4. Supports:
   - Module dependency tracking
   - Test priority ordering
   - Always-run tests list
5. Integrates with CI for efficient regression

Save to smart_test_select.py
```

### Advanced 3: Report Dashboard Generator

```
Create a script that generates an HTML dashboard:

1. Collects data from various sources:
   - Test results (JSON)
   - Timing reports
   - Area reports
   - Coverage data
2. Generates interactive HTML with:
   - Summary cards (pass/fail, slack, coverage)
   - Trend charts
   - Drill-down capability
   - Comparison to baseline
3. Deployable as static HTML (no server needed)

Save to generate_dashboard.py
```

---

## Prompting Tips for Automation

### What Works Well
- Creating scripts from workflow descriptions
- Parsing structured log files
- Building Makefiles and CI configs
- Generating shell scripts with proper error handling
- Creating data processing pipelines

### What Requires Caution
- Complex shell quoting (test carefully)
- Platform-specific commands
- Tool version dependencies
- Security (credentials, permissions)

### Effective Context to Include
- Tools and versions in use
- Directory structure
- Input/output file formats
- Error handling requirements
- Target execution environment

---

## Key Takeaways

1. **Scripts are documentation** - self-documenting process
2. **Makefiles handle dependencies** - right tool for incremental builds
3. **Python for complex logic** - parsing, analysis, reporting
4. **CI catches issues early** - automate quality gates
5. **Monitor and trend** - track metrics over time

---

## Keep Exploring

The exercises above are just starting points. Feel free to:

- **Automate your daily tasks** - what do you do repeatedly?
- **Build a personal toolkit** - scripts you reuse across projects
- **Create project templates** - standardize new project setup
- **Integrate with your tools** - connect EDA tools to automation
- **Share with your team** - good automation benefits everyone

The more you experiment, the better you'll understand how to leverage AI in your automation workflow.

---

## Share Your Feedback

We'd love to hear about your experience with this module!

- What worked well? What was frustrating?
- What improvements would you like to see in specialized **Workflow Automation agents** beyond what Claude Code can do?
- What automation tasks would benefit most from AI assistance?

**Send your feedback to: hello@aidachip.com**

Your insights will directly shape what we're building next - and we have some exciting launches coming soon that you won't want to miss!

---

## Next Module

Continue your workshop journey:
- [10_Management](../10_Management/) - Engineering management with AI
- [Back to Workshop Home](../README.md)

---

*Module 09 Complete - You've learned to use GenAI for workflow automation!*

---

**AIDAChip** - Follow us for more insights on AI-driven chip design automation.
