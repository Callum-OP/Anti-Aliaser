import cv2
import cv2.ximgproc as ximgproc
import numpy as np

# Load image in grayscale
image = cv2.imread('LineDrawing.png', cv2.IMREAD_GRAYSCALE)

# Threshold to binary
_, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

# Invert lines so they become white on black background
inverted = cv2.bitwise_not(binary)

# Thin the lines
kernel = np.ones((2, 2), np.uint8)
eroded = cv2.erode(inverted, kernel, iterations=1)

# Thin the lines to thinnest possible
thinnedOriginal = ximgproc.thinning(inverted, thinningType=ximgproc.THINNING_ZHANGSUEN)

# Restore line color
thinned = cv2.bitwise_not(eroded)

# Blend thinned version with original image
thinned = cv2.addWeighted(image, 0.3, thinned, 0.7, 0)

# Convert to BGR for anti-aliasing
thinnedBgr = cv2.cvtColor(thinned, cv2.COLOR_GRAY2BGR)
thinnedOriginal = cv2.cvtColor(thinned, cv2.COLOR_GRAY2BGR)

# Apply Gaussian blur for anti-aliasing
blurred = cv2.GaussianBlur(thinnedBgr, (3, 3), sigmaX=1.2)

# Blend original and blurred image
smoothed = cv2.addWeighted(thinnedBgr, 0.6, blurred, 0.4, 0)

# Save result
cv2.imwrite('output.png', smoothed)