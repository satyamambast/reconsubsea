"""
Default IP to use:
192.168.1.30- PC 
192.168.1.31- PC default Gateway
192.168.1.33- Raspberry
192.168.1.41- IP Camera
192.168.1.4x- For Subsequent IP CAMERAS
"""
import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import threading
import time
from pymavlink import mavutil
master = mavutil.mavlink_connection('udp:0.0.0.0:14143')
def ipshow(ip,a):
    cap=cv2.VideoCapture(ip)
    while True:
        ret, frame = cap.read()
        #h,w = frame.shape[:2]
        #frame1=cv2.resize(frame,(w/2,h/2), interpolation = cv2.INTER_LINEAR)
        cv2.imshow(a,frame)
        cv2.waitKey(1)

def digitalshow(s,a):
    socket=s
    conn,addr=socket.accept()
    data = b""
    payload_size = struct.calcsize(">L")    
    while True:
        while len(data) < payload_size:
            #print("Recv: {}".format(len(data)))
            data += conn.recv(4096)

        #print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        #print("msg_size: {}".format(msg_size))
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        h,w = frame.shape[:2]

        frame1=cv2.resize(frame,(2*w,2*h), interpolation = cv2.INTER_LINEAR)   
        
        cv2.imshow(a,frame1)
        cv2.waitKey(1)
def printpar(dictn,param):
    if param in dictn:
        return (param+" : "+dict[param])
def pixhawk_parameters():
    while True:
        try:
            dict=master.recv_match().to_dict()
            #print(dict['yaw'],dict['pitch'],dict['roll'])
        except:
            pass
        time.sleep(0.1)

if __name__=='__main__':
    HOST=''
    PORT=8485
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket created')
    s.bind((HOST,PORT))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')
    """ip=ipcamera('rtsp://admin:@192.168.1.41/user=admin&password=&channel=1&stream=0.sdp?')
    dig=digcamera(s)"""
    ip='rtsp://admin:@192.168.2.41/user=admin&password=&channel=1&stream=0.sdp?'
    t1=threading.Thread(target=ipshow, args=(ip,'IP Camera 1'))
    t2=threading.Thread(target=digitalshow, args=(s,'Digital Camera 1'))
    t3=threading.Thread(target=pixhawk_parameters)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

    """while True:
        ip.show()
        dig.show()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break"""
