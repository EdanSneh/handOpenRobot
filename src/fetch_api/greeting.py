#! /usr/bin/env python

import rospy
from sensor_msgs.msg import Image
import numpy as np
from cv_bridge import CvBridge, CvBridgeError

from .arm import Arm
from .gripper import Gripper
from .util import Util
from .handPoseImage import HandPoseImage

def Greeting(object):
    def __init__(self, arm, gripper, image_sub):
        self.arm = arm
        self.gripper = gripper
        self.image_sub = rospy.Subscriber("/head_camera/rgb/image_raw", Image, self.image_callback)
    
    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.bridge = CvBridge()
            if isHandOpen(cv_image):
                self.hi_five()
            else:
                self.fist()
        except CvBridgeError as e:
           print(e)

    def hi_five(self):
        pose = 
        self.arm.move_to_pose()
        self.gripper.open()
        self.arm.reset_post()

    def fist(self):
        pose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.arm.move_to_pose(ArmJoints.from_list(pose))
        self.gripper.close()
        self.arm.reset_post()
