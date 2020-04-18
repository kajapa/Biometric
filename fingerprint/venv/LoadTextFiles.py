import os

#załadowanie wszystkich plików tekstowych z wskazanego folderu
#fumkcja
def LoadTextsFromFolder(folder):
    texts = []

    f = open(os.path.join(folder, "TEST.txt"), 'r')
    text = f.readlines()
    texts.append(text)

    for filename in os.listdir(folder):
        if(filename == "TEST.txt"):
            continue
        f = open(os.path.join(folder,filename), 'r')
        text = f.readlines()
        if text is not None:
            texts.append(text)
    return texts