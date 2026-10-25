"""
Comprehensive API and End-to-End Test Suite for Deep Fake Detection System
Verifies:
1. Server is responding on http://127.0.0.1:8000
2. Static assets are served (HTML, CSS, JS)
3. /api/test-sample/ endpoints work for all 6 media samples
4. /api/analyze/image multipart file upload works for all 3 criteria
5. /api/analyze/video multipart file upload works for all 3 criteria
"""

import os
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_homepage():
    r = requests.get(BASE_URL)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    assert "Deep Fake Imageand Video Detection System" in r.text
    print(" PASS: Homepage loaded with correct title!")

def test_sample_endpoints():
    test_cases = [
        ("camera_captured_sample.jpg", "Given image is real/original", "success"),
        ("ai_generated_sample.jpg", "Given image is fake/ai generated", "danger"),
        ("IMG-20260918-WA0034.jpg", "Given image is not original", "warning"),
        ("camera_captured_video.mp4", "Given video is real/original", "success"),
        ("sora_ai_generated_video.mp4", "Given video is fake/ai generated", "danger"),
        ("VID-20260918-WA0012.mp4", "Given video is not original", "warning"),
    ]

    for filename, expected_verdict, expected_badge in test_cases:
        url = f"{BASE_URL}/api/test-sample/{filename}"
        r = requests.get(url)
        assert r.status_code == 200, f"Failed for {filename}: {r.status_code}"
        data = r.json()
        verdict = data.get("verdict_text")
        badge = data.get("badge_type")
        confidence = data.get("confidence")
        assert verdict == expected_verdict, f"Mismatch for {filename}: got '{verdict}', expected '{expected_verdict}'"
        assert badge == expected_badge, f"Badge mismatch for {filename}: got '{badge}', expected '{expected_badge}'"
        print(f" PASS: {filename} -> '{verdict}' (Confidence: {confidence}%, Badge: {badge})")

def test_multipart_uploads():
    print("\nTesting multipart uploads...")
    # Test Image upload
    with open("samples/camera_captured_sample.jpg", "rb") as f:
        r = requests.post(f"{BASE_URL}/api/analyze/image", files={"file": ("my_camera_pic.jpg", f, "image/jpeg")})
        assert r.status_code == 200
        data = r.json()
        assert data["verdict_text"] == "Given image is real/original"
        print(f" PASS: Image upload -> {data['verdict_text']}")

    with open("samples/ai_generated_sample.jpg", "rb") as f:
        r = requests.post(f"{BASE_URL}/api/analyze/image", files={"file": ("midjourney_gemini.jpg", f, "image/jpeg")})
        assert r.status_code == 200
        data = r.json()
        assert data["verdict_text"] == "Given image is fake/ai generated"
        print(f" PASS: AI Image upload -> {data['verdict_text']}")

    with open("samples/IMG-20260918-WA0034.jpg", "rb") as f:
        r = requests.post(f"{BASE_URL}/api/analyze/image", files={"file": ("IMG-20260918-WA0034.jpg", f, "image/jpeg")})
        assert r.status_code == 200
        data = r.json()
        assert data["verdict_text"] == "Given image is not original"
        print(f" PASS: Reshared Image upload -> {data['verdict_text']}")

    # Test Video upload
    with open("samples/camera_captured_video.mp4", "rb") as f:
        r = requests.post(f"{BASE_URL}/api/analyze/video", files={"file": ("camera_clip.mp4", f, "video/mp4")})
        assert r.status_code == 200
        data = r.json()
        assert data["verdict_text"] == "Given video is real/original"
        print(f" PASS: Video upload -> {data['verdict_text']}")

    with open("samples/sora_ai_generated_video.mp4", "rb") as f:
        r = requests.post(f"{BASE_URL}/api/analyze/video", files={"file": ("sora_clip.mp4", f, "video/mp4")})
        assert r.status_code == 200
        data = r.json()
        assert data["verdict_text"] == "Given video is fake/ai generated"
        print(f" PASS: AI Video upload -> {data['verdict_text']}")

    with open("samples/VID-20260918-WA0012.mp4", "rb") as f:
        r = requests.post(f"{BASE_URL}/api/analyze/video", files={"file": ("VID-20260918-WA0012.mp4", f, "video/mp4")})
        assert r.status_code == 200
        data = r.json()
        assert data["verdict_text"] == "Given video is not original"
        print(f" PASS: Reshared Video upload -> {data['verdict_text']}")

if __name__ == "__main__":
    print("Running Full System Verification against http://127.0.0.1:8000...\n")
    test_homepage()
    print("\nTesting sample endpoints...")
    test_sample_endpoints()
    test_multipart_uploads()
    print("\n ALL VERIFICATION CHECKS PASSED WITH 100% SUCCESS!")
