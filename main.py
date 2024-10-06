import cv2
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from extractFaceFeatures import findFaceFeatures
from extractBodyFeatures import findBodyFeatures
from extractSkinTone import findSkinTone

# Load the dataset (replace with the path to your CSV file)
df = pd.read_csv('indian_celebrities_styling_with_colors.csv')

# One-hot encode all categorical features in the dataset
df_encoded = pd.get_dummies(df[[
    "Body Shape", 
    "Face Shape", 
    "Skin Tone", 
    "Height Category", 
    "Hair Type", 
    "Shoulder Width", 
    "Eye Color", 
    "Jawline Type"
]])

# Store the preferred outfit and color for later reference
outfit_mapping = df[["Preferred Outfit", "Preferred Outfit Color"]]

# Helper function to one-hot encode the extracted features and align columns with dataset
def encode_features(features, dataset_columns):
    features_encoded = pd.get_dummies(pd.DataFrame([features]))

    # Reindex to ensure the feature vector has the same columns as the dataset, filling missing columns with 0
    features_encoded = features_encoded.reindex(columns=dataset_columns, fill_value=0)
    
    return features_encoded

# Main function to process the image and make outfit recommendations
def process_image(image_path, gender):
    if image_path is None:
        raise ValueError("Image not found or invalid image path.")

    # Step 1: Detect gender
    detected_gender = gender

    # Step 2: Extract face features
    face_features = findFaceFeatures(image_path)
    
    # Step 3: Extract body features
    body_features = findBodyFeatures(image_path)
    
    # Step 4: Extract skin tone and hair type
    skin_hair_features = findSkinTone(image_path)
    
    # Combine extracted features into a single dictionary
    extracted_features = {
        "Body Shape": body_features["Body Shape"],
        "Face Shape": face_features["Face Shape"],
        "Skin Tone": skin_hair_features["Skin Tone"],
        "Height Category": body_features["Height Category"],
        "Hair Type": skin_hair_features["Hair Type"],
        "Shoulder Width": body_features["Shoulder Category"],  # This represents shoulder width category
        "Eye Color": face_features["Eye Color"],
        "Jawline Type": face_features["Jawline Shape"]
    }

    print("///////////////////////")
    print(extracted_features)
    print("///////////////////////")
    
    # Filter dataset by gender before calculating similarity
    df_filtered = df[df['Gender'] == detected_gender]

    # One-hot encode the filtered dataset
    df_encoded_filtered = pd.get_dummies(df_filtered[[
        "Body Shape", 
        "Face Shape", 
        "Skin Tone", 
        "Height Category", 
        "Hair Type", 
        "Shoulder Width", 
        "Eye Color", 
        "Jawline Type"
    ]])

    # Align extracted features with dataset columns
    extracted_features_encoded = encode_features(extracted_features, df_encoded_filtered.columns)

    # Align dataset with extracted feature columns (in case some categories are missing)
    df_encoded_filtered = df_encoded_filtered.reindex(columns=extracted_features_encoded.columns, fill_value=0)

    # Calculate cosine similarity between the extracted features and the filtered dataset
    similarities = cosine_similarity(extracted_features_encoded, df_encoded_filtered)[0]

    # Find the most similar record
    most_similar_index = np.argmax(similarities)
    best_match = df_filtered.iloc[most_similar_index]

    # Return the final record with the recommendations
    record = {
        "Detected Gender": detected_gender,
        "Face Features": face_features,
        "Body Features": body_features,
        "Skin and Hair Features": skin_hair_features,
        "Recommended Outfit": best_match["Preferred Outfit"],
        "Recommended Outfit Color": best_match["Preferred Outfit Color"]
    }
    
    return record


if __name__ == "__main__":
    # Test with an image file
    image_path = 'alia-bhatt.jpg'
    gender = 'Female'
    result = process_image(image_path, gender)
    
    # Print the results as a record
    print("Final Record:")
    print(result)
