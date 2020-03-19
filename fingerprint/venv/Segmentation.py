import cv2

#rozdzelenie obrazu tak, żeby wyciąć tło z prawej oraz lewej strony
#zwraca 2 tablice oznaczające odległosć w pikselach od lewej krawędzi gdzie zaczyna się i kończy odcisk
def FingerprintSegmentation(image, theshold):
    left = []
    right = []
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if(image[y, x] < theshold):
                left.append(x)
                break;
            if(x == image.shape[1] - 1):
                left.append(image.shape[1] - 1)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if (image[y, image.shape[1] - x - 1] < theshold):
                right.append(image.shape[1] - x - 1)
                break;
            if (x == image.shape[1] - 1):
                right.append(0)

    return left, right