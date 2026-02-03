#!/usr/bin/env python3
"""
Enhanced Master Script Runner - Run All Scripts in Order
"""

import asyncio
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def print_banner():
    print("=" * 80)
    print("DOSA CLUB - MASTER SCRIPT RUNNER")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Running all setup scripts in order...")
    print("-" * 80)

async def run_script(script_name, description):
    """Run a single script and capture output."""
    print(f"\n[{script_name}] {description}")
    print("-" * 40)
    
    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable, script_name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.path.dirname(__file__)
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            print(f"{script_name} completed successfully")
            if stdout:
                print(stdout.decode())
        else:
            print(f"{script_name} failed with code {process.returncode}")
            if stderr:
                print(stderr.decode())
                
    except Exception as e:
        print(f"Error running {script_name}: {e}")

async def main():
    print_banner()
    
    scripts = [
        ("setup_core_tables.py", "Create DynamoDB tables"),
        ("seed_menu_items.py", "Seed menu items"),
        ("seed_menu_images.py", "Seed menu images"),
        ("seed_health_rules.py", "Seed health rules"),
        ("seed_test_users.py", "Seed test users"),
        ("setup_guest_sessions.py", "Setup guest sessions")
    ]
    
    for script_name, description in scripts:
        await run_script(script_name, description)
        await asyncio.sleep(1)  # Brief pause between scripts
    
    print("\n" + "=" * 80)
    print("ALL SCRIPTS COMPLETED!")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
