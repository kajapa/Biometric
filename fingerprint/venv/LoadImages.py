import cv2
import os

#załadowanie obrazów z wskazanego folderu
#fumkcja ładuje wszystkie obrazy z wybranego folderu i zwraca tablice obrazów
def LoadImagesFromFolder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images