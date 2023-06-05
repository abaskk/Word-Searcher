# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 22:39:15 2021

@author: amrut
"""

#https://stackoverflow.com/questions/56216376/extract-text-from-an-image-using-google-cloud-vision-api-using-cv2-in-python

import cv2
import os
from google.cloud import vision
import io

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='modules/vision_key.json'


def detect_document(img):
    """Detects document features in an image."""
    result = ""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=img)
    response = client.document_text_detection(image=image,image_context={"language_hints": ["en"]})
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    for symbol in word.symbols:
                        result = symbol.text
                        break
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
        
    return result


