# Testing Guide - Video Action Recognition

## Quick Start

### Option 1: Using Run Scripts

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

### Option 2: Manual Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open browser to `http://localhost:5000`

## Testing the Application

### 1. Web Interface Testing

1. **Upload a Video**
   - Click on the upload area or drag & drop a video file
   - Supported formats: MP4, AVI, MOV, MKV, WMV
   - Max file size: 100MB

2. **Get Predictions**
   - Click "Predict Action" button
   - Wait for processing (may take 10-30 seconds)
   - View results with confidence scores

3. **Expected Actions**
   The model can recognize these 6 actions:
   - CricketShot
   - PlayingCello
   - Punch
   - ShavingBeard
   - TennisSwing
   - WritingOnBoard

### 2. API Testing

#### Test with curl (Upload video)

```bash
curl -X POST -F "video=@path/to/your/video.mp4" http://localhost:5000/predict
```

#### Test with Python

```python
import requests

url = "http://localhost:5000/predict"
files = {'video': open('path/to/video.mp4', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

#### Health Check

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## Sample Test Videos

For testing, you can:

1. **Download UCF101 Dataset samples** from:
   - https://www.crcv.ucf.edu/data/UCF101.php

2. **Record your own videos**:
   - Record short clips (3-10 seconds) of the supported actions
   - Use any camera or smartphone
   - Keep good lighting and clear action visibility

3. **Use online video samples**:
   - Search for free stock videos of the supported actions
   - Ensure the video clearly shows the action

## Expected Results

### Good Predictions
- **High Confidence (>70%)**: Clear, well-lit video with focused action
- **Medium Confidence (40-70%)**: Partially visible or ambiguous action
- **Low Confidence (<40%)**: Unclear video or action not in training set

### Model Performance
- Test Accuracy: 93.75%
- Training was on UCF101 subset with 6 classes
- Best results on videos similar to training data

## Troubleshooting

### Model Not Loading
```
Error: Cannot load model file
Solution: Ensure ucf101_mobilenet_lstm.h5 is in the root directory
```

### Video Processing Errors
```
Error: Cannot open video
Solution: 
- Check video format (MP4, AVI, MOV, MKV, WMV)
- Ensure video is not corrupted
- Try converting to MP4 format
```

### Out of Memory
```
Error: OOM when processing
Solution:
- Use shorter videos (under 30 seconds)
- Reduce video resolution before upload
- Close other applications
```

### Slow Predictions
```
Issue: Taking too long to predict
Solutions:
- Expected time: 10-30 seconds per video
- Use GPU if available (TensorFlow GPU)
- Reduce video length
```

## Performance Optimization

### For CPU:
```python
# In app.py, add at the top:
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
```

### For GPU (if available):
```bash
pip install tensorflow-gpu==2.15.0
```

## Directory Structure After Setup

```
Assignment 3(221415)/
├── app.py                      # Flask application ✓
├── templates/
│   └── index.html             # Web interface ✓
├── uploads/                    # Created automatically
├── ucf101_mobilenet_lstm.h5   # Model file ✓
├── requirements.txt           # Dependencies ✓
├── run.bat                    # Windows startup ✓
├── run.sh                     # Linux/Mac startup ✓
├── .gitignore                 # Git ignore rules ✓
├── TESTING.md                 # This file ✓
└── README.md                  # Documentation ✓
```

## API Response Examples

### Successful Prediction
```json
{
  "success": true,
  "predicted_action": "Punch",
  "confidence": 0.9456,
  "all_predictions": [
    {"label": "Punch", "confidence": 0.9456},
    {"label": "CricketShot", "confidence": 0.0234},
    {"label": "TennisSwing", "confidence": 0.0156},
    {"label": "PlayingCello", "confidence": 0.0089},
    {"label": "ShavingBeard", "confidence": 0.0042},
    {"label": "WritingOnBoard", "confidence": 0.0023}
  ]
}
```

### Error Response
```json
{
  "error": "Invalid file format. Allowed formats: mp4, avi, mov, mkv, wmv"
}
```

## Browser Compatibility

Tested and working on:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

## Interview Preparation

Key points to explain:

1. **Architecture**: MobileNetV2 for spatial features + LSTM for temporal
2. **Preprocessing**: Extract 10 frames, resize to 224x224, MobileNet preprocessing
3. **Training**: 30 epochs on UCF101 subset, 93.75% test accuracy
4. **API Design**: RESTful POST endpoint for predictions
5. **Frontend**: Modern, responsive UI with drag-drop support
6. **Error Handling**: File validation, size limits, error messages

## Performance Metrics

- **Inference Time**: ~10-30 seconds per video (CPU)
- **Memory Usage**: ~2-4GB RAM during prediction
- **Model Size**: ~11.37 MB
- **Supported Video Length**: Up to 2 minutes (optimal: 3-10 seconds)

## Contact

For issues or questions, refer to the course instructor or raise an issue in the repository.

---

**Happy Testing! 🎬🚀**
