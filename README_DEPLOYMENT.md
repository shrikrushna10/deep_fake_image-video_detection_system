# Deployment Guide - Deepfake Detection System

This guide outlines how to deploy the **Deep Fake Image and Video Detection System** to the cloud or share it publicly.

---

## 🚀 1. Local Live Server (Currently Running)

The application is currently running live on your machine:
- **Local URL:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive API Docs (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative Docs (ReDoc):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

To restart the server manually in the future:
```powershell
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

---

## 🌐 2. Deploy to Render.com (Recommended Free Cloud Hosting)

Render provides free hosting for Python FastAPI web services with automatic HTTPS:

1. **Push your code to GitHub:**
   - Create a new repository on [GitHub](https://github.com/new).
   - Push this directory to your GitHub repository.
2. **Create Web Service on Render:**
   - Go to [dashboard.render.com](https://dashboard.render.com/).
   - Click **New +** > **Web Service**.
   - Select your GitHub repository.
3. **Configure Settings:**
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt && python create_samples.py`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
4. Click **Deploy Web Service**. Render will provision your app with a free `https://your-app.onrender.com` domain.

*(Note: `render.yaml` and `Procfile` are already included in the project for automatic configuration).*

---

## 🤗 3. Deploy to Hugging Face Spaces (100% Free AI/ML Hosting)

Hugging Face Spaces is ideal for computer vision & forensic applications:

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2. Enter Space Name (e.g., `deepfake-detection-system`).
3. Select **Docker** or **Gradio/FastAPI** as the Space SDK.
4. Clone the space repository and copy these project files into it.
5. In Hugging Face Spaces, the `Dockerfile` automatically builds with `ffmpeg` and `opencv-python-headless`.
6. Push to Hugging Face Git:
   ```bash
   git add .
   git commit -m "Deploy deepfake detection system"
   git push
   ```
7. Hugging Face builds and exposes your public app at `https://huggingface.co/spaces/<username>/<space-name>`.

---

## 🐳 4. Deploy with Docker (Any VPS, Railway, Fly.io, AWS, DigitalOcean)

A production-ready [Dockerfile](file:///c:/Users/VICTUS/.gemini/antigravity-ide/scratch/deepfake-detection-system/Dockerfile) is included:

```bash
# Build the Docker image
docker build -t deepfake-detection-system .

# Run the container
docker run -d -p 8000:8000 --name deepfake-app deepfake-detection-system
```
Access at `http://localhost:8000`.

---

## ⚡ 5. Instant Public URL from your PC (Cloudflare Tunnel / ngrok)

If you want someone anywhere in the world to access your running local server right now without hosting setup:

### Using Cloudflare Quick Tunnel (Free, no account needed):
1. Download [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).
2. Run:
   ```powershell
   cloudflared tunnel --url http://127.0.0.1:8000
   ```
3. Copy the generated `https://xxxx.trycloudflare.com` URL to share with anyone.

### Using ngrok:
```powershell
ngrok http 8000
```
