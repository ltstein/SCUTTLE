import cv2
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX


v1_min = 0     # Minimum H value
v2_min = 180     # Minimum S value
v3_min = 130    # Minimum V value

v1_max = 10     # Maximum H value
v2_max = 255     # Maximum S value
v3_max = 255    # Maximum V value

width  = 240
height = 160

#    RGB or HSV

# filter = 'HSV'  # Use HSV to describe pixel color values

class MyFilter:

    def colorTracking(self, image):

        image = cv2.resize(image,(240,160))

        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if len(cnts) > 0:

            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 6:

                cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(image,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)

        thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        all = np.hstack((image, thresh, mask))

        cv2.line(all,(width,0),(width,height), (0xff, 0xff, 0xff), thickness=3)
        cv2.line(all,(width*2,0),(width*2,height), (0xff, 0xff, 0xff), thickness=3)

        cv2.putText(all,'Original',(10,int(height/10)), font, 0.5,(255,255,255),1,cv2.LINE_AA)
        cv2.putText(all,'Thresh',(width+10,int(height/10)), font, 0.5,(255,255,255),1,cv2.LINE_AA)
        cv2.putText(all,'Mask',((width*2)+10,int(height/10)), font, 0.5,(255,255,255),1,cv2.LINE_AA)

        return all

def init_filter():
    f = MyFilter()
    return f.colorTracking