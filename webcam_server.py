import numpy as np
import cv2
import time
import imutils
import pickle
import sys

cap = cv2.VideoCapture(0) # Capture video from camera
cap.set(cv2.CAP_PROP_FPS, 10)

# Get the width and height of frame
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use the lower case
# # out = cv2.VideoWriter('output_feet_close_not_low.mp4', fourcc, 20.0, (width, height))
# out = cv2.VideoWriter('jacques_squat.mp4', fourcc, 20.0, (width, height))

frames = []

num_frames = 0
time_start = time.time()

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.flip(frame,0)
        frame = imutils.rotate(frame, 270)


        # write the flipped frame
        # print(frame.shape)
        frames.append(cv2.resize(frame, (450, 450)))

        # out.write(frame)
        if time.time()-time_start > 5.0:
            break 

cap.release()
cv2.destroyAllWindows()

frames = np.asarray(frames)

serialized_frames = pickle.dumps(frames, protocol=2)

import socket

# TCP_IP = '192.168.1.4'
TCP_IP = '52.233.168.92'
TCP_PORT = 9010

BUFFER_SIZE = 4096
# MESSAGE = "Hello, World!"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.sendall(serialized_frames)
s.send('end'.encode())
data = s.recv(BUFFER_SIZE)
s.close()
print("received data:", data)
data = data.decode()

from gtts import gTTS
import os

if data == "nosquat":
    tts = gTTS(text='I did not see a squat', lang='en')
elif data == "":
    tts = gTTS(text='That was a perfect squat!', lang='en')
elif data == "notlow":
    tts = gTTS(text='You need to squat lower.', lang='en')
elif data == "#feetclose":
    tts =gTTS(text='You need to widen your stance.', lang='en')
else:
    tts = gTTS(text='You need to squat lower and widen your stance.', lang='en')

tts.save('foo.mp3')
os.system("afplay foo.mp3")



# with h5py.File('jacques_squat.h5', 'w') as hf:
#     hf.create_dataset("squat.h5",  data=np.asarray(frames))

    # Release everything if job is finished
# out.release()
