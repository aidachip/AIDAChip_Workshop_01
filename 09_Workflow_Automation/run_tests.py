#!/usr/bin/env python3
"""
Simple Test Runner for Verilog Simulations

This is a starter template for Exercise 1. Extend it with:
- Email notification
- Parallel execution
- HTML report generation

Usage:
    python run_tests.py
    python run_tests.py --test specific_test
    python run_tests.py -j 4  # parallel execution (to be implemented)
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TestResult:
    """Holds the result of a single test run."""
    name: str
    passed: bool
    duration: float
    output: str
    error_message: Optional[str] = None


def discover_tests(tb_dir: str = "tb") -> List[str]:
    """
    Discover all testbench files in the specified directory.

    Args:
        tb_dir: Directory containing testbench files

    Returns:
        List of testbench names (without extension)
    """
    tests = []
    tb_path = Path(tb_dir)

    if not tb_path.exists():
        print(f"Warning: Test directory '{tb_dir}' not found")
        return tests

    # Find all *_tb.v and *_tb.sv files
    for pattern in ["*_tb.v", "*_tb.sv"]:
        for tb_file in tb_path.glob(pattern):
            test_name = tb_file.stem
            tests.append(test_name)

    return sorted(tests)


def run_single_test(test_name: str, build_dir: str = "build") -> TestResult:
    """
    Run a single test and capture results.

    Args:
        test_name: Name of the testbench to run
        build_dir: Directory for build artifacts

    Returns:
        TestResult with pass/fail status and details
    """
    start_time = time.time()

    # Compile
    compile_cmd = [
        "iverilog", "-Wall", "-g2012",
        "-o", f"{build_dir}/{test_name}.vvp",
        "-s", test_name,
        f"tb/{test_name}.v"
    ]

    # Add source files
    src_files = list(Path("src").glob("*.v")) + list(Path("src").glob("*.sv"))
    compile_cmd.extend([str(f) for f in src_files])

    try:
        # Create build directory
        Path(build_dir).mkdir(exist_ok=True)

        # Compile
        compile_result = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if compile_result.returncode != 0:
            return TestResult(
                name=test_name,
                passed=False,
                duration=time.time() - start_time,
                output=compile_result.stdout,
                error_message=f"Compilation failed:\n{compile_result.stderr}"
            )

        # Run simulation
        sim_result = subprocess.run(
            ["vvp", f"{build_dir}/{test_name}.vvp"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        duration = time.time() - start_time
        output = sim_result.stdout + sim_result.stderr

        # Check for pass/fail in output
        passed = "FAIL" not in output and "ERROR" not in output
        if "PASS" not in output and passed:
            # No explicit PASS, check return code
            passed = sim_result.returncode == 0

        error_msg = None
        if not passed:
            # Extract failure details
            lines = output.split('\n')
            error_lines = [l for l in lines if 'FAIL' in l or 'ERROR' in l]
            error_msg = '\n'.join(error_lines[:5])  # First 5 error lines

        return TestResult(
            name=test_name,
            passed=passed,
            duration=duration,
            output=output,
            error_message=error_msg
        )

    except subprocess.TimeoutExpired:
        return TestResult(
            name=test_name,
            passed=False,
            duration=time.time() - start_time,
            output="",
            error_message="Test timed out"
        )
    except Exception as e:
        return TestResult(
            name=test_name,
            passed=False,
            duration=time.time() - start_time,
            output="",
            error_message=str(e)
        )


def print_summary(results: List[TestResult]) -> int:
    """
    Print a summary of all test results.

    Args:
        results: List of TestResult objects

    Returns:
        Exit code (0 if all passed, 1 if any failed)
    """
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    total_time = sum(r.duration for r in results)

    # Print individual results
    for result in results:
        status = "\033[32mPASS\033[0m" if result.passed else "\033[31mFAIL\033[0m"
        print(f"  {status}: {result.name} ({result.duration:.2f}s)")
        if result.error_message:
            for line in result.error_message.split('\n')[:3]:
                print(f"         {line}")

    print("-" * 60)
    print(f"Total: {len(results)} tests, {passed} passed, {failed} failed")
    print(f"Time:  {total_time:.2f} seconds")
    print("=" * 60)

    return 0 if failed == 0 else 1


def main():
    parser = argparse.ArgumentParser(description='Run Verilog testbenches')
    parser.add_argument('--test', '-t', help='Specific test to run')
    parser.add_argument('--parallel', '-j', type=int, default=1,
                        help='Number of parallel jobs (not yet implemented)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show full test output')
    parser.add_argument('--tb-dir', default='tb',
                        help='Testbench directory')
    parser.add_argument('--build-dir', default='build',
                        help='Build output directory')

    args = parser.parse_args()

    # Discover or select tests
    if args.test:
        tests = [args.test]
    else:
        tests = discover_tests(args.tb_dir)

    if not tests:
        print("No tests found!")
        return 1

    print(f"Found {len(tests)} test(s) to run")
    print("-" * 40)

    # Run tests
    results = []
    for test in tests:
        print(f"Running {test}...", end=" ", flush=True)
        result = run_single_test(test, args.build_dir)
        results.append(result)

        if result.passed:
            print("\033[32mPASS\033[0m")
        else:
            print("\033[31mFAIL\033[0m")

        if args.verbose and result.output:
            print(result.output)

    # Print summary and return exit code
    return print_summary(results)


if __name__ == '__main__':
    sys.exit(main())
