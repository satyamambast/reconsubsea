import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
class ipcamera(object):
    def __init__(self,ip):
        self.ip=ip
        self.cap = cv2.VideoCapture(ip)
    def show(self):
        ret, frame = self.cap.read()
        cv2.imshow('frame',frame)
class digcamera(object):
    def __init__(self,socket):
        self.socket=socket
        self.conn,self.addr=self.socket.accept()
        self.data = b""
        self.payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(self.payload_size))
    def show(self):
        while len(self.data) < self.payload_size:
            print("Recv: {}".format(len(self.data)))
            self.data += self.conn.recv(4096)
        print("Done Recv: {}".format(len(self.data)))
        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))
        while len(self.data) < msg_size:
            self.data += self.conn.recv(4096)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        h,w = frame.shape[:2]
        frame1=cv2.resize(frame,(2*w,2*h), interpolation = cv2.INTER_LINEAR)   
        cv2.imshow('ImageWindow',frame)


if __name__=='__main__':
    HOST=''
    PORT=8489
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket created')
    s.bind((HOST,PORT))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')
    ip=ipcamera('rtsp://admin:@169.254.99.116/user=admin&password=&channel=1&stream=0.sdp?')
    dig=digcamera(s)
    while True:
        ip.show()
        dig.show()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break