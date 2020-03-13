import cv2
import os
import sys

def LoadImagesFromFolder(folder): #załadowanie obrazów z wskazanego folderu
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

def FingerprintSegmentation(image, theshold): #rozdzelenie obrazu tak, żeby wyciąć tło z prawej oraz elwej strony
    left = []
    right = []
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if(image[y, x] < theshold):
                left.append(x)
                break;
            if(x == image.shape[1] - 1):
                left.append(image.shape[1] - 1)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if (image[y, image.shape[1] - x - 1] < theshold):
                right.append(image.shape[1] - x - 1)
                break;
            if (x == image.shape[1] - 1):
                right.append(0)

    return left, right

def MedianBlur1D(array, power):
    if(len(array) == 0):
        print("This array no have elements")
        return array
    newArray = []
    for p in range(power): #dodanie początku bez zmian
        newArray.append(array[p])

    for i in range(power, len(array) - power): #użycie filtru medianowego do rozycia obrazu
        medians = []
        for p in range(power * 2 + 1):
            medians.append(array[i - power + p])
        medians.sort()
        newArray.append(medians[int(len(medians) / 2)])

    for p in range(power): #dodanie końca bez zmian
        newArray.append(array[len(array) - power + p])

    return newArray

def GetStartPoint():
    startPoint = (10, 10)
    # do
    # {
    #     while( aktualny węzeł należy do tła ∨ aktualny węzeł był odwiedzony )
    #     {
    #         przejdź do następnego węzła siatki;
    #     }
    #     punkt początkowy = aktualny węzeł siatki;
    #     wyznacz kierunek linii w nowym punkcie początkowym;
    #     utwórz sekcję w oparciu o wyznaczony startPoint i kierunek linii;
    #     startPoint = minimum utworzonej sekcji;
    # }
    # while ( startPoint należy do tła ∨ punkt początkowy był odwiedzony );

    return startPoint;

def CheckStop():
    stop = 0
    # if ( nowe minimum leży poza rejonem wysegmentowanym z tła ):
    #     kryterium stopu = opuszczenie obszaru odcisku
    # elif( przeskoczono pomiędzy liniami ):
    #     kryterium stopu = zakończenie linii
    # elif( nowe minimum jest oznaczone jako już odwiedzone ):
    #     kryterium stopu = przecięcie linii;

    return stop;



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
        cropSize = [sys.maxsize, sys.maxsize, 0, 0]  # rozmiar przycięcia obrazu
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
        #segmentacjia obrazu palca tak aby uzystakć tylko obrys palca + wygładzenie
        left, right = FingerprintSegmentation(crop, 230)
        left = MedianBlur1D(left, 4)
        right = MedianBlur1D(right, 4)
        #print(str(len(left)) + " " + str(len(right)) + " " + str(crop.shape[0]) + " " + str(crop.shape[1])) #DEBUG
        for y in range(crop.shape[0]):
            for x in range(crop.shape[1]):
                if(x < left[y] or x > right[y]):
                    crop[y, x] = 30

        cv2.imshow('test', crop)

cv2.destroyAllWindows()