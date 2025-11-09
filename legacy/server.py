from flask import Flask, request
import datetime
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    # Read raw bytes from ESP32
    image_data = request.data

    if not image_data:
        return "No image data received", 400

    # Create unique filename based on timestamp
    filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Save image
    with open(filepath, 'wb') as f:
        f.write(image_data)

    print(f"✅ Image saved: {filepath}")
    return "Image received", 200

if __name__ == '__main__':
    # 0.0.0.0 = accept connections from other devices on the same network
    app.run(host='0.0.0.0', port=5000, debug=True)
   