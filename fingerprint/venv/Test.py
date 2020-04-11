import cv2
import numpy as np
from LoadImages import *

images = LoadImagesFromFolder('./../../../probki/DB1_B/')

imageIndex = 0
sizeX = 0
sizeY = 0

while True:
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', images[imageIndex])

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # wyłącz aplikację
        break
    elif key == ord('a'):  # poprzedni pocisk
        if imageIndex > 0:
            imageIndex -= 1
    elif key == ord('d'):  # następny odcisk
        if imageIndex < len(images) - 1:
            imageIndex += 1
    elif key == ord('w'):
        img = PrepareImage(images[imageIndex])
        cv2.imshow('test', img)

        FingerPrint2File(sizeY, sizeX, "TEST")

cv2.destroyAllWindows()