#!/usr/bin/env python3
"""
Extract version information from versions.json for use in build scripts.
"""

import json
import argparse
import sys
from pathlib import Path


def get_package_info(versions_data, package_name, field=None):
    """Get information about a specific package."""
    # Search through all categories
    for category, packages in versions_data.get('packages', {}).items():
        if package_name in packages:
            pkg_info = packages[package_name]
            if field:
                return pkg_info.get(field, '')
            return pkg_info
    return None


def list_packages(versions_data, category=None, used_by=None):
    """List all packages, optionally filtered by category or usage."""
    packages = []
    for cat, pkgs in versions_data.get('packages', {}).items():
        if category and cat != category:
            continue
        for pkg_name, pkg_info in pkgs.items():
            if used_by:
                if 'usedBy' not in pkg_info or used_by not in pkg_info['usedBy']:
                    continue
            packages.append({
                'name': pkg_name,
                'category': cat,
                **pkg_info
            })
    return packages


def main():
    parser = argparse.ArgumentParser(
        description='Extract version information from versions.json'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Get package info command
    get_parser = subparsers.add_parser('get', help='Get package information')
    get_parser.add_argument('package', help='Package name')
    get_parser.add_argument('--field', help='Specific field to retrieve (version, repository, etc.)')
    
    # List packages command
    list_parser = subparsers.add_parser('list', help='List packages')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--used-by', help='Filter by project that uses the package')
    list_parser.add_argument('--format', choices=['text', 'json', 'csv'], default='text',
                           help='Output format')
    
    args = parser.parse_args()
    
    # Load versions.json
    script_dir = Path(__file__).parent
    versions_file = script_dir / 'versions.json'
    
    try:
        with open(versions_file, 'r') as f:
            versions_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"ERROR: Could not load versions.json: {e}", file=sys.stderr)
        return 1
    
    # Execute command
    if args.command == 'get':
        result = get_package_info(versions_data, args.package, args.field)
        if result is None:
            print(f"ERROR: Package '{args.package}' not found", file=sys.stderr)
            return 1
        if isinstance(result, dict):
            print(json.dumps(result, indent=2))
        else:
            print(result)
    
    elif args.command == 'list':
        packages = list_packages(versions_data, args.category, args.used_by)
        
        if args.format == 'json':
            print(json.dumps(packages, indent=2))
        elif args.format == 'csv':
            if packages:
                # Get all unique keys
                keys = set()
                for pkg in packages:
                    keys.update(pkg.keys())
                keys = sorted(keys)
                
                # Print header
                print(','.join(keys))
                
                # Print rows
                for pkg in packages:
                    values = [str(pkg.get(k, '')) for k in keys]
                    print(','.join(f'"{v}"' for v in values))
        else:  # text format
            for pkg in packages:
                name = pkg.get('name', 'unknown')
                version = pkg.get('version', 'N/A')
                category = pkg.get('category', 'unknown')
                print(f"{name:30} {version:20} [{category}]")
    
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
