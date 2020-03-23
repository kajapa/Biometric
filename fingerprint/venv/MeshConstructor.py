mesh = []

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