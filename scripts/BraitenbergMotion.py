from RobotMotion import RobotMotion

class BraitenbergMotion:

    braitenbergL= (-0.2, -0.4, -0.6, -0.8, -1, -1.2, -1.4, -1.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    braitenbergR= (-1.6,-1.4,-1.2,-1,-0.8,-0.6,-0.4,-0.2, 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0)
    noDetectionDist=0.8
    maxDetectionDist=0.2
    v0 = 5

    def __init__(self, robotMotion):
        self.robot = robotMotion
        self.leftSpeed = 0
        self.rightSpeed = 0
        self.detect = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    def DoMove(self):
        #START WALKING AT MAX SPEED
        for i in range(1, 16):
            res,dist = self.robot.GetSensorDistance(i)
            if res & (dist<self.noDetectionDist):
                if (dist<self.maxDetectionDist):
                    dist=self.maxDetectionDist
                self.detect[i-1]=1-((dist-self.maxDetectionDist)/(self.noDetectionDist-self.maxDetectionDist))
            else:
                self.detect[i-1]=0

        vLeft=self.v0
        vRight=self.v0

        for i in range(1, 16):
            vLeft=vLeft+self.braitenbergL[i-1]*self.detect[i-1]
            vRight=vRight+self.braitenbergR[i-1]*self.detect[i-1]

        print ('Moving the robot with vLeft: {0} / vRight: {1}',vLeft,vRight)
        self.robot.MoveForward(vLeft,vRight)