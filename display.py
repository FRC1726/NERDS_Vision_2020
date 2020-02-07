import cv2
import numpy
import math
from enum import Enum
import network_tables

import reflective_detective as rd

def live_video(camera_port=1):
        """
        Opens a window with live video.
        :param camera:
        :return:
        """
        nt = network_tables.NTHandler()
        hue_min = nt.addListener("Vision/Hue/Min")
        hue_max = nt.addListener("Vision/Hue/Max")
        sat_min = nt.addListener("Vision/sat/Min")
        sat_max = nt.addListener("Vision/sat/Max")
        val_min = nt.addListener("Vision/val/Min")
        val_max = nt.addListener("Vision/val/Max")


        video_capture = cv2.VideoCapture(1)
        pipeline = rd.GripPipeline()

        pipeline.NT_HSV([hue_min, hue_max], [sat_min, sat_max], [val_min, val_max])

        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            # Display the resulting frame
            cv2.imshow('Video', frame)
            pipeline.process(frame)
            cv2.imshow("grip", pipeline.hsv_threshold_output)

            contours = pipeline.filter_contours_output

            cv2.drawContours(frame, contours, -1, (0,255,0), 3)

            cv2.imshow("contours", frame)
            
            if contours:
                moment = cv2.moments(contours[0])
                center = (moment['m10'] / (moment['m00'] + 1e-5), moment['m01'] / (moment['m00'] + 1e-5))

                nt.addValue("Vision/Center/X", center[0])
                nt.addValue("Vision/Center/Y", center[1])

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows() 

if __name__ == "__main__":
    live_video(1)