import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_single_prediction():
    print("Testing /predict endpoint...")
    data = {
        "review_text": "This product is amazing! Highly recommend to everyone. Best purchase ever!"
    }
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_batch_prediction():
    print("Testing /predict_batch endpoint...")
    data = {
        "reviews": [
            "Great product, works perfectly!",
            "Terrible quality, broke immediately.",
            "Amazing! Best thing ever! Highly recommend! Perfect!"
        ]
    }
    response = requests.post(f"{BASE_URL}/predict_batch", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("="*60)
    print("API TESTING SUITE")
    print("="*60 + "\n")
    
    try:
        test_health()
        test_single_prediction()
        test_batch_prediction()
        print("✅ All tests completed!")
    except Exception as e:
        print(f"❌ Error: {e}")
