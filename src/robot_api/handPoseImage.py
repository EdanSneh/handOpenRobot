#!/usr/bin/env python

from __future__ import division
import cv2
import time
import numpy as np
import rospy 
import os

protoFile = "hand/pose_deploy.prototxt"
weightsFile = "hand/pose_iter_102000.caffemodel"
nPoints = 22
POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]

class HandPoseImage(object):
    @staticmethod
    def isHandOpen(frame, fileDir):
        t = rospy.Time.now().to_sec()
        net = cv2.dnn.readNetFromCaffe(os.path.join(fileDir, protoFile), os.path.join(fileDir,weightsFile))

        frameCopy = np.copy(frame)
        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]
        aspect_ratio = frameWidth/frameHeight

        threshold = 0.1

        # input image dimensions for the network
        inHeight = 368
        inWidth = int(((aspect_ratio*inHeight)*8)//8)
        inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)

        net.setInput(inpBlob)

        output = net.forward()
        #print("time taken by network : {:.3f}".format(time.time() - t))

        # Empty list to store the detected keypoints
        points = []

        for i in range(nPoints):
            # confidence map of corresponding body's part.
            probMap = output[0, i, :, :]
            probMap = cv2.resize(probMap, (frameWidth, frameHeight))

            # Find global maxima of the probMap.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

            if prob > threshold :
                cv2.circle(frameCopy, (int(point[0]), int(point[1])), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                cv2.putText(frameCopy, "{}".format(i), (int(point[0]), int(point[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)

                # Add the point to the list if the probability is greater than the threshold
                points.append((int(point[0]), int(point[1])))
            else :
                points.append(None)
        avgX = 0
        avgY = 0
        for index in range(nPoints):
            point = points[index]
            if (point != None):
                avgX += point[0]
                avgY += point[1]

        avgX = avgX / nPoints
        avgY = avgY / nPoints

        varianceFingers = 0
        detect = 0
        #get variance
        for i in [20, 16, 12, 8]:
            point = points[i]
            if point is not None:
                varianceFingers += (point[0] - avgX)**2
                varianceFingers += (point[1] - avgY)**2
                detect += 1
        if (detect != 0):
            varianceFingers = varianceFingers/detect
        else:
            varianceFingers = 0

        varianceBase = 0
        detect = 0
        for i in [18, 14, 10, 6]:
            point = points[i]
            if point is not None:
                varianceBase += (point[0] - avgX)**2
                varianceBase += (point[1] - avgY)**2
                detect += 1
        if (detect != 0):
            varianceBase = varianceBase/detect
        else:
            varianceBase  = 0

        #print(varianceBase)
        #print(varianceFingers)
        rospy.loginfo((rospy.Time.now().to_sec() - t))
        if (varianceBase == varianceFingers and varianceFingers == 0):
            return None
        return varianceFingers - varianceBase > 0

if __name__ == "__main__":
    frame = cv2.imread("../../_temp/hand.jpg")
    hpi = HandPoseImage()
    ans = hpi.isHandOpen(frame, "/home/robotics/work/learnopencv/HandPose/")
    print(ans)