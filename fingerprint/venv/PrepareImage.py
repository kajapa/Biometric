from MaskCrop import *
from Segmentation import *
from MedianBlur1D import *
from MeshConstructor import *
from Morphological import *
import queue

fillLaplacion = None
tempFillLaplacion = None

def PrepareImage(img): #przetwarzania obrazu lini papilarnej na szkielet
    orginal = img.copy()
    gray = cv2.cvtColor(orginal, cv2.COLOR_BGR2GRAY)
    # ograniczenie rozmiaru przetwarzanego obrazu do samego odcisku palca (wykasowanie tła)
    crop = MaskCrop(gray)
    # zastosowanie filtru medianowego w celu usunięcia z obrazu porów
    crop = cv2.medianBlur(crop, 5)
    # segmentacjia obrazu palca tak aby uzystakć tylko obrys palca
    left, right = FingerprintSegmentation(crop, 230)
    # wygładzanie żeby elementy siatki
    left = MedianBlur1D(left, 4)
    right = MedianBlur1D(right, 4)
    # print(str(len(left)) + " " + str(len(right)) + " " + str(crop.shape[0]) + " " + str(crop.shape[1])) #DEBUG

    # out = cv2.erode(crop, np.ones((2, 2), np.uint8))
    # out = cv2.dilate(out, np.ones((2, 2), np.uint8))

    # wykrywanie krawędzi i zamiana obrzu na binarny
    edge = cv2.GaussianBlur(crop, (3, 3), 0)
    laplacian = cv2.Laplacian(edge, cv2.CV_64F)
    cv2.imshow('edge1', laplacian)
    laplacian = FillPrintHole(laplacian, 8).copy()
    cv2.imshow('edge2', laplacian)

    # edge = cv2.erode(edge, np.ones((3, 3), np.uint8))
    # edge = cv2.dilate(edge, np.ones((3, 3), np.uint8))

    # zamiana szarego obrazu na binarny
    for y in range(edge.shape[0]):
        for x in range(edge.shape[1]):
            if (laplacian[y, x] < 1 or x < left[y] or x > right[y]):
                edge[y, x] = 0
            else:
                edge[y, x] = 255

    #filtr szkieletujący
    edge = SkeletonK3M(edge, 5)
    #filtr usuwający tzw gałęzie
    edge = SkeletonK3MBranch(edge, 8)

    #zapsanie rozmiaru obrazu
    sizeX = edge.shape[1]
    sizeY = edge.shape[0]
    printIndex = 0
    SeparateFingerprints(edge) #wyodrębnia poszczególnych lini
    FindMinutiae(edge) #podział minucji na typy

    # przygotowanie podglądu z zaznaczonymi minucjami
    testColorImage = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
    for y in range(testColorImage.shape[0]):
        for x in range(testColorImage.shape[1]):
            if (x < left[y] or x > right[y]): #pole poza obczaszarem
                testColorImage[y, x, 0] = 0
                testColorImage[y, x, 1] = 0
                testColorImage[y, x, 2] = 255
            elif (edge[y, x] < 1): #brak linii
                testColorImage[y, x, 0] = 0
                testColorImage[y, x, 1] = 0
                testColorImage[y, x, 2] = 0
            else: #występują linie
                testColorImage[y, x, 0] = 255
                testColorImage[y, x, 1] = 255
                testColorImage[y, x, 2] = 255

    if (len(minutiaeCandidate) > 0): #minucje potrówjne
        for mc in minutiaeCandidate:
            testColorImage[mc[0], mc[1], 0] = 255
            testColorImage[mc[0], mc[1], 1] = 0
            testColorImage[mc[0], mc[1], 2] = 255

    if (len(minutiaeStar) > 0): #minucje poczwórne
        for mc in minutiaeStar:
            testColorImage[mc[0], mc[1], 0] = 0
            testColorImage[mc[0], mc[1], 1] = 255
            testColorImage[mc[0], mc[1], 2] = 0

    if (len(minutiaeEnd) > 0): #minucje krańcowe
        for mc in minutiaeEnd:
            testColorImage[mc[0], mc[1], 0] = 255
            testColorImage[mc[0], mc[1], 1] = 0
            testColorImage[mc[0], mc[1], 2] = 0

    return testColorImage, sizeX, sizeY

def FillPrintHole(img, step): #wypełnianie pzestrzeni/porów wewnątrz linii
    newImg = img.copy()
    for y in range(1, img.shape[0] - 1):
        for x in range(1, img.shape[1] - 1):
            if(img[y, x] == 0):
                #img[y, x] = 255
                tempfill = newImg.copy()
                #print(tempfill.shape[0])
                ispass, newFill = FillHole(tempfill, y, x, step)
                if(ispass == True):
                    #print(str(y) + " " + str(x))
                    newImg = newFill.copy()
    return newImg

def FillHole(img, y, x, step): #likwidacja porów skórnych
    stepover = True
    q = queue.Queue()
    q.put((y, x, 0))
    img[y, x] = 255

    #jeśli jest to pojedyńczy otoczony piksel to jest traktowany jako por i jest zamalowywany
    if(img[y - 1, x] > 0 and img[y + 1, x] > 0 and img[y, x - 1] > 0 and img[y, x + 1] > 0):
        return True, img

    #przeszukiwanie obrazu metodą kubełka w celu zlikwdowania porów
    while not q.empty():
        pos = q.get()
        if(pos[2] >= step): #jeśli obszar jest większy niż podany jest traktowany nie jako por
            stepover = False
            break
        if(pos[0] > 0 and img[pos[0] - 1, pos[1]] == 0):
            q.put((pos[0] - 1, pos[1], pos[2] + 1))
            img[pos[0] - 1, pos[1]] = 255
        if(pos[1] < (img.shape[1] - 1) and img[pos[0], pos[1] + 1] == 0):
            q.put((pos[0], pos[1] + 1, pos[2] + 1))
            img[pos[0], pos[1] + 1] = 255
        if(pos[0] < (img.shape[0] - 1) and img[pos[0] + 1, pos[1]] == 0):
            q.put((pos[0] + 1, pos[1], pos[2] + 1))
            img[pos[0] + 1, pos[1]] = 255
        if(pos[1] > 0 and img[pos[0], pos[1] - 1] == 0):
            q.put((pos[0], pos[1] - 1, pos[2] + 1))
            img[pos[0], pos[1] - 1] = 255

    return stepover, img

def FillHoleOld(img, y, x, step): #stara metoda usówania porów oparta na algorytmi rekursywnym (nie działa poprawnie)
    if(step <= -1):
        return False, img

    print(str(img.shape[0]) + " " + str(img.shape[1]) + " " + str(y) + " " + str(x) + " " + str(step) + " " + str(img[y, x]))
    img[y, x] = 255

    if (x > 0 and img[y, x - 1] == 0):
        img[y, x - 1] = 255
        if(FillHole(img, y, x - 1, step - 1) == False):
            return False, img
    if (x < img.shape[1] - 1 and img[y, x + 1] == 0):
        img[y, x + 1] = 255
        if(FillHole(img, y, x + 1, step - 1) == False):
            return False, img
    if (y > 0 and img[y - 1, x] == 0):
        img[y - 1, x] = 255
        if(FillHole(img, y - 1, x, step - 1) == False):
            return False, img
    if (y < img.shape[0] - 1 and img[y + 1, x] == 0):
        img[y + 1, x] = 255
        if(FillHole(img, y + 1, x, step - 1) == False):
            return False, img

    return True, img