#!/usr/bin/env python3
"""
Can I Access? - Simple Installation Script

This script makes the tool easy to run for new Python users.
"""

import os
import sys
import stat
import shutil
from pathlib import Path

def main():
    print("Can I Access? CLI Tool - Setup")
    print("=" * 35)
    print("GitHub: https://github.com/RiceC-at-MasonHS/can-i-access")
    print()
    
    script_dir = Path(__file__).parent
    can_i_access_script = script_dir / "can-i-access"
    
    # Make the main script executable on Unix-like systems
    if os.name != 'nt':  # Not Windows
        try:
            current_perms = os.stat(can_i_access_script).st_mode
            os.chmod(can_i_access_script, current_perms | stat.S_IEXEC)
            print("✓ Made can-i-access executable")
        except Exception as e:
            print(f"⚠ Could not make executable: {e}")
    
    print("✓ Zero-dependency CLI tool ready!")
    print("\\nYou can now run the tool in several ways:")
    print()
    print("1. As a Python module (recommended):")
    print("   python -m can_i_access --help")
    print()
    print("2. Directly (Unix/Linux/macOS):")
    print("   ./can-i-access --help")
    print()
    print("3. With Python interpreter:")
    print("   python can-i-access --help")
    print()
    print("For detailed documentation:")
    print("   python -m can_i_access --man")
    print()
    print("Quick start examples:")
    print("   python -m can_i_access                    # Test default URLs")
    print("   python -m can_i_access --cyber1           # Test Cyber1 curriculum")
    print("   python -m can_i_access --csv my-urls.csv  # Test from CSV file")
    print("   python -m can_i_access --url example.com  # Test single URL")
    print()
    print("💡 TIP: Use the web version at https://ricec-at-masonhs.github.io/can-i-access/")
    print("    for quick tests, or this CLI tool for batch processing and reports!")
    print()
    print("📚 For complete documentation: python -m can_i_access --man")

if __name__ == '__main__':
    main()
