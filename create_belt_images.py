import os
from PIL import Image, ImageDraw
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configuration
cloudinary.config(
    cloud_name="holwfsrwh",
    api_key="751324248687953",
    api_secret="cWnCSmjPRk6p4-2vqX3_0V6957g",
    secure=True
)

# Create directory for generated belt images
output_dir = "generated_belts"
os.makedirs(output_dir, exist_ok=True)

# Belt colors (RGB)
colors = {
    "white": (255, 255, 255),
    "gray": (169, 169, 169),
    "yellow": (255, 215, 0),
    "orange": (255, 140, 0),
    "green": (0, 128, 0),
    "blue": (52, 144, 220),
    "purple": (149, 97, 226),
    "brown": (138, 109, 59),
    "black": (42, 42, 42)
}

# Belt dimensions
width = 300
height = 60

# Generate and upload belt images
belt_urls = {}

# Helper to create belt image
def create_belt_image(colors_list, filename):
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    if len(colors_list) == 1:
        # Solid color belt
        draw.rectangle([(0, 0), (width, height)], fill=colors_list[0])
    else:
        # Two-tone belt (split in half horizontally)
        draw.rectangle([(0, 0), (width // 2, height)], fill=colors_list[0])
        draw.rectangle([(width // 2, 0), (width, height)], fill=colors_list[1])
    
    # Add a border
    draw.rectangle([(0, 0), (width-1, height-1)], outline=(100, 100, 100))
    
    # Save the image
    img_path = os.path.join(output_dir, filename)
    img.save(img_path)
    return img_path

# Generate single color belts
for name, color in colors.items():
    filename = f"{name}.png"
    img_path = create_belt_image([color], filename)
    
    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(
        img_path,
        public_id=f"belts/{name}",
        overwrite=True
    )
    belt_urls[name] = upload_result["secure_url"]
    print(f"Uploaded {name}: {belt_urls[name]}")

# Generate mixed color belts
mixed_belts = [
    ("graywhite", "gray", "white"),
    ("grayblack", "gray", "black"),
    ("yellowwhite", "yellow", "white"),
    ("yellowblack", "yellow", "black"),
    ("orangewhite", "orange", "white"),
    ("orangeblack", "orange", "black"),
    ("greenwhite", "green", "white"),
    ("greenblack", "green", "black")
]

for belt_name, color1_name, color2_name in mixed_belts:
    filename = f"{belt_name}.png"
    img_path = create_belt_image([colors[color1_name], colors[color2_name]], filename)
    
    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(
        img_path,
        public_id=f"belts/{belt_name}",
        overwrite=True
    )
    belt_urls[belt_name] = upload_result["secure_url"]
    print(f"Uploaded {belt_name}: {belt_urls[belt_name]}")

# Print summary of all uploaded belt URLs
print("\nBelt URLs:")
for belt, url in belt_urls.items():
    print(f"{belt}: {url}")

print("\nAdd these URLs to your templates to reference the Cloudinary-hosted belt images.") 