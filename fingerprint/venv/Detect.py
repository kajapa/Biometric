import cv2
import os
import sys

def LoadImagesFromFolder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

def FingerprintSegmentation(image, theshold):
    left = []
    right = []
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if(image[y, x] < theshold):
                left.append(x)
                break;
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if (image[y, image.shape[1] - x - 1] < theshold):
                right.append(image.shape[1] - x - 1)
                break;

    return left, right


cropSize = [sys.maxsize, sys.maxsize, 0, 0] #rozmiar przycięcia obrazu

images = LoadImagesFromFolder('./../../../probki/DB1_B/')
#images += LoadImagesFromFolder('./../../../probki/DB2_B/')
#images += LoadImagesFromFolder('./../../../probki/DB3_B/')
#images += LoadImagesFromFolder('./../../../probki/DB4_B/')
imageIndex = 0

print(len(images))

while True:
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', images[imageIndex])

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('a'):
        if imageIndex > 0:
            imageIndex -= 1
    elif key == ord('d'):
        if imageIndex < len(images) - 1:
            imageIndex += 1
    elif key == ord('w'):
        orginal = images[imageIndex].copy()
        gray = cv2.cvtColor(orginal, cv2.COLOR_BGR2GRAY)
        #ograniczenie rozmiaru przetwarzanego obrazu do samego odcisku palca (wykasowanie tła)
        _, mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        for x in range(mask.shape[1]):
            for y in range(mask.shape[0]):
                if(mask[y, x] < 255):
                    if(cropSize[0] > x):
                        cropSize[0] = x
                    if(cropSize[1] > y):
                        cropSize[1] = y
                    if (cropSize[2] < x):
                        cropSize[2] = x
                    if (cropSize[3] < y):
                        cropSize[3] = y
        crop = gray[cropSize[1]:cropSize[3], cropSize[0]:cropSize[2]]
        #zastosowanie filtru medianowego w celu usunięcia z obrazu porów
        crop = cv2.medianBlur(crop, 3)
        #segmentacjia obrazu palca tak aby uzystakć tylko obrys palca
        left, right = FingerprintSegmentation(crop, 230)
        
        cv2.imshow('orginal', crop)

cv2.destroyAllWindows()