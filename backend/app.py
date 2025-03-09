from flask import Flask, request, jsonify
import os
from PIL import Image
import numpy as np
import cv2
import torch
from realesrgan import RealESRGANer
from gfpgan import GFPGANer

app = Flask(__name__)

# Initialize Real-ESRGAN for upscaling
upscaler = RealESRGANer(
    scale=4,
    model_path='models/RealESRGAN_x4plus.pth',
    model=None,
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=False
)

# Initialize GFPGAN for face enhancement
face_enhancer = GFPGANer(
    model_path='models/GFPGANv1.3.pth',
    upscale=1,
    arch='clean',
    channel_multiplier=2,
    bg_upsampler=None
)

def reduce_noise(image):
    """Reduce noise using OpenCV's fastNlMeansDenoisingColored."""
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

def enhance_faces(image):
    """Enhance faces using GFPGAN."""
    _, _, output = face_enhancer.enhance(image, has_aligned=False, only_center_face=False, paste_back=True)
    return output

@app.route('/enhance', methods=['POST'])
def enhance_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    resolution = int(request.form['resolution'])
    sharpness = int(request.form.get('sharpness', 50))
    colorize = request.form.get('colorize') == 'true'

    # Save the uploaded image
    input_path = 'static/input_image.png'
    file.save(input_path)

    # Open the image
    img = Image.open(input_path).convert('RGB')
    img = np.array(img)

    # Reduce noise
    img = reduce_noise(img)

    # Enhance faces (if the image contains faces)
    img = enhance_faces(img)

    # Upscale the image
    output, _ = upscaler.enhance(img, outscale=resolution / max(img.shape[:2]))

    # Adjust sharpness
    if sharpness != 50:
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * (sharpness / 50)
        output = cv2.filter2D(output, -1, kernel)

    # Save the enhanced image
    output_img = Image.fromarray(output)
    output_path = 'static/enhanced_image.png'
    output_img.save(output_path)

    # Return the enhanced image URL
    return jsonify({'url': f'/{output_path}'})

if __name__ == '__main__':
    app.run(debug=True)