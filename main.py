import cv2
import random
import numpy as np

# 讀入照片
def readPhoto(name):
    return cv2.imread(name)


# 儲存照片
def savePhoto(name, im):
    cv2.imwrite(name + '.png', im)


# 取得並儲存灰階照片
def readGrayImage(name):
    grayImage = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
    savePhoto('gray_image', grayImage)
    return grayImage


# 加上雜訊
def addNoiseWithPercent(image, percent=0):
    if percent == 0:
        savePhoto('noise_Image', image)
        return image

    height = image.shape[0]
    width = image.shape[1]
    newImage = np.zeros((height, width, 3), np.uint8)
    for x in range(width):
        for y in range(height):
            ran = random.randint(1, 10)
            if ran % 10 < percent:
                noiseRan = random.randint(1, 10)
                if noiseRan % 2 == 0:
                    newImage[y][x] = 0
                else:
                    newImage[y][x] = 255
            else:
                newImage[y][x] = image[y][x]

    savePhoto('noise_Image', newImage)
    return newImage


# 取得zMax, zMed, zMin, zXY各個值
def getGrayLevelValue(image, x, y, mask=3):
    height = image.shape[0]
    width = image.shape[1]
    pixels = []

    for j in range(mask):
        pixelY = y - mask // 2 + j
        if pixelY < 0 or pixelY >= height:
            continue
        for i in range(mask):
            pixelX = x - mask // 2 + i
            if pixelX < 0 or pixelX >= width:
                continue
            pixels.append(image[pixelY][pixelX][0])

    pixels.sort()
    zMin = pixels[0]
    zMax = pixels[-1]
    med = len(pixels) // 2
    zMed = pixels[med]
    zXY = image[y][x][0]
    return zMax, zMed, zMin, zXY


# 做Median Filter
def adaptiveMedianFilter(image, x, y, size=3, sizeMax=7):
    zMax, zMed, zMin, zXY = getGrayLevelValue(image, x, y, size)
    # LevelA
    a1 = int(zMed) - int(zMin)
    a2 = int(zMed) - int(zMax)
    if a1 > 0 and a2 < 0:
    # if zMin < zMed < zMax:
        # Level B
        b1 = int(zXY) - int(zMin)
        b2 = int(zXY) - int(zMax)
        if b1 > 0 and b2 < 0:
        # if zMin < zXY < zMax:
            return zXY
        else:
            return zMed
    else:
        newSize = size + 2

    if newSize <= sizeMax:
        # repeat LevelA
        return adaptiveMedianFilter(image, x, y, newSize)
    else:
        return zMed


# 過濾雜訊
def filterNoise(image):
    height = image.shape[0]
    width = image.shape[1]
    # height, width, _ = source.shape
    newImage = np.zeros((height, width, 3), np.uint8)
    for x in range(width):
        for y in range(height):
            pixel = adaptiveMedianFilter(image, x, y)
            newImage[y][x] = pixel
    savePhoto('filterNoise_Image', newImage)


grayImage = readGrayImage('lena_color.png')
# grayImage = readGrayImage('source.jpg')
noiseImage = addNoiseWithPercent(grayImage, 5)
filterNoise(noiseImage)