import cv2
import numpy as np
import os

size=(1080,1350)
base_pic=np.zeros((size[1],size[0],3),np.uint8)
pic1 = cv2.imread("../download_image/MONTE-CARLO,_MONACO_-_MAY_24__Kevin_Magnussen_of_Denmark_driving_the_(20)_Haas_F1_VF-24_Ferrari_in.jpg")
h,w=pic1.shape[:2]
ash=size[1]/h
asw=size[0]/w
if asw<ash:
    sizeas=(int(w*asw),int(h*asw))
else:
    sizeas=(int(w*ash),int(h*ash))
pic1 = cv2.resize(pic1,dsize=sizeas)
base_pic[int(size[1]/2-sizeas[1]/2):int(size[1]/2+sizeas[1]/2), int(size[0]/2-sizeas[0]/2):int(size[0]/2+sizeas[0]/2),:]=pic1
cv2.imshow("pc1",base_pic)
os.chdir("../after_processing_image")
cv2.imwrite("AA.jpg",base_pic)



# resize1 = cv2.resize(img, (1080, 1350))
# resize2 = cv2.resize(img, (0, 0), fx=0.3, fy=0.8, interpolation=cv2.INTER_AREA)
# cv2.imshow("resize1", resize1)
# cv2.imshow("resize2", resize2)
# cv2.waitKey(0)