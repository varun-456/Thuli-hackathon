import cv2
import numpy as np

def findSkinTone(inputImage):
    # Load the image
    image = cv2.imread(inputImage)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert image to HSV for better color analysis
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define HSV range for skin color detection
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Create a mask for skin detection
    skin_mask = cv2.inRange(hsv_image, lower_skin, upper_skin)

    # Extract the skin region
    skin_region = cv2.bitwise_and(image_rgb, image_rgb, mask=skin_mask)

    # Calculate average color in the skin region
    average_skin_color = np.mean(skin_region[skin_mask > 0], axis=0).astype(np.uint8)

    # Determine skin tone based on average RGB value
    def get_skin_tone(average_color):
        r, g, b = average_color
        if r > 200 and g > 180 and b > 170:
            return "Light"
        elif r > 140 and g > 100 and b > 80:
            return "Medium"
        else:
            return "Dark"

    skin_tone = get_skin_tone(average_skin_color)
    print(f"Detected Skin Tone: {skin_tone}")

    # ================= Hair Type Detection =======================
    # Convert image to grayscale for hair texture analysis
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use edge detection to find hair texture
    edges = cv2.Canny(gray_image, threshold1=100, threshold2=200)

    # Hair mask (assuming hair is the darkest region in the image)
    _, hair_mask = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY_INV)

    # Find the amount of edges (hair texture) in the hair region
    hair_edges = cv2.bitwise_and(edges, edges, mask=hair_mask)

    # Count non-zero pixels in the hair region (edge density)
    edge_density = np.count_nonzero(hair_edges) / np.count_nonzero(hair_mask)

    # Classify hair type based on edge density
    def classify_hair_type(density):
        if density > 0.3:  # High edge density indicates curly hair
            return "Curly"
        elif density > 0.15:  # Medium edge density indicates wavy hair
            return "Wavy"
        else:  # Low edge density indicates straight hair
            return "Straight"

    hair_type = classify_hair_type(edge_density)
    print(f"Detected Hair Type: {hair_type}")

    return {
        "Skin Tone": skin_tone,
        "Hair Type": hair_type
    }

# ================= Visualization =============================

# Show skin and hair regions
# cv2.imshow("Skin Region", skin_region)
# cv2.imshow("Hair Edges", hair_edges)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
