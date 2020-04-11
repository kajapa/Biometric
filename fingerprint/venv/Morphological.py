import cv2
import numpy as np

def SkeletonK3M(img, skeletonIteration):
    #dodanie ramki do obliczeń
    result = np.ones((img.shape[0] + 2, img.shape[1] + 2))
    result[1:(img.shape[0] + 1), 1:(img.shape[1] + 1)] = img[0:img.shape[0],0:img.shape[1]]

    #przygotowanie tablic do szkieletyzacji
    N = []
    N.append([[-1, 0, -1],[-1, 1, -1],[1, 1, 1]])
    N.append(np.rot90(N[0], 1))
    N.append(np.rot90(N[0], 2))
    N.append(np.rot90(N[0], 3))

    #sprawdzamy wszystkie piksele pokolei
    for t in range(skeletonIteration):
        for y in range(1, result.shape[0] - 1):
            for x in range(1, result.shape[1] - 1):
                if result[y, x] > 0: #jeśli piksel jest biały
                    for n in N: #jeśli jest spełnianiana jakokolwiek z masek zmianiamy piksel na czarny
                        weightSum = 0
                        for ny in [-1, 0, 1]:
                            for nx in [-1, 0, 1]:
                                if (result[y + ny, x + nx] > 0 and n[ny + 1][nx + 1] == 1) or (result[y + ny, x + nx] == 0 and n[ny + 1][nx + 1] == 0):
                                    weightSum = weightSum + 1
                        if weightSum == 5:
                            result[y, x] = 0
                            break

    # wyciecie nadmiarowej ramki
    img[0:img.shape[0], 0:img.shape[1]] = result[1:(result.shape[0] - 1), 1:(result.shape[1] - 1)]
    return img

def SkeletonK3MBranch(img, branchIteration):
    result = np.ones((img.shape[0] + 2, img.shape[1] + 2))
    result[1:(img.shape[0] + 1), 1:(img.shape[1] + 1)] = img[0:img.shape[0], 0:img.shape[1]]

    M = []
    M.append([[0, -1, -1], [0, 1, 0], [0, 0, 0]])
    M.append(np.rot90(M[0], 1))
    M.append(np.rot90(M[0], 2))
    M.append(np.rot90(M[0], 3))

    for t in range(branchIteration):
        for y in range(1, result.shape[0] - 1):
            for x in range(1, result.shape[1] - 1):
                if result[y, x] > 0:  # jeśli piksel jest biały
                    for n in M:  # jeśli jest spełnianiana jakokolwiek z masek zmianiamy piksel na czarny
                        weightSum = 0
                        for my in [-1, 0, 1]:
                            for mx in [-1, 0, 1]:
                                if (result[y + my, x + mx] > 0 and n[my + 1][mx + 1] == 1) or (
                                        result[y + my, x + mx] == 0 and n[my + 1][mx + 1] == 0):
                                    weightSum = weightSum + 1
                        if weightSum == 7:
                            result[y, x] = 0
                            break

    #wyciecie nadmiarowej ramki
    img[0:img.shape[0],0:img.shape[1]] = result[1:(result.shape[0] - 1), 1:(result.shape[1] - 1)]
    return img

#działa na jeden piksel w około
def Dylatation(img):
    result = np.zeros((img.shape[0] + 2, img.shape[1] + 2))
    result[1:(img.shape[0] + 1), 1:(img.shape[1] + 1)] = img[0:img.shape[0], 0:img.shape[1]]

    #sprawdzenie czy dookoła danego czarnego piksela jest przynajmniej jeden biały
    for y in range(1, result.shape[0] - 1):
        for x in range(1, result.shape[1] - 1):
            if result[y, x] == 0:
                for ny in [-1, 0, 1]:
                    for nx in [-1, 0, 1]:
                        if result[y + ny, x + nx] == 255:  # jeśli jest to zaznacz jako taki do przekolorowania
                            result[y, x] = 50


    # przekolorowanie
    for y in range(1, result.shape[0] - 1):
        for x in range(1, result.shape[1] - 1):
            if result[y, x] == 50:
                result[y, x] = 255

    # wyciecie nadmiarowej ramki
    img[0:img.shape[0], 0:img.shape[1]] = result[1:(result.shape[0] - 1), 1:(result.shape[1] - 1)]
    return img

#działa tylko po krzyżu
def SoftDylatation(img):
    result = np.zeros((img.shape[0] + 2, img.shape[1] + 2))
    result[1:(img.shape[0] + 1), 1:(img.shape[1] + 1)] = img[0:img.shape[0], 0:img.shape[1]]

    #sprawdzenie czy po krzyżu od danego czarnego piksela jest przynajmniej jeden biały
    for y in range(1, result.shape[0] - 1):
        for x in range(1, result.shape[1] - 1):
            if result[y, x] == 0: #jeśli jest to zaznacz jako taki do przekolorowania
                if result[y - 1, x] == 255 or result[y + 1, x] == 255 or result[y, x - 1] == 255 or result[y, x + 1] == 255:
                    result[y, x] = 50

    # przekolorowanie
    for y in range(1, result.shape[0] - 1):
        for x in range(1, result.shape[1] - 1):
            if result[y, x] == 50:
                result[y, x] = 255

    # wyciecie nadmiarowej ramki
    img[0:img.shape[0], 0:img.shape[1]] = result[1:(result.shape[0] - 1), 1:(result.shape[1] - 1)]
    return img

def Erosion(img):
    result = np.zeros((img.shape[0] + 2, img.shape[1] + 2))
    result[1:(img.shape[0] + 1), 1:(img.shape[1] + 1)] = img[0:img.shape[0], 0:img.shape[1]]

    #sprawdzenie czy dookoła danego białego piksela jest przynajmniej jeden czarny
    for y in range(1, result.shape[0] - 1):
        for x in range(1, result.shape[1] - 1):
            if result[y, x] == 255:
                for ny in [-1, 0, 1]:
                    for nx in [-1, 0, 1]:
                        if result[y + ny, x + nx] == 0: # jeśli jest to zaznacz jako taki do przekolorowania
                            result[y, x] = 50

    # przekolorowanie
    for y in range(1, result.shape[0] - 1):
        for x in range(1, result.shape[1] - 1):
            if result[y, x] == 50:
                result[y, x] = 0

    # wyciecie nadmiarowej ramki
    img[0:img.shape[0], 0:img.shape[1]] = result[1:(result.shape[0] - 1), 1:(result.shape[1] - 1)]
    return img

def SoftErosion(img):
    result = np.zeros((img.shape[0] + 2, img.shape[1] + 2))
    result[1:(img.shape[0] + 1), 1:(img.shape[1] + 1)] = img[0:img.shape[0], 0:img.shape[1]]

    #sprawdzenie czy dookoła danego białego piksela jest przynajmniej jeden czarny
    for y in range(1, result.shape[0] - 1):
        for x in range(1, result.shape[1] - 1):
            if result[y, x] == 255: #jeśli jest to zaznacz jako taki do przekolorowania
                if result[y - 1, x] == 0 or result[y + 1, x] == 0 or result[y, x - 1] == 0 or result[y, x + 1] == 0:
                    result[y, x] = 50

    # przekolorowanie
    for y in range(1, result.shape[0] - 1):
        for x in range(1, result.shape[1] - 1):
            if result[y, x] == 50:
                result[y, x] = 0

    # wyciecie nadmiarowej ramki
    img[0:img.shape[0], 0:img.shape[1]] = result[1:(result.shape[0] - 1), 1:(result.shape[1] - 1)]
    return img