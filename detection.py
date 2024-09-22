import cv2

def faceDetect(imagePath):
    img = cv2.imread(imagePath)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    face = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.3, minNeighbors=5, minSize=(40, 40)
    )
    if len(face) > 0:
        for (x, y, w, h) in face:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
        cv2.imwrite(imagePath , img)
        return True
    else:
        return False

