# Deployment Guide

This guide covers deploying the DripDrop backend to various platforms.

## Render

### Option 1: Using Procfile (Recommended)

The `Procfile` in the `backend/` directory automatically configures Render:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Setup Steps:**

1. Connect your GitHub repository to Render
2. Create a new **Web Service**
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: (Leave empty - Procfile will be used automatically)
   - **Python Version**: 3.11 or higher

### Option 2: Manual Start Command

If you prefer not to use Procfile, set the start command in Render dashboard:

```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Important Settings:**

- **Root Directory**: Set to `backend` (so Render runs commands from the backend directory)
- **Environment Variables**: Add all required env vars:
  - `OPENAI_API_KEY`
  - `OPENAI_MODEL` (optional, defaults to `gpt-5.2`)
  - `TINYBIRD_TOKEN` (or your database credentials)
  - Any other environment variables your app needs

### Render Configuration

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables:**
- `OPENAI_API_KEY` - Required
- `OPENAI_MODEL` - Optional (defaults to `gpt-5.2`)
- `TINYBIRD_TOKEN` - Required (or your database connection string)
- `PORT` - Automatically set by Render (don't set manually)

## Other Platforms

### Railway

**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Heroku

**Procfile:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Docker

**Dockerfile example:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Environment Variables

Make sure to set all required environment variables in your deployment platform:

- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENAI_MODEL` - Model name (default: `gpt-5.2`)
- Database credentials (Tinybird token, ClickHouse connection string, etc.)

## Testing Deployment

After deployment, test the endpoints:

1. **Health Check**: `GET https://your-app.onrender.com/health`
2. **Query Endpoint**: `POST https://your-app.onrender.com/query`

## Troubleshooting

### Issue: "Module not found" errors

**Solution**: Make sure the **Root Directory** is set to `backend` in Render settings.

### Issue: Port binding errors

**Solution**: Use `--host 0.0.0.0 --port $PORT` in your start command. Render sets `$PORT` automatically.

### Issue: Environment variables not loading

**Solution**: 
- Check that env vars are set in Render dashboard
- Ensure `.env` file is not committed (it's gitignored)
- Environment variables in Render override `.env` files

