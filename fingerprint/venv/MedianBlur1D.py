def MedianBlur1D(array, power):
    if(len(array) == 0):
        print("This array no have elements")
        return array
    newArray = []
    for p in range(power): #dodanie początku bez zmian
        newArray.append(array[p])

    for i in range(power, len(array) - power): #użycie filtru medianowego do rozycia obrazu
        medians = []
        for p in range(power * 2 + 1):
            medians.append(array[i - power + p])
        medians.sort()
        newArray.append(medians[int(len(medians) / 2)])

    for p in range(power): #dodanie końca bez zmian
        newArray.append(array[len(array) - power + p])

    return newArray