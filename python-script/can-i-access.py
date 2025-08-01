#!/usr/bin/env python3
"""
Can I Access? - School Network URL Accessibility Checker (CLI Edition)

A zero-dependency command-line tool for testing educational website accessibility
from within school networks.

Usage:
    python -m can_i_access [options]
    ./can-i-access [options]

For help: python -m can_i_access --help
For manual: python -m can_i_access --man
"""

import sys
import os

# Add the package directory to path if running as script
if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(script_dir) == 'can_i_access':
        # Running from within package directory
        sys.path.insert(0, os.path.dirname(script_dir))
    
    from can_i_access import main
    main()
