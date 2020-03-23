import cv2
import numpy as np
from LoadImages import *
from MaskCrop import *
from Segmentation import *
from MedianBlur1D import *
from MeshConstructor import *

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
        orginal = images[imageIndex].copy()
        gray = cv2.cvtColor(orginal, cv2.COLOR_BGR2GRAY)
        #ograniczenie rozmiaru przetwarzanego obrazu do samego odcisku palca (wykasowanie tła)
        crop = MaskCrop(gray)
        #zastosowanie filtru medianowego w celu usunięcia z obrazu porów
        crop = cv2.medianBlur(crop, 3)
        #segmentacjia obrazu palca tak aby uzystakć tylko obrys palca
        left, right = FingerprintSegmentation(crop, 230)
        #wygładzanie żeby elementy siatki
        left = MedianBlur1D(left, 4)
        right = MedianBlur1D(right, 4)
        #print(str(len(left)) + " " + str(len(right)) + " " + str(crop.shape[0]) + " " + str(crop.shape[1])) #DEBUG

        #out = cv2.erode(crop, np.ones((2, 2), np.uint8))
        #out = cv2.dilate(out, np.ones((2, 2), np.uint8))

        #wykrywanie krawędzi i zamiana obrzu na binarny
        edge = cv2.GaussianBlur(crop, (3, 3), 0)
        laplacian = cv2.Laplacian(edge, cv2.CV_64F)
        #cv2.imshow('edge', laplacian)

        #przygotowanie podglądu
        testColorImage = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
        for y in range(testColorImage.shape[0]):
            for x in range(testColorImage.shape[1]):
                if(x < left[y] or x > right[y]):
                    testColorImage[y, x, 0] = 0
                    testColorImage[y, x, 1] = 0
                    testColorImage[y, x, 2] = 255
                elif(laplacian[y, x] < 1):
                    testColorImage[y, x, 0] = 0
                    testColorImage[y, x, 1] = 0
                    testColorImage[y, x, 2] = 0
                else:
                    testColorImage[y, x, 0] = 255
                    testColorImage[y, x, 1] = 255
                    testColorImage[y, x, 2] = 255


        #rysowanie siatki punktów
        meshDensity = 4
        for y in range(testColorImage.shape[0]):
            for x in range(testColorImage.shape[1]):
                if(x > left[y] and x < right[y]):
                    if(testColorImage[y, x, 0] > 0):
                        if (x % meshDensity == 0 and y % meshDensity == 0):
                            mesh.append((y, x))

        #edycja siatki punktów
        ValidGridPosition(testColorImage, mesh)

        for m in range(len(mesh)):
            testColorImage[mesh[m][0], mesh[m][1], 0] = 255
            testColorImage[mesh[m][0], mesh[m][1], 1] = 0
            testColorImage[mesh[m][0], mesh[m][1], 2] = 0

        cv2.imshow('test', testColorImage)

cv2.destroyAllWindows()