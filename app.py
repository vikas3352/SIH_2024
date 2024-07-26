from flask import Flask, request, send_from_directory, jsonify
from PIL import Image, ImageEnhance
import pytesseract
import re
import os

app = Flask(__name__)

medical_data = [
    # (Your medical data list here)
]

def preprocess_image(image):
    gray_image = image.convert('L')
    enhance = ImageEnhance.Contrast(gray_image)
    enhanced = enhance.enhance(2.0)
    return enhanced

def extract_text(image):
    text = pytesseract.image_to_string(image, config='--oem 3 --psm 6')
    return text

def find_keywords(text, keywords):
    found_keywords = []
    for keyword in keywords:
        if re.search(re.escape(keyword), text, re.IGNORECASE):
            found_keywords.append(keyword)
    return found_keywords

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        image = Image.open(file)
        processed_image = preprocess_image(image)
        text = extract_text(processed_image)
        found_keywords = find_keywords(text, medical_data)

        if not found_keywords:
            return jsonify('Your degree is not related to our requirements.'), 404
        else:
            return jsonify('Your degree is related to the medical field.'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
