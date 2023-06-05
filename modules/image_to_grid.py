# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 19:17:49 2021

@author: amrut
"""

from modules.ml_pipeline import ImageDataTransform
from modules.ocr import detect_document
from modules.word_search import word_search
#import pytesseract
import base64
import cv2
import io
import numpy as np
#import cv2
import random
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

class ImageToGrid:
    
    def __init__(self,image,height,width,has_grid,words):
        self.image = None
        self.image_b64 = image
        self.height = height
        self.width = width
        self.words = words
        self.has_grid = has_grid
        self.grid = None
        self.widths = None
        self.heights = None
    
    def draw_rects(self,lst):
        final_im = cv2.cvtColor(self.image,cv2.COLOR_GRAY2RGB)
        
        for loc in lst:
            if loc["found"] == True:
                s_y,s_x = loc["start_coord"]
                e_y,e_x = loc["end_coord"]
                cell_height = (self.heights[1] - self.heights[0]) // 2  #+10
                cell_width = (self.widths[1] - self.widths[0]) // 2 #+ 10
            
                if s_x == e_x:
                    cell_height += 10
                x1,y1 = self.heights[s_x] +cell_height,self.widths[s_y] + cell_width
                x2,y2 = self.heights[e_x] + cell_height,self.widths[e_y] + cell_width
                final_im = cv2.line(final_im, (x1, y1), (x2, y2), (255,0, 0), thickness=4)
        return final_im



    def form_word_grid(self):
        self.decode_image()
        self.init_grid_holder()
        self.process_grid()

        
        
        for i in range(len(self.words)):
            self.words[i] = self.words[i].strip()
        found_words = word_search(self.words,self.grid)
        result_im = self.draw_rects(found_words)
        base64_im = self.encode_image(result_im)
        return base64_im
        #return "poop"


    def encode_image(self,image):
        im = cv2.resize(image, (500,500))
        retval, buffer = cv2.imencode('.jpg', im)
        pic_str = base64.b64encode(buffer)
        pic_str = pic_str.decode()
        return pic_str


    def decode_image(self):
        #string_buffer = io.StringIO()
        #string_buffer.write(base64.b64decode(self.image_b64))
        #real_im = cv2.imread(string_buffer)
        #self.image =  cv2.cvtColor(np.array(real_im), cv2.COLOR_RGB2BGR)
        encoded_data = self.image_b64.split(',')[1]
        nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        self.image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
   
        
    def detect_letter(self,image):
        # resizes, letter, sharpens it, dilates it to emphasize white letter
        mappings = {"0":"O",
                    "2":"Z",
                    "1":"L",
                    "พ":"w",
                    "2":"z",
                    "'ៗ":"l"}

        resize = cv2.resize(image,(1200,1200))
        
        kernel = np.array([[0,-1,0], [-1,5,-1], [0,1,0]])
        sharpen = cv2.filter2D(resize, -1, kernel)
        kernel2 = np.ones((1,4), np.uint8) 
        better_edge = cv2.dilate(sharpen, kernel2, iterations=1)
        invert_col  = cv2.bitwise_not(better_edge)
        bit_im = cv2.imencode('.png',invert_col)[1].tobytes()
        
        # google ocr
        res = detect_document(bit_im)
        if res in mappings.keys():
            res = mappings[res]
        res = res.lower()
        return res
       
        
    def init_grid_holder(self):
        self.grid = [[' ' for i in range(self.width)] 
                        for j in range(self.height)]
        
    def process_grid(self):
        transformer = ImageDataTransform(self.image)
        proc_grid = transformer.preprocess(transformer.img,self.has_grid)
        self.image = proc_grid
        h,w = proc_grid.shape
        cell_height = h//self.height
        cell_width = w//self.width
        
        height_dims = [i*cell_height for i in range(self.height+1)]
        width_dims = [i*cell_width for i in range(self.width+1)]
        self.widths = width_dims
        self.heights = height_dims
        
        for i in range(len(height_dims)-1):
            for j in range(len(width_dims)-1):
                hs,he = height_dims[i],height_dims[i+1] 
                ws,we = width_dims[j],width_dims[j+1]
                self.grid[i][j] = self.detect_letter(proc_grid[hs:he,
                                                               ws:we])
                
        print(self.grid)
                

          
        
        
        
        
        