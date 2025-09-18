import os
import re
import shutil
from pathlib import Path

# Set the root directory of the project
PROJECT_ROOT = Path('.')

# Define the list of statically referenced directories we know are used
KNOWN_USED_DIRS = [
    'dist',           # AdminLTE core
    'plugins',        # AdminLTE plugins container
    'bootstrap',      # Bootstrap core
    'fontawesome-free', # Font Awesome
    'jquery',         # jQuery core
    'jquery-ui',      # jQuery UI
    'images',         # Custom images
    'chart.js',       # Charts
    'datatables',     # DataTables core
    'css',            # Core CSS
    'js',             # Core JS
    'moment',         # Moment.js for dates
    'tempusdominus-bootstrap-4',  # Date/time picker
    'summernote',     # Rich text editor
    'icheck-bootstrap', # Checkbox styles
    'daterangepicker', # Date range picker
    'jqvmap',         # Vector maps
    'overlayScrollbars', # Custom scrollbars
    'sparklines',     # Sparkline charts
]

# Get all template files
template_files = []
for root, dirs, files in os.walk(PROJECT_ROOT):
    for file in files:
        if file.endswith('.html') or file.endswith('.js') or file.endswith('.py'):
            template_files.append(os.path.join(root, file))

# Read all template files to check for static references
template_content = ""
for template_file in template_files:
    try:
        with open(template_file, 'r', encoding='utf-8', errors='ignore') as f:
            template_content += f.read()
    except Exception as e:
        print(f"Error reading {template_file}: {e}")

# Get all static directories
static_dirs = []
for item in os.listdir('static'):
    if os.path.isdir(os.path.join('static', item)) and item != 'archived':
        static_dirs.append(item)

# Check which static directories are not referenced in templates
potentially_unused_dirs = []
for static_dir in static_dirs:
    # Skip known used directories
    if static_dir in KNOWN_USED_DIRS:
        continue
        
    # Check for common patterns of static file references
    patterns = [
        rf"static['\"]?/{static_dir}/",  # {% static 'dir/file' %}
        rf"static['\"]?/plugins/{static_dir}/",  # {% static 'plugins/dir/file' %}
        rf"/{static_dir}/",  # Direct reference like /dir/file
        rf"['\"]/{static_dir}/",  # "/dir/file"
        rf"['\"]\.\./{static_dir}/",  # "../dir/file"
        rf"['\"]\./{static_dir}/",  # "./dir/file"
        rf"{static_dir}\.min\.(js|css)",  # dir.min.js, dir.min.css
    ]
    
    is_used = False
    for pattern in patterns:
        if re.search(pattern, template_content):
            is_used = True
            break
    
    if not is_used:
        potentially_unused_dirs.append(static_dir)

# Archive potentially unused directories
archive_dir = os.path.join('static', 'archived')
if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)

print("\nMoving potentially unused static directories to static/archived/:")
for unused_dir in sorted(potentially_unused_dirs):
    src_path = os.path.join('static', unused_dir)
    dst_path = os.path.join(archive_dir, unused_dir)
    
    print(f"- Moving {src_path} to {dst_path}")
    try:
        shutil.move(src_path, dst_path)
    except Exception as e:
        print(f"  Error moving {src_path}: {e}")

print("\nNote: These directories were moved to the 'static/archived/' folder.")
print("If you notice any issues, you can move them back to the 'static/' directory.") 