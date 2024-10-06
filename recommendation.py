from sqlalchemy import create_engine, case
from sqlalchemy.orm import sessionmaker
from models import Occasion, Outfit, Accessories

from extractFaceFeatures import findFaceFeatures
from extractBodyFeatures import findBodyFeatures
from extractSkinTone import findSkinTone



# Database connection setup
DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/postgres'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

def get_user_features(image_path, gender):
    face_features = findFaceFeatures(image_path)
    
    # Step 3: Extract body features
    body_features = findBodyFeatures(image_path)
    
    # Step 4: Extract skin tone and hair type
    skin_hair_features = findSkinTone(image_path)
    
    # Combine extracted features into a single dictionary
    extracted_features = {
        "body_shape": body_features["Body Shape"],
        "face_shape": face_features["Face Shape"],
        "skin_tone": skin_hair_features["Skin Tone"],
        "height_category": body_features["Height Category"],
        "gender": gender,
        "hair_type": skin_hair_features["Hair Type"],
        "shoulder_width": body_features["Shoulder Category"],  # This represents shoulder width category
        "eye_color": face_features["Eye Color"],
        "jawline_type": face_features["Jawline Shape"]
    }

    return extracted_features

# Rule-based logic for color based on skin tone
def get_color_based_on_skin_tone(skin_tone):
    if skin_tone == "Light":
        return "Dark colors (Navy, Maroon)"
    elif skin_tone == "Medium":
        return "Pastels (Peach, Beige)"
    elif skin_tone == "Dark":
        return "Bright colors (Yellow, Orange)"
    return "Neutral colors"

# Rule-based logic for outfit style based on body shape
def get_style_based_on_body_shape(body_shape):
    # More flexible mapping for body shape to style
    return case(
        (body_shape == 'Athletic', 'Formal'),
        (body_shape == 'Hourglass', 'Traditional'),
        (body_shape == 'Pear', 'Indo-Western'),
        else_='Casual'
    )

# Function to get recommendations based on user features and occasion
def get_recommendations(user_features, occasion_name):
    body_shape = user_features['body_shape']
    skin_tone = user_features['skin_tone']
    height_category = user_features['height_category']
    gender = user_features['gender']

    print(f"Debug: Occasion Name = {occasion_name}")
    print(f"Debug: User Gender = {gender}, Body Shape = {body_shape}, Skin Tone = {skin_tone}, Height Category = {height_category}")

    # First, find the formality level for the given occasion
    occasion = session.query(Occasion).filter(Occasion.occasion_name == occasion_name).first()

    if not occasion:
        print("No occasion found.")
        return []

    formality_level = occasion.formality_level
    print(f"Debug: Formality Level = {formality_level}")

    # Query for suitable outfits based on occasion, formality level, body shape, and gender
    outfits = session.query(Outfit).join(Occasion).filter(
        Occasion.occasion_name == occasion_name,
        Outfit.gender == gender,
        Outfit.formality_level == formality_level
    ).all()

    print(f"Debug: Number of Outfits Found = {len(outfits)}")

    if len(outfits) == 0:
        print("No outfits found. Please check your data or input.")
        return []

    # Query for matching accessories based on outfit and occasion
    accessories = session.query(Accessories).join(Outfit).join(Occasion).filter(
        Occasion.occasion_name == occasion_name,
        Outfit.gender == gender,
        Outfit.formality_level == formality_level
    ).all()

    print(f"Debug: Number of Accessories Found = {len(accessories)}")

    if len(accessories) == 0:
        print("No accessories found.")

    # Prepare the final recommendations
    recommendations = []
    for outfit in outfits:
        color_suggestion = get_color_based_on_skin_tone(skin_tone)
        matching_accessories = [acc.accessories for acc in accessories if acc.outfit_id == outfit.outfit_id]
        accessories_str = ", ".join(matching_accessories)

        recommendations.append({
            'Outfit': outfit.outfit_type,
            'Color Suggestions': f"{outfit.color_suggestions}, {color_suggestion}",
            'Fabric Suggestions': outfit.fabric_suggestions,
            'Style': outfit.style,
            'Accessories': accessories_str
        })

    print(f"Debug: Number of Recommendations Prepared = {len(recommendations)}")
    return recommendations

# Example user features
# user_features = {
#     'body_shape': 'Athletic',
#     'face_shape': 'Oval',
#     'skin_tone': 'Medium',
#     'height_category': 'Tall',
#     'gender': 'Male',
#     'hair_type': 'Straight',
#     'shoulder_width': 'Broad',
#     'eye_color': 'Brown',
#     'jawline_type': 'Defined'
# }

# Example occasion input
occasion_name = "Wedding"

image_path = '3f09.jpg'
gender = 'Male'

user_features = get_user_features(image_path, gender)

# Get recommendations
result = get_recommendations(user_features, occasion_name)

# Display the recommendations
if result:
    for recommendation in result:
        print(f"Outfit: {recommendation['Outfit']}")
        print(f"Color Suggestions: {recommendation['Color Suggestions']}")
        print(f"Fabric Suggestions: {recommendation['Fabric Suggestions']}")
        print(f"Style: {recommendation['Style']}")
        print(f"Accessories: {recommendation['Accessories']}")
        print("-" * 50)
else:
    print("No recommendations found.")