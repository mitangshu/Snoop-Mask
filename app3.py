from flask import Flask, render_template, Response, request
import numpy as np
import cv2
import time
import winsound
import urllib.request

app = Flask(__name__)
#cameras = ['G:\Mitangshu_TensorFlow\Mask_Yolo\Pro5.mp4','G:\Mitangshu_TensorFlow\Mask_Yolo\Pro3.mp4',  'G:\Mitangshu_TensorFlow\Mask_Yolo\Pro2.mp4', 0]

class Camera:
    def Get_camera(self, camera):
        #cm = camera
        return camera

    def find_camera(self, id):
        print('Camera list =>', self.Get_camera(cm))
        return self.Get_camera(cm)[int(id)]
    #  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
    #  for webcam use zero(0)
     

    def gen_frames(self, camera_id):
         
        cam = self.find_camera(camera_id)
        cap=  cv2.VideoCapture(cam)
        net = cv2.dnn.readNetFromDarknet("G:/Mitangshu_TensorFlow/SnoopMaskRevive/V3_2/yolov3-tiny_masks.cfg","G:/Mitangshu_TensorFlow/SnoopMaskRevive/V3_2/yolov3-tiny_masks_best.weights")
        #net = cv2.dnn.readNet('G:\Mitangshu_TensorFlow\Mask_Yolo\Mask_NOMask\yolov3_training_last.weights', 'G:\Mitangshu_TensorFlow\Mask_Yolo\yolov3_testing_mask.cfg')
        classes = []
        with open("G:\Mitangshu_TensorFlow\SnoopMaskRevive\obj.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]
        print(len(classes))
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))

        # Loading camera
        #cap = cv2.VideoCapture('https://192.168.29.112:8080/video')

        font = cv2.FONT_HERSHEY_PLAIN
        starting_time = time.time()
        frame_id = 0


        while True:
            # Capture frame-by-frame
            success, frame = cap.read()
            # read the camera frame
            frame_id += 1
            frame = cv2.resize(frame,(480,320),fx=0.4,fy=0.4)
            img = cv2.imread('G:\Mitangshu_TensorFlow\SnoopMaskRevive\SnoopMaskBG.png')
            height, width, channels = frame.shape
            
            blob = cv2.dnn.blobFromImage(frame, 0.005, (160, 160), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)
            
            img = cv2.resize(img, (170,30))
        
            img_h, img_w, img_c = img.shape
            y = 290
            x = 0
            frame[ y:y+img_h , x:x+img_w ] = img

            # Showing informations on the screen
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        # Rectangle coordinates
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)

            elapsed_time = time.time() - starting_time
            fps = frame_id / elapsed_time
            '''
            cv2.rectangle(frame,(0,0), (400, 40), (170,198,57), thickness = cv2.FILLED )
            cv2.putText(frame, "Rider Assist System", (5, 30), font, 2, (0,0,0), 2)'''
            cv2.rectangle(frame,(160,290), (480, 320), (154,250,0), thickness = cv2.FILLED )
        
        
            cv2.putText(frame,"fps= "+"{0:.2f}".format(fps),(5, 15),1, font, (0,0,0), 2 )
            cv2.putText(frame, "Mask= " ,(190, 310), font, 1.2, (0,0,0), 1 )
            cv2.putText(frame, "No Mask= ",(330,310), font, 1.2, (0,0,0), 1 )
            cv2.line(frame, (320,292), (320,318), (0,0,0), 1)
            mask_counter = 0
            nomask_counter = 0

            for i in range(len(boxes)):

                if i in indexes:

                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = confidences[i]
                    color = colors[class_ids[i]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + 10), color, -1)
                    cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 10), font, 0.8, (255,255,255), 2)
                    #if confidence>0.6:
                        #cv2.putText(frame,"Boxes: "+ str(i),(5, 120), font, 1, (0,0,0), 1 )

                    if class_ids[i] == 0:
                        mask_counter =mask_counter+ 1


                    elif class_ids[i] == 1:
                        nomask_counter =nomask_counter+ 1


            safe = (mask_counter-nomask_counter)
            if safe<0:
            
                cv2.rectangle(frame,(390, 0),(480, 20), (0,0,255), thickness = cv2.FILLED)
                cv2.putText(frame,"UNSAFE",(400, 15),font,1.2,(255,255,255),2)
            else:
                cv2.rectangle(frame,(390, 0),(480, 20), (0,255,0), thickness = cv2.FILLED)
                cv2.putText(frame,"SAFE",(410,15),font,1.2,(255,255,255),2)


            cv2.putText(frame,str(mask_counter),(270, 310), font, 1.2, (0,0,0), 1 )
            cv2.putText(frame,str(nomask_counter),(440,310), font, 1.2,(0,0,0), 1 )    
            
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

#print(len(cameras))
C = Camera()

@app.route('/video_feed/<string:id>/', methods=["GET"])
def video_feed(id):
   
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(C.gen_frames(id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/', methods = ['GET','POST'])
def data():
    num= []
    if request.method == 'POST':
        
        num = request.form.getlist('Camera Links')
        num1 = num[0]
        num2 = num[1]
        num3 = num[2]
        num4 = num[3]
        print(num)
        global cm
        cm = num
        cm = [0 if i == '0' else i for i in num]
        C.Get_camera(num)
        result = num1 
        '''for i in range(0,3):
            a = request.form['i']
            links.append(a)'''
        #print(links)
        
    else:
        num1 = ''
        num2 = ''
        num3 = ''
        num4 = ''
        result = ''
    

        
        #form_data = request.form
        
    return render_template('index2.html',num1 = num1, num2 = num2,num3=num3, result = result, num4=num4,data = len(num))

'''@app.route('/', methods=["GET"])
def index():

    return render_template('index2.html',num1 = num1, num2 = num2,num3=num3, result = result, num4=num4, data = len(Get_camera()))
'''
if __name__ == '__main__':
    app.run()