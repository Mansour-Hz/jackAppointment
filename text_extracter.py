import cv2
import numpy as np
import pytesseract
import sys
import time

# Load the image
image = cv2.imread('./image.png')

# Preprocess the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
dilated = cv2.dilate(thresh, kernel, iterations=2)
denoise = cv2.fastNlMeansDenoising(dilated, None, 10, 7, 21)
cv2.imshow('jafar', image); time.sleep(50) ;sys.exit()
# Tesseract OCR
text = pytesseract.image_to_string(denoise, lang='eng')
print(text.strip())
