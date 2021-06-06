![Snoop Mask Logo](https://github.com/mitangshu/Snoop-Mask---Heroku/blob/main/SnoopMaskBGBlack.jpg)
# **Snoop Mask**
It is a mask detection system which can detect the number of people wearing and number of people not wearing masks in a room through real time video feed using Ip cameras. It is a custom trained tiny yolo v3 model. The Web application is created using flask where you can provide the url of Ip cameras and start surveillance of your work place, school or institution.

## Software requirements

- Flask==2.0.1
- Jinja2==3.0.1
- numpy==1.20.3
- opencv-python==4.2.0.32
- Pillow-PIL==0.1.dev0
- requests==2.22.0
- simplejson==3.17.0
- urllib3==1.25.7

## Working

The Snoop Mask asks the user to provide the url of Ip camera or webcam to capture the video.

### Webcam
For accessing the webcam input the value **0** in the input field. This will allow the Videocapture() in cv2 to access the webcam of your device. 
```
cv2.VideoCapture(0)
```
### Ip Camera
For accessing the Ip camera input the **rtsp/http link** in the input field. Make sure the system and the Ip camera are connected through the same wireless network (i.e. Wifi).
```
cv2.VideoCapture('rtsp://username:password@camera_ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp')
```
You can also use your old smartphone as Ip camera by downloading [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&) in your smartphone and click on start server this will open up your camera and the http/rtsp link will be visible to you which you can copy and paste into the input field.

The tiny yolov3 model is trained using darknet and it uses the ReadFromDarknet() present inside dnn opencv module to read and fetch the network architecture of necessary weights and cfg file.

```
cv2.dnn.readNetFromDarknet("yolov3-tiny_masks.cfg","yolov3-tiny_masks_best.weights")
```

## Run server

To run the server open command line and navigate to the project folder and run.
```
python app.py
```
the model is applied over the frames of 
