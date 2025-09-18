import cloudinary
import cloudinary.uploader
import os
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'focus.settings')
import django
django.setup()

from focus.settings import CLOUDINARY_STORAGE

# Configure Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET']
)

# Upload the logo
try:
    # Find the logo file - using the same one as the login page
    logo_path = "static/images/focus_logo_new.jpg"
    if not os.path.exists(logo_path):
        print(f"Logo file not found at {logo_path}")
        sys.exit(1)
    
    print("Uploading logo to Cloudinary...")
    result = cloudinary.uploader.upload(
        logo_path,
        public_id="focus_logo",
        folder="email_templates",
        overwrite=True
    )
    
    print("✅ Logo uploaded successfully!")
    print(f"Cloudinary URL: {result['secure_url']}")
    print(f"Public ID: {result['public_id']}")
    
    # Save the URL to a file for easy access
    with open("cloudinary_logo_url.txt", "w") as f:
        f.write(result['secure_url'])
    
    print("URL saved to cloudinary_logo_url.txt")
    
except Exception as e:
    print(f"❌ Error uploading to Cloudinary: {e}")
    sys.exit(1) 