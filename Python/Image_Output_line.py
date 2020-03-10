import numpy as np
import cv2
#テスト用画像を生成するソース。
#三本線を生成するソース。

# Create a black image
img = np.zeros((512,512,3), np.uint8)

# Draw a diagonal blue line with thickness of 5 px
img = cv2.line(img,(170,170),(350,170),(255,255,255),1)
img = cv2.line(img,(170,256),(350,256),(255,255,255),1)
img = cv2.line(img,(170,340),(350,340),(255,255,255),1)

cv2.imwrite('C:/Users/herom/Desktop/NY_Laser_Project/output/sample_line.jpg', img)

cv2.imshow('image',img)

cv2.waitKey(0)
cv2.destroyAllWindows()