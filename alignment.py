import dlib
import cv2
# Load the face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


def align_faces(face_images):
    aligned_faces = []

    for face in face_images:
        # Perform face alignment
        dets = detector(face, 1)
        for d in dets:
            shape = predictor(face, d)
            aligned_face = dlib.get_face_chip(face, shape)
            aligned_faces.append(aligned_face)
    # cv2.imshow("face detection", aligned_faces)
    return aligned_faces


