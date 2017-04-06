# -*- encoding: UTF-8 -*- 

import vrep
import time
import sys
from RobotMotion import RobotMotion
from BraitenbergMotion import BraitenbergMotion
from BumperMotion import BumperMotion
import time

import numpy as np
import matplotlib.pyplot as plt

def main(robotIP, robotPort, motionMode):

	#INIT V-REP SIM
    vrep.simxFinish(-1) #close all open connections
    clientID=vrep.simxStart(robotIP,robotPort,True,True,5000,5)
    #Get all the handles
    if clientID!=-1:
        print('Connected to remote API server')
        #Get the robot handle
        res1,robotHandle=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx',vrep.simx_opmode_oneshot_wait)
        #Get wheel handles
        res2,rightWheel=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_rightMotor',vrep.simx_opmode_oneshot_wait)
        res3,leftWheel=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx_leftMotor',vrep.simx_opmode_oneshot_wait)

        #Get the sensor handles
        sensorHandles = []
        for i in range(1, 16):
            path = 'Pioneer_p3dx_ultrasonicSensor' + str(i)
            res3,sensor=vrep.simxGetObjectHandle(clientID,path,vrep.simx_opmode_oneshot_wait)
            sensorHandles.append(sensor)

        motionProxy = RobotMotion(clientID, robotHandle, leftWheel, rightWheel, sensorHandles)

        if(motionMode == 1):
            motionLogic = BraitenbergMotion(motionProxy)
        else:
            if(motionMode == 2):
               motionLogic = BumperMotion(motionProxy)
            else:
                print('Invalid motion mode!!')
                vrep.simxFinish(-1)
                exit(-1)

        #WHILE NOT BUMPING, KEEP WALKING
        #IF OBJECT FOUND, TURN AROUND
        print ("Starting the main loop")
        x = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        y = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        x_robot = []
        y_robot = []
        while (vrep.simxGetConnectionId(clientID)!=-1):
            #Get the image from the vision sensor
            motionLogic.DoMove();
            x_pos, y_pos, _ = motionLogic.robot.GetRobotPosition()
            x_robot.append(x_pos)
            y_robot.append(y_pos)
            for i in range(16):
                x_pos, y_pos = motionLogic.robot.GetSensorPoint(i, [x_pos,y_pos,_])
                if x_pos != float('inf'):
                    x[i].append(x_pos)
                    y[i].append(y_pos)

        NUM_COLORS = 16

        cm = plt.get_cmap('gist_rainbow')
        colors = [cm(1. * i / NUM_COLORS) for i in range(NUM_COLORS)]


        vrep.simxFinish(-1)
        for i in range(16):
            plt.scatter(y[i], x[i], s=1, c=colors[i])
        plt.scatter(y_robot, x_robot, s=1, c='BLACK')
        plt.gca().invert_xaxis()
        plt.show()
        exit(-1)

    else:
        print('NOT Connected to remote API server. Check if the server is running!')


if __name__ == "__main__":
    robotIp = "127.0.0.1"
    robotPort = 25000
    motionMode = 2 #1 - Braitenberg, 2 - Bumper

    if len(sys.argv) <= 1:
        print ("Usage python moveAround.py robotIP robotPort (optional default: 127.0.0.1 25000)")
    else:
        robotIp = sys.argv[1]
        robotPort = sys.argv[2]
        motionMode = sys.argv[3]

    main(robotIp, robotPort, motionMode)
