from flask import Flask, render_template, request, jsonify
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv', 'wmv'}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Model parameters
IMG_SIZE = 224
FRAMES_PER_VIDEO = 10
MODEL_PATH = 'ucf101_mobilenet_lstm.h5'

# UCF101 action classes (based on the notebook output showing 6 classes)
# These are common UCF101 classes, adjust based on your actual training
ACTION_CLASSES = [
    'CricketShot',
    'PlayingCello',
    'Punch',
    'ShavingBeard',
    'TennisSwing',
    'WritingOnBoard'
]

# Load the model
print("Loading model...")
model = load_model(MODEL_PATH)
print("Model loaded successfully!")


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def extract_frames(video_path, num_frames=FRAMES_PER_VIDEO):
    """Extract frames from video for prediction"""
    cap = cv2.VideoCapture(video_path)
    frames = []
    
    if not cap.isOpened():
        print("Cannot open video:", video_path)
        return None
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        cap.release()
        print("Empty video:", video_path)
        return None
    
    step = max(total_frames // num_frames, 1)
    
    for i in range(num_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * step)
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
        frame = preprocess_input(frame)
        frames.append(frame)
    
    cap.release()
    
    # Pad frames if fewer than num_frames
    while len(frames) < num_frames:
        if frames:
            frames.append(frames[-1])
        else:
            frames.append(np.zeros((IMG_SIZE, IMG_SIZE, 3)))
    
    return np.array(frames)


def predict_action(video_path):
    """Predict action from video"""
    # Extract frames
    frames = extract_frames(video_path, num_frames=FRAMES_PER_VIDEO)
    
    if frames is None:
        return None, None
    
    # Add batch dimension
    frames = np.expand_dims(frames, axis=0)
    
    # Predict
    predictions = model.predict(frames, verbose=0)
    pred_class_idx = np.argmax(predictions, axis=1)[0]
    confidence = float(predictions[0][pred_class_idx])
    
    # Get predicted label
    if pred_class_idx < len(ACTION_CLASSES):
        pred_label = ACTION_CLASSES[pred_class_idx]
    else:
        pred_label = f"Class_{pred_class_idx}"
    
    # Get all class probabilities
    all_predictions = []
    for idx, prob in enumerate(predictions[0]):
        if idx < len(ACTION_CLASSES):
            label = ACTION_CLASSES[idx]
        else:
            label = f"Class_{idx}"
        all_predictions.append({
            'label': label,
            'confidence': float(prob)
        })
    
    # Sort by confidence
    all_predictions.sort(key=lambda x: x['confidence'], reverse=True)
    
    return pred_label, confidence, all_predictions


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', action_classes=ACTION_CLASSES)


@app.route('/predict', methods=['POST'])
def predict():
    """Handle video upload and prediction"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    
    if file.filename == '':
        return jsonify({'error': 'No video selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file format. Allowed formats: mp4, avi, mov, mkv, wmv'}), 400
    
    try:
        # Save uploaded video
        filename = secure_filename(file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)
        
        # Make prediction
        pred_label, confidence, all_predictions = predict_action(video_path)
        
        if pred_label is None:
            return jsonify({'error': 'Failed to process video'}), 500
        
        # Clean up uploaded file
        os.remove(video_path)
        
        return jsonify({
            'success': True,
            'predicted_action': pred_label,
            'confidence': confidence,
            'all_predictions': all_predictions
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
