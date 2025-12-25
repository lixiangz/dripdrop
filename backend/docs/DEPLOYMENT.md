# Deployment Guide

Quick deployment guide for the DripDrop backend.

## Render (Recommended)

**Setup:**
1. Connect GitHub repo to Render
2. Create **Web Service**
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: (Leave empty - Procfile used automatically)
   - **Python Version**: 3.11+

**Procfile** (auto-detected):
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables:**
- `OPENAI_API_KEY` (required)
- `OPENAI_MODEL` (optional, defaults to `gpt-5.2`)
- `TINYBIRD_TOKEN` (or database credentials)

## Other Platforms

### Railway / Heroku
**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Testing Deployment

1. Health check: `GET https://your-app.onrender.com/health`
2. Query endpoint: `POST https://your-app.onrender.com/query`

## Troubleshooting

- **"Module not found"**: Set Root Directory to `backend` in platform settings
- **Port binding errors**: Use `--host 0.0.0.0 --port $PORT`
- **Environment variables**: Set in platform dashboard (not `.env` file)
