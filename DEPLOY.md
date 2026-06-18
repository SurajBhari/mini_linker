# Deploying mini_linker

This app ships ready to deploy on a free host (Render, Railway, Fly.io, …). A `Dockerfile`, `Procfile`, and `render.yaml` are included.

## Option A — Render free tier (easiest)

1. Go to https://render.com → **New → Web Service** → connect this repo.
2. Render auto-detects `render.yaml` — click **Apply**.
   Manual settings if needed:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn main:app --bind 0.0.0.0:$PORT --timeout 120`
3. Deploy. You get a public `*.onrender.com` URL.

## Option B — Docker (Railway / Fly.io / any host)

```bash
docker build -t mini_linker .
docker run -p 8080:8080 mini_linker
```

The container listens on `$PORT` (defaults to 8080).
