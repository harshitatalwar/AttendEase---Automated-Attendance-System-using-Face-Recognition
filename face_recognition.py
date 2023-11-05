# from Embeddings import encodings
import cv2
import os
import dlib
import numpy as np


# Path to the directory where aligned faces are saved
aligned_faces_dir = "data/"

# Load aligned faces from the directory
aligned_faces = []
for filename in os.listdir(aligned_faces_dir):
    if filename.endswith(".jpg"):
        face_image = cv2.imread(os.path.join(aligned_faces_dir, filename))
        aligned_faces.append(face_image)

# Now, aligned_faces contains all the aligned faces

color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
faceCascade = cv2.CascadeClassifier('frontalface.xml')
pose_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_encoder = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

encodings_dir = "encodings"

def dlib_detector(img):
    dlib_face_detector = dlib.get_frontal_face_detector()
    dlib_face_locations = dlib_face_detector(img)
    return dlib_face_locations


def encodings(img,face_locations,pose_predictor,face_encoder):
    predictors = [pose_predictor(img, face_location) for face_location in face_locations]
    return [np.array(face_encoder.compute_face_descriptor(img, predictor, 1)) for predictor in predictors]


def extract_user_image_ids(filename):
    parts = filename.split(".")
    if len(parts) >= 3:
        user_id = int(parts[1])
        img_id = int(parts[2])
        return user_id, img_id
    else:
        return None, None


# Initialize variables to keep track of the previous user ID and its folder
user_ids = set()

for subdir in os.listdir(encodings_dir):
    if subdir.startswith("user_"):
        user_id = int(subdir.split("_")[1])
        user_ids.add(user_id)

# Find the next available user ID
next_user_id = 1
while next_user_id in user_ids:
    next_user_id += 1

print("Next available user ID:", next_user_id)


existing_img_ids = []
# Create the user directory for the next available user
user_dir = os.path.join(encodings_dir, f"user_{next_user_id}")
os.makedirs(user_dir, exist_ok=True)
print("Saving encodings to:", user_dir)

user_dir_prev = os.path.join(encodings_dir, f"user_{next_user_id}")

# Collect existing image IDs for the next_user_id
# user_dir = os.path.join(encodings_dir, f"user_{next_user_id}")
for subdir in os.listdir(user_dir_prev):
    if subdir.startswith("encoding_") and subdir.endswith(".npy"):
        img_id = int(subdir.split("_")[1].split(".")[0])
        existing_img_ids.append(img_id)

# Find the next available image ID
next_img_id = max(existing_img_ids) + 1 if existing_img_ids else 1

print("Next available image ID for user", next_user_id, ":", next_img_id)

sorted_filenames = sorted(os.listdir(aligned_faces_dir), key=lambda x: (int(x.split('.')[1]), int(x.split('.')[2])))

starting_filename = f"user.{next_user_id}.{next_img_id}.jpg"


for filename in sorted_filenames:
    user_id, img_id = extract_user_image_ids(filename)
    if user_id >= next_user_id and filename.endswith(".jpg"):
        # Extract user ID and image ID from the filename
        if user_id is not None and img_id is not None:
            # Load the image
            face_image = cv2.imread(os.path.join(aligned_faces_dir, filename))

            # Get the face locations
            face_locations = dlib_detector(face_image)

            # Ensure that face_locations is not empty before calling encodings
            if face_locations:

                # Generate a new encoding filename for this image
                encoding_filename = f"encoding_{img_id}.npy"
                encoding_file = os.path.join(user_dir, encoding_filename)

                # Save the encodings for this user and image
                np.save(encoding_file, encodings(face_image, face_locations, pose_predictor, face_encoder))
                print(f"Encoding saved for user {user_id}, image {img_id}.")

            else:
                print(f"No faces found in the image for user {user_id}.")

        else:
            print("Invalid filename format: ", filename)

        next_img_id += 1

    # elif filename > starting_filename and not filename.endswith(".jpg"):
    #     break