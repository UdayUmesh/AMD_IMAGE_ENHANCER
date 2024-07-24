from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import io
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def auto_tone(image):
    # Convert to LAB color space
    lab = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L-channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    
    # Merge the CLAHE enhanced L-channel back with A and B channels
    limg = cv2.merge((cl, a, b))
    
    # Convert back to RGB color space
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
    
    return final

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/enhance', methods=['POST'])
def enhance():
    logging.debug("Request received")
    logging.debug(f"Request files: {request.files}")
    logging.debug(f"Request form: {request.form}")
    
    if 'file' not in request.files:
        logging.debug("No file part in the request")
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        logging.debug("No selected file")
        return jsonify({'error': 'No selected file'}), 400
    if file:
        try:
            logging.debug("Processing the file")
            image = Image.open(file.stream).convert('RGB')
            enhanced_image = auto_tone(image)
            enhanced_image_pil = Image.fromarray(enhanced_image)
            img_byte_arr = io.BytesIO()
            enhanced_image_pil.save(img_byte_arr, format='JPEG')
            img_byte_arr.seek(0)
            return send_file(
                img_byte_arr,
                mimetype='image/jpeg',
                as_attachment=True,
                download_name='enhanced_image.jpg'
            )
        except Exception as e:
            logging.error(f"Error processing the file: {e}")
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# import cv2
# import numpy as np
# from PIL import Image
# import io
# import logging

# app = Flask(__name__)
# CORS(app)

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# def auto_tone(image):
#     # Convert to LAB color space
#     lab = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2LAB)
#     l, a, b = cv2.split(lab)
    
#     # Apply CLAHE to L-channel
#     clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
#     cl = clahe.apply(l)
    
#     # Merge the CLAHE enhanced L-channel back with A and B channels
#     limg = cv2.merge((cl, a, b))
    
#     # Convert back to RGB color space
#     final = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
    
#     return final

# @app.route('/enhance', methods=['POST'])
# def enhance():
#     logging.debug("Request received")
#     logging.debug(f"Request files: {request.files}")
#     logging.debug(f"Request form: {request.form}")
    
#     if 'file' not in request.files:
#         logging.debug("No file part in the request")
#         return jsonify({'error': 'No file part'}), 400
#     file = request.files['file']
#     if file.filename == '':
#         logging.debug("No selected file")
#         return jsonify({'error': 'No selected file'}), 400
#     if file:
#         try:
#             logging.debug("Processing the file")
#             image = Image.open(file.stream).convert('RGB')
#             enhanced_image = auto_tone(image)
#             enhanced_image_pil = Image.fromarray(enhanced_image)
#             img_byte_arr = io.BytesIO()
#             enhanced_image_pil.save(img_byte_arr, format='JPEG')
#             img_byte_arr.seek(0)
#             return send_file(
#                 img_byte_arr,
#                 mimetype='image/jpeg',
#                 as_attachment=True,
#                 download_name='enhanced_image.jpg'
#             )
#         except Exception as e:
#             logging.error(f"Error processing the file: {e}")
#             return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
