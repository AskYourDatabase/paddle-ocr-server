#!/usr/bin/env python3
"""
PaddleOCR wrapper script
Supports PaddleOCR 2.x API
"""

import sys
import json

from paddleocr import PaddleOCR

# Initialize OCR (lazy load)
ocr = None

def get_ocr():
    global ocr
    if ocr is None:
        # PaddleOCR 2.x API
        ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=True, show_log=False)
        print('PaddleOCR initialized', file=sys.stderr)
    return ocr

def detect_text(image_path):
    """Detect text in image"""
    try:
        ocr_instance = get_ocr()
        # PaddleOCR 2.x uses ocr() method
        result = ocr_instance.ocr(image_path, cls=True)

        elements = []
        if result and result[0]:
            for line in result[0]:
                bbox, (text, confidence) = line
                x_coords = [p[0] for p in bbox]
                y_coords = [p[1] for p in bbox]

                x_min = min(x_coords)
                x_max = max(x_coords)
                y_min = min(y_coords)
                y_max = max(y_coords)

                elements.append({
                    'type': 'text',
                    'text': text,
                    'x': int((x_min + x_max) / 2),
                    'y': int((y_min + y_max) / 2),
                    'width': int(x_max - x_min),
                    'height': int(y_max - y_min),
                    'confidence': int(confidence * 100)
                })

        return {'success': True, 'elements': elements}

    except Exception as e:
        import traceback
        return {'success': False, 'error': str(e), 'traceback': traceback.format_exc(), 'elements': []}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'error': 'Usage: paddleOCR.py <image_path>', 'elements': []}))
        sys.exit(1)
    print(json.dumps(detect_text(sys.argv[1])))

if __name__ == '__main__':
    main()
