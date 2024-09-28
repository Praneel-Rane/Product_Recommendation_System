from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from services.recommendation_service import process_image_and_recommend

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "AI Product Recommendation Backend is running!"

# Image upload route
@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected image'}), 400

    # Save the uploaded image
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    # Delegate image processing and recommendation to the service
    recommendations = process_image_and_recommend(image_path)

    return jsonify(recommendations), 200

if __name__ == '__main__':
    app.run(debug=True)
