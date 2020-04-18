import cv2
import numpy as np
import math
from LoadImages import *
from LoadTextFiles import *
from PrepareImage import *

def Rotate(p, angle):
    p[0] = math.cos(math.radians(angle)) * p[0] - math.sin(math.radians(angle)) * p[0]
    p[1] = math.sin(math.radians(angle)) * p[1] + math.cos(math.radians(angle)) * p[1]
    return p

def Rotate(p, angle, center):
    p[0] = math.cos(math.radians(angle)) * (p[0] - center[0]) - math.sin(math.radians(angle)) * (p[0] - center[1]) + center[0]
    p[1] = math.sin(math.radians(angle)) * (p[1] - center[0]) + math.cos(math.radians(angle)) * (p[1] - center[1]) + center[1]
    return p

def Distance2D(x1, x2, y1, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

def Normal(x1, x2, y1, y2):
    dis = Distance2D(x1, x2, y1, y2)
    return ((x2 - x1) / dis, (y2 - y1) / dis)

def Normal(x1, x2, y1, y2, distance):
    return ((x2 - x1) / distance, (y2 - y1) / distance)

def DotProduct(x1, x2, y1, y2):
    return x1 * x2 + y1 * y2

def ComparePrints(minutiaePattern, distancesPattern, positionsPattern, normalsPattern, minutiae, distances, positions, normals):
    angleDifference = 5
    normalsSum = 0
    for np in range(len(normalsPattern)):
        degreesPattern = (math.acos(DotProduct(normalsPattern[np][0], 1, normalsPattern[np][1], 0)) * 180 * math.pi) % 360

        for n in range(len(normals)):
            degrees = (math.acos(DotProduct(normals[n][0], 1, normals[n][1], 0)) * 180 * math.pi) % 360
            dp = degreesPattern
            if(dp >= 360 - angleDifference):
                dp = dp - 90
                degrees = degrees - 90
            if (dp <= angleDifference):
                dp = dp + 90
                degrees = degrees + 90

            d = math.fabs(dp - degrees)
            if(d < angleDifference):
                normalsSum = normalsSum + 1

    return (normalsSum > (len(normals) // 2))

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
        img, sizeX, sizeY = PrepareImage(images[imageIndex])
        cv2.imshow('test', img)

        FingerPrint2File(sizeY, sizeX, "TEST")

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
            for line in range((len(lines) - 1) // 5):
                positions.append((int(lines[line * 5 + 1]), int(lines[line * 5 + 2])))
                minutia = (lines[line * 5 + 3][0:-1]).split(" ")
                minutiae.append((float(minutia[0]), float(minutia[1])))
                minutia = (lines[line * 5 + 4][0:-1]).split(" ")
                minutiae.append((float(minutia[0]), float(minutia[1])))
                minutia = (lines[line * 5 + 5][0:-1]).split(" ")
                minutiae.append((float(minutia[0]), float(minutia[1])))

                distances.append(Distance2D(width / 2, positions[line][0], height / 2, positions[line][1]))
                normals.append(Normal(width / 2, positions[line][0], height / 2, positions[line][1], distances[line]))

            # print(minutiae)
            # print(distances)
            # print(positions)
            # print(normals)

            printStack.append((minutiae, distances, positions, normals))

            if(index > 0):
                print(ComparePrints(printStack[0][0], printStack[0][1], printStack[0][2], printStack[0][3], printStack[index][0], printStack[index][1], printStack[index][2], printStack[index][3]))
            index = index + 1

cv2.destroyAllWindows()