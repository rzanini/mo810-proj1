import vrep,time,sys
from math import sqrt,pi, cos, sin

class RobotMotion:

    def __init__(self, clientId, robot, left, right, sensors):
        self.clientId = clientId
        self.robot = robot    # instance variable unique to each instance
        self.leftWheel = left    # instance variable unique to each instance
        self.rightWheel = right    # instance variable unique to each instance
        self.sensors = sensors
        self.InitProximitySensors()
        self.InitRobotPosition()
        self.InitRobotOrientation()
        self.sensorAngles = [-90, -50, -30, -10, 10, 30, 50, 90 ,90, 130, 150, 170, -170, -150, -130, -90]
        for i in range(16):
            self.sensorAngles[i] = self.sensorAngles[i]*pi / 180  # convert to radian

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
        res,robotPosition = vrep.simxGetObjectPosition(self.clientId,self.robot,-1,vrep.simx_opmode_buffer)
        return robotPosition

    def InitRobotPosition(self):
        res,robotPosition = vrep.simxGetObjectPosition(self.clientId,self.robot,-1,vrep.simx_opmode_streaming)
        return robotPosition

    def GetRobotOrientation(self):
        res,robotOrientation = vrep.simxGetObjectOrientation(self.clientId,self.robot,-1,vrep.simx_opmode_buffer)
        return robotOrientation

    def InitRobotOrientation(self):
        res,robotOrientation = vrep.simxGetObjectOrientation(self.clientId,self.robot,-1,vrep.simx_opmode_streaming)
        return robotOrientation

    def InitProximitySensors(self):
        for i in range(1, 16):
            res,state,point,detectedObj,vector = vrep.simxReadProximitySensor(self.clientId,self.sensors[i-1],vrep.simx_opmode_streaming)

    def GetSensorDistance(self, i):
        ret, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(self.clientId,self.sensors[i-1],vrep.simx_opmode_buffer)
        #distance = sqrt(sum([x ** 2 for x in detectedPoint]))
        distance = detectedPoint[2]
        return detectionState, distance, detectedPoint

    def GetSensorPoint(self,i,robotPosition):
        _,_,robot_angle = self.GetRobotOrientation()
        #robot_x,robot_y, _  = self.GetRobotPosition()
        robot_x = robotPosition[0]
        robot_y = robotPosition[1]
        angle = self.sensorAngles[i] + robot_angle
        state, d, point = self.GetSensorDistance(i)
        if(state == 0): return [float('inf'),float('inf')]
        d = d + 0.0975
        x_delta = cos(angle) * d
        y_delta = sin(angle) * d
        x_pos = robot_x + x_delta
        y_pos = robot_y + y_delta
        #x_pos = robot_x + point[0]
        #y_pos = robot_y + point[1]
        return [x_pos, y_pos]
