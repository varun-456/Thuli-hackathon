import cv2
import dlib
import numpy as np
import mediapipe as mp

def findFaceFeatures(inputImage):

    # Load face detector and facial landmarks predictor from dlib
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Download from dlib's repository

    # Load the image
    image = cv2.imread(inputImage)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect face
    faces = detector(gray)
    for face in faces:
        # Get facial landmarks
        landmarks = predictor(gray, face)

        # Extract jawline points (facial landmarks 0-16)
        jawline_points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(0, 17)]

        # Extract eye region points (landmarks 36-41 for left eye, 42-47 for right eye)
        left_eye_points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]
        right_eye_points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]

        # Analyze face shape (based on jawline width, height, etc.)
        def analyze_face_shape(jawline):
            jaw_width = jawline[16][0] - jawline[0][0]
            jaw_height = jawline[8][1] - min(jawline[0][1], jawline[16][1])
            ratio = jaw_width / jaw_height

            if ratio > 1.5:
                return "Square"
            elif ratio > 1.3:
                return "Oval"
            else:
                return "Round"

        face_shape = analyze_face_shape(jawline_points)
        print(f"Detected Face Shape: {face_shape}")

        # Jawline shape analysis based on curvature
        def analyze_jawline_shape(jawline):
            jaw_curve = np.polyfit([p[0] for p in jawline], [p[1] for p in jawline], 2)  # Fit a quadratic curve
            curvature = abs(jaw_curve[0])  # Curvature of the quadratic fit

            if curvature < 0.001:  # Almost straight
                return "Defined"
            elif 0.001 <= curvature < 0.005:  # Slight curve
                return "Sharp"
            elif 0.005 <= curvature < 0.01:  # Rounded curve
                return "Round"
            else:  # Very soft curve
                return "Soft"

        jawline_shape = analyze_jawline_shape(jawline_points)
        print(f"Detected Jawline Shape: {jawline_shape}")

        # Crop eye regions for color detection
        left_eye_img = image[left_eye_points[1][1]:left_eye_points[4][1], left_eye_points[0][0]:left_eye_points[3][0]]
        right_eye_img = image[right_eye_points[1][1]:right_eye_points[4][1], right_eye_points[0][0]:right_eye_points[3][0]]

        # Compute average color of eyes (eye color)
        avg_left_eye_color = np.mean(left_eye_img, axis=(0, 1))
        avg_right_eye_color = np.mean(right_eye_img, axis=(0, 1))

        def get_eye_color(avg_color):
            avg_color = avg_color.astype(int)
            if avg_color[0] > 150:
                return "Blue"
            elif avg_color[1] > 100:
                return "Green"
            else:
                return "Brown"

        eye_color = get_eye_color((avg_left_eye_color + avg_right_eye_color) / 2)
        print(f"Detected Eye Color: {eye_color}")

        return {
            "Face Shape": face_shape,
            "Jawline Shape": jawline_shape,
            "Eye Color": eye_color
        }

# # Show the image
# cv2.imshow("Image", image)
# cv2.waitKey(0)
