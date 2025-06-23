import cv2
import cv2.ximgproc as ximgproc
import numpy as np


# --- Load image ---
image = cv2.imread('LineDrawing.png', cv2.IMREAD_UNCHANGED)


# --- Apply anti-aliasing by thinning the lines and then blurring with GaussianBlur ---
# Threshold to binary
_, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

# Invert lines so they become white on black background
inverted = cv2.bitwise_not(binary)

# Thin the lines
kernel = np.ones((2, 2), np.uint8)
eroded = cv2.erode(inverted, kernel, iterations=1)

# Restore line color
thinned = cv2.bitwise_not(eroded)

# Blend thinned version with original image
thinned = cv2.addWeighted(image, 0.3, thinned, 0.7, 0)

# Convert to BGR for anti-aliasing
thinnedBgr = cv2.cvtColor(thinned, cv2.COLOR_BGRA2BGR)

# Apply Gaussian blur for anti-aliasing
blurred = cv2.GaussianBlur(thinnedBgr, (3, 3), sigmaX=1.2)

# Blend original and blurred image
smoothed = cv2.addWeighted(thinnedBgr, 0.8, blurred, 0.2, 0)


# --- Transform smooth image so that it has both transparency and semi transparency ---
# Convert to grayscale
gray = cv2.cvtColor(smoothed, cv2.COLOR_BGR2GRAY)

# Invert grayscale so dark lines become bright
inverted_gray = cv2.bitwise_not(gray)

# Allow full transparency and semi transparency
alpha_float = np.power(inverted_gray / 255.0, 3.0)
alpha = (alpha_float * 255).astype(np.uint8)

# Soften alpha for smoother transparency
alpha = cv2.GaussianBlur(alpha, (3, 3), 0)

# Darken RGB channels so faded areas are darker and not white
smoothed_dark = (smoothed.astype(np.float32) * (alpha[:, :, np.newaxis] / 255.0) ** 1.5).astype(np.uint8)

# Merge BGR (colour) and alpha (transparency)
result = cv2.merge((smoothed_dark[:, :, 0], smoothed_dark[:, :, 1], smoothed_dark[:, :, 2], alpha))


# --- Generate thinned line art (1-pixel skeleton) to be overlayed over result image ---
gray_input = cv2.imread('LineDrawing.png', cv2.IMREAD_GRAYSCALE)
_, binary = cv2.threshold(gray_input, 127, 255, cv2.THRESH_BINARY)
inverted = cv2.bitwise_not(binary)

# Apply thinning (Zhang-Suen)
thinned = ximgproc.thinning(inverted, thinningType=ximgproc.THINNING_ZHANGSUEN)

# Invert back to get black lines on white
thinned = cv2.bitwise_not(thinned)

# Convert to 4-channel (BGRA)
thinned_bgra = cv2.cvtColor(thinned, cv2.COLOR_GRAY2BGRA)
thinned_bgra[:, :, 3] = 255  # Fully solid lines


# --- Transform thinned image so that it does not have white pixels ---
# Create a mask where thinned lines are black
gray_thinned = cv2.cvtColor(thinned_bgra, cv2.COLOR_BGRA2GRAY)
_, mask = cv2.threshold(gray_thinned, 250, 255, cv2.THRESH_BINARY_INV)

# Convert mask to 3-channel and normalize
mask = cv2.merge([mask, mask, mask, mask]) / 255.0

# Multiply by mask to keep only black lines
thinned_bgra = (thinned_bgra.astype(np.float32) * mask).astype(np.uint8)


# --- Overlay thin lines over result to ensure there is at least a 1 pixel solid line ---
result = cv2.addWeighted(result, 1, thinned_bgra, 1, 0)


# Save result
cv2.imwrite('output.png', result)