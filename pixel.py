import cv2
import numpy as np

imgPath = 'demo.jpg'  # img path
HOGThreshold = 1000  # border
resizeShape = (100, 100)  # output size
colorSteps = 16  # Used to determine the color scale of the output image

# How to handle the output image boundary, 'dark': deepen, 'color': solid color
edgeMod = "darken"
edgeDakenRate = 0.7  # If edgeMode is' daken ', please set the scale here
edgeColor = [0, 0, 0]  # If edgeMode is' color ', please set RGB color here


img = cv2.imread(f'./input/{imgPath}', cv2.IMREAD_COLOR)

height = img.shape[0]
width = img.shape[1]

grayImage = cv2.imread(f'./input/{imgPath}', cv2.IMREAD_GRAYSCALE)
gradient_values_x = cv2.Sobel(
    grayImage, cv2.CV_64F, 1, 0, ksize=5)  # X-direction gradient
gradient_values_y = cv2.Sobel(
    grayImage, cv2.CV_64F, 0, 1, ksize=5)  # Y-direction gradient
hog = np.sqrt(np.power(gradient_values_x, 2) +
              np.power(gradient_values_y, 2))  # Composite gradient


for r in range(height):
    for c in range(width):
        hog[r][c] = abs(hog[r][c])
        if (hog[r][c] < HOGThreshold):
            hog[r][c] = 0


resizedHog = cv2.resize(hog, resizeShape, interpolation=cv2.INTER_CUBIC)

resizedImg = cv2.resize(img, resizeShape, interpolation=cv2.INTER_CUBIC)


colorStepNum = 255/colorSteps
for r in range(resizeShape[0]):
    for c in range(resizeShape[1]):
        for i in range(3):
            resizedImg[r][c][i] = int(
                resizedImg[r][c][i]/colorStepNum)*colorStepNum
            if (resizedHog[r][c] != 0):
                if (edgeMod == "color"):
                    resizedImg[r][c] = edgeColor
                if (edgeMod == "darken"):

                    resizedImg[r][c][i] = min(
                        int(resizedImg[r][c][i] * edgeDakenRate), 255)
# cv2.imshow("output", resizedImg)
# cv2.waitKey()
cv2.imwrite(img=resizedImg, filename=str(f'./output/{imgPath[:-3]}png'))
