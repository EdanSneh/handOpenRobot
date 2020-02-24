#! /usr/bin/env python

import rospy
import robot_api

def wait_for_time():
    """
    Wait for simulated time to begin.
    """
    while rospy.Time().now().to_sec() == 0:
        pass

def main():
    rospy.init_node('greeting_demo')
    wait_for_time()

    filedir = "/home/robotics/work/learnopencv/HandPose"
    #filedir = rospy.get_param('~opencv_dir')
    arm_joints = robot_api.ArmJoints()
    arm = robot_api.Arm()
    gripper = robot_api.Gripper()
    joints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    greeting = robot_api.Greeting(arm, gripper, filedir)
    greeting.fist_bump()
    greeting.hi_five()
    rospy.loginfo("done")



if __name__ == '__main__':
    main()