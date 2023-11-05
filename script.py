import cv2

roi_list=[];
def draw_boundary(img, classifier, scaleFactor,minNeigbors, color, text):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeigbors)
    coords = []
    for(x,y,w,h) in features:
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
        cv2.putText(img, text,(x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]

    return coords

def detect(img, faceCascade, eyecascade,nosecascade, mouthcascade):
    color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}

    coords = draw_boundary(img, faceCascade, 1.1, 10, color['blue'], "Face")

    if len(coords)== 4:
        roi_img = img[coords[1]:coords[1] + coords[3], coords[0]:coords[0] + coords[2]]
        coords = draw_boundary(roi_img, eyecascade,1.2,14, color['red'], "Eyes")
        coords = draw_boundary(roi_img, nosecascade, 1.6, 5, color['green'], "Nose")
        coords = draw_boundary(roi_img, mouthcascade, 1.2, 20, color['white'], "Mouth")

    return img

faceCascade = cv2.CascadeClassifier('frontalface.xml')
nosecascade = cv2.CascadeClassifier('Nose.xml')
mouthcascade = cv2.CascadeClassifier('Mouth.xml')
eyecascade = cv2.CascadeClassifier('Eye.xml')
video_capture = cv2.VideoCapture(0)

while True:

    _,img =video_capture.read()
    img= detect(img, faceCascade,eyecascade,nosecascade, mouthcascade)
    cv2.imshow("face detection", img)
    roi_list.append(img);

    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
print("Number of ROI images stored:", len(roi_list))

video_capture.release()
cv2.destroyAllWindows()