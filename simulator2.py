import numpy as np


class treasureHuntSimulator:
    def __init__(self, row, col, verbose=False):
        self.row = row
        self.col = col
        self.verbose=verbose
    def reset(self):
        self.done=False
        self.prob=np.random.rand(self.row*self.col)
        self.prob=self.prob/sum(self.prob)
        self.digTime=np.random.randint(low=2,high=5,size=self.row*self.col)
        self.agentPosition=np.zeros(self.row*self.col)
        self.agentPosition[0]=1
        self.agentPositionId=0
        treasureProb=np.random.rand(1)
        treasureSum=0
        self.treasureId=0
        puzzleNo = int((self.row*self.col)**(1/2))
        self.makeGroup(puzzleNo)
        for i in self.prob:
            treasureSum+=i
            if treasureProb<treasureSum:
                break
            else:
                self.treasureId+=1
        self.timeStemp=0
    
    def makeGroup(self,puzzleNo):
        groupID=0
        groupInfo=np.zeros((puzzleNo,4)) ## show each edge
        groupInfo[0] = [0,0,self.row-1,self.col-1]
        groupMap=np.zeros((self.row,self.col))
        for i in range(puzzleNo):
            x = np.random.randint(groupID+1) ## choose puzzle Id to divie
            y = np.random.randint(2) ## choose row or colunm to divide
            if y==0:
                upLine = groupInfo[x][2]
                downLine = groupInfo[x]][0]
            else:
                upLine = groupInfo[x][3]
                downLine = groupInfo[x]][1]
            cutRange=upLine-downLine
            cutLine = np.random.randint(cutRange+1)
            if y==0:
                groupInfo[x][2] = cutLine+downLine
                groupInfo[groupID+1][0] = cutLine+downLine
                groupInfo[groupID+1][2] = upLine
                groupInfo[groupID+1][1] = groupInfo[x][1]
                groupInfo[groupID+1][3] = groupInfo[x][3]
            else:
                groupInfo[x][3] = cutLine+downLine
                groupInfo[groupID+1][1] = cutLine+downLine
                groupInfo[groupID+1][3] = upLine
                groupInfo[groupID+1][0] = groupInfo[x][0]
                groupInfo[groupID+1][2] = groupInfo[x][2]
            groupID+=1
        tempID=0
        for i in groupInfo:
            for row in range(i[0],i[2]+1):
                for col in range(i[1],i[3]+1):
                    groupMap[row][col]=tempID
            tempID+=1
        self.groupMap = groupMap
        self.groupInfo = groupInfo

            

        

    def moveAgent(self,action):
        if action=="R" and self.agentPositionId%self.col != (self.col-1):
            self.agentPosition[self.agentPositionId]=0
            self.agentPositionId+=1
            self.agentPosition[self.agentPositionId]=1
            self.timeStemp+=1
        elif action=="L" and self.agentPositionId%self.col != 0:
            self.agentPosition[self.agentPositionId]=0
            self.agentPositionId-=1
            self.agentPosition[self.agentPositionId]=1
            self.timeStemp+=1
        elif action=="U" and self.agentPositionId//self.col != (self.row-1):
            self.agentPosition[self.agentPositionId]=0
            self.agentPositionId+=self.col
            self.agentPosition[self.agentPositionId]=1
            self.timeStemp+=1
        elif action=="D" and self.agentPositionId//self.col != 0:
            self.agentPosition[self.agentPositionId]=0
            self.agentPositionId-=self.col
            self.agentPosition[self.agentPositionId]=1
            self.timeStemp+=1
        elif action=="G":
            if self.digTime[self.agentPositionId] == 0:
                self.timeStemp+=1
            else:
                self.timeStemp+=self.digTime[self.agentPositionId]
                self.digTime[self.agentPositionId]=0
            if self.treasureId == self.agentPositionId:
                self.done=True
            self.prob[self.agentPositionId]=0
            self.prob=self.prob/sum(self.prob)
        else:
            self.timeStemp+=1
        if self.verbose:
            for i in range(self.row,0,-1):
                for j in range(self.col):
                    if self.agentPosition[(i-1)*self.col+j] != 1:
                        print([self.prob[(i-1)*self.col+j],self.digTime[(i-1)*self.col+j],self.agentPosition[(i-1)*self.col+j]], end='')
                    else:
                        print('***',[self.prob[(i-1)*self.col+j],self.digTime[(i-1)*self.col+j],self.agentPosition[(i-1)*self.col+j]],'***', end='')
                print("")
            print("Timestemp : ", self.timeStemp)
        if self.done==True:
            return self.getScore()
        else:
            return 0


    def getObservation(self):
        return [self.prob, self.digTime, self.agentPosition] ## [prob,digTime,agentPosition]
    
    def getScore(self):
        print(-self.timeStemp)
        return - self.timeStemp
    def showGrid(self):
        for i in range(self.row,0,-1):
            for j in range(self.col):
                if self.agentPosition[(i-1)*self.col+j] != 1:
                    print([self.prob[(i-1)*self.col+j],self.digTime[(i-1)*self.col+j],self.agentPosition[(i-1)*self.col+j]], end='')
                else:
                    print('***',[self.prob[(i-1)*self.col+j],self.digTime[(i-1)*self.col+j],self.agentPosition[(i-1)*self.col+j]],'***', end='')
            print("")
        print("Timestemp : ", self.timeStemp)
    
