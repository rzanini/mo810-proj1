import vrep,time,sys
from math import sqrt

class RobotMotion:

    def __init__(self, clientId, robot, left, right, sensors):
        self.clientId = clientId
        self.robot = robot    # instance variable unique to each instance
        self.leftWheel = left    # instance variable unique to each instance
        self.rightWheel = right    # instance variable unique to each instance
        self.sensors = sensors
        self.InitProximitySensors()

    def MoveForward(self, left, right):
        #START WALKING AT MAX SPEED
        vrep.simxSetJointTargetVelocity(self.clientId, self.leftWheel, left, vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(self.clientId, self.rightWheel, right, vrep.simx_opmode_streaming)

    def Stop(self):
        #TARGET VELOCITY
        print ("Stoping!!")
        vrep.simxSetJointTargetVelocity(self.clientId, self.leftWheel, 0, vrep.simx_opmode_streaming)
        vrep.simxSetJointTargetVelocity(self.clientId, self.rightWheel, 0, vrep.simx_opmode_streaming)

    def GetRobotPosition(self):
        res,robotPosition = vrep.simxGetObjectPosition(self.clientId,self.robot,-1,vrep.simx_opmode_streaming)
        return robotPosition

    def GetRobotOrientation(self):
        res,robotOrientation = vrep.simxGetObjectOrientation(self.clientId,self.robot,-1,vrep.simx_opmode_streaming)
        return robotOrientation

    def InitProximitySensors(self):
        for i in range(1, 16):
            res,state,point,detectedObj,vector = vrep.simxReadProximitySensor(self.clientId,self.sensors[i-1],vrep.simx_opmode_streaming)

    def GetSensorDistance(self, i):
        ret, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(self.clientId,self.sensors[i-1],vrep.simx_opmode_buffer)
        distance = sqrt(sum([x ** 2 for x in detectedPoint]))
        return detectionState, distance