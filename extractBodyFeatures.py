import mediapipe as mp
import cv2
import numpy as np

def findBodyFeatures(inputImage):
    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)

    # Load the image
    image = cv2.imread(inputImage)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform pose detection
    result = pose.process(image_rgb)

    # Check if any pose is detected
    if result.pose_landmarks:
        # Extract key landmarks
        landmarks = result.pose_landmarks.landmark

        # Extract the x, y positions for relevant landmarks
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]

        # Calculate shoulder width (distance between shoulders)
        shoulder_width = np.linalg.norm(np.array([left_shoulder.x, left_shoulder.y]) -
                                        np.array([right_shoulder.x, right_shoulder.y])) * image.shape[1]

        # Calculate hip width (distance between hips)
        hip_width = np.linalg.norm(np.array([left_hip.x, left_hip.y]) -
                                np.array([right_hip.x, right_hip.y])) * image.shape[1]

        # Calculate the shoulder-to-hip ratio for body shape classification
        shoulder_to_hip_ratio = shoulder_width / hip_width

        # Classify body shape
        if shoulder_to_hip_ratio > 1.1:
            body_shape = "Athletic"
        elif shoulder_to_hip_ratio < 0.9:
            body_shape = "Pear"
        else:
            body_shape = "Rectangular"

        print(f"Body Shape: {body_shape}")

        # Shoulder width categorization based on ratio of shoulder width to image width
        shoulder_width_ratio = shoulder_width / image.shape[1]

        if shoulder_width_ratio < 0.2:
            shoulder_category = "Narrow"
        elif 0.2 <= shoulder_width_ratio <= 0.4:
            shoulder_category = "Medium"
        else:
            shoulder_category = "Broad"

        print(f"Shoulder Width: {shoulder_width:.2f} pixels")
        print(f"Shoulder Category: {shoulder_category}")

        # Estimating height category based on leg-to-torso ratio (simple heuristic)
        torso_length = np.linalg.norm(np.array([left_shoulder.y, left_shoulder.x]) - 
                                    np.array([left_hip.y, left_hip.x])) * image.shape[0]
        leg_length = np.linalg.norm(np.array([left_hip.y, left_hip.x]) - 
                                    np.array([left_knee.y, left_knee.x])) * image.shape[0]

        leg_to_torso_ratio = leg_length / torso_length

        if leg_to_torso_ratio > 1.2:
            height_category = "Tall"
        elif leg_to_torso_ratio < 0.8:
            height_category = "Short"
        else:
            height_category = "Average"

        print(f"Height Category: {height_category}")

        # Visualize the detected pose
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # # Display the image with landmarks
        # cv2.imshow("Pose Detection", image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    else:
        print("No pose detected.")

    return {
        "Body Shape": body_shape,
        "Shoulder Category": shoulder_category,
        "Height Category": height_category
    }