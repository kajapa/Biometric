import cv2
import numpy as np
from LoadImages import *
from PrepareImage import *

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
printIndex = 0
sizeX = 0
sizeY = 0

while True:
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', images[imageIndex])

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): #wyłącz aplikację
        break
    elif key == ord('a'): #poprzedni pocisk
        if imageIndex > 0:
            imageIndex -= 1
    elif key == ord('d'): #następny odcisk
        if imageIndex < len(images) - 1:
            imageIndex += 1
    elif key == ord('z'): #poprzednia linia papilarna
        if printIndex > 0:
            printIndex -= 1
        fpimg = np.zeros((sizeY, sizeX, 1), dtype="uint8")
        for fp in fingerprints[printIndex]:
            fpimg[fp[0], fp[1]] = 255
        #cv2.imshow('finger print', fpimg)
        fpgrid = GenerateGrid(fpimg, fingerprints[printIndex])
        cv2.imshow('fpgrid print', fpgrid)
    elif key == ord('x'): #następna linia papilarna
        if printIndex < len(fingerprints) - 1:
            printIndex += 1
        fpimg = np.zeros((sizeY, sizeX, 1), dtype="uint8")
        for fp in fingerprints[printIndex]:
            fpimg[fp[0], fp[1]] = 255
        #cv2.imshow('finger print', fpimg)
        fpgrid = GenerateGrid(fpimg, fingerprints[printIndex])
        cv2.imshow('fpgrid print', fpgrid)
    elif key == ord('e'):
        print(str(sizeX) + " " + str(sizeY))
        FingerPrint2File(sizeY, sizeX, imageIndex)
    elif key == ord('w'): #wykryj linie papilarne
        img, sizeX, sizeY = PrepareImage(images[imageIndex])
        cv2.imshow('test', img)

cv2.destroyAllWindows()