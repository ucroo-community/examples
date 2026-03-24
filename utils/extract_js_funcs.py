#!/usr/bin/env python3
"""
Extract jsFunc strings from JSON file and save them as separate .js files
"""

import json
import os
import re
from pathlib import Path


def sanitize_filename(name):
    """Convert a string into a valid filename"""
    # Replace invalid characters with underscore
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Remove extra spaces and truncate if too long
    name = '_'.join(name.split())
    return name[:100]  # Limit filename length


def extract_js_functions(json_file, output_dir='extracted_js'):
    """Extract all jsFunc values from JSON and save to separate files"""

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Check if file exists and is not empty
    json_path = Path(json_file)
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_file}")
    if json_path.stat().st_size == 0:
        raise ValueError(f"JSON file is empty: {json_file}")

    # Load JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {json_file}: {e}")

    js_func_count = 0

    # Walk through the JSON structure
    def walk_json(obj, path=''):
        nonlocal js_func_count

        if isinstance(obj, dict):
            # Check if this dict has a jsFunc
            if 'jsFunc' in obj:
                js_code = obj['jsFunc']
                js_func_count += 1

                # Try to determine a meaningful name from context
                step_name = obj.get('name', f'function_{js_func_count}')

                # Create filename
                filename = f"{js_func_count:03d}_{sanitize_filename(step_name)}.js"
                filepath = output_path / filename

                # Write the JS code to file
                with open(filepath, 'w', encoding='utf-8') as js_file:
                    js_file.write(js_code)

                print(f"Extracted: {filename}")

            # Recurse into dict values
            for key, value in obj.items():
                walk_json(value, f"{path}.{key}" if path else key)

        elif isinstance(obj, list):
            # Recurse into list items
            for i, item in enumerate(obj):
                walk_json(item, f"{path}[{i}]")

    # Process the JSON
    walk_json(data)

    print(f"\n✓ Extracted {js_func_count} JavaScript functions to '{output_dir}/' directory")
    return js_func_count


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_js_functions.py <json_file> [output_dir]")
        print("Example: python extract_js_functions.py data.json extracted_js")
        sys.exit(1)

    json_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'extracted_js'

    extract_js_functions(json_file, output_dir)
