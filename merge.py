#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import numpy as np


color_dict_1 = {"black": [0, 0, 0], 
              "red": [0, 0, 255]}

def gray2rgb(gray,color_dict_1):
    
    # 定義新涵式
    rgb_image = np.zeros(shape=(*gray.shape, 3))
    # 上色
    for i in range(rgb_image.shape[0]):
        for j in range(rgb_image.shape[1]):
            #不同的灰度值上不同的顏色
            if gray[i, j] < 127:
                rgb_image[i, j, :] = color_dict_1["black"]
            else:
                rgb_image[i, j, :] = color_dict_1["red"]

    return rgb_image.astype(np.uint8)



def addImage():
    img1 = cv2.imread("Photos/result_well.png")
    src = cv2.imread("Photos/ROI_image_new.png")

    h, w, _ = img1.shape
    
    img2 = cv2.resize(src, (w,h))

    alpha = 0.5
    beta = 1-alpha
    gamma = 1
    img_add = cv2.addWeighted(img1, alpha, img2, beta, gamma)
    
    cv2.imwrite("Photos/merge_finish_test.png",img_add)
    print("finish")
    cv2.imshow('img_add',img_add)
    cv2.waitKey()
    
    cv2.destroyAllWindows()

img_result_well = cv2.imread("Photos/result_well.png",0)
img_ROI_image = cv2.imread("Photos/ROI_image.png",0)
ret, th2 = cv2.threshold(img_ROI_image, 70, 255, cv2.THRESH_BINARY)
img_new_2 = gray2rgb(th2, color_dict_1)
cv2.imwrite("Photos/ROI_image_new.png",img_new_2)


addImage()