import cv2
import numpy as np
import os

size=(1080,1350)
base_pic=cv2.imread("../after_processing_image/background.jpg")
pic1 = cv2.imread("../download_image/MONTE-CARLO,_MONACO_-_MAY_24__Kevin_Magnussen_of_Denmark_driving_the_(20)_Haas_F1_VF-24_Ferrari_in.jpg")
h,w=pic1.shape[:2]
ash=size[1]/h
asw=size[0]/w
if asw<ash:
    sizeas=(int(w*asw),int(h*asw))
else:
    sizeas=(int(w*ash),int(h*ash))
pic1 = cv2.resize(pic1,dsize=sizeas)
#base_pic[int(size[1]/2-sizeas[1]/2):int(size[1]/2+sizeas[1]/2), int(size[0]/2-sizeas[0]/2):int(size[0]/2+sizeas[0]/2),:]=pic1
base_pic[0:sizeas[1], 0:sizeas[0],:]=pic1
cv2.imshow("pc1",base_pic)
os.chdir("../after_processing_image")
cv2.imwrite("../after_processing_image/"+"pic1"+".jpg",base_pic)

