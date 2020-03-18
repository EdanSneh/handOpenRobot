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
import datetime
from move_base_msgs.msg import MoveBaseGoal

class Intro(object):
    def __init__(self, base):
        self.person = None
        self.executing = False
        self.move_base_client = base
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/head_camera/rgb/image_raw", Image, self.image_callback, queue_size=None, buff_size=2**4)
        #self.opencv_dir = opencv_dir
        #self.busy = False
        rospy.loginfo("finished intro")
    
    def move_coords(self, x, y, z_o, w_o):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x 
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.z = z_o
        goal.target_pose.pose.orientation.w = w_o
        self.move_base_client.send_goal(goal)

        wait = self.move_base_client.wait_for_result()
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        else:
            print "robot moving to X: " + str(x) + " Y: " + str(y) + "!"

    def image_callback(self, msg):
        #insures no spam
        if (self.executing):
            return
        x = raw_input("What should I do John?: ")
        x = lower(x)
        if x != None:
            self.executing = True
            if "move" in x and "door" in x:
                #change to door coordinates
                self.move_coords(5.87850, -4.437968, -0.72877, 0.684753)
                # if human is detected at door
                if (True):
                   self.person = self.ask_for_info();
                print "Please follow me " + self.person[0] + ", we are moving back to john"
                self.move_coords(-1.1198997, -2.3416571, 0.85388, 0.5204697778)
            elif self.person != None and "who" in x and "that" in x:
                print("John this is your friend " + self.person[0] + "who came from the door and they would love to have some " + self.person[1])
            self.executing = False

    def ask_for_info(self):
        name_list = ["jessica", "allison", "fred", "jeff", "brian", "ashley"]
        drink_list = ["milk", "water", "punch", "root beer"]
        result_name = None
        result_drink = None
        print("Can you please provide your name and drink?")
        tries = 5
        remaining = tries
        while (result_name is None or result_drink is None) and remaining != 0:
            if tries != remaining:
                if result_name is None and result_drink is None:
                    print("Sorry I didnt quite catch that")
                elif result_name is None:
                    print("Can you please repeat your name")
                elif result_drink is None:
                    print("Can you please repeat your favorite drink")
            text = raw_input() 
            lower_text = text.lower()
            if result_name is None:
                for name in name_list:
                    if name.lower() in lower_text:
                        result_name = name
                        break

            if result_drink is None:
                for drink in drink_list:
                    if drink.lower() in lower_text:
                        result_drink = drink
                        break
            remaining -= 1
        # bad path, robot failed to recognize speech
        if result_name is None or result_drink is None:
            return None
        # good path, robot recognized name and drink
        result = (result_name, result_drink)
        print("Hi, " + result[0] + " intresting to hear your favorite drink is " + result[1])
        return result
