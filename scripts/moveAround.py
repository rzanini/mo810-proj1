# -*- encoding: UTF-8 -*- 

import vrep,time,sys
from RobotMotion import RobotMotion
from BraitenbergMotion import BraitenbergMotion
import time

def main(robotIP, robotPort):

	#INIT V-REP SIM
    vrep.simxFinish(-1) #close all open connections
    clientID=vrep.simxStart(robotIP,robotPort,True,True,5000,5)
    #Get all the handles
    if clientID!=-1:
        print('Connected to remote API server')
        #Get the robot handle
        res1,robotHandle=vrep.simxGetObjectHandle(clientID,'Pioneer_p3dx',vrep.simx_opmode_blocking)
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

        motionLogic = BraitenbergMotion(motionProxy)

        #WHILE NOT BUMPING, KEEP WALKING
        #IF OBJECT FOUND, TURN AROUND
        print ("Starting the main loop")
        while (vrep.simxGetConnectionId(clientID)!=-1):
            #Get the image from the vision sensor
            motionLogic.DoMove();

        motionProxy.Stop()

    else:
        print('NOT Connected to remote API server. Check if the server is running!')


if __name__ == "__main__":
    robotIp = "127.0.0.1"
    robotPort = 25000

    if len(sys.argv) <= 1:
        print ("Usage python moveAround.py robotIP robotPort (optional default: 127.0.0.1 25000)")
    else:
        robotIp = sys.argv[1]
        robotPort = sys.argv[2]

    main(robotIp, robotPort)
