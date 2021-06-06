![Snoop Mask Logo](https://github.com/mitangshu/Snoop-Mask---Heroku/blob/main/SnoopMaskBGBlack.jpg)
# Snoop Mask
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

The tiny yolov3 model is trained using darknet and it uses the ReadFromDarknet() present inside dnn opencv module to read and fetch the necessary weights and cfg file.

'''
cv2.dnn.readNetFromDarknet("yolov3-tiny_masks.cfg","yolov3-tiny_masks_best.weights")
'''
