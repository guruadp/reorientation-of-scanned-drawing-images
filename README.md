
# Reorientation of scanned drawing images

This project rotates tilted or wrongly rotated 2d scanned images especifically the drawing images using hough transform and Tesseract OCR.


## Installation

Download Python 3.8 or newer 
https://www.python.org/downloads/

If already installed and to check the version run

```bash
  python --version
```
Install OpenCV
```bash
  pip install opencv-contrib-python
```
Install pdf2image
```bash
  pip install pdf2image
```

Download and install tesseract ocr from https://github.com/UB-Mannheim/tesseract/wiki
```bash
  pip install pytesseract
```

## Output Images

<div class="container" style="display: flex; flex-wrap: wrap;">
    <div class="image" style="width: 50%;">
        <h4>Gray scale image</h4>
            <img style="width: calc(100% - (20px * 2));
        margin: 20px;" src="https://github.com/guruadp/reorientation-of-scanned-drawing-images/blob/main/sample.jpg?raw=true" />
    </div>
    <div class="image" style="width: 50%;">
        <h4>Gray scale image</h4>
            <img style="width: calc(100% - (20px * 2));
        margin: 20px;" src="https://github.com/guruadp/reorientation-of-scanned-drawing-images/blob/main/output/gray.jpg?raw=true" />
    </div>
    <div class="image" style="width: 50%;">
        <h4>Binary image</h4>
            <img style="width: calc(100% - (20px * 2));
        margin: 20px;" src="https://github.com/guruadp/reorientation-of-scanned-drawing-images/blob/main/output/binary.jpg?raw=true" />
    </div>
    <div class="image" style="width: 50%;">
        <h4>Canny image</h4>
            <img style="width: calc(100% - (20px * 2));
        margin: 20px;" src="https://github.com/guruadp/reorientation-of-scanned-drawing-images/blob/main/output/canny.jpg?raw=true" />
    </div>
    <div class="image" style="width: 50%;">
        <h4>Lines detected using hough transform</h4>
            <img style="width: calc(100% - (20px * 2));
        margin: 20px;" src="https://github.com/guruadp/reorientation-of-scanned-drawing-images/blob/main/output/hough.jpg?raw=true" />
    </div>
    <div class="image" style="width: 50%;">
        <h4>Image rotated after hough transform</h4>
            <img style="width: calc(100% - (20px * 2));
        margin: 20px;" src="https://github.com/guruadp/reorientation-of-scanned-drawing-images/blob/main/output/sample_hough_rotated.jpg?raw=true" />
    </div>
    <div class="image" style="width: 50%;">
        <h4>Image rotated after OCR orientation</h4>
            <img style="width: calc(100% - (20px * 2));
        margin: 20px;" src="https://github.com/guruadp/reorientation-of-scanned-drawing-images/blob/main/output/sample_ocr_rotated.jpg?raw=true" />
    </div>
</div>
