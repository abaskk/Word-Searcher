# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 18:28:05 2021

@author: amrut
"""
import math
import cv2
import numpy as np
#import matplotlib.pyplot as plt
#import pytesseract

class ImageDataTransform:
    def __init__(self,img):
        self.img = img
        
    def resize(self,im):
        #im = cv2.resize(im,(0,0),fx = 0.75, fy = 0.75)
        im = cv2.resize(im,(1000,1000))
        return im
    
    def grayscale(self,im):
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        return im
    
    def gaussian_blur(self,im):
        #im = cv2.GaussianBlur(im,(7,7),0)
        im = cv2.GaussianBlur(im,(1,5),0)
        return im
    
    def threshold(self,im):
    # threshold determined adaptively, max values rounded to 255
        im = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                       cv2.THRESH_BINARY_INV,15,2)
        return im


    def canny(im):
        im = cv2.Canny(im,60,180)
        return im
    
    def max_contour(self,im):
        im = np.uint8(im)
        cnts,_ = cv2.findContours(im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        shapes = sorted(cnts,key = cv2.contourArea,reverse = True)
        #print(shapes[0].shape)
        max_cnt = shapes[0]
        return max_cnt


#source: https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
    def vertex_coords(self,polygon):
        br_candidates = [coord[0][0]+coord[0][1] for coord in polygon]
        br = max(range(len(br_candidates)),key = br_candidates.__getitem__)
    
        bl_candidates = [coord[0][0]-coord[0][1] for coord in polygon]
        bl = min(range(len(bl_candidates)),key = bl_candidates.__getitem__)
    
        tr_candidates = [coord[0][0]-coord[0][1] for coord in polygon]
        tr = max(range(len(tr_candidates)),key = tr_candidates.__getitem__)
    
        tl_candidates = [coord[0][0]+coord[0][1] for coord in polygon]
        tl = min(range(len(tl_candidates)),key = tl_candidates.__getitem__)
    
    
        return (tl,tr,bl,br)


    def morph(self,im):
        kernel = np.ones((2,2),np.uint8)
        #kernel2 = np.zeros((5,5),np.uint8)
        morp = cv2.morphologyEx(im,cv2.MORPH_OPEN,kernel)
        return morp
    
    def dilate(self,im):
        kernel = np.ones((1,3), np.uint8) 
        img_dil = cv2.dilate(im, kernel, iterations=2) 
        return img_dil

    def euclidean_dist(self,pt1,pt2):
        dist_sq = (pt2[0]-pt1[0])**2 + (pt2[1]-pt1[1])**2
        dist = math.sqrt(dist_sq)
        return dist

    def perspective_new_coords(self,vertices):
        tl,tr,bl,br = vertices
        width1 = self.euclidean_dist(tl,tr)
        width2 = self.euclidean_dist(bl,br)
        max_width = int(max(width1,width2))
        height1 = self.euclidean_dist(tl,bl)
        height2 = self.euclidean_dist(tr,br)
        max_height = int(max(height1,height2))
        new_coords = [[0,0],[max_width,0],
                  [0,max_height],[max_width,max_height]]
        return new_coords,max_width,max_height

# credit: https://stackoverflow.com/questions/59182827/how-to-get-the-cells-of-a-sudoku-grid-with-opencv
    def remove_grid(self,im):
        # whiten out the grid
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
        detected_lines = cv2.morphologyEx(im, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
        cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
        detected_lines = cv2.morphologyEx(im, cv2.MORPH_OPEN, vertical_kernel, iterations=1)
        cnts2 = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        cnts2 = cnts2[0] if len(cnts) == 2 else cnts2[1]
        for c in cnts2:
            cv2.drawContours(im, [c], -1, (255,255,255), 3)

        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(im, [c], -1, (255,255,255), 3)
        return im
    
    
    
    def perspective_shift(self,im,grid_contour):
    
        tl_idx,tr_idx,bl_idx,br_idx = self.vertex_coords(grid_contour)
        orig_coords = [grid_contour[tl_idx][0],grid_contour[tr_idx][0],
                       grid_contour[bl_idx][0],grid_contour[br_idx][0]]
        new_coords,nw,nh = self.perspective_new_coords(orig_coords)
        mat_trans = cv2.getPerspectiveTransform(np.float32(orig_coords),
                                            np.float32(new_coords))
        adjust_im = cv2.warpPerspective(im,mat_trans,(nw,nh))
        return adjust_im

    def preprocess(self,im,grid):
        resized_im = self.resize(im)
        
        gs_im = self.grayscale(resized_im)
       
        blurred = self.gaussian_blur(gs_im)
        thresh = self.threshold(blurred)
       
        if not grid:
           #return thresh
           return gs_im
       
        grid_contour = self.max_contour(thresh)
        bird_eye_im = self.perspective_shift(thresh,grid_contour)
        bird_eye_im = self.resize(bird_eye_im)
        

        
        invert_col = cv2.bitwise_not(bird_eye_im)
        dilated_im = self.dilate(invert_col)
        return dilated_im







