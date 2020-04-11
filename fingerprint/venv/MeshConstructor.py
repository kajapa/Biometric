import cv2
import numpy as np

mesh = [] #siatka do pierwszer próbu zbudowania siatki
fingerprints = [] #wykryte poszczególne linie papilarne
minutiaeCandidate = [] #kandydaci na minucję (piksele w otoczeniu 3 innych białych)
minutiaeStar = [] #kandydaci na minucję (piksele w otoczeniu 4 innych białych)
minFingerprintLen = 15 #minimalna długość lini papilarnej (mniejsz są wyrzucane)
fingerprintMesh = [] #siatka zbudowana w oparciu o fingerprints oraz kandydtów na minucję

def ValidGridPosition(img, grid):
    for m in range(len(grid)):
        xPlus = 1
        xMinus = 1
        yPlus = 1
        yMinus = 1
        for x in range(6):
            if(grid[m][0] + yPlus < img.shape[0]):
                if(img[grid[m][0] + yPlus, grid[m][1], 0] == 255):
                    yPlus += 1
            if(grid[m][1] - yMinus > 0):
                if(img[grid[m][0] - yMinus, grid[m][1], 0] == 255):
                    yMinus += 1
            if(grid[m][1] + xPlus < img.shape[1]):
                if(img[grid[m][0], grid[m][1] + xPlus, 0] == 255):
                    xPlus += 1
            if(grid[m][1] - xPlus > 0):
                if(img[grid[m][0], grid[m][1] - xMinus, 0] == 255):
                    xMinus += 1

        if(xMinus + xPlus < yMinus + yPlus):
            grid[m] = (grid[m][0], grid[m][1] + xPlus - xMinus)
        elif(yMinus + yPlus < xMinus + xPlus):
            grid[m] = (grid[m][0] + yPlus - yMinus, grid[m][1])
        else:
            grid[m] = (grid[m][0] + yPlus - yMinus, grid[m][1] + xPlus - xMinus)

    return grid

#wyodrębnia poszczególne linie papilarne
def SeparateFingerprints(image):
    img = image.copy()
    fingerprints.clear()

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if(img[y, x] > 0):
                currprint = []
                DFS2(img, y, x, currprint)
                if(len(currprint) > minFingerprintLen):
                    fingerprints.append(currprint)

#przeszukuje linie papilarne po pikselach żeby wydzielić poszczególne z nich
def DFS2(img, y, x, currprint):
    currprint.append((y, x))
    img[y, x] = 0
    if(x > 0 and img[y, x - 1] > 0):
        DFS2(img, y, x - 1, currprint)
    if(x < img.shape[1] - 1 and img[y, x + 1] > 0):
        DFS2(img, y, x + 1, currprint)
    if (y > 0 and img[y - 1, x] > 0):
        DFS2(img, y - 1, x, currprint)
    if (y < img.shape[0] - 1 and img[y + 1, x] > 0):
        DFS2(img, y + 1, x, currprint)

def FindMinutiae(img):
    minutiaeCandidate.clear()
    minutiaeStar.clear()
    for fp in fingerprints:
        for f in fp:
            sum = 0
            if(f[0] > 0 and f[1] > 0 and f[0] < img.shape[0] - 1 and f[1] < img.shape[1] - 1):
                if (img[f[0] - 1, f[1]]):
                    sum = sum + 1
                if (img[f[0] + 1, f[1]]):
                    sum = sum + 1
                if (img[f[0], f[1] - 1]):
                    sum = sum + 1
                if (img[f[0], f[1] + 1]):
                    sum = sum + 1
                if(sum == 3):
                    minutiaeCandidate.append((f[0], f[1]))
                if (sum == 4):
                    minutiaeStar.append((f[0], f[1]))

def GenerateGrid(fpimg, fingerprintLine):
    y = fpimg.shape[0]
    x = fpimg.shape[1]
    img = np.zeros((fpimg.shape[0], fpimg.shape[1], 1), dtype="uint8")
    for fp in fingerprintLine:
        if(fp[1] < x):
            y = fp[0]
            x = fp[1]
        if (fp[1] == x and fp[0] < y):
            y = fp[0]
            x = fp[1]
        #img[fp[0], fp[1]] = 200

    fingerprintMesh.clear()
    #img[y, x] = 255
    DFS2Grid(fpimg, y, x, fingerprintMesh, 4, 4, -1)
    connections = []

    for fp in fingerprintMesh:
        connections.append([])

    for fp in range(len(fingerprintMesh)):
        if(fingerprintMesh[fp][2] >= 0):
            connections[fingerprintMesh[fp][2]].append(fp)

    for fp in range(len(fingerprintMesh)):
        if(fingerprintMesh[fp][2] >= 0):
            connections[fp].append(fingerprintMesh[fp][2])

    for fp in fingerprintMesh:
        img[fp[0], fp[1]] = 120

    for c in range(len(connections)):
        if(len(connections[c]) > 2):
            img[fingerprintMesh[c][0], fingerprintMesh[c][1]] = 255

    f = open("fingerprint.txt", "w+")

    for c1 in range(len(connections)):
        if(len(connections[c1]) > 2):

            val = 0
            for c2 in connections[c1]: # sprawdzenie długości poszczególnych minucji i omijanie tych za krótkich
                val = val + GoDeeper(c1, c2, connections, 2)

            if(val > 2):
                #f.write(str(c1) + " " + str(connections[c1]) + "\n" + str(fingerprintMesh[c2][0]) + "\n" + str(fingerprintMesh[c2][1]) + "\n")
                f.write(str(fingerprintMesh[c2][0]) + "\n" + str(fingerprintMesh[c2][1]) + "\n")
                for c2 in connections[c1]:
                    f.write(LineFromPoints(fingerprintMesh[c2], fingerprintMesh[connections[connections[c2][0]][0]]) + "\n")
    f.close()

    return img

def LineFromPoints(P, Q):
    a = 0
    #b = 0
    if (P[0] != Q[0]):
        a = (Q[1] - P[1]) / (Q[0] - P[0])
        #b = -((P[1] - Q[1]) / (P[0] - Q[0]) * P[0] - P[1])

    return str(a)# + "\n" + str(b)

def GoDeeper(lastConnection, currConnection, connections, level):
    if(level <= 0):
        return 1

    if (len(connections[lastConnection]) > 1):
        for nextConnection in connections[currConnection]:
            if(len(connections[nextConnection]) > 1 and nextConnection != lastConnection):
                continue

            if(len(connections[nextConnection]) > 1):
                #print(str(currConnection) + " " + str(nextConnection) + " " + str(connections) + " " + str(level))
                val = GoDeeper(currConnection, nextConnection, connections, level - 1)
                if(val == 0):
                    return 0
            else:
                return 0
    else:
        return 0

    return 1

def DFS2Grid(img, y, x, mesh, distance, currdistance, father):
    img[y, x] = 0
    index = father
    if(currdistance >= distance):
        index = len(mesh)
        mesh.append((y, x, father))
        currdistance = 0
    if(x > 0 and img[y, x - 1] > 0):
        DFS2Grid(img, y, x - 1, mesh, distance, currdistance + 1, index)
    if(x < img.shape[1] - 1 and img[y, x + 1] > 0):
        DFS2Grid(img, y, x + 1, mesh, distance, currdistance + 1, index)
    if(y > 0 and img[y - 1, x] > 0):
        DFS2Grid(img, y - 1, x, mesh, distance, currdistance + 1, index)
    if(y < img.shape[0] - 1 and img[y + 1, x] > 0):
        DFS2Grid(img, y + 1, x, mesh, distance, currdistance + 1, index)

def FingerPrint2File(sizeY, sizeX, imageIndex):

    f = open("./db/" + str(imageIndex) + ".txt", "w+")

    for fingerprintLine in fingerprints:
        fpimg = np.zeros((sizeY, sizeX, 1), dtype="uint8")
        for fp in fingerprintLine:
            fpimg[fp[0], fp[1]] = 255

        y = fpimg.shape[0]
        x = fpimg.shape[1]
        img = np.zeros((fpimg.shape[0], fpimg.shape[1], 1), dtype="uint8")
        for fp in fingerprintLine:
            if (fp[1] < x):
                y = fp[0]
                x = fp[1]
            if (fp[1] == x and fp[0] < y):
                y = fp[0]
                x = fp[1]

        fingerprintMesh.clear()
        DFS2Grid(fpimg, y, x, fingerprintMesh, 4, 4, -1)
        connections = []

        for fp in fingerprintMesh:
            connections.append([])

        for fp in range(len(fingerprintMesh)):
            if (fingerprintMesh[fp][2] >= 0):
                connections[fingerprintMesh[fp][2]].append(fp)

        for fp in range(len(fingerprintMesh)):
            if (fingerprintMesh[fp][2] >= 0):
                connections[fp].append(fingerprintMesh[fp][2])

        for c1 in range(len(connections)):
            if (len(connections[c1]) > 2):
                val = 0
                for c2 in connections[c1]:  # sprawdzenie długości poszczególnych minucji i omijanie tych za krótkich
                    val = val + GoDeeper(c1, c2, connections, 2)

                if (val > 2):
                    f.write(str(fingerprintMesh[c2][0]) + "\n" + str(fingerprintMesh[c2][1]) + "\n")
                    for c2 in connections[c1]:
                        f.write(LineFromPoints(fingerprintMesh[c2], fingerprintMesh[connections[connections[c2][0]][0]]) + "\n")

                    f.write("\n")
    f.close()
    return