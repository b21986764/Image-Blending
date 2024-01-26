import cv2
import numpy as np

def downsample(img):
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    return cv2.resize(blurred, (blurred.shape[1] // 2, blurred.shape[0] // 2))

def upsample(img, size):
    return cv2.resize(img, size)

def buildGaussianPyramid(img, levels):
    pyramid = [img]
    for _ in range(levels - 1):
        img = downsample(img)
        pyramid.append(img)
    return pyramid

def buildLaplacianPyramid(gaussPyramid):
    lapPyramid = []
    for i in range(len(gaussPyramid) - 1):
        size = (gaussPyramid[i].shape[1], gaussPyramid[i].shape[0])
        upsampled = upsample(gaussPyramid[i + 1], size)
        laplacian = cv2.subtract(gaussPyramid[i], upsampled)
        lapPyramid.append(laplacian)
    lapPyramid.append(gaussPyramid[-1])
    return lapPyramid

def collapsePyramid(pyramid):
    img = pyramid[-1]
    for i in range(len(pyramid) - 2, -1, -1):
        img = upsample(img, (pyramid[i].shape[1], pyramid[i].shape[0]))
        img = cv2.add(pyramid[i], img)
    return img

# Load images
img1 = cv2.imread('madrid1.jpg')
img2 = cv2.imread('barca1.jpg')
print("img1 shape:", img1.shape)
print("img2 shape:", img2.shape)
img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
#Select ROI
roi = cv2.selectROI(img2)
cv2.destroyAllWindows()

#Extract selected region
x, y, w, h = roi
mask = np.zeros(img2.shape[:2], dtype=np.uint8)
mask[y:y+h, x:x+w] = 255

#Display mask
cv2.imshow("Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

levels = 11
#Build pyramids
gaussPyramid1 = buildGaussianPyramid(img1, levels)
lapPyramid1 = buildLaplacianPyramid(gaussPyramid1)

gaussPyramid2 = buildGaussianPyramid(img2, levels)
lapPyramid2 = buildLaplacianPyramid(gaussPyramid2)

maskGaussPyramid = buildGaussianPyramid(mask, levels)

#Blend pyramids
blendedPyramid = []
for i in range(levels):
    L1 = lapPyramid1[i]
    L2 = lapPyramid2[i]
    maskLayer = maskGaussPyramid[i]

    #Normalize mask for blending and expand dimensions to match color image
    maskNorm = maskLayer.astype(np.float32) / 255.0
    maskNorm = np.expand_dims(maskNorm, axis=2)  #Expanding to add a third dimension
    maskNorm = np.repeat(maskNorm, 3, axis=2)   #Repeating the mask for 3 channels

    #Blend
    blendedLayer = L1 * maskNorm + L2 * (1 - maskNorm)
    blendedPyramid.append(blendedLayer)

#Collapse blended pyramid
finalBlendedImg = collapsePyramid(blendedPyramid)
imageout = "blendedImage.jpg"
cv2.imwrite(imageout, finalBlendedImg)

minVal = np.min(finalBlendedImg)
maxVal = np.max(finalBlendedImg)

#Subtract the minimum value from all the elements
shiftedImg = finalBlendedImg - minVal

#Scale the shifted values to get the maximum value to 255
scaleFactor = 255 / (maxVal - minVal)

scaledImage = shiftedImg * scaleFactor

#Convert the scaled image to 8-bit unsigned integers (uint8)
normalizedImg = scaledImage.astype(np.uint8)
#Show final blended image
cv2.imshow("Blended Image", normalizedImg)
cv2.waitKey(0)
cv2.destroyAllWindows()


