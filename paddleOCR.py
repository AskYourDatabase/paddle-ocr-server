#!/usr/bin/env python3
"""
PaddleOCR wrapper script for Node.js integration
Returns JSON output compatible with scanScreenshot.js
Supports PaddleOCR 3.x API
"""

import sys
import json
import os

# Clear proxy settings that might interfere with model downloads
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

# Suppress model source check warnings
os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'

from paddleocr import PaddleOCR
import paddle

# Initialize OCR (lazy load, will be cached)
ocr = None

def get_ocr():
    global ocr
    if ocr is None:
        # Auto-detect GPU, fallback to CPU
        if paddle.device.is_compiled_with_cuda() and paddle.device.cuda.device_count() > 0:
            device = 'gpu:0'
            print(f'Using GPU for OCR', file=sys.stderr)
        else:
            device = 'cpu'
            print(f'Using CPU for OCR (no GPU available)', file=sys.stderr)

        # PaddleOCR 3.x API
        # 禁用文档预处理（旋转检测），因为手机截图不需要
        ocr = PaddleOCR(
            lang='en',
            device=device,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
        )
    return ocr

def detect_text(image_path):
    """
    Detect text in image and return elements in scanScreenshot.js format
    """
    try:
        ocr_instance = get_ocr()
        # Use predict() instead of ocr() to avoid deprecation warning
        result = ocr_instance.predict(image_path)

        elements = []

        # PaddleOCR 3.x returns list of OCRResult objects (dict-like)
        if result and len(result) > 0:
            item = result[0]

            # Handle OCRResult dict-like object (PaddleOCR 3.x)
            if hasattr(item, 'get') and item.get('rec_texts') is not None:
                texts = item.get('rec_texts') or []
                scores = item.get('rec_scores') or []
                polys = item.get('rec_polys') or []

                for i, text in enumerate(texts):
                    confidence = scores[i] if i < len(scores) else 0.9

                    # Get bounding box
                    if i < len(polys):
                        poly = polys[i]
                        # poly is array of 4 points [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                        x_coords = [p[0] for p in poly]
                        y_coords = [p[1] for p in poly]

                        x_min = min(x_coords)
                        x_max = max(x_coords)
                        y_min = min(y_coords)
                        y_max = max(y_coords)

                        center_x = int((x_min + x_max) / 2)
                        center_y = int((y_min + y_max) / 2)
                        width = int(x_max - x_min)
                        height = int(y_max - y_min)
                    else:
                        center_x, center_y, width, height = 0, 0, 0, 0

                    elements.append({
                        'type': 'text',
                        'text': text,
                        'x': center_x,
                        'y': center_y,
                        'width': width,
                        'height': height,
                        'confidence': int(confidence * 100)
                    })

            # Handle old format (list of [bbox, (text, confidence)])
            elif isinstance(item, list):
                for line in item:
                    try:
                        bbox, (text, confidence) = line
                        x_coords = [p[0] for p in bbox]
                        y_coords = [p[1] for p in bbox]

                        x_min = min(x_coords)
                        x_max = max(x_coords)
                        y_min = min(y_coords)
                        y_max = max(y_coords)

                        center_x = int((x_min + x_max) / 2)
                        center_y = int((y_min + y_max) / 2)
                        width = int(x_max - x_min)
                        height = int(y_max - y_min)

                        elements.append({
                            'type': 'text',
                            'text': text,
                            'x': center_x,
                            'y': center_y,
                            'width': width,
                            'height': height,
                            'confidence': int(confidence * 100)
                        })
                    except (ValueError, TypeError):
                        continue

        return {
            'success': True,
            'elements': elements
        }

    except Exception as e:
        import traceback
        return {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc(),
            'elements': []
        }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'error': 'Usage: paddleOCR.py <image_path>',
            'elements': []
        }))
        sys.exit(1)

    image_path = sys.argv[1]
    result = detect_text(image_path)
    print(json.dumps(result))

if __name__ == '__main__':
    main()
