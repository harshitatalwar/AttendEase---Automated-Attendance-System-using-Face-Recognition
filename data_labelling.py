import os
import numpy as np
import cv2
from preprocessing import preprocess_image

def labelling_data(data_folder="C:\\Users\\mandv\\PycharmProjects\\AutomatedAttendace\\ProcterAI\\data", max_images_per_user=20):
    a = []  # Training images
    b = []  # Training labels

    # Dictionary to map user IDs to classes (indexes)
    classes = {}

    # Dictionary to keep track of the number of images loaded for each user ID
    image_count_per_user = {}

    # Iterate through the images in the data folder
    for filename in os.listdir(data_folder):
        if filename.endswith(".jpg"):
            # Extract user ID from the filename (assuming filename format: user.<user_id>.<image_id>.jpg)
            user_id = int(filename.split('.')[1])

            # Check if the user ID is already assigned a class index
            if user_id not in classes:
                classes[user_id] = len(classes)  # Assign a new class index for this user ID

            class_idx = classes[user_id]  # Get the class index for this user ID

            # Check if we have loaded the maximum allowed number of images for this user ID
            if user_id not in image_count_per_user:
                image_count_per_user[user_id] = 0
            if image_count_per_user[user_id] >= max_images_per_user:
                continue

            # Load and preprocess the image(you may need to modify the preprocessing based on your specific requirements
            img_path = os.path.join(data_folder, filename)
            preprocessed_img = preprocess_image(cv2.imread(img_path))

            # Append the preprocessed image and its corresponding class index to the training data
            a.append(preprocessed_img)
            b.append(class_idx)

            # Increment the image count for this user ID
            image_count_per_user[user_id] += 1

            # Check if we have loaded the maximum allowed number of images for this user ID
            if image_count_per_user[user_id] >= max_images_per_user:
                continue

    # Convert the lists to numpy arrays for further processing
    a = np.array(a)
    b = np.array(b)

    print("Training data shape - Features:", a.shape, " Labels:", b.shape)
    print("Mapping of user IDs to class indexes:")
    print(classes)
    print("Image Count per User:")
    print(image_count_per_user)

    # Return the training data and related information
    return a, b, classes, image_count_per_user


# Usage example
data_folder = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\data"  # Modify this path as needed
max_images_per_user = 20  # Modify this value as needed
a, b, classes, image_count_per_user = labelling_data(data_folder, max_images_per_user)

