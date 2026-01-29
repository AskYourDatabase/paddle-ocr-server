# PaddleOCR HTTP Server

A simple HTTP server for PaddleOCR, designed for deployment on vast.ai GPU instances.

## Quick Deploy on vast.ai

1. Rent a GPU instance (e.g., RTX 3060, ~$0.06/hr)
2. SSH into the instance
3. Run:

```bash
git clone https://github.com/AskYourDatabase/paddle-ocr-server.git
cd paddle-ocr-server
bash setup.sh
python server.py
```

## API

### Health Check
```bash
curl http://<ip>:8000/health
```

### Run OCR
```bash
IMAGE_BASE64=$(base64 -w 0 screenshot.png)
curl -X POST http://<ip>:8000/ocr \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"$IMAGE_BASE64\"}"
```

### Response
```json
{
  "elements": [
    {
      "text": "Hello World",
      "x": 100,
      "y": 50,
      "width": 200,
      "height": 30,
      "confidence": 0.95,
      "type": "text"
    }
  ],
  "count": 1,
  "processing_time_ms": 150.5
}
```
