from flask import Flask, request, jsonify
import os
from PIL import Image
import numpy as np
import torch
from realesrgan import RealESRGANer
from colorization import colorize_image  # We'll create this later

app = Flask(__name__)

# Initialize Real-ESRGAN model
model = RealESRGANer(
    scale=4,
    model_path='models/RealESRGAN_x4plus.pth',
    model=None,
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=False
)

@app.route('/enhance', methods=['POST'])
def enhance_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    resolution = int(request.form['resolution'])
    colorize = request.form.get('colorize') == 'true'

    # Save the uploaded image
    input_path = 'static/input_image.png'
    file.save(input_path)

    # Enhance the image using Real-ESRGAN
    img = Image.open(input_path).convert('RGB')
    img = np.array(img)
    output, _ = model.enhance(img, outscale=resolution / max(img.shape[:2]))

    # Colorize the image if requested
    if colorize:
        output = colorize_image(output)

    # Save the enhanced image
    output_img = Image.fromarray(output)
    output_path = 'static/enhanced_image.png'
    output_img.save(output_path)

    # Return the enhanced image URL
    return jsonify({'url': f'/{output_path}'})

if __name__ == '__main__':
    app.run(debug=True)