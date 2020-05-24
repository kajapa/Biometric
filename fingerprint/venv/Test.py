import cv2
import numpy as np
import math
from LoadImages import *
from LoadTextFiles import *
from PrepareImage import *

#pbraca punkt o dany kąt
def Rotate(p, angle):
    p[0] = math.cos(math.radians(angle)) * p[0] - math.sin(math.radians(angle)) * p[0]
    p[1] = math.sin(math.radians(angle)) * p[1] + math.cos(math.radians(angle)) * p[1]
    return p

#obraca punkt o dany kąt względem podanego środka
def Rotate(p, angle, center):
    p[0] = math.cos(math.radians(angle)) * (p[0] - center[0]) - math.sin(math.radians(angle)) * (p[0] - center[1]) + center[0]
    p[1] = math.sin(math.radians(angle)) * (p[1] - center[0]) + math.cos(math.radians(angle)) * (p[1] - center[1]) + center[1]
    return p

#dwuwymiarowa odległość pomiędzy poszczególnymi punktami
def Distance2D(x1, x2, y1, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

#normalizuje wektor
def Normal(x1, x2, y1, y2):
    dis = Distance2D(x1, x2, y1, y2)
    return ((x2 - x1) / dis, (y2 - y1) / dis)

#normalizuje wektor, ale dystans nie jest obliczany tylko podany w parametrze
def Normal(x1, x2, y1, y2, distance):
    return ((x2 - x1) / distance, (y2 - y1) / distance)

#iloczyn skalarny pomiędzy dwoma punktami/wektorami
def DotProduct(x1, x2, y1, y2):
    return x1 * x2 + y1 * y2

def Magnitude(x, y):
    return math.sqrt(x * x + y * y)

def ComparePrints(minutiaePattern, distancesPattern, positionsPattern, normalsPattern, minutiae, distances, positions, normals):
    angleDifference = 5
    distanceDiffrence = 10
    matchAmount = 0

    # podział minucji względem typów ponieważ najpierw łatwiej jest wykluczać odciski poprzez dopasowanie bardzie skomplikowanych minucji
    minutiaePattern3Match = []
    minutiaePattern1Match = []
    for m in minutiaePattern:
        if(len(m) == 3):
            minutiaePattern3Match.append(m)
        if(len(m) == 1):
            minutiaePattern1Match.append(m)
    minutiae3Match = []
    minutiae1Match = []
    for m in minutiaePattern:
        if (len(m) == 3):
            minutiae3Match.append(m)
        if (len(m) == 1):
            minutiae1Match.append(m)

    for m in minutiaePattern3Match:
        alpha = DotProduct(m[0][0], m[1][0], m[0][1], m[1][1]) / (Magnitude(m[0][0], m[0][1]) * Magnitude(m[1][0], m[1][1]))
        betha = DotProduct(m[1][0], m[2][0], m[1][1], m[2][1]) / (Magnitude(m[1][0], m[1][1]) * Magnitude(m[2][0], m[2][1]))
        gamma = DotProduct(m[2][0], m[0][0], m[2][1], m[0][1]) / (Magnitude(m[2][0], m[2][1]) * Magnitude(m[0][0], m[0][1]))

        alpha2 = 0
        betha2 = 0
        gamma2 = 0
        for mp in minutiae3Match:
            alpha2 = DotProduct(mp[0][0], mp[1][0], mp[0][1], mp[1][1]) / (Magnitude(mp[0][0], mp[0][1]) * Magnitude(mp[1][0], mp[1][1]))
            betha2 = DotProduct(mp[1][0], mp[2][0], mp[1][1], mp[2][1]) / (Magnitude(mp[1][0], mp[1][1]) * Magnitude(mp[2][0], mp[2][1]))
            gamma2 = DotProduct(mp[2][0], mp[0][0], mp[2][1], mp[0][1]) / (Magnitude(mp[2][0], mp[2][1]) * Magnitude(mp[0][0], mp[0][1]))

            if(equalNear(alpha, alpha2, 0.01) and equalNear(betha, betha2, 0.01) and equalNear(gamma, gamma2, 0.01)):
                #przekręć
                break
            if(equalNear(alpha, betha2, 0.01) and equalNear(betha, gamma2, 0.01) and equalNear(gamma, alpha2, 0.01)):
                break
            if(equalNear(alpha, gamma2, 0.01) and equalNear(betha, alpha2, 0.01) and equalNear(gamma, betha2, 0.01)):
                break

    # for angle in range(0, 32, 2):
    #     currangle = angle - 16
    #     normalsSum = 0
    #     for pattern in range(len(normalsPattern)):
    #         degreesPattern = (math.acos(DotProduct(normalsPattern[pattern][0], 1, normalsPattern[pattern][1], 0)) * 180 * math.pi) % 360
    #         degreesPattern = degreesPattern + currangle
    #         for current in range(len(normals)): #porównywanie kontów
    #             degrees = (math.acos(DotProduct(normals[current][0], 1, normals[current][1], 0)) * 180 * math.pi) % 360
    #             dp = degreesPattern
    #             if(dp >= 360 - angleDifference):
    #                 dp = dp - 90
    #                 degrees = degrees - 90
    #             if (dp <= angleDifference):
    #                 dp = dp + 90
    #                 degrees = degrees + 90
    #
    #             d = math.fabs(dp - degrees)
    #             if(d < angleDifference): #porównywanie odległości poszczególnych elementów
    #                 distanceDiff = math.fabs(distancesPattern[pattern] - distances[current])
    #                 if(distanceDiff <= distanceDiffrence):
    #                     normalsSum = normalsSum + 1
    #
    #     sum = (len(normals) // 4) * 3
    #     if(normalsSum > sum):
    #         break

    return str(matchAmount) + " " + str(len(minutiaePattern)) + " " + (matchAmount / len(minutiaePattern))

def equalNear(a, b, diff):
    return  math.fabs(a - b) < diff

#images = LoadImagesFromFolder('./../../../probki/DB1_B/')
images = LoadImagesFromFolder('./test_fingerprint/')

imageIndex = 0
sizeX = 0
sizeY = 0
leftBorder = []
rightBorder = []

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
    elif key == ord('w'): #przetestuj
        img, sizeX, sizeY, leftBorder, rightBorder = PrepareImage(images[imageIndex])
        cv2.imshow('test', img)

        FingerPrint2File(sizeY, sizeX, "TEST", leftBorder, rightBorder)

        texts = LoadTextsFromFolder('./db/')
        print("-------test-------")

        index = 0
        printStack = []
        for lines in texts:
            size = lines[0].split(" ")
            width = int(size[0])
            height = int(size[1])
            #print(str(width) + " " + str(height))

            minutiae = []
            distances = []
            positions = []
            normals = []
            line = 1
            while(True):
                #print(line)
                type = int(lines[line])
                positions.append((int(lines[line + 1]), int(lines[line + 2])))
                minutiaTemp = []
                minutia = (lines[line + 3][0:-1]).split(" ")
                minutiaTemp.append((float(minutia[0]), float(minutia[1])))
                if type >= 2:
                    minutia = (lines[line + 4][0:-1]).split(" ")
                    minutiaTemp.append((float(minutia[0]), float(minutia[1])))
                if type >= 3:
                    minutia = (lines[line + 5][0:-1]).split(" ")
                    minutiaTemp.append((float(minutia[0]), float(minutia[1])))
                if type >= 4:
                    minutia = (lines[line + 6][0:-1]).split(" ")
                    minutiaTemp.append((float(minutia[0]), float(minutia[1])))

                minutiae.append(minutiaTemp)
                distances.append(Distance2D(width / 2, positions[len(positions) - 1][0], height / 2, positions[len(positions) - 1][1]))
                normals.append(Normal(width / 2, positions[len(positions) - 1][0], height / 2, positions[len(positions) - 1][1], distances[len(distances) - 1]))
                line = line + type + 3
                if (line >= (len(lines) - 1)):
                    break

            # print(minutiae)
            # print(distances)
            # print(positions)
            # print(normals)

            printStack.append((minutiae, distances, positions, normals))

            if(index > 0):
                print(ComparePrints(printStack[0][0], printStack[0][1], printStack[0][2], printStack[0][3], printStack[index][0], printStack[index][1], printStack[index][2], printStack[index][3]))
            index = index + 1

cv2.destroyAllWindows()