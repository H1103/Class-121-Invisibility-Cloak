import numpy as np
import time
import cv2

# To save the output in a file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

#starting the webcam
cap = cv2.VideoCapture(0)
time.sleep(2)

# Capturing the background
bg = 0

for i in range(60):
    ret, bg = cap.read()

bg = np.flip(bg, axis = 1)

# reading the captured frame until the camera is on
while (cap.isOpened()):
    ret, img = cap.read()

    if not ret:
        break
    # flipping the image for consistency
    img = np.flip(img, axis = 1)

    # bgr means blue green red and hsv means hue saturation value
    # hue : this channel encodes color information
    # saturation : this channel encodes the intensity 
    # value : this encodes the brightness
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # creating mask to detect red color
    # detect the red color and segment it
    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255, 255])

    # after segmenting out red color, mask it
    mask_1 = cv2.inRange(hsv, lower_red, upper_red)
    
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])

    mask_2 = cv2.inRange(hsv, lower_red, upper_red)

    mask_1 = mask_1 + mask_2

    # morphologyEx(src, dst, op, kernels)
    # open and expand the image where the is mask 1
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))

    mask_2 = cv2.bitwise_not(mask_1)

    # keeping only the part of the images without red color
    res_1 = cv2.bitwise_and(img, img, mask = mask_2)
    
    # keeping only those part of images with red color 
    res_2 = cv2.bitwise_and(bg, bg, mask = mask_1)

    # generating the final output as magical effect     
    # generating the final output by merging res_1 and res_2
    final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)
    output_file.write(final_output)

    # displaying the output to the user
    cv2.imshow("MAGIC", final_output)
    cv2.waitKey(1)

# releasing the webcam
cap.release()
cv2.destroyAllWindows()
