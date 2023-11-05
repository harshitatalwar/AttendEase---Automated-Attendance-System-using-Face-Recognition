import cv2
from preprocessing import preprocess_image
from data_labelling import labelling_data
from data_splitting import split_data
from alignment import align_faces
import os

data_folder = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\data"
existing_user_ids = set()
for filename in os.listdir(data_folder):
    if filename.startswith("user.") and filename.endswith(".jpg"):
        user_id = int(filename.split(".")[1])
        existing_user_ids.add(user_id)

next_user_id = 1
while next_user_id in existing_user_ids:
    next_user_id += 1


existing_img_ids = set()
for filename in os.listdir(data_folder):
    if filename.startswith("user.") and filename.endswith(".jpg"):
        user_id = int(filename.split(".")[2])
        existing_img_ids.add(user_id)

next_img_id = 1
while next_img_id in existing_img_ids:
    next_img_id += 1

print("Starting to store images for user", next_user_id)
user_id = next_user_id
img_count_per_user = 0
prev_user_id = user_id
# Method to generate dataset to recognize a person


def generate_dataset(img, id, img_id):
    preprocessed_img = preprocess_image(img)
    # write image in data dir
    cv2.imwrite("data/user."+str(id)+"."+str(img_id)+".jpg", preprocessed_img*255)


# Method to draw boundary around the detected feature
def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    # Converting image to gray-scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detecting features in gray-scale image, returns coordinates, width and height of features
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    # drawing rectangle around the feature and labeling it
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]
    return coords


# Method to detect the features
def detect(img, faceCascade, img_id):
    color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
    coords = draw_boundary(img, faceCascade, 1.1, 10, color['blue'], "Face")
    # If feature is detected, the draw_boundary method will return the x,y coordinates and width and height of rectangle else the length of coords will be 0
    if len(coords)==4:
        # Updating region of interest by cropping image
        roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
        aligned_faces = align_faces([roi_img])  # Align the detected face
        if len(aligned_faces) > 0:
            # Assuming we're aligning a single face at a time
            aligned_face = aligned_faces[0]
            # Updating region of inte rest by cropping image
            roi_img = aligned_face

        return roi_img, True
        # img_id to make the name of each image unique
        # generate_dataset(roi_img, user_id, img_id)
    else:
        return img, False


# Loading classifiers
faceCascade = cv2.CascadeClassifier('frontalface.xml')


# Capturing real time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
video_capture = cv2.VideoCapture(0)

# Initialize img_id with 0
img_id = next_img_id
while True:
    _, img = video_capture.read()

    img, face_detected = detect(img, faceCascade, img_id)

    # Increment img_id only when a face is detected and image is stored
    if face_detected:

        if img_count_per_user < 20:
            key = cv2.waitKey(0)
            print("Press 's' to store next image...")
            if key == ord('s'):
                generate_dataset(img, user_id, img_id)
                img_count_per_user += 1
                img_id += 1
        if img_count_per_user >= 20:
            print("Stored", img_count_per_user, "images for user", user_id)
            print("Press 'n' to store images for the next user...")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            while cv2.waitKey(1) & 0xFF != ord('n'):
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                pass
            user_id += 1
            img_count_per_user = 0

    cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)
    screen_width, screen_height = 1920, 1080  # Set your screen resolution
    window_width, window_height = 640, 480  # Set your window size
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    cv2.moveWindow("Camera Feed", x, y)
    cv2.imshow("Camera Feed", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


data_folder = "data/"
max_images_per_user = 20
a, b, _, _ = labelling_data(data_folder, max_images_per_user)
x_train, x_test, y_train, y_test = split_data(a, b)

# releasing web-cam
video_capture.release()
# Destroying output window
cv2.destroyAllWindows()
