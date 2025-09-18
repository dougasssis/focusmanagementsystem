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

# Upload the banner image
try:
    image_path = "static/images/background_focus3.png"
    if not os.path.exists(image_path):
        print(f"Image file not found at {image_path}")
        sys.exit(1)

    print(f"Uploading {image_path} to Cloudinary...")
    result = cloudinary.uploader.upload(
        image_path,
        public_id="email_banner",
        folder="email_templates",
        overwrite=True
    )

    print("✅ Image uploaded successfully!")
    banner_url = result['secure_url']
    print(f"Cloudinary URL: {banner_url}")

    # Save the URL to a file for easy access
    with open("cloudinary_banner_url.txt", "w") as f:
        f.write(banner_url)

    print("URL saved to cloudinary_banner_url.txt")

except Exception as e:
    print(f"❌ Error uploading to Cloudinary: {e}")
    sys.exit(1) 