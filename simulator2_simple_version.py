import numpy as np
from scipy.stats import multivariate_normal



class treasureHuntSimulator:
    def __init__(self, row, col, verbose=False):
        self.row = row
        self.col = col
        self.verbose=verbose
    def reset(self):
        self.done=False
        self.treasureId, a, b =self.makeTreasure()
        self.prob = self.makeProbability(a,b)
        self.digTime=np.random.randint(low=5,high=6,size=self.row*self.col)
        self.agentPosition=np.zeros(self.row*self.col)
        self.agentPosition[0]=1
        self.agentPositionId=0
        #puzzleNo = int((self.row*self.col)**(1/2))
        self.makeGroupSimple(9)

        self.timeStemp=0
    def makeGroupSimple(self, size):
        sideLength = int(size**(1/2))
        groupMap = np.zeros((self.row, self.col))
        groupInfo=np.zeros(((self.row*self.col)//size,4),dtype=int)
        for row in range(self.row):
            for col in range(self.col):
                groupMap[row][col] = (row//sideLength)*(self.col//sideLength)+col//sideLength+1
        self.groupMap = groupMap
        self.groupInfo = groupInfo


    def makeGroup(self,puzzleNo):
        groupID=0
        groupInfo=np.zeros((puzzleNo,4),dtype=int) ## show each edge
        groupInfo[0] = [0,0,self.row,self.col]
        groupMap=np.zeros((self.row,self.col))
        for i in range(puzzleNo-1):
            cutRange=0
            while cutRange <= 1:
                x = np.random.randint(groupID+1) ## choose puzzle Id to divie
                y = np.random.randint(2) ## choose row or colunm to divide
                if y==0:
                    upLine = groupInfo[x][2]
                    downLine = groupInfo[x][0]
                else:
                    upLine = groupInfo[x][3]
                    downLine = groupInfo[x][1]
                cutRange=upLine-downLine
            cutLine = np.random.randint(1,cutRange)
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
            for row in range(i[0],i[2]):
                for col in range(i[1],i[3]):
                    groupMap[row][col]=tempID
            tempID+=1
        self.groupMap = groupMap
        self.groupInfo = groupInfo

            
    def makeTreasure(self):
        a = np.random.randint(0,self.row)
        b = np.random.randint(0,self.col)
        distribution = multivariate_normal(mean=[a,b],cov=[[1,0],[0,1]])
        x,y=np.mgrid[0:self.row:1, 0:self.col:1]
        pos = np.dstack((x,y))
        probability = distribution.pdf(pos)
        totalSum=np.sum(probability)
        for i in range(len(probability)):
            for j in range(len(probability[i])):
                probability[i][j] = probability[i][j]/totalSum
        treasureId=0
        treasureProb=np.random.rand(1)
        treasureSum=0
        for i in probability:
            for j in i:
                treasureSum+=j
                if treasureProb<treasureSum:
                    break
                else:
                    treasureId+=1
        return treasureId,a,b

    def makeProbability(self,a,b):
        an = np.random.randint(-2,3)
        bn = np.random.randint(-2,3)
        distribution = multivariate_normal(mean=[a+an,b+bn],cov=[[1,0],[0,1]])
        x,y=np.mgrid[0:self.row:1, 0:self.col:1]
        pos = np.dstack((x,y))
        probability = distribution.pdf(pos)
        totalSum=np.sum(probability)
        for i in range(len(probability)):
            for j in range(len(probability[i])):
                probability[i][j] = probability[i][j]/totalSum
        finalProb = np.reshape(probability,(self.row*self.col))
        return finalProb
        

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
        print("Area information : ")
        print(self.groupMap)
    
