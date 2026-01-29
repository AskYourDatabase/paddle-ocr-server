#!/usr/bin/env python3
"""
HTTP wrapper for paddleOCR.py
"""

import base64
import time
import tempfile
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from paddleOCR import get_ocr, detect_text

# Pre-load OCR model
print("Pre-loading PaddleOCR model...")
get_ocr()
print("Ready.")

app = FastAPI(title="PaddleOCR API", version="1.0.0")


class OCRRequest(BaseModel):
    image: str  # base64


class OCRResponse(BaseModel):
    success: bool
    elements: list
    count: int
    processing_time_ms: float


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/ocr", response_model=OCRResponse)
def ocr(request: OCRRequest):
    start = time.time()

    # Save base64 image to temp file
    img_bytes = base64.b64decode(request.image)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        f.write(img_bytes)
        tmp_path = f.name

    try:
        result = detect_text(tmp_path)
        processing_time = (time.time() - start) * 1000
        return OCRResponse(
            success=result['success'],
            elements=result['elements'],
            count=len(result['elements']),
            processing_time_ms=round(processing_time, 1)
        )
    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
