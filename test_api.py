"""
Sample script to test the Video Action Recognition API
This script demonstrates how to programmatically interact with the Flask API
"""

import requests
import json
import sys
import os

# Configuration
API_URL = "http://localhost:5000"
PREDICT_ENDPOINT = f"{API_URL}/predict"
HEALTH_ENDPOINT = f"{API_URL}/health"


def check_health():
    """Check if the API is running and healthy"""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API Status:", data['status'])
            print("✅ Model Loaded:", data['model_loaded'])
            return True
        else:
            print("❌ API returned error:", response.status_code)
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is the server running?")
        print("   Start the server with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error checking health: {str(e)}")
        return False


def predict_video(video_path):
    """Send video to API and get prediction"""
    
    # Check if file exists
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        return None
    
    # Check file size
    file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
    print(f"📁 File size: {file_size:.2f} MB")
    
    if file_size > 100:
        print("⚠️  Warning: File size exceeds 100MB limit")
        return None
    
    print(f"📤 Uploading: {os.path.basename(video_path)}")
    print("⏳ Processing... (this may take 10-30 seconds)")
    
    try:
        # Open and send file
        with open(video_path, 'rb') as video_file:
            files = {'video': video_file}
            response = requests.post(PREDICT_ENDPOINT, files=files, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print("\n" + "="*60)
                print("🎯 PREDICTION RESULTS")
                print("="*60)
                print(f"\n🎬 Predicted Action: {data['predicted_action']}")
                print(f"📊 Confidence: {data['confidence']*100:.2f}%")
                print(f"\n📈 All Predictions:")
                print("-"*60)
                
                for pred in data['all_predictions']:
                    label = pred['label']
                    conf = pred['confidence'] * 100
                    bar_length = int(conf / 2)  # Scale to 50 chars max
                    bar = "█" * bar_length + "░" * (50 - bar_length)
                    print(f"{label:20s} {bar} {conf:5.2f}%")
                
                print("="*60 + "\n")
                return data
            else:
                print(f"❌ Prediction failed: {data.get('error', 'Unknown error')}")
                return None
        else:
            print(f"❌ Server error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error message: {error_data.get('error', 'Unknown')}")
            except:
                print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout. Video processing took too long.")
        return None
    except Exception as e:
        print(f"❌ Error making prediction: {str(e)}")
        return None


def main():
    """Main function"""
    print("\n" + "="*60)
    print("VIDEO ACTION RECOGNITION - API TEST SCRIPT")
    print("="*60 + "\n")
    
    # Check API health
    print("1. Checking API health...")
    if not check_health():
        print("\n⚠️  Please start the Flask server first:")
        print("   python app.py")
        sys.exit(1)
    
    print("\n✅ API is ready!\n")
    
    # Get video path from command line or prompt
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        video_path = input("Enter video file path (or drag & drop): ").strip('"').strip("'")
    
    if not video_path:
        print("❌ No video path provided")
        sys.exit(1)
    
    # Make prediction
    print(f"\n2. Processing video: {video_path}\n")
    result = predict_video(video_path)
    
    if result:
        print("✅ Test completed successfully!")
        
        # Optionally save results to JSON
        save = input("\n💾 Save results to JSON file? (y/n): ").lower()
        if save == 'y':
            output_file = 'prediction_results.json'
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"✅ Results saved to: {output_file}")
    else:
        print("❌ Test failed")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
