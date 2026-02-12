import cv2

vid = cv2.VideoCapture(0)
vid.set(3, 400)
vid.set(4, 200)

while(True):
    rect, frame = vid.read()
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()