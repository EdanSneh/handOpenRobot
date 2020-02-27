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
    def __init__(self, arm, gripper, opencv_dir):
        self.arm = arm
        self.gripper = gripper
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/head_camera/rgb/image_raw", Image, self.image_callback, queue_size=14)
        self.opencv_dir = opencv_dir
        self.busy = False
        rospy.loginfo("finish startup")
    
    def image_callback(self, msg):
        rospy.loginfo("busy: " + str(self.busy))
        if not self.busy:
            self.busy = True
            try:
                cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                self.bridge = CvBridge()
                hand_status = HandPoseImage.isHandOpen(cv_image, self.opencv_dir)
                rospy.loginfo(hand_status)
                if hand_status:
                    self.hi_five()
                elif hand_status is not None:
                    self.fist_bump()
            except CvBridgeError as e:
                print(e)
            self.busy = False

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
