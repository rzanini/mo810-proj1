from RobotMotion import RobotMotion

# Implementation of a bumper car
# When it is about to bump into something
# it stops, turn around and moves forward again
# It uses a simple threshold as a bumping alert mechanism
#

class BumperMotion:

    bumpDistance = 0.2
    v0 = 3.0
    vTurn = 1.0

    def __init__(self, robotMotion):
        self.robot = robotMotion
        self.leftSpeed = 0
        self.rightSpeed = 0
        self.shouldTurn = ''
        self.isTurning = False
        self.isMovingForward = False
        print ('Using Braitenberg Simple Vehicle 2a - running away from obstacles')

    def DoMove(self):
        #START WALKING AT MAX SPEED
        vLeft=self.v0
        vRight=self.v0

        #Check the groundtruth
        position = self.robot.GetRobotPosition()
        orientation = self.robot.GetRobotOrientation()

        self.shouldTurn = ''
        #Check if it is about to bump into something on the left
        for i in range(1, 4):
            res,dist,point = self.robot.GetSensorDistance(i)
            if res & (dist<=self.bumpDistance):
                self.shouldTurn = 'Right'

        #Check if it is about to bump into something on the left
        for i in range(5, 8):
            res,dist,point = self.robot.GetSensorDistance(i)
            if res & (dist<=self.bumpDistance):
                self.shouldTurn = 'Left'

        if(self.shouldTurn != ''):
            if(not self.isTurning):
                self.robot.Stop()
                if(self.shouldTurn == 'Left'):
                    vLeft= - self.vTurn
                    vRight= self.vTurn
                    print ('Turning left!')
                if(self.shouldTurn == 'Right'):
                    vLeft= self.vTurn
                    vRight= - self.vTurn
                    print ('Turning right!')
                self.isTurning = True
                self.isMovingForward = False
                self.robot.MoveForward(vLeft,vRight)
        else:
            if(not self.isMovingForward):
                print ('Moving forward!')
                self.isTurning = False
                self.isMovingForward = True
                vLeft=vRight=self.v0
                self.robot.MoveForward(vLeft,vRight)