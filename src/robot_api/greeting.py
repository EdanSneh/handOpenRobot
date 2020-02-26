#! /usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
import numpy as np
from cv_bridge import CvBridge, CvBridgeError

from .gripper import Gripper
from .arm import Arm
from .util import Util
from .handPoseImage import HandPoseImage
from .arm_joints import ArmJoints

class Greeting(object):
    def __init__(self, arm, gripper, image_sub, opencv_dir):
        self.arm = arm
        self.gripper = gripper
        self.image_sub = rospy.Subscriber("/head_camera/rgb/image_raw", Image, self.image_callback)
        self.opencv_dir = opencv_dir
    
    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.bridge = CvBridge()
            if HandPoseImage.isHandOpen(cv_image, self.opencv_dir):
                self.hi_five()
            else:
                self.fist()
        except CvBridgeError as e:
           print(e)

    def hi_five(self):
        rospy.loginfo("start hi five")
        '''
        pose = Pose(Point(0.042, 0.384, 1.826), Quaternion(0.173, -0.693, -0.242, 0.657))
        ps = PoseStamped()
        ps.header.frame_id = 'base_link'
        ps.pose = pose
        err = self.arm.move_to_pose(ps)
        rospy.sleep(1)
        if err is not None:
            rospy.logerr(err)
        '''
        self.gripper.open()
        rospy.sleep(1)
        #self.arm.reset_post()
        #rospy.sleep(1)

    def fist_bump(self):
        rospy.loginfo("start fist bump")
        '''
        joints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        err = self.arm.move_to_joints(ArmJoints.from_list(joints))
        rospy.sleep(1)
        if err is not None:
            rospy.logerr(err)
        '''
        self.gripper.close()
        rospy.sleep(1)
        #self.arm.reset_post()
        rospy.sleep(1)
