#!/usr/bin/env python3
"""Run scripts for PersonalWealth"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python run.py <command>")
        print("\nAvailable commands:")
        print("  init      - Initialize database")
        print("  sample    - Add sample data")
        print("  snapshot  - Record daily snapshot")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'init':
        from scripts.init_db import *
    elif command == 'sample':
        from scripts.add_sample_data import *
    elif command == 'snapshot':
        from scripts.daily_snapshot import *
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
