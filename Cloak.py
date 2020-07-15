#Importing our libraries

import numpy as np
import cv2
import time
#selecting in built webcam
cap= cv2.VideoCapture(0) 
time.sleep(2)
background = 0
#cap.read() returns 2 things: image and boolean return value, if ret is True, read is working fine 
#CAPTURING THE BACKGROUND HERE
for i in range(30):
#We have given 30 iterations so that it can capture the background in nice detail
    ret, background= cap.read() # here we are capturing the background

#This code will run unless the cap is running 
while(cap.isOpened()):    
    ret, img= cap.read() #Capturing our image to perform operation on it
    if not ret: #This will happen when the camera is switched off
        break
    
    hsv= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    #We are separating out the cloak part here
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    #Now we will overload the + for OR function
    mask1 = mask1+mask2

    # Now we will use the morphologyEx function to remove the noises from our surroundings
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations= 10) #Every image is a matrix, so here we are creating a 3*3 matrix
    # Now we will try to increase the smoothness of the image
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8), iterations= 10)

    mask2 = cv2.bitwise_not(mask1) # So here, everything except the cloak part would be there
    #Here we are using AND b/w the background and mask1
    res1= cv2.bitwise_and(background, background, mask=mask1) # used for the segmentation of colours
    res2= cv2.bitwise_and(img,img, mask=mask2) #Used to display the background when we have the cloak over us

    #Now we will superimpose the 2 images
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) #a*res1+ b*res2 +c (adding 2 images linearly)

    cv2.imshow("Eureka!!", final_output)
    k = cv2.waitKey(10) 
    if k==27: #k=27: ESC key
        break

cap.release()
cv2.destroyAllWindows()

