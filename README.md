# Drowsiness-Detection-on-Rpi
Drowsiness Detection on Rpi 3b+ with location tracking and obstacle detection

Drowsiness of an individual can be measured by the prolonged period of time for which his/her eyes are in shut state. In our process, first the image data is attained by the USB camera for processing. Then we utilize the Haarcascade file face.xml to examine and detect the faces in each discrete frame. When a face is detected, then a region of interest i.e., eyes are marked within the face. If an eye is detected and it is open then the counter is reduced by 1. If the eyes are closed in a particular frame, then the counter is incremented by 1. When the eyes are closed for more time and the frame counter becomes more than 5, then it is deducible that the user is feeling drowsy. Hence tiredness is detected and an alarm is signalled.

Additionally, if the user comes too close to an obstacle or another vehicle, then the ultrasonic sensor will detect closeness of the obstacle and sound an alarm accordingly. By calculating the travel time and the speed of sound, the distance can be preconceived in advance.

GPS module has been used to get location data of the vehicle in terms of latitude and longitude. The module receives a cluster of information in the form of NMEA sentences, which are then parsed to obtain coordinates of the vehicle.

<h2>Drowsiness Detector Assembly</h2>

An ML-based program trained over 2000 pictures to detect drowsiness based on open/closed eyes will be used with a webcam connected to Raspberry Pi on a real-time basis.
This assembly involves building a program to detect whether a person is feeling drowsy or not while driving, based on a given image or video stream. It has been accomplished by two main programs, one for training a model based on a given dataset of open and closed eyes which specifies whether the driver is feeling sleepy or not, and the second, by using the model so-trained to check faces for drowsiness in video streams in real time. 

For this purpose, we have used python script with Keras and TensorFlow for model processing and training and OpenCV for face detection and image processing. 

![image](https://user-images.githubusercontent.com/54680381/174845200-e2016351-01e6-4c0c-bdb2-3efc01749d79.png)
