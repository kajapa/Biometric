from MaskCrop import *
from Segmentation import *
from MedianBlur1D import *
from MeshConstructor import *
from Morphological import *

def PrepareImage(img):
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
    cv2.imshow('edge123', laplacian)

    # edge = cv2.erode(edge, np.ones((3, 3), np.uint8))
    # edge = cv2.dilate(edge, np.ones((3, 3), np.uint8))

    # zamiana szarego obrazu na binarny
    for y in range(edge.shape[0]):
        for x in range(edge.shape[1]):
            if (laplacian[y, x] < 1 or x < left[y] or x > right[y]):
                edge[y, x] = 0
            else:
                edge[y, x] = 255

    # edge = SoftErosion(edge)
    # cv2.imshow('erostion', edge)
    # edge = SoftDylatation(edge)
    # cv2.imshow('dylatation', edge)
    # out = SkeletonK3M(edge, 5, 0)
    # cv2.imshow('SkeletonK3M', out)
    edge = SkeletonK3M(edge, 5)
    # cv2.imshow('skel', edge)
    edge = SkeletonK3MBranch(edge, 9)
    # cv2.imshow('branch', edge)

    sizeX = edge.shape[1]
    sizeY = edge.shape[0]
    printIndex = 0
    SeparateFingerprints(edge)
    FindMinutiae(edge)

    # przygotowanie podglądu
    testColorImage = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
    for y in range(testColorImage.shape[0]):
        for x in range(testColorImage.shape[1]):
            if (x < left[y] or x > right[y]):
                testColorImage[y, x, 0] = 0
                testColorImage[y, x, 1] = 0
                testColorImage[y, x, 2] = 255
            elif (edge[y, x] < 1):
                testColorImage[y, x, 0] = 0
                testColorImage[y, x, 1] = 0
                testColorImage[y, x, 2] = 0
            else:
                testColorImage[y, x, 0] = 255
                testColorImage[y, x, 1] = 255
                testColorImage[y, x, 2] = 255

    if (len(minutiaeCandidate) > 0):
        for mc in minutiaeCandidate:
            testColorImage[mc[0], mc[1], 0] = 255
            testColorImage[mc[0], mc[1], 1] = 0
            testColorImage[mc[0], mc[1], 2] = 255

    if (len(minutiaeStar) > 0):
        for mc in minutiaeStar:
            testColorImage[mc[0], mc[1], 0] = 0
            testColorImage[mc[0], mc[1], 1] = 255
            testColorImage[mc[0], mc[1], 2] = 0

    # #rysowanie siatki punktów
    # meshDensity = 4
    # for y in range(testColorImage.shape[0]):
    #     for x in range(testColorImage.shape[1]):
    #         if(x > left[y] and x < right[y]):
    #             if(testColorImage[y, x, 0] > 0):
    #                 if (x % meshDensity == 0 and y % meshDensity == 0):
    #                     mesh.append((y, x))
    #
    # #edycja siatki punktów
    # ValidGridPosition(testColorImage, mesh)
    #
    # for m in range(len(mesh)):
    #     testColorImage[mesh[m][0], mesh[m][1], 0] = 255
    #     testColorImage[mesh[m][0], mesh[m][1], 1] = 0
    #     testColorImage[mesh[m][0], mesh[m][1], 2] = 0

    return testColorImage
