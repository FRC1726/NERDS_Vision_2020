import cv2
import numpy
import math
from enum import Enum

import reflective_detective as rd

def live_video(camera_port=1):
        """
        Opens a window with live video.
        :param camera:
        :return:
        """

        video_capture = cv2.VideoCapture(1)
        pipeline = rd.GripPipeline()

        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            # Display the resulting frame
            cv2.imshow('Video', frame)
            pipeline.process(frame)
            cv2.imshow("grip", pipeline.hsv_threshold_output)
            cv2.drawContours(frame, pipeline.filter_contours_output, -1, (0,255,0), 3)

            cv2.imshow("contours", frame)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows() 

if __name__ == "__main__":
    live_video(1)