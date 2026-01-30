# PaddleOCR HTTP Server

A simple HTTP server for PaddleOCR, designed for deployment on vast.ai GPU instances.

## Current Endpoint

```
https://gtk-marcus-formerly-favorite.trycloudflare.com
```

## API Reference

### Health Check

```bash
curl https://gtk-marcus-formerly-favorite.trycloudflare.com/health
```

Response:
```json
{"status": "healthy"}
```

### OCR Endpoint

**POST** `/ocr`

Request body:
```json
{
  "image": "<base64_encoded_image>"
}
```

Response:
```json
{
  "success": true,
  "elements": [
    {
      "type": "text",
      "text": "Hello World",
      "x": 100,
      "y": 50,
      "width": 200,
      "height": 30,
      "confidence": 95
    }
  ],
  "count": 1,
  "processing_time_ms": 150.5
}
```

## Linux Client Examples

### Bash + curl

```bash
# Health check
curl https://gtk-marcus-formerly-favorite.trycloudflare.com/health

# OCR request
IMAGE_BASE64=$(base64 -w 0 screenshot.png)
curl -X POST https://gtk-marcus-formerly-favorite.trycloudflare.com/ocr \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"$IMAGE_BASE64\"}"
```

### Python

```python
import base64
import requests

OCR_ENDPOINT = "https://gtk-marcus-formerly-favorite.trycloudflare.com/ocr"

def ocr_image(image_path: str) -> dict:
    """Send image to OCR service and return detected text elements."""
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    response = requests.post(
        OCR_ENDPOINT,
        json={"image": image_base64},
        timeout=30
    )
    return response.json()

# Usage
result = ocr_image("/path/to/screenshot.png")
print(f"Found {result['count']} text elements in {result['processing_time_ms']}ms")

for elem in result["elements"]:
    print(f"  [{elem['confidence']}%] {elem['text']} at ({elem['x']}, {elem['y']})")
```

### Python (async with aiohttp)

```python
import base64
import aiohttp

OCR_ENDPOINT = "https://gtk-marcus-formerly-favorite.trycloudflare.com/ocr"

async def ocr_image_async(image_path: str) -> dict:
    """Async version for high-throughput applications."""
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    async with aiohttp.ClientSession() as session:
        async with session.post(
            OCR_ENDPOINT,
            json={"image": image_base64},
            timeout=aiohttp.ClientTimeout(total=30)
        ) as response:
            return await response.json()
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether OCR completed successfully |
| `elements` | array | List of detected text elements |
| `count` | int | Number of elements detected |
| `processing_time_ms` | float | Processing time in milliseconds |

### Element Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always "text" |
| `text` | string | Detected text content |
| `x` | int | Center X coordinate (pixels) |
| `y` | int | Center Y coordinate (pixels) |
| `width` | int | Bounding box width |
| `height` | int | Bounding box height |
| `confidence` | int | Confidence score (0-100) |

## Deploy Your Own Instance

### vast.ai Deployment

1. Rent a GPU instance (RTX 3060 recommended, ~$0.06/hr)
2. SSH into the instance
3. Run:

```bash
git clone https://github.com/AskYourDatabase/paddle-ocr-server.git
cd paddle-ocr-server
bash setup.sh
python server.py
```

4. Set up Cloudflare tunnel for HTTPS access:
```bash
cloudflared tunnel --url http://localhost:8000
```

### Requirements

- Python 3.8-3.12 (not 3.13, imghdr removed)
- NVIDIA GPU with CUDA support
- ~2GB GPU memory

## Notes

- Endpoint URL changes when vast.ai instance restarts (Cloudflare tunnel regenerates)
- Processing time: ~300-700ms per image depending on complexity
- Supports PNG, JPG, and other common image formats
