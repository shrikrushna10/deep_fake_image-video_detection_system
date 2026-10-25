"""
Script to create sample test images and videos covering the three user-specified criteria:
1. Real / Original (Camera Captured with hardware EXIF)
2. Fake / AI Generated (Synthetic AI spectrum & generative tags)
3. Not Original (Reshared WhatsApp / Web-compressed stripped image)
And corresponding video samples.
"""

import os
import io
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import piexif

os.makedirs("samples", exist_ok=True)

# -------------------------------------------------------------
# 1. Real / Original Camera Captured Sample
# -------------------------------------------------------------
def make_real_camera_sample():
    width, height = 800, 600
    # Create natural outdoor landscape gradient with organic tree/mountain shapes
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Sky gradient
    for y in range(int(height * 0.6)):
        r = int(110 + (y / (height * 0.6)) * 40)
        g = int(160 + (y / (height * 0.6)) * 40)
        b = int(220 + (y / (height * 0.6)) * 25)
        img[y, :] = [b, g, r]
        
    # Mountain shapes
    pts = np.array([[0, 360], [180, 240], [350, 340], [520, 220], [680, 310], [800, 250], [800, 600], [0, 600]], np.int32)
    cv2.fillPoly(img, [pts], (45, 90, 50))
    
    # Foreground grass
    pts2 = np.array([[0, 420], [250, 410], [500, 440], [800, 420], [800, 600], [0, 600]], np.int32)
    cv2.fillPoly(img, [pts2], (30, 130, 40))
    
    # Add genuine camera Poisson-Gaussian sensor shot noise (PRNU)
    noise = np.random.normal(0, 4.5, (height, width, 3)).astype(np.float32)
    img_noisy = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    
    pil_img = Image.fromarray(cv2.cvtColor(img_noisy, cv2.COLOR_BGR2RGB))
    
    # Add rich authentic EXIF metadata matching Apple iPhone 15 Pro
    zeroth_ifd = {
        piexif.ImageIFD.Make: b"Apple",
        piexif.ImageIFD.Model: b"iPhone 15 Pro",
        piexif.ImageIFD.Software: b"17.5.1",
        piexif.ImageIFD.DateTime: b"2026:09:15 10:14:32"
    }
    exif_ifd = {
        piexif.ExifIFD.DateTimeOriginal: b"2026:09:15 10:14:32",
        piexif.ExifIFD.ExposureTime: (1, 240),
        piexif.ExifIFD.FNumber: (178, 100),
        piexif.ExifIFD.ISOSpeedRatings: 64,
        piexif.ExifIFD.FocalLength: (686, 100),
        piexif.ExifIFD.LensModel: b"iPhone 15 Pro back camera 6.86mm f/1.78"
    }
    exif_dict = {"0th": zeroth_ifd, "Exif": exif_ifd}
    exif_bytes = piexif.dump(exif_dict)
    
    out_path = os.path.join("samples", "camera_captured_sample.jpg")
    pil_img.save(out_path, "JPEG", exif=exif_bytes, quality=95)
    print("Created:", out_path)

# -------------------------------------------------------------
# 2. Fake / AI Generated Sample
# -------------------------------------------------------------
def make_ai_generated_sample():
    width, height = 512, 512
    # Create synthetic generative-looking image with characteristic diffusion high-frequency grid & smooth surfaces
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Surreal AI color gradient
    for y in range(height):
        for x in range(width):
            r = int(127 + 127 * np.sin(x * 0.02 + y * 0.015))
            g = int(127 + 127 * np.cos(y * 0.02 - x * 0.01))
            b = int(180 + 75 * np.sin((x + y) * 0.01))
            img[y, x] = [b, g, r]
            
    # Add characteristic periodic grid artifacts from transposed convolution / latent upsampling
    grid_pattern = np.zeros((height, width), dtype=np.float32)
    grid_pattern[::16, :] += 14.0
    grid_pattern[:, ::16] += 14.0
    for c in range(3):
        img[:, :, c] = np.clip(img[:, :, c].astype(np.float32) + grid_pattern, 0, 255).astype(np.uint8)
        
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    # Embed AI generative metadata (Midjourney / Stable Diffusion / DALL-E)
    ai_prompt_comment = (
        "parameters: Cinematic futuristic portrait, ultra detailed, ray tracing, "
        "photorealistic, octane render. Steps: 30, Sampler: DPM++ 2M Karras, "
        "CFG scale: 7.0, Seed: 3948271049, Model: Midjourney_SDXL_v6, "
        "AI Generator: ChatGPT DALL-E 3 / Gemini Imagen"
    )
    
    zeroth_ifd = {
        piexif.ImageIFD.Software: b"Stable Diffusion WebUI / ComfyUI",
        piexif.ImageIFD.ImageDescription: ai_prompt_comment.encode('utf-8')
    }
    exif_ifd = {
        piexif.ExifIFD.UserComment: ai_prompt_comment.encode('utf-8')
    }
    exif_dict = {"0th": zeroth_ifd, "Exif": exif_ifd}
    exif_bytes = piexif.dump(exif_dict)
    
    out_path = os.path.join("samples", "ai_generated_sample.jpg")
    pil_img.save(out_path, "JPEG", exif=exif_bytes, quality=90)
    print("Created:", out_path)

# -------------------------------------------------------------
# 3. Not Original (Reshared / Unedited WhatsApp Media)
# -------------------------------------------------------------
def make_reshared_sample():
    # A real scene, but stripped of EXIF, saved with WhatsApp naming and re-compression
    width, height = 720, 540
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Real room / table scene
    cv2.rectangle(img, (0, 0), (width, height), (220, 215, 205), -1) # Wall
    cv2.rectangle(img, (0, 350), (width, height), (60, 45, 35), -1)   # Wooden table
    # Coffee cup
    cv2.ellipse(img, (360, 370), (50, 20), 0, 0, 360, (245, 245, 245), -1)
    cv2.ellipse(img, (360, 350), (50, 15), 0, 0, 360, (50, 80, 120), -1)
    
    # Real camera sensor noise
    noise = np.random.normal(0, 3.8, (height, width, 3)).astype(np.float32)
    img_noisy = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    
    pil_img = Image.fromarray(cv2.cvtColor(img_noisy, cv2.COLOR_BGR2RGB))
    
    # Reshared via WhatsApp: Stripped EXIF, standard social media compression quality ~72
    out_path = os.path.join("samples", "IMG-20260918-WA0034.jpg")
    pil_img.save(out_path, "JPEG", quality=72)
    print("Created:", out_path)

# -------------------------------------------------------------
# 4. Video Samples (Camera Captured vs AI Generated)
# -------------------------------------------------------------
def make_video_samples():
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # 4a. Real Camera Video
    real_vid_path = os.path.join("samples", "camera_captured_video.mp4")
    out_real = cv2.VideoWriter(real_vid_path, fourcc, 24.0, (320, 240))
    for i in range(48): # 2 seconds
        frame = np.zeros((240, 320, 3), dtype=np.uint8)
        # Background
        frame[:] = (70, 60, 50)
        # Moving physical object smoothly
        x = int(60 + i * 4)
        cv2.circle(frame, (x, 120), 28, (60, 180, 240), -1)
        # Steady camera sensor noise
        noise = np.random.normal(0, 3.2, (240, 320, 3)).astype(np.float32)
        frame_noisy = np.clip(frame.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        out_real.write(frame_noisy)
    out_real.release()
    print("Created:", real_vid_path)
    
    # 4b. AI Generated Video (Flickering / Morphing / Sora Runway style)
    ai_vid_path = os.path.join("samples", "sora_ai_generated_video.mp4")
    out_ai = cv2.VideoWriter(ai_vid_path, fourcc, 24.0, (320, 240))
    for i in range(48):
        frame = np.zeros((240, 320, 3), dtype=np.uint8)
        # Morphing unnatural background colors
        bg_col = (int(100 + 40 * np.sin(i * 0.4)), int(80 + 60 * np.cos(i * 0.3)), int(140 + 50 * np.sin(i * 0.2)))
        frame[:] = bg_col
        # Morphing shape (radius and position jittering unnaturally)
        rad = int(30 + 15 * np.sin(i * 0.8))
        x = int(160 + 20 * np.cos(i * 0.5))
        y = int(120 + 25 * np.sin(i * 0.9))
        cv2.circle(frame, (x, y), max(10, rad), (240, 200, 50), -1)
        out_ai.write(frame)
    out_ai.release()
    print("Created:", ai_vid_path)

    # 4c. Reshared WhatsApp Video (Real camera scene recompressed without camera tags)
    reshared_vid_path = os.path.join("samples", "VID-20260918-WA0012.mp4")
    out_wa = cv2.VideoWriter(reshared_vid_path, fourcc, 24.0, (320, 240))
    for i in range(48):
        frame = np.zeros((240, 320, 3), dtype=np.uint8)
        frame[:] = (90, 85, 80)
        # Slow moving real object
        x = int(50 + i * 2)
        cv2.circle(frame, (x, 120), 25, (120, 200, 150), -1)
        noise = np.random.normal(0, 2.5, (240, 320, 3)).astype(np.float32)
        frame_noisy = np.clip(frame.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        out_wa.write(frame_noisy)
    out_wa.release()
    print("Created:", reshared_vid_path)

if __name__ == "__main__":
    make_real_camera_sample()
    make_ai_generated_sample()
    make_reshared_sample()
    make_video_samples()
    print("All sample assets generated successfully!")
