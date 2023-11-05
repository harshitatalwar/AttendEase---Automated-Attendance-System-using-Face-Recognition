import cv2
import dlib
import os
import numpy as np
from alignment import align_faces
import mysql.connector

encodings_dir = "encodings"
detected_faces_dir = "detected_faces"
pose_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_encoder = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
recognized_faces = []
stored_encodings = {}
faceCascade = cv2.CascadeClassifier('frontalface.xml')


def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    # Converting image to gray-scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detecting features in gray-scale image, returns coordinates, width and height of features
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords_list = []  # Store coordinates for all detected faces

    # drawing rectangle around the feature and labeling it
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, text, (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]
        coords_list.append(coords)  # Accumulate coordinates for all detected faces

    return coords_list


# Method to detect the features
def detect(img, faceCascade):
    color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0), "white": (255, 255, 255)}
    coords_list = draw_boundary(img, faceCascade, 1.1, 10, color['blue'], "Face")
    roi_images = []

    # Loop through the coordinates for each detected face
    for coords in coords_list:
        # Updating region of interest by cropping image
        roi_img = img[coords[1]:coords[1] + coords[3], coords[0]:coords[0] + coords[2]]
        aligned_faces = align_faces([roi_img])  # Align the detected face
        if len(aligned_faces) > 0:
            # Assuming we're aligning a single face at a time
            aligned_face = aligned_faces[0]
            # Updating region of interest by cropping image
            roi_img = aligned_face

        roi_images.append(roi_img)

    return roi_images


def dlib_detector(roi_images_list):
    dlib_face_detector = dlib.get_frontal_face_detector()
    all_dlib_face_locations = []

    # Loop through each ROI image and detect faces
    for roi_img in roi_images_list:
        dlib_face_locations = dlib_face_detector(roi_img)
        all_dlib_face_locations.extend(dlib_face_locations)

    return all_dlib_face_locations



def encodings(img,face_locations,pose_predictor,face_encoder):
    predictors = [pose_predictor(img, face_location) for face_location in face_locations]
    return [np.array(face_encoder.compute_face_descriptor(img, predictor, 1)) for predictor in predictors]


# Load stored encodings
for user_id_folder in os.listdir(encodings_dir):
    user_id = int(user_id_folder.split('_')[1])
    stored_encodings[user_id] = []

    # Load each encoding file for the user
    for encoding_filename in os.listdir(os.path.join(encodings_dir, user_id_folder)):
        if encoding_filename.startswith("encoding_") and encoding_filename.endswith(".npy"):
            encoding_path = os.path.join(encodings_dir, user_id_folder, encoding_filename)
            encoding = np.load(encoding_path)
            stored_encodings[user_id].append(encoding[0])

for user_id in stored_encodings:
    stored_encodings[user_id] = stored_encodings[user_id]



# def save_detected_faces(images, face_locations):
#     for i, face_location in enumerate(face_locations):
#         top, right, bottom, left = face_location.top(), face_location.right(), face_location.bottom(), face_location.left()
#         # Access the correct ROI image using the index i
#         roi_img = images[i]
#         face_image = roi_img[top:bottom, left:right]
#         cv2.imwrite(f"{detected_faces_dir}/detected{i + 1}.jpg", face_image)



def calculate_recognized_users(detected_face_encodings):

    recognized_faces = []
    for detected_face_name, detected_encoding in detected_face_encodings.items():
        min_distance = float('inf')
        recognized_user = None

        # Iterate through stored encodings for each user
        distances = []
        for user_id, stored_user_encodings in stored_encodings.items():
            distances = []  # Initialize an array to store distances for each stored encoding

            # Calculate Euclidean distance for each stored encoding
            for stored_encoding in stored_user_encodings:
                distance = np.linalg.norm(detected_encoding - stored_encoding)
                distances.append(distance)

            # Calculate the mean distance for this user
            avg_distance = np.mean(distances)

            # Check if this is the minimum mean distance so far
            if avg_distance < min_distance:
                min_distance = avg_distance
                recognized_user = user_id
                detected_face = detected_face_name
            distances = []
        if min_distance < 0.5:  # Adjust the threshold as needed
            recognized_faces.append(
                {"detected_face": detected_face, "recognized_user": recognized_user, "distance": min_distance})
        else:
            recognized_faces.append(
                {"detected_face": detected_face, "recognized_user": None, "distance": min_distance})

        return recognized_faces


# Create detected_faces directory if it doesn't exist
os.makedirs(detected_faces_dir, exist_ok=True)

# Capturing real-time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
video_capture = cv2.VideoCapture(0)

# Initialize a flag to determine when to stop processing faces
# save_faces = True
recognise=[]
# Initialize a dictionary to store encodings for each detected face
detected_face_encodings = {}

while True:
    _, img = video_capture.read()

    roi_images = detect(img, faceCascade)

    for i, roi_img in enumerate(roi_images):
        face_locations = dlib_detector([roi_img])  # Pass a list containing the current ROI image

        print(f"Number of detected faces in ROI {i + 1}: {len(face_locations)}")
        # for face_location in face_locations:
        #     top, right, bottom, left = face_location.top(), face_location.right(), face_location.bottom(),face_location.left()
        #     cv2.rectangle(roi_img, (left, top), (right, bottom), (0, 255, 0), 2)
        #
        # cv2.imshow(f"ROI {i + 1}", roi_img)

        if len(face_locations) > 0:
            # save_detected_faces([roi_img], face_locations)  # Pass a list containing the current ROI image

            # Iterate through each detected face
            for j, face_location in enumerate(face_locations):
                # Calculate the face image for the detected face
                top, right, bottom, left = face_location.top(), face_location.right(), face_location.bottom(), face_location.left()
                face_image = roi_img[top:bottom, left:right]

                # Get the face encodings for the detected face
                encoding = encodings(face_image, [face_location], pose_predictor, face_encoder)[0]

                # Store the encoding in the dictionary
                detected_face_encodings[f"detected{i + 1}_{j + 1}"] = encoding

                # Calculate recognized users for this face
                recognized_faces_for_face = calculate_recognized_users({f"detected{i + 1}_{j + 1}": encoding})

                for face_info in recognized_faces_for_face:
                    recognized_user = face_info['recognized_user']

                    if recognized_user in recognized_faces:
                        # This recognized user has already been processed, skip and remove encoding
                        if recognized_user in detected_face_encodings:
                            # Remove the last added encoding
                            detected_face_encodings.popitem()
                        continue

                    else:
                        recognized_faces.extend(recognized_faces_for_face)

        # save_faces = False  # Stop saving faces after this frame
    recognise = recognized_faces
    print("Detected face encodings:")
    for key, encoding in detected_face_encodings.items():
        print(f"{key}: {encoding}")

        # Writing processed image in a new window
    print("Recognized users:")
    for face_info in recognized_faces:
        print(
            f"Detected face: {face_info['detected_face']}, Recognized user: {face_info['recognized_user']}, Distance: {face_info['distance']}")

    break


# releasing web-cam
video_capture.release()
# Destroying the output window
cv2.destroyAllWindows()





