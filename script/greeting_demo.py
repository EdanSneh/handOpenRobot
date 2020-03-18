#! /usr/bin/env python

import rospy
import robot_api
import os
import actionlib
from move_base_msgs.msg import MoveBaseAction

def wait_for_time():
    """
    Wait for simulated time to begin.
    """
    while rospy.Time().now().to_sec() == 0:
        pass

def main():
    rospy.init_node('greeting_demo')
    wait_for_time()
    
    #r = rospy.Rate(10)
    filedir = os.getcwd()
    #filedir = rospy.get_param('~opencv_dir')
    arm_joints = robot_api.ArmJoints()
    arm = robot_api.Arm()
    move_base_client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    move_base_client.wait_for_server()
    # arm = None
    gripper = robot_api.Gripper()
    greeting = robot_api.Intro(move_base_client)
    #greeting.fist_bump()
    #greeting.hi_five()
    rospy.loginfo("done")
    rospy.spin()

if __name__ == '__main__':
    main()
