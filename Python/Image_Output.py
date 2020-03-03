import numpy as np
import cv2
#テスト用画像を生成するソース。

# Create a black image
img = np.zeros((512,512,3), np.uint8)

# Draw a diagonal blue line with thickness of 5 px
img = cv2.line(img,(256,150),(256,350),(255,0,0),1)
img = cv2.line(img,(150,256),(350,256),(255,0,0),1)
img = cv2.rectangle(img,(1,1),(511,511),(0,255,255),4)

cv2.imwrite('C:/Users/herom/Desktop/NY_Laser_Project/output/sample.jpg', img)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()