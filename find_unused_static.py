import os
import re
from pathlib import Path

# Set the root directory of the project
PROJECT_ROOT = Path('.')

# Get all template files
template_files = []
for root, dirs, files in os.walk(PROJECT_ROOT):
    for file in files:
        if file.endswith('.html'):
            template_files.append(os.path.join(root, file))

# Read all template files to check for static references
template_content = ""
for template_file in template_files:
    with open(template_file, 'r', encoding='utf-8', errors='ignore') as f:
        try:
            template_content += f.read()
        except Exception as e:
            print(f"Error reading {template_file}: {e}")

# Get all static directories
static_dirs = []
for item in os.listdir('static'):
    if os.path.isdir(os.path.join('static', item)):
        static_dirs.append(item)

# Check which static directories are not referenced in templates
unused_dirs = []
for static_dir in static_dirs:
    # Check for common patterns of static file references
    patterns = [
        rf"static['\"]?/{static_dir}/",  # {% static 'dir/file' %}
        rf"static['\"]?/plugins/{static_dir}/",  # {% static 'plugins/dir/file' %}
        rf"/{static_dir}/",  # Direct reference like /dir/file
    ]
    
    is_used = False
    for pattern in patterns:
        if re.search(pattern, template_content):
            is_used = True
            break
    
    if not is_used:
        unused_dirs.append(static_dir)

# Print results
print("\nPotentially unused static directories:")
for unused_dir in sorted(unused_dirs):
    print(f"- static/{unused_dir}/")

print("\nNote: This is a basic analysis and may not catch all references.")
print("Please verify before deleting any directories.") 