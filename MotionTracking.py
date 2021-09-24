import cv2
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-in", "--input", required = True, help = "input source video")
ap.add_argument("-d","--delay", required = False, type = int, default= 25, help = "input delay")
args = vars(ap.parse_args())

last_frame = None
i = 0
delay = args["delay"]

font = cv2.FONT_HERSHEY_SIMPLEX
base_frame = np.ones((50,50), np.uint8)

walk_img = './images/walk.jpg'
img = cv2.imread(walk_img)
img = cv2.resize(img,(75,75))

if args["input"] == "0":
    cap = cv2.VideoCapture(int(args["input"]))
else:
    cap = cv2.VideoCapture(args["input"])

while True:    
    ret, frame = cap.read()
    if ret:
        
        #resize the frame
        frame = cv2.resize(frame, (640,480))
        #convert color the frame to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #apply filter GaussianBlur with kernel (5,5)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        
        #save the first frame in the last frame variable
        if last_frame is None:
            last_frame = gray     
        
        #calculate subtract last_frame and gray(current frame)
        delta_frame = cv2.absdiff(last_frame, gray)
        #save the current frame(gray) in the last frame variable
        last_frame = gray
        #apply threshold
        threshold = cv2.threshold(delta_frame, 25,255,cv2.THRESH_BINARY)[1]
        #apply dilate with iteration = 2
        dilation = cv2.dilate(threshold, None, 2)
        #apply findContours to get boundary points
        contours = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        #resize dilation
        dilation = cv2.resize(dilation, (50,50))
        
        #if mean of subtraction base_frame - dilation larger 1.5 
        #it means that a motion has occurred in the frame
        #but if this happens in 25 consecutive frames, we record it as a move 
        #you can change the delay with Input Arguments
        if np.mean(base_frame - dilation) > 1.5: 
            delay -= 1
            if delay <= 0:
                delay = 25
                i += 1
                
            for c in contours:
                if cv2.contourArea(c) < 900:
                    continue
                #coordinate of each bounding box
                (x,y,w,h) = cv2.boundingRect(c)
                #change color of bounding box to red
                frame[y:y+h, x:x+w, 2] = 230
                #show image of  motion tracking in coordinate (w->0:75, h-> 0:75)
                frame[:75,:75] = img
                cv2.putText(frame, 'Moving', (85,40), font, 1, (0,0,154), 2)
        cv2.imshow('frame', frame)
 
        if cv2.waitKey(25)& 0xFF == ord('q'):
            break
    else:
        break
            
cap.release()
cv2.destroyAllWindows()