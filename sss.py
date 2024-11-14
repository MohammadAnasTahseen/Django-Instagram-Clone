from PIL import Image
import cv2
import numpy as np

# Load the image
image_path = r"C:\Users\Anas\Desktop\counting\3.png"  # Replace with your image path
image = Image.open(image_path)

# Get image dimensions
width, height = image.size

# Define coordinates for the first quadrant (top-left corner)
left = 0
top = 0
right = width // 2
bottom = height // 2

# Crop the image to the first quadrant
quadrant_image = image.crop((left, top, right, bottom))

# Convert the PIL image to a format compatible with OpenCV
quadrant_image_cv = np.array(quadrant_image)
quadrant_image_cv = cv2.cvtColor(quadrant_image_cv, cv2.COLOR_RGB2BGR)

# Convert to grayscale and apply blurring to reduce noise
gray = cv2.cvtColor(quadrant_image_cv, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (15, 15), 0)

# Use a binary threshold to highlight potential faces
_, thresholded = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)

# Find contours in the thresholded image
contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours by size to approximate individual heads
min_contour_area = 50  # Minimum area of a contour to consider it as a person
person_count = sum(1 for contour in contours if cv2.contourArea(contour) > min_contour_area)

# Estimated total count by multiplying by 4 (since we analyzed one quadrant)
estimated_total_count = person_count * 4

# Display results
print("People counted in one quadrant:", person_count)
print("Estimated total count:", estimated_total_count)
