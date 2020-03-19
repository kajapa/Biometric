import sys
import cv2

#na podstawie jasności funkcja przycina obraz tak by wyciąć jak najwięcej tła
def MaskCrop(img):
    cropSize = [sys.maxsize, sys.maxsize, 0, 0] #wczytanie startowych wartości
    _, mask = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY) #zmiana obrazy na czarno-biały

    #znalezienie pierwszego i ostatniego czarnego piksela w osiach X i Y
    for x in range(mask.shape[1]):
        for y in range(mask.shape[0]):
            if (mask[y, x] < 255):
                if (cropSize[0] > x):
                    cropSize[0] = x
                if (cropSize[1] > y):
                    cropSize[1] = y
                if (cropSize[2] < x):
                    cropSize[2] = x
                if (cropSize[3] < y):
                    cropSize[3] = y

    return img[cropSize[1]:cropSize[3], cropSize[0]:cropSize[2]]
