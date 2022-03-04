import cv2
import numpy as np
import matplotlib.pyplot as plt

color_dict = {"black": [0, 0, 0], 
              "blue": [255, 255, 255]}


def gray2rgb(gray, color_dict):

    # 定義新涵式
    rgb_image = np.zeros(shape=(*gray.shape, 3))
    # 上色
    for i in range(rgb_image.shape[0]):
        for j in range(rgb_image.shape[1]):
            #不同的灰度值上不同的顏色
            if gray[i, j] < 127:
                rgb_image[i, j, :] = color_dict["black"]
            else:
                rgb_image[i, j, :] = color_dict["blue"]

    return rgb_image.astype(np.uint8)

img = cv2.imread("Photos/result_well.png",0)
ret, th = cv2.threshold(img, 70, 255, cv2.THRESH_BINARY)
img_new = gray2rgb(th, color_dict)



cv2.imshow("result",img_new)
cv2.imwrite("Photos/result_well_new.png",img_new)
cv2.waitKey(0)
cv2.destroyAllWindows()