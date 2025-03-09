import os
import requests

def download_file(url, output_path):
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded to {output_path}")

# Create the models directory if it doesn't exist
os.makedirs("backend/models", exist_ok=True)

# Download RealESRGAN model
download_file(
    "https://drive.google.com/file/d/1X1oLnl5vgtdVzxLGSxGUW_YjkOjalwna/view?usp=drive_link",
    "backend/models/RealESRGAN_x4plus.pth"
)

# Download GFPGAN model
download_file(
    "https://drive.google.com/file/d/1ySSattZX_NUDMEq_7ntVeHfrQg_hemaO/view?usp=drive_link",
    "backend/models/GFPGANv1.3.pth"
)