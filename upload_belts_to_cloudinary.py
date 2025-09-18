import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configuration       
cloudinary.config( 
    cloud_name = "holwfsrwh", 
    api_key = "751324248687953", 
    api_secret = "cWnCSmjPRk6p4-2vqX3_0V6957g",
    secure = True
)

# Directory containing belt images
belt_dir = "static/images/belts"

# Dictionary to store belt URLs
belt_urls = {}

# List of belt images to upload
belt_types = [
    "white", "gray", "graywhite", "grayblack", 
    "yellow", "yellowwhite", "yellowblack",
    "orange", "orangewhite", "orangeblack",
    "green", "greenwhite", "greenblack",
    "blue", "purple", "brown", "black"
]

# Upload each belt image and store its URL
for belt in belt_types:
    image_path = os.path.join(belt_dir, f"{belt}.png")
    if os.path.exists(image_path):
        upload_result = cloudinary.uploader.upload(
            image_path,
            public_id=f"belts/{belt}",
            overwrite=True
        )
        belt_urls[belt] = upload_result["secure_url"]
        print(f"Uploaded {belt}: {belt_urls[belt]}")
    else:
        print(f"Warning: {image_path} not found")

# Print summary of all uploaded belt URLs
print("\nBelt URLs:")
for belt, url in belt_urls.items():
    print(f"{belt}: {url}")

print("\nAdd these URLs to your templates to reference the Cloudinary-hosted belt images") 