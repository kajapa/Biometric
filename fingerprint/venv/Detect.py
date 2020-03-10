import cv2
import os

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

images = load_images_from_folder('./../../../probki/DB1_B/')
images += load_images_from_folder('./../../../probki/DB2_B/')
images += load_images_from_folder('./../../../probki/DB3_B/')
images += load_images_from_folder('./../../../probki/DB4_B/')
imageIndex = 0

print(len(images))

while True:
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', images[imageIndex])

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('a'):
        if imageIndex > 0:
            imageIndex -= 1
    elif key == ord('d'):
        if imageIndex < len(images) - 1:
            imageIndex += 1

cv2.destroyAllWindows()