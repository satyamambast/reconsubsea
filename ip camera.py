import cv2

cap = cv2.VideoCapture('rtsp://admin:@169.254.99.116/user=admin&password=&channel=1&stream=0.sdp?')

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
