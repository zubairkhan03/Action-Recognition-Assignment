# Quick Reference - Video Action Recognition App

## 🚀 Quick Start Commands

### Windows
```bash
run.bat
```

### Linux/Mac
```bash
chmod +x run.sh && ./run.sh
```

### Manual Start
```bash
pip install -r requirements.txt
python app.py
```

## 🌐 Access Points

- **Web Interface**: http://localhost:5000
- **API Endpoint**: http://localhost:5000/predict
- **Health Check**: http://localhost:5000/health

## 📝 File Structure

```
Root Directory/
├── app.py                    # Main Flask application
├── templates/index.html      # Web UI
├── ucf101_mobilenet_lstm.h5 # Trained model (REQUIRED)
├── requirements.txt          # Dependencies
└── uploads/                  # Auto-created temp folder
```

## 🎯 Supported Actions

1. CricketShot
2. PlayingCello  
3. Punch
4. ShavingBeard
5. TennisSwing
6. WritingOnBoard

## 📹 Video Requirements

- **Formats**: MP4, AVI, MOV, MKV, WMV
- **Max Size**: 100MB
- **Recommended**: 3-10 seconds, clear action visibility

## 💡 Tips for Best Results

1. Use well-lit videos
2. Keep action centered in frame
3. Avoid shaky camera
4. Use videos similar to UCF101 dataset
5. Keep file size under 50MB for faster processing

## 🔧 Dependencies

```
Flask 3.0.0
TensorFlow 2.15.0
OpenCV 4.8.1
NumPy 1.24.3
Werkzeug 3.0.1
```

## ⚡ API Examples

### cURL
```bash
curl -X POST -F "video=@video.mp4" http://localhost:5000/predict
```

### Python
```python
import requests
response = requests.post(
    'http://localhost:5000/predict',
    files={'video': open('video.mp4', 'rb')}
)
print(response.json())
```

### JavaScript
```javascript
const formData = new FormData();
formData.append('video', fileInput.files[0]);

fetch('/predict', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Port 5000 busy | Change port in app.py: `app.run(port=5001)` |
| Model not found | Ensure .h5 file is in root directory |
| Slow prediction | Use shorter videos or GPU acceleration |
| Out of memory | Close other apps, use smaller videos |

## 📊 Model Info

- **Architecture**: MobileNetV2 + LSTM
- **Input**: 10 frames at 224x224 pixels
- **Training**: UCF101 subset, 6 classes
- **Accuracy**: 93.75% on test set

## 🎓 For Presentation/Interview

**Key Points to Explain:**

1. **CNN (MobileNetV2)**: Extracts spatial features from each frame
2. **LSTM**: Captures temporal relationships between frames
3. **TimeDistributed**: Applies CNN to each frame independently
4. **Preprocessing**: Frame extraction, resizing, normalization
5. **API**: RESTful design with POST endpoint
6. **Frontend**: Modern UI with drag-drop, animations
7. **Dataset**: UCF101 - standard action recognition benchmark

## 📞 Getting Help

1. Check TESTING.md for detailed testing guide
2. Review README.md for full documentation
3. Check Flask logs in terminal for errors
4. Verify all files are present
5. Ensure Python 3.8+ is installed

---

**Made with ❤️ for Deep Learning Assignment**
**Student ID: 221415**
