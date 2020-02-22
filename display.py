import cv2
import numpy
import math
from enum import Enum
import network_tables
from cscore import CameraServer, VideoSource, UsbCamera, MjpegServer

import reflective_detective as rd

def live_video(camera, ntinstance = None):
        """
        Opens a window with live video.
        :param camera:
        :return:
        """
        nt = network_tables.NTHandler(ntinstance)
        hue_min = nt.addListener("Vision/Hue/Min", 40)
        hue_max = nt.addListener("Vision/Hue/Max", 86)
        sat_min = nt.addListener("Vision/sat/Min", 0)
        sat_max = nt.addListener("Vision/sat/Max", 84)
        val_min = nt.addListener("Vision/val/Min", 220)
        val_max = nt.addListener("Vision/val/Max", 255)
        min_area = nt.addListener("Vision/area/min", 3800)
        max_area = nt.addListener("Vision/area/max", 5000)

        cs = CameraServer.getInstance()

        cvSink = cs.getVideo(camera = camera)
        outputStream = cs.putVideo("Contours", 1280, 720)

        #video_capture = cv2.VideoCapture(0)
        pipeline = rd.GripPipeline()

        pipeline.NT_HSV([hue_min, hue_max], [sat_min, sat_max], [val_min, val_max],)
        pipeline.NT_Area(min_area, max_area)

        frame = numpy.zeros(shape=(1280, 720, 3), dtype=numpy.uint8)

        while True:
            # Capture frame-by-frame
            # ret, frame = video_capture.read()
            time, frame = cvSink.grabFrame(frame)

            # Display the resulting frame
            #cv2.imshow('Video', frame)
            pipeline.process(frame)
            #cv2.imshow("grip", pipeline.hsv_threshold_output)
            
            contours = pipeline.filter_contours_output

            cv2.drawContours(frame, contours, -1, (127,0,255), 3)
            outputStream.putFrame(frame)

            #cv2.imshow("contours", frame)

            if contours:
                moment = cv2.moments(contours[0])
                center = (moment['m10'] / (moment['m00'] + 1e-5), moment['m01'] / (moment['m00'] + 1e-5))

                screen_height = numpy.size(frame, 0)
                screen_width = numpy.size(frame, 1)

                nt.addValue("Vision/Center/X", center[0] - screen_width/2)
                nt.addValue("Vision/Center/Y", center[1] - screen_height/2)

            else:
                nt.addValue("Vision/Center/X", 0)
                nt.addValue("Vision/Center/Y", 0)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            
        # When everything is done, release the capture
        #video_capture.release()
        cv2.destroyAllWindows() 

if __name__ == "__main__":
    live_video(1)