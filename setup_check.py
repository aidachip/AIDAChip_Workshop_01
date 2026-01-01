#!/usr/bin/env python3
"""
AIDAChip GenAI Workshop - Environment Setup Checker

Run this script to verify your environment is ready for the workshop.

Usage:
    python3 setup_check.py           # Check all requirements
    python3 setup_check.py --full    # Include optional module-specific tools
"""

import sys
import subprocess
import shutil
from typing import Tuple, Optional

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_status(name: str, status: bool, version: str = "", required: bool = True) -> None:
    """Print the status of a check."""
    if status:
        icon = f"{Colors.GREEN}[OK]{Colors.END}"
        version_str = f" ({version})" if version else ""
    elif required:
        icon = f"{Colors.RED}[MISSING]{Colors.END}"
        version_str = ""
    else:
        icon = f"{Colors.YELLOW}[NOT FOUND]{Colors.END}"
        version_str = " (optional)"

    req_str = "" if required else f"{Colors.YELLOW}(optional){Colors.END} "
    print(f"  {icon} {req_str}{name}{version_str}")

def check_python_version() -> Tuple[bool, str]:
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    is_valid = version.major == 3 and version.minor >= 8
    return is_valid, version_str

def check_python_library(name: str) -> Tuple[bool, str]:
    """Check if a Python library is installed."""
    try:
        module = __import__(name)
        version = getattr(module, '__version__', 'installed')
        return True, version
    except ImportError:
        return False, ""

def check_command(command: str, version_flag: str = "--version") -> Tuple[bool, str]:
    """Check if a command-line tool is available."""
    if not shutil.which(command):
        return False, ""

    try:
        result = subprocess.run(
            [command, version_flag],
            capture_output=True,
            text=True,
            timeout=10
        )
        # Extract version from output (first line, first few words)
        output = result.stdout.strip() or result.stderr.strip()
        version = output.split('\n')[0][:50] if output else "installed"
        return True, version
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        return shutil.which(command) is not None, "installed"

def check_claude_code() -> Tuple[bool, str]:
    """Check if Claude Code is installed."""
    # Try 'claude' command
    if shutil.which('claude'):
        return check_command('claude', '--version')
    return False, ""

def main():
    """Run all environment checks."""
    print_header("AIDAChip GenAI Workshop - Setup Check")

    full_check = '--full' in sys.argv
    all_required_ok = True

    # Python Version Check
    print(f"{Colors.BOLD}Python Environment:{Colors.END}")
    py_ok, py_version = check_python_version()
    print_status("Python 3.8+", py_ok, py_version)
    all_required_ok &= py_ok

    # Required Python Libraries
    print(f"\n{Colors.BOLD}Python Libraries (required):{Colors.END}")
    required_libs = ['numpy', 'matplotlib', 'pandas', 'yaml']
    lib_names = {'yaml': 'pyyaml'}  # Display name mapping

    for lib in required_libs:
        display_name = lib_names.get(lib, lib)
        ok, version = check_python_library(lib)
        print_status(display_name, ok, version)
        all_required_ok &= ok

    # Claude Code Check
    print(f"\n{Colors.BOLD}Claude Code:{Colors.END}")
    claude_ok, claude_version = check_claude_code()
    print_status("claude", claude_ok, claude_version)
    all_required_ok &= claude_ok

    # Optional: Module-Specific Tools
    if full_check:
        print(f"\n{Colors.BOLD}Module-Specific Tools (optional):{Colors.END}")

        optional_tools = [
            ('ngspice', '--version', 'Circuit Design (Module 01)'),
            ('iverilog', '-V', 'RTL/DV (Modules 02, 03)'),
            ('verilator', '--version', 'RTL/DV (Modules 02, 03)'),
            ('yosys', '--version', 'Synthesis (Module 02)'),
            ('klayout', '-v', 'Layout (Module 05)'),
            ('magic', '--version', 'Layout/DRC (Module 05)'),
        ]

        for tool, flag, description in optional_tools:
            ok, version = check_command(tool, flag)
            print_status(f"{tool} - {description}", ok, version, required=False)
    else:
        print(f"\n{Colors.YELLOW}Tip: Run with --full to check module-specific tools{Colors.END}")

    # Summary
    print_header("Summary")

    if all_required_ok:
        print(f"{Colors.GREEN}{Colors.BOLD}All required components are installed!{Colors.END}")
        print(f"\nYou're ready to start the workshop.")
        print(f"Begin with: {Colors.BLUE}cd 00_LLM_Fundamentals{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}Some required components are missing.{Colors.END}")
        print(f"\nPlease install the missing components listed above.")
        print(f"See {Colors.BLUE}SETUP.md{Colors.END} for installation instructions.")

    print(f"\n{'─'*60}")
    print(f"{Colors.BOLD}AIDAChip GenAI Workshop for Silicon Engineers{Colors.END}")
    print(f"Follow us for more insights on AI-driven chip design!")
    print(f"{'─'*60}\n")

    return 0 if all_required_ok else 1

if __name__ == "__main__":
    sys.exit(main())
