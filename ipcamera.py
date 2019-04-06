import cv2

cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

while(True):
    ret, frame = cap.read()
    ret1, frame1 = cap1.read()
    cv2.imshow('frame',frame)
    cv2.imshow('frame1',frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
