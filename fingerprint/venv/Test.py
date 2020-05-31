import cv2
import numpy as np
import math
from LoadImages import *
from LoadTextFiles import *
from PrepareImage import *

#pbraca punkt o dany kąt
def Rotate(p, angle):
    q = [0.0] * 2
    #print(math.cos(math.radians(angle)))
    #print(p[0])
    #print(math.cos(math.radians(angle)) * p[0])
    q[0] = math.cos(math.radians(angle)) * p[0] - math.sin(math.radians(angle)) * p[0]
    q[1] = math.sin(math.radians(angle)) * p[1] + math.cos(math.radians(angle)) * p[1]
    return q

#obraca punkt o dany kąt względem podanego środka
def RotateCentral(p, angle, center):
    q = [0.0] * 2
    newAngle = angle * math.pi / 180.0
    #rotatedX = Math.cos(angle) * (point.x - center.x) - Math.sin(angle) * (point.y - center.y) + center.x;
    #rotatedY = Math.sin(angle) * (point.x - center.x) + Math.cos(angle) * (point.y - center.y) + center.y;

    q[0] = math.cos(newAngle) * (p[0] - float(center[0])) - math.sin(newAngle) * (p[1] - float(center[1])) + float(center[0])
    q[1] = math.sin(newAngle) * (p[0] - float(center[0])) + math.cos(newAngle) * (p[1] - float(center[1])) + float(center[1])
    return q

#dwuwymiarowa odległość pomiędzy poszczególnymi punktami
def Distance2D(x1, x2, y1, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

#normalizuje wektor
def NormalWithoutDistance(x1, x2, y1, y2):
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

def GetAngle(p, q):
    return math.degrees(math.atan2(q[1]-p[1], q[0]-p[0]))
    #return DotProduct(p[0], q[0], p[1], q[1]) / (Magnitude(p[0], p[1]) * Magnitude(q[0], q[1]))

def ComparePrints(minutiaePattern, distancesPattern, positionsPattern, normalsPattern, minutiae, distances, positions, normals):
    print("----COMPARE----")
    angleDifference = 5
    distanceDiffrence = 10
    similarity = 0 #miara podobieństwa
    angleAccuracy = 10
    distance3 = 8
    distance1 = 8
    similarityMultipler3 = 5
    similarityList = [] #lista wszystkich dopasowań z których będize wybierane najlepsze oznaczane jako wynik końcowy

    # podział minucji względem typów ponieważ najpierw łatwiej jest wykluczać odciski poprzez dopasowanie bardziej skomplikowanych minucji
    #podział normalnych minucji
    minutiaePattern3Match = []
    minutiaePattern1Match = []
    for m in minutiaePattern:
        if(len(m) == 3):
            minutiaePattern3Match.append(m)
        elif(len(m) == 1):
            minutiaePattern1Match.append(m)
    minutiae3Match = []
    minutiae1Match = []
    for m in minutiae:
        if (len(m) == 3):
            minutiae3Match.append(m)
        elif(len(m) == 1):
            minutiae1Match.append(m)
    #podział pozycji
    positionsPattern3Match = []
    positionsPattern1Match = []
    for m in range(len(minutiaePattern)):
        if(len(minutiaePattern[m]) == 3):
            positionsPattern3Match.append(positionsPattern[m])
        elif(len(minutiaePattern[m]) == 1):
            positionsPattern1Match.append(positionsPattern[m])
    positions3Match = []
    positions1Match = []
    for m in range(len(minutiae)):
        if (len(minutiae[m]) == 3):
            positions3Match.append(positions[m])
        elif (len(minutiae[m]) == 1):
            positions1Match.append(positions[m])

    mp3m = -1 # indeks aktualnie przeglądanej minucji z wzorca, względem której będzie dopasowywane
    for m in minutiaePattern3Match:
        alpha = GetAngle(m[0], m[1])#DotProduct(m[0][0], m[1][0], m[0][1], m[1][1]) / (Magnitude(m[0][0], m[0][1]) * Magnitude(m[1][0], m[1][1]))
        betha = GetAngle(m[1], m[2])#DotProduct(m[1][0], m[2][0], m[1][1], m[2][1]) / (Magnitude(m[1][0], m[1][1]) * Magnitude(m[2][0], m[2][1]))
        gamma = GetAngle(m[2], m[0])#DotProduct(m[2][0], m[0][0], m[2][1], m[0][1]) / (Magnitude(m[2][0], m[2][1]) * Magnitude(m[0][0], m[0][1]))
        mp3m = mp3m + 1
        alpha2 = 0
        betha2 = 0
        gamma2 = 0
        m3m = -1 #indeks dopasowanej minucji z porównywanego odcisku
        angleDifference = 0 #kąt o jaki różni się oryginał
        similarity = 0
        isSuit = False
        for mp in minutiae3Match:
            m3m = m3m + 1
            alpha2 = GetAngle(mp[0], mp[1])#DotProduct(mp[0][0], mp[1][0], mp[0][1], mp[1][1]) / (Magnitude(mp[0][0], mp[0][1]) * Magnitude(mp[1][0], mp[1][1]))
            betha2 = GetAngle(mp[1], mp[2])#DotProduct(mp[1][0], mp[2][0], mp[1][1], mp[2][1]) / (Magnitude(mp[1][0], mp[1][1]) * Magnitude(mp[2][0], mp[2][1]))
            gamma2 = GetAngle(mp[2], mp[0])#DotProduct(mp[2][0], mp[0][0], mp[2][1], mp[0][1]) / (Magnitude(mp[2][0], mp[2][1]) * Magnitude(mp[0][0], mp[0][1]))

            #print(str(alpha) + " " + str(betha) + " " + str(gamma) + " +=+ " + str(alpha2) + " " + str(betha2) + " " + str(gamma2))

            #dopasowanie odpowiednich kątów i wyliczenie o ile są przekręcone
            anglePattern = GetAngle(m[0], (1,0))#DotProduct(m[0][0], 1, m[0][1], 0) / Magnitude(m[0][0], m[0][1])
            if(equalNear(alpha, alpha2, angleAccuracy) and equalNear(betha, betha2, angleAccuracy) and equalNear(gamma, gamma2, angleAccuracy)):
                angleMatch = GetAngle(mp[0], (1,0))#DotProduct(mp[0][0], 1, mp[0][1], 0) / Magnitude(mp[0][0], mp[0][1])
                angleDifference = angleMatch - anglePattern
                if(angleDifference > -15 and angleDifference < 15): #jeśli przekręcenie odpowiednio
                    isSuit = True
                    break
            if(equalNear(alpha, betha2, angleAccuracy) and equalNear(betha, gamma2, angleAccuracy) and equalNear(gamma, alpha2, angleAccuracy)):
                angleMatch = GetAngle(mp[1], (1,0))#DotProduct(mp[1][0], 1, mp[1][1], 0) / Magnitude(mp[1][0], mp[1][1])
                angleDifference = angleMatch - anglePattern
                if (angleDifference > -15 and angleDifference < 15):  # jeśli przekręcenie odpowiednio
                    isSuit = True
                    break
            if(equalNear(alpha, gamma2, angleAccuracy) and equalNear(betha, alpha2, angleAccuracy) and equalNear(gamma, betha2, angleAccuracy)):
                angleMatch = GetAngle(mp[2], (1,0))#DotProduct(mp[2][0], 1, mp[2][1], 0) / Magnitude(mp[2][0], mp[2][1])
                angleDifference = angleMatch - anglePattern
                if (angleDifference > -15 and angleDifference < 15):  # jeśli przekręcenie odpowiednio
                    isSuit = True
                    break

        if(isSuit):
            similarity = similarity + similarityMultipler3 # +3 do podobieństwa ponieważ jeden element na pewno pasuje
            mmp3m = -1 #indeks kolejnych minucji z wzoru
            minutiae3MatchRotated = [] #tablica poobracanych normalnych minucji
            positions3MatchRotated = []  #tablica poobracanych pozycji minucji
            for mp in minutiae3Match: #obrócenie minucji o jednakowy kąt
                currMinutiae = []
                currMinutiae.append(GetAngle(Rotate(mp[0], angleDifference), (1, 0)))
                currMinutiae.append(GetAngle(Rotate(mp[1], angleDifference), (1, 0)))
                currMinutiae.append(GetAngle(Rotate(mp[2], angleDifference), (1, 0)))
                minutiae3MatchRotated.append(currMinutiae)
            for pos in positions3Match: #obrucenie pozycji elementów o dany kąt względem wybranej minucji
                if(pos[0] == positions3Match[m3m][0] and pos[1] == positions3Match[m3m][1]):
                    positions3MatchRotated.append(positions3Match[m3m])
                else:
                    positions3MatchRotated.append(RotateCentral(pos, angleDifference, positions3Match[m3m]))
            used = [0] * len(positions3MatchRotated) #stwórz tablice z informacją czy nadna minucja nie była już sprawdzona
            used[m3m] = 1
            for mm in minutiaePattern3Match:
                mmp3m = mmp3m + 1
                if(mp3m == mmp3m): # żeby nie sprawdzać tej samej minucji z tą samą
                    continue
                #relatywna pozycja między wzorcową minucją a innymi
                currAlpha = GetAngle(minutiaePattern3Match[mmp3m][0], (1, 0))
                currBetha = GetAngle(minutiaePattern3Match[mmp3m][1], (1, 0))
                currGamma = GetAngle(minutiaePattern3Match[mmp3m][2], (1, 0))
                relativeMinutePatternPosition = (positionsPattern3Match[mmp3m][0] - positionsPattern3Match[mp3m][0], positionsPattern3Match[mmp3m][1] - positionsPattern3Match[mp3m][1])
                for p in range(len(positions3MatchRotated)): #porównanie pozycji minucji
                    if(used[p] == 0):
                        relativeCurrentPosition = (positions3MatchRotated[p][0] - positions3Match[m3m][0], positions3MatchRotated[p][1] - positions3Match[m3m][1])
                        #print("pos-> " + str(relativeMinutePatternPosition) + " " + str(relativeCurrentPosition))
                        if(equalNear(relativeCurrentPosition[0], relativeMinutePatternPosition[0], distance3) and equalNear(relativeCurrentPosition[1], relativeMinutePatternPosition[1], distance3)):
                            if ((equalNear(currAlpha, minutiae3MatchRotated[p][0], angleAccuracy)
                            and equalNear(currBetha, minutiae3MatchRotated[p][1], angleAccuracy)
                            and equalNear(currGamma, minutiae3MatchRotated[p][2], angleAccuracy))
                            or (equalNear(currAlpha, minutiae3MatchRotated[p][1], angleAccuracy)
                            and equalNear(currBetha, minutiae3MatchRotated[p][2], angleAccuracy)
                            and equalNear(currGamma, minutiae3MatchRotated[p][0], angleAccuracy))
                            or (equalNear(currAlpha, minutiae3MatchRotated[p][2], angleAccuracy)
                            and equalNear(currBetha, minutiae3MatchRotated[p][0], angleAccuracy)
                            and equalNear(currGamma, minutiae3MatchRotated[p][1], angleAccuracy))):
                                used[p] = 1
                                similarity = similarity + similarityMultipler3
                            # used[p] = 1
                            # similarity = similarity + similarityMultipler3
                #poszukaj elementów oddalonych o +- tyle somo w obu osiach i sprawdź czy pasują do siebie nawzajem

            #minucje z jedną normalną
            minutiae1MatchRotated = []
            for mp in minutiae1Match: #obrócenie minucji o jednakowy kąt
                minutiae1MatchRotated.append(GetAngle(Rotate(mp[0], angleDifference), (1, 0)))
                #print(minutiae1MatchRotated[len(minutiae1MatchRotated) - 1])
            positions1MatchRotated = []  # tablica poobracanych pozycji minucji
            for pos in positions1Match: #obrucenie pozycji elementów o dany kąt względem wybranej minucji
                temp = RotateCentral(pos, angleDifference, positions3Match[m3m])
                positions1MatchRotated.append(temp)
                #print("rot -> " + str(pos) + " " + str(temp))
            used1 = [0] * len(positions1MatchRotated)
            for mm in range(len(minutiaePattern1Match)):
                #print(str(len(minutiae1Match)) + " " + str(len(positionsPattern1Match)))
                currAngle = GetAngle(minutiaePattern1Match[mm][0], (1, 0))
                relativeMinutePatternPosition = (positionsPattern1Match[mm][0] - positionsPattern3Match[mp3m][0],
                                                 positionsPattern1Match[mm][1] - positionsPattern3Match[mp3m][1])

                for p in range(len(positions1MatchRotated)):  # porównanie pozycji minucji
                    if (used1[p] == 0):
                        if(equalNear(currAngle, minutiae1MatchRotated[p], angleAccuracy)):
                            relativeCurrentPosition = (positions1MatchRotated[p][0] - positions3Match[m3m][0], positions1MatchRotated[p][1] - positions3Match[m3m][1])
                            if (equalNear(relativeCurrentPosition[0], relativeMinutePatternPosition[0], distance1) and equalNear(relativeCurrentPosition[1], relativeMinutePatternPosition[1], distance1)):
                                used1[p] = 1
                                similarity = similarity + 1


            print(str(similarity) + "/" + str(len(positions3Match) * similarityMultipler3 + len(positions1Match)) + " " + str(similarity / ((len(positions3Match) * similarityMultipler3) + len(positions1Match))) + " angle:" + str(angleDifference))
            similarityList.append(similarity)
        else:
            print("0/" + str(len(positions3Match) * similarityMultipler3 + len(positions1Match)) + " 0.0")
            similarityList.append(0)


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

    maxSimilar = max(similarityList)

    return "match -> " + str(maxSimilar / ((len(minutiaePattern3Match) * similarityMultipler3) + len(minutiaePattern1Match))) #str(similarity) + " " + str(len(minutiaePattern)) + " " + str(similarity / len(minutiaePattern))

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

        FingerPrint2File(sizeY, sizeX, "TEST", leftBorder, rightBorder) #tworzenie pliku z obecnie przeglądanego odcisku

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