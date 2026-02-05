#!/usr/bin/env python3
"""
Validate the versions.json file format and check for consistency.
"""

import json
import sys
from pathlib import Path


def validate_versions_file(filepath):
    """Validate the structure and content of versions.json."""
    errors = []
    warnings = []
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON format: {e}")
        return False
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        return False
    
    # Check required top-level fields
    required_fields = ['packages', 'lastUpdated']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Validate package structure
    if 'packages' in data:
        packages = data['packages']
        all_packages = {}
        
        for category, items in packages.items():
            if not isinstance(items, dict):
                errors.append(f"Category '{category}' should be a dictionary")
                continue
                
            for pkg_name, pkg_info in items.items():
                # Collect all packages for cross-reference checking
                all_packages[pkg_name] = pkg_info
                
                # Check required package fields (except for build category)
                if category != 'build':
                    required_pkg_fields = ['version', 'type', 'repository', 'description']
                    for field in required_pkg_fields:
                        if field not in pkg_info:
                            errors.append(f"Package '{pkg_name}' missing field: {field}")
                    
                    # Validate type
                    if 'type' in pkg_info and pkg_info['type'] not in ['git_tag', 'version', 'branch']:
                        warnings.append(f"Package '{pkg_name}' has unusual type: {pkg_info['type']}")
                    
                    # Check if repository is a valid URL
                    if 'repository' in pkg_info:
                        repo = pkg_info['repository']
                        if not (repo.startswith('http://') or repo.startswith('https://')):
                            warnings.append(f"Package '{pkg_name}' repository should be a URL")
        
        # Check usedBy references
        for pkg_name, pkg_info in all_packages.items():
            if 'usedBy' in pkg_info:
                for used_by in pkg_info['usedBy']:
                    # This is informational - we can't validate external project names
                    pass
    
    # Print results
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("\nWARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and not warnings:
        print("✓ versions.json is valid!")
        return True
    elif not errors:
        print("\n✓ versions.json is valid (with warnings)")
        return True
    else:
        return False


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    versions_file = script_dir / 'versions.json'
    
    success = validate_versions_file(versions_file)
    sys.exit(0 if success else 1)
