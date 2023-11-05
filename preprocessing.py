import cv2


def preprocess_image(img, target_size=(128, 128)):
    # Resize the image to the target size
    img_resized = cv2.resize(img, target_size)

    # Normalize pixel values to [0, 1]
    img_normalized = img_resized / 255.0

    return img_normalized
