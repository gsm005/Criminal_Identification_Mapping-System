import face_recognition
import cv2
import numpy as np
import os
import smtplib
import winsound
import email
import time

# To produce a notifying sound 
def make_noise():
  duration = 1000  # milliseconds
  freq = 440 # Hz
  winsound.Beep(freq, duration)

# To send a notification mail 
# server=smtplib.SMTP('smtp.gmail.com',587)
# server.starttls()
# server.login('sender username','password' )  # set up your email id before running the program
# def mail(text):
#     subject="Identified a Face"
#     message='Subject: {}\n\n{}'.format(subject,text)
#     server.sendmail('sender email id','reciever email id',message)  # Enter the senders and recievers address before running the program

video_capture = cv2.VideoCapture(0)

print("loading image")
image1 = face_recognition.load_image_file(os.path.abspath("Criminal Detection System\known_faces\srk.jpg"))
image2 = face_recognition.load_image_file(os.path.abspath("Criminal Detection System\known_faces\Donald Trump.jpg"))
image3 = face_recognition.load_image_file(os.path.abspath("Criminal Detection System\known_faces\Mark Zuckerberg.jpg"))
image4 = face_recognition.load_image_file(os.path.abspath("Criminal Detection System\criminal_faces\Takeshi.jpeg"))
print("processing image")
image1_face_encoding = face_recognition.face_encodings(image1)[0]
image2_face_encoding = face_recognition.face_encodings(image2)[0]
image3_face_encoding = face_recognition.face_encodings(image3)[0]
image4_face_encoding = face_recognition.face_encodings(image4)[0]

known_face_encodings = [image1_face_encoding,
    image2_face_encoding,image3_face_encoding,image4_face_encoding]
known_face_names = [
    "Shah Rukh Khan","Donald Trump","Mark Zuckerberg","Takeshi"
]

face_locations = []
face_encodings = []
face_names = []
check=[]
process_this_frame = True

i=0
while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    print(rgb_small_frame)
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_names.append(name)

    process_this_frame = not process_this_frame
    print ("Face detected -- {}".format(face_names))
    if('Shah Rukh Khan' in face_names or 'Donald Trump' in face_names or 'Mark Zuckerberg' in face_names or 'Takeshi' in face_names):
        make_noise()
        # To prevent from sending spam 
        if (i==0):
            t=time.localtime()
            current_time=time.strftime("%H:%M:%S",t)
            text="Face detected -- {} at time--{}".format(face_names,current_time)
            # mail(text)
            i=1
            check=face_names
        if(check!=face_names):
            i=0
        
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()