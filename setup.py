#!/usr/bin/env python3
"""
Setup script for McDoc - Document Framework
"""

import os
import sys
from pathlib import Path


def setup_mcdoc():
    """Initialize McDoc environment"""
    print("=" * 60)
    print("McDoc - Document Framework Setup")
    print("=" * 60)
    print()
    
    base_dir = Path.cwd()
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return 1
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Create required directories
    directories = ['documents', 'library']
    for dir_name in directories:
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            print(f"✓ Created directory: {dir_name}/")
        else:
            print(f"✓ Directory exists: {dir_name}/")
    
    # Verify template directory
    templates_dir = base_dir / 'templates'
    if templates_dir.exists():
        template_count = len(list(templates_dir.glob('*.md')))
        print(f"✓ Templates directory: {template_count} templates found")
    else:
        print("⚠ Warning: templates/ directory not found")
    
    # Verify source code
    src_dir = base_dir / 'src' / 'mcdoc'
    if src_dir.exists() and (src_dir / '__init__.py').exists():
        print("✓ Source code: mcdoc package found")
    else:
        print("⚠ Warning: mcdoc package not found in src/")
    
    # Verify CLI
    cli_path = base_dir / 'src' / 'mcdoc_cli.py'
    if cli_path.exists():
        print("✓ CLI: mcdoc_cli.py found")
    else:
        print("⚠ Warning: CLI script not found")
    
    print()
    print("=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print()
    print("Quick Start:")
    print("  1. List templates:")
    print("     python src/mcdoc_cli.py list-templates")
    print()
    print("  2. Import an example:")
    print("     python src/mcdoc_cli.py import examples/example_basic.json")
    print()
    print("  3. Create a new document:")
    print("     python src/mcdoc_cli.py create --template basic")
    print()
    print("Documentation: See DOCUMENTATION.md for detailed usage")
    print()
    
    return 0


if __name__ == '__main__':
    sys.exit(setup_mcdoc())
