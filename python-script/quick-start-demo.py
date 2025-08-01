#!/usr/bin/env python3
"""
Can I Access? - Quick Start Guide

This script demonstrates common usage patterns for new users.
Run this script to see the tool in action with various examples.
"""

import subprocess
import sys
import time

def run_command(description, command):
    """Run a command and show the results"""
    print(f"\\n{'='*60}")
    print(f"EXAMPLE: {description}")
    print(f"{'='*60}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        if result.returncode != 0:
            print(f"Command exited with code: {result.returncode}")
    except subprocess.TimeoutExpired:
        print("Command timed out after 30 seconds")
    except Exception as e:
        print(f"Error running command: {e}")
    
    print("\\nPress Enter to continue to next example...")
    input()

def main():
    print("Can I Access? - Quick Start Demo")
    print("=" * 40)
    print("This script will demonstrate various features of the CLI tool.")
    print("Each example will run and show you the output.")
    print("\\nPress Enter to start...")
    input()
    
    examples = [
        ("Show help information", "python -m can_i_access --help"),
        ("List available data sources", "python -m can_i_access list --sources"),
        ("Test a single URL", "python -m can_i_access --url https://example.com"),
        ("Test with verbose output", "python -m can_i_access --url https://google.com -v"),
        ("Test sample CSV file", "python -m can_i_access --csv sample-urls.csv"),
        ("Test with filtering", "python -m can_i_access --csv sample-urls.csv --filter warnings"),
        ("Save results to JSON", "python -m can_i_access --url https://khanacademy.org --output demo-results.json"),
        ("Generate HTML report", "python -m can_i_access report demo-results.json --format html -o demo-report.html"),
    ]
    
    for description, command in examples:
        run_command(description, command)
    
    print("\\n" + "="*60)
    print("DEMO COMPLETE!")
    print("="*60)
    print("You've seen the major features of Can I Access?")
    print("\\nFor more information:")
    print("• Full manual: python -m can_i_access --man")
    print("• GitHub: https://github.com/RiceC-at-MasonHS/can-i-access")
    print("• README: README.md")
    print("\\nThe tool is ready to use for testing your school's network!")

if __name__ == '__main__':
    main()
