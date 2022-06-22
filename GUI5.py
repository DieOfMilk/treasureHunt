from lib2to3.pgen2.literals import simple_escapes
import tkinter
import tkinter.ttk
import numpy as np
import os
from PIL import Image, ImageTk

class TreasureGUI():
    def __init__(self,row, col, sideLength, trajectoryL,treasureList,probList,trajectoryR,distribution_info):
        np.set_printoptions(formatter={'float_kind': lambda x: "{0:0.3f}".format(x)})
        self.window=tkinter.Tk()
        self.row = row
        self.col = col
        self.G = sideLength
        self.trajectoryL = trajectoryL
        self.treasureList = treasureList
        self.probList=probList
        self.trajectoryR = trajectoryR
        self.window.title("Treasure Hunt Problem")
        # window.geometry("640x400+100+100")
        # window.resizable(False,False)
        self.label=tkinter.Label(self.window,text="row : {}, col : {}".format(self.row,self.col))
        self.label.grid(row=3,column=3)
        # self.btn1=tkinter.Button(self.window,text="1 step",command=self.btncmd)
        # self.btn2=tkinter.Button(self.window,text="continue")
        # self.btn3=tkinter.Button(self.window,text="stop")
        # self.btn4=tkinter.Button(self.window,text="show history",command=self.update_trajectory)
        # self.btn5=tkinter.Button(self.window,text="show probability",command=self.show_prob)
        # self.btn6=tkinter.Button(self.window,text="show trajectory",command=self.show_trajectory3)
        # self.btn4.grid(row=0,column=0)
        # self.btn5.grid(row=0,column=1)
        # self.btn6.grid(row=0,column=2)
        self.showCheck=2
        self.distribution_info = distribution_info

        self.window.geometry("1680x970+5+10")
        self.canvasHeight=970
        self.canvasWidth=1680
        self.canvas = tkinter.Canvas(self.window,width=self.canvasWidth,height=self.canvasHeight,bg='white',bd=2)
        self.canvas.create_line(10,10,10,self.canvasHeight-10,width=5)
        self.canvas.create_line(10,10,self.canvasWidth-10,10,width=5)
        self.canvas.create_line(self.canvasWidth-10,10,self.canvasWidth-10,self.canvasHeight-10,width=5)
        self.canvas.create_line(10,self.canvasHeight-10,self.canvasWidth-10,self.canvasHeight-10,width=5)
        self.canvas.grid()
        for r in range(self.row-1):
            if r%self.G==2:
                self.canvas.create_line(10,10+((self.canvasHeight-20)/self.row)*(r+1),self.canvasWidth-10,10+((self.canvasHeight-20)/self.row)*(r+1),width=5)
            else:
                self.canvas.create_line(10,10+((self.canvasHeight-20)/self.row)*(r+1),self.canvasWidth-10,10+((self.canvasHeight-20)/self.row)*(r+1))
        for c in range(self.col-1):
            if c%self.G==2:
                self.canvas.create_line(10+((self.canvasWidth-20)/self.col)*(c+1),10,10+((self.canvasWidth-20)/self.col)*(c+1),self.canvasHeight-10,width=5)
            else:
                self.canvas.create_line(10+((self.canvasWidth-20)/self.col)*(c+1),10,10+((self.canvasWidth-20)/self.col)*(c+1),self.canvasHeight-10)
        Pa = int(round(self.distribution_info[0][0]))
        Pb = int(round(self.distribution_info[1][0]))
        Pr = self.distribution_info[2][0]
        Qa = min(int(round(Pa+self.distribution_info[3][0])),col-1)
        Qb = min(int(round(Pb+self.distribution_info[4][0])),row-1)
        Qr = self.distribution_info[5][0]
        trueProb = self.distribution_info[6]
        cell_width =  (self.canvasWidth-20)/self.col
        cell_height =  (self.canvasHeight-20)/self.row
        
        
        
        shape = 0
        extendNo = 0
        middlePoint = col*Pa + Pb ## why? first axis mean is Pa, second axis mean is Pb. Thus, trueprob[x][y] shape is reshaped as -1 axis. 
        sum = trueProb[0][middlePoint]
        # while True:
        #     if shape == 0:
        #         if Pa - 1 - extendNo >=0:
        #             sum += self.probList[0][middlePoint - 1 - extendNo]
        #         if Pa + 1 + extendNo <= col-1:
        #             sum += self.probList[0][middlePoint + 1 + extendNo]
        #         if Pb -1 -extendNo >= 0: 
        #             sum += self.probList[0][middlePoint - col - extendNo*col]
        #         if Pb +1 + extendNo <= row-1:
        #             sum += self.probList[0][middlePoint + col + extendNo*col]
        #         if sum > 0.5:
        #             break
        #         shape = (shape+1)%2
        #     if shape == 1:
        #         if Pa - 1 - extendNo >=0 and Pb -1 -extendNo >= 0:
        #             sum += self.probList[0][middlePoint - 1 - extendNo - col - extendNo*col]
        #         if Pa - 1 - extendNo >=0 and Pb +1 + extendNo <= row-1 :
        #             sum += self.probList[0][middlePoint - 1 - extendNo + col + extendNo*col]
        #         if Pa + 1 + extendNo <= col-1 and Pb -1 -extendNo >= 0:
        #             sum += self.probList[0][middlePoint + 1 + extendNo - col - extendNo*col]
        #         if Pa + 1 + extendNo <= col-1 and Pb +1 + extendNo <= row-1:
        #             sum += self.probList[0][middlePoint + 1 + extendNo + col + extendNo*col]
        #         if sum > 0.5:
        #             break
        #         shape = (shape+1)%2
        #         extendNo+=1
        testset = []
        while True: ## be sure (x,y) position prob exchanged as x*16 + y  becasue truprob[x][y] is resahped as -1
            for i in range(extendNo+1):
                j = extendNo - i
                if Pa - 1 - i>=0 and Pb - j >=0:
                    sum += trueProb[0][middlePoint - col - i*col - 1*j]
                    testset.append(middlePoint - col - i*col - 1*j)
                if Pa + 1 + i <= col-1 and Pb + j <= row - 1:
                    sum += trueProb[0][middlePoint + col + i*col + 1*j]
                    testset.append(middlePoint + col + i*col + 1*j)
                if Pb -1 - i >=0 and Pa + j <= col-1:
                    sum += trueProb[0][middlePoint - 1 - i*1 + col*j]
                    testset.append(middlePoint - 1 - i*1 + col*j)
                if Pb + 1 + i <= row-1 and Pa - j >=0:
                    sum += trueProb[0][middlePoint + 1 + i*1 - col*j]
                    testset.append(middlePoint + 1 + i*1 - col*j)
            if sum > 0.5:
                break
            extendNo+=1
        testset.append(middlePoint)
        for i in testset:
            testA = i//col
            testB = i%col
            if not i-col in testset:
                self.canvas.create_line(cell_width*testA+5,cell_height*testB+5,cell_width*testA+5, cell_height*testB+cell_height+5,fill="cyan",width=5) ## left
            if not i+col in testset:
                self.canvas.create_line(cell_width*testA+cell_width+5,cell_height*testB+5,cell_width*testA+cell_width+5, cell_height*testB+cell_height+5,fill="cyan",width=5) ## right
            if not i-1 in testset:
                self.canvas.create_line(cell_width*testA+5,cell_height*testB+5,cell_width*testA+cell_width+5, cell_height*testB+5,fill="cyan",width=5) ## below
            if not i+1 in testset:
                self.canvas.create_line(cell_width*testA+5,cell_height*testB+cell_height+5,cell_width*testA+cell_width+5, cell_height*testB+cell_height+5,fill="cyan",width=5) ## up

        

        shape = 0
        extendNo = 0
        middlePoint = col*Qa + Qb ## why? first axis mean is Pa, second axis mean is Pb. Thus, trueprob[x][y] shape is reshaped as -1 axis. 
        sum = probList[0][middlePoint]
        # while True:
        #     if shape == 0:
        #         if Pa - 1 - extendNo >=0:
        #             sum += self.probList[0][middlePoint - 1 - extendNo]
        #         if Pa + 1 + extendNo <= col-1:
        #             sum += self.probList[0][middlePoint + 1 + extendNo]
        #         if Pb -1 -extendNo >= 0: 
        #             sum += self.probList[0][middlePoint - col - extendNo*col]
        #         if Pb +1 + extendNo <= row-1:
        #             sum += self.probList[0][middlePoint + col + extendNo*col]
        #         if sum > 0.5:
        #             break
        #         shape = (shape+1)%2
        #     if shape == 1:
        #         if Pa - 1 - extendNo >=0 and Pb -1 -extendNo >= 0:
        #             sum += self.probList[0][middlePoint - 1 - extendNo - col - extendNo*col]
        #         if Pa - 1 - extendNo >=0 and Pb +1 + extendNo <= row-1 :
        #             sum += self.probList[0][middlePoint - 1 - extendNo + col + extendNo*col]
        #         if Pa + 1 + extendNo <= col-1 and Pb -1 -extendNo >= 0:
        #             sum += self.probList[0][middlePoint + 1 + extendNo - col - extendNo*col]
        #         if Pa + 1 + extendNo <= col-1 and Pb +1 + extendNo <= row-1:
        #             sum += self.probList[0][middlePoint + 1 + extendNo + col + extendNo*col]
        #         if sum > 0.5:
        #             break
        #         shape = (shape+1)%2
        #         extendNo+=1
        testset2 = []
        while True: ## be sure (x,y) position prob exchanged as x*16 + y  becasue truprob[x][y] is resahped as -1
            for i in range(extendNo+1):
                j = extendNo - i
                if Qa - 1 - i>=0 and Qb - j >=0:
                    sum += probList[0][middlePoint - col - i*col - 1*j]
                    testset2.append(middlePoint - col - i*col - 1*j)
                if Qa + 1 + i <= col-1 and Qb + j <= row - 1:
                    sum += probList[0][middlePoint + col + i*col + 1*j]
                    testset2.append(middlePoint + col + i*col + 1*j)
                if Qb -1 - i >=0 and Qa + j <= col-1:
                    sum += probList[0][middlePoint - 1 - i*1 + col*j]
                    testset2.append(middlePoint - 1 - i*1 + col*j)
                if Qb + 1 + i <= row-1 and Qa - j >=0:
                    sum += probList[0][middlePoint + 1 + i*1 - col*j]
                    testset2.append(middlePoint + 1 + i*1 - col*j)
            if sum > 0.5:
                break
            extendNo+=1
        testset2.append(middlePoint)
        for i in testset2:
            testA = i//col
            testB = i%col
            if not i-col in testset2:
                self.canvas.create_line(cell_width*testA+15,cell_height*testB+15,cell_width*testA+15, cell_height*testB+cell_height+15,fill="magenta",width=5) ## left
            if not i+col in testset2:
                self.canvas.create_line(cell_width*testA+cell_width+15,cell_height*testB+15,cell_width*testA+cell_width+15, cell_height*testB+cell_height+15,fill="magenta",width=5) ## right
            if not i-1 in testset2:
                self.canvas.create_line(cell_width*testA+15,cell_height*testB+15,cell_width*testA+cell_width+15, cell_height*testB+15,fill="magenta",width=5) ## below
            if not i+1 in testset2:
                self.canvas.create_line(cell_width*testA+15,cell_height*testB+cell_height+15,cell_width*testA+cell_width+15, cell_height*testB+cell_height+15,fill="magenta",width=5) ## up


        # for i in testset:
        #     testA = i//col
        #     testB = i%col
        #     self.canvas.create_line(cell_width*testA+10,cell_height*testB+10,cell_width*testA+cell_width+10, cell_height*testB+10,fill="cyan",width=5) ## below
        #     self.canvas.create_line(cell_width*testA+10,cell_height*testB+10,cell_width*testA+10, cell_height*testB+cell_height+10,fill="cyan",width=5) ## left
        #     self.canvas.create_line(cell_width*testA+cell_width+10,cell_height*testB+10,cell_width*testA+cell_width+10, cell_height*testB+cell_height+10,fill="cyan",width=5) ## right
        #     self.canvas.create_line(cell_width*testA+10,cell_height*testB+cell_height+10,cell_width*testA+cell_width+10, cell_height*testB+cell_height+10,fill="cyan",width=5) ## up



        self.canvas.create_line(cell_width*Pa+10,cell_height*Pb+10,cell_width*Pa+cell_width+10, cell_height*Pb+10,fill="cyan",width=5)
        self.canvas.create_line(cell_width*Pa+10,cell_height*Pb+10,cell_width*Pa+10, cell_height*Pb+cell_height+10,fill="cyan",width=5)
        self.canvas.create_line(cell_width*Pa+cell_width+10,cell_height*Pb+10,cell_width*Pa+cell_width+10, cell_height*Pb+cell_height+10,fill="cyan",width=5)
        self.canvas.create_line(cell_width*Pa+10,cell_height*Pb+cell_height+10,cell_width*Pa+cell_width+10, cell_height*Pb+cell_height+10,fill="cyan",width=5)
        # self.canvas.create_oval(cell_width*(Pa-Pr+0.5)+10,cell_height*(Pb-Pr+0.5),cell_width*(Pa+Pr+0.5)+10,cell_height*(Pb+Pr+0.5),outline="cyan",width=5)
        self.canvas.create_line(cell_width*Qa+10,cell_height*Qb+10,cell_width*Qa+cell_width+10, cell_height*Qb+10,fill="magenta",width=5)
        self.canvas.create_line(cell_width*Qa+10,cell_height*Qb+10,cell_width*Qa+10, cell_height*Qb+cell_height+10,fill="magenta",width=5)
        self.canvas.create_line(cell_width*Qa+cell_width+10,cell_height*Qb+10,cell_width*Qa+cell_width+10, cell_height*Qb+cell_height+10,fill="magenta",width=5)
        self.canvas.create_line(cell_width*Qa+10,cell_height*Qb+cell_height+10,cell_width*Qa+cell_width+10, cell_height*Qb+cell_height+10,fill="magenta",width=5)
        # self.canvas.create_oval(cell_width*(Qa-Qr+0.5)+10,cell_height*(Qb-Qr+0.5),cell_width*(Qa+Qr+0.5)+10,cell_height*(Qb+Qr+0.5),outline="magenta",width=5)


        self.canvas.update()
        print("hi")
        
        
    def update_trajectory(self):
        self.timeStemp +=5
        self.show_trajectory2()
        self.window.update()
        
    def from_rgb(self,rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        r, g, b = rgb
        return f'#{r:02x}{g:02x}{b:02x}'
    def show_history(self):
        # for i in range(len(self.textList)):
        #     self.textList[i].set(self.simulator.history[i])
        #     self.labelList[i].config(text=self.textList[i])
        self.showCheck=1
    def show_prob(self):
        for i in range(len(self.textList)):
            self.textList[i].set(self.probList[:,i])
            self.labelList[i].config(text=self.textList[i])
        self.showCheck=0    
    def show_dig(self):
        # for i in range(len(self.textList)):
        #     self.textList[i].set(self.simulator.digTime[i])
        self.showCheck=2  
    # def show_trajectory(self):
    #     for i in range(len(self.textList)):
    #         if self.trajectoryL[i] == 0:
    #             self.labelList[i].config(image=self.emptyImg)
    #             self.labelList[i].image=self.emptyImg
    #         elif self.trajectoryL[i] == 1:
    #             self.labelList[i].config(image=self.leftImg)  
    #             self.labelList[i].image=self.leftImg
    #         elif self.trajectoryL[i] == 2:
    #             self.labelList[i].config(image=self.rightImg)
    #             self.labelList[i].image=self.rightImg
    #         elif self.trajectoryL[i] == 3:
    #             self.labelList[i].config(image=self.upImg)
    #             self.labelList[i].image=self.upImg
    #         elif self.trajectoryL[i] == 4:
    #             self.labelList[i].config(image=self.downImg)
    #             self.labelList[i].image=self.downImg
    #         elif self.simulator.agentPositionId == i:
    #             self.labelList[i].config(image=self.agentImg)
    #             self.labelList[i].image=self.agentImg
    #         elif self.trajectoryL[i] == 5:
    #             self.labelList[i].config(image=self.digImg)
    #             self.labelList[i].image=self.digImg
    #     self.showCheck=2   
    #     print("finished")

    def show_trajectory2(self):
        for i in range(len(self.textList)):
            if len(self.trajectoryL)-self.timeStemp>= 0:
                text=[]
                for j in self.trajectoryL[i][::]:
                    if j[0] == 5:
                        text.append("D" + str(j[1]))
                    elif j[0] == 1:
                        text.append("← " + str(j[1]))
                    elif j[0] == 2:
                        text.append("→ "+ str(j[1]))
                    elif j[0] == 3:
                        text.append("↑ "+ str(j[1]))
                    elif j[0] == 4:
                        text.append("↓ "+ str(j[1]))
                if i in self.treasureList:
                    text.append("\n T")
                self.textList[i].set(text)
        self.canvas.update()
        # print(self.simulator.agentPositionId)
    def show_trajectory3(self):
        cell_width =  (self.canvasWidth-20)/self.col
        cell_height =  (self.canvasHeight-20)/self.row
        # y = 10 + (self.canvasHeight-20)/self.row/2
        # x = 10 + (self.canvasWidth-20)/self.col/2
        x = 10 + np.random.randint(20,cell_width-20)
        y = 10 + np.random.randint(20,cell_height-20)
        x_init = 10
        y_init = 10
        for i in self.treasureList:
            r = i//self.col
            c = i%self.col
            self.canvas.create_line(cell_width*c+10,cell_height*r+10,cell_width*c+cell_width+10, cell_height*r+10,fill="red",width=5)
            self.canvas.create_line(cell_width*c+10,cell_height*r+10,cell_width*c+10, cell_height*r+cell_height+10,fill="red",width=5)
            self.canvas.create_line(cell_width*c+cell_width+10,cell_height*r+10,cell_width*c+cell_width+10, cell_height*r+cell_height+10,fill="red",width=5)
            self.canvas.create_line(cell_width*c+10,cell_height*r+cell_height+10,cell_width*c+cell_width+10, cell_height*r+cell_height+10,fill="red",width=5)
        color = 150
        for i in range(len(self.trajectoryR)):
        # for i in range(1):
        #     print("hi")
            # if i>0:
            #     if self.trajectoryR[i-1] == 1: ## came from left

            #     elif self.trajectoryR[i-1] == 2: ## came from right
                
            #     elif self.trajectoryR[i-1] == 3: ## came from below
                
            #     elif self.trajectoryR[i-1] == 4 : ## came from above

            #     elif self.trajectoryR[i-1] == 5 : ## do dig
            if self.trajectoryR[i] == 1: ## go to left
                if x_init-cell_width >= 10:
                    x_rand = np.random.randint(20,cell_width-20)
                    y_rand = np.random.randint(20,cell_height-20)
                    self.canvas.create_line(x,y,x_init-cell_width + x_rand,y_init + y_rand,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    x_init = x_init - cell_width
                    x = x_init+ x_rand
                    y = y_init+ y_rand
                else:
                    self.canvas.create_line(x,y,x-cell_width/2,y,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    self.canvas.create_line(x-cell_width/2,y,x-cell_width/2,y+cell_height/4,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    self.canvas.create_line(x-cell_width/2,y+cell_height/4,x,y+cell_height/4,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    self.canvas.create_line(x,y+cell_height/4,x,y,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
            elif self.trajectoryR[i] == 2: ## go to right
                if x_init+cell_width <= self.canvasWidth-10:
                    x_rand = np.random.randint(20,cell_width-20)
                    y_rand = np.random.randint(20,cell_height-20)
                    self.canvas.create_line(x,y,x_init+cell_width + x_rand,y_init + y_rand,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    x_init = x_init + cell_width
                    x = x_init+ x_rand
                    y = y_init+ y_rand
                else:
                    self.canvas.create_line(x,y,x+cell_width/2,y,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    self.canvas.create_line(x+cell_width/2,y,x+cell_width/2,y-cell_height/4,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    self.canvas.create_line(x+cell_width/2,y-cell_height/4,x,y-cell_height/4,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    self.canvas.create_line(x,y-cell_height/4,x,y,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
            elif self.trajectoryR[i] == 4: ## go to below
                if y_init-cell_height >= 10:
                    x_rand = np.random.randint(20,cell_width-20)
                    y_rand = np.random.randint(20,cell_height-20)
                    self.canvas.create_line(x,y,x_init+x_rand,y_init - cell_height + y_rand,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    y_init = y_init - cell_height
                    x = x_init+ x_rand
                    y = y_init+ y_rand
                else:
                    self.canvas.create_line(x,y,x,y-cell_height/2,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    self.canvas.create_line(x,y-cell_height/2,x-cell_width/4,y-cell_height/2,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    self.canvas.create_line(x-cell_width/4,y-cell_height/2,x-cell_width/4,y,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    self.canvas.create_line(x-cell_width/4,y,x,y,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
            elif self.trajectoryR[i] == 3 : ## go to above
                if y_init+cell_height <= self.canvasHeight - 10:
                    x_rand = np.random.randint(20,cell_width-20)
                    y_rand = np.random.randint(20,cell_height-20)
                    self.canvas.create_line(x,y,x_init+x_rand,y_init+cell_height+y_rand,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    y_init = y_init + cell_height
                    x = x_init+ x_rand
                    y = y_init+ y_rand
                else:
                    self.canvas.create_line(x,y,x,y+cell_height/2,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    self.canvas.create_line(x,y+cell_height/2,x+cell_width/4,y+cell_height/2,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    self.canvas.create_line(x+cell_width/4,y+cell_height/2,x+cell_width/4,y,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
                    self.canvas.create_line(x+cell_width/4,y,x,y,arrow=tkinter.LAST,fill=self.from_rgb((color,color,255)))
            elif self.trajectoryR[i] == 5 : ## do dig
                self.canvas.create_oval(x,y,x+cell_width/16, y+cell_width/16,fill="black")
            color -=5
            if color < 0:
                color = 0
        self.canvas.update()
        print("hi")
    def generate_cell(self,window,i,j,text="?",check=0):
        if check==0:
            fgC="white"
        else:
            fgC="red"
        label = tkinter.Label(window, textvariable=text, height=5, width=15, relief='ridge', bg="gray30", fg=fgC, font="Helvetica 10")
        label.grid(row=i, column=j, sticky='w', pady=1, padx=1)
        label.grid(row=i, column=j, sticky='w', pady=1, padx=1)
        return label
    def btncmd(self):
        print("hi")
    # def run(self):
    #     self.labelList = np.zeros(self.row*self.col,dtype=object)
    #     self.textList = np.zeros(self.row*self.col,dtype=object)
    #     check =1
    #     for outer_row in range(self.row//self.G):
    #         for outer_col in range(self.col//self.G):
    #             f = tkinter.Frame(self.window)
    #             f.grid(row=self.row//self.G-outer_row, column=outer_col, padx=5, pady=5)            
    #             for inner_row in range(self.G):
    #                 for inner_col in range(self.G):
    #                     position = outer_row*27+outer_col*3 + inner_row*9 + inner_col
    #                     text=self.probList[:,position]
    #                     text = tkinter.StringVar(f, value=(text))
    #                     self.textList[position] = text
    #                     self.labelList[position] = self.generate_cell(f, self.G-inner_row, inner_col, text,check)
    #                     check=0
        # self.window.mainloop()
    def update(self):
        # print(self.simulator.digTime)
        if self.showCheck==1:
            self.show_history()
        elif self.showCheck==2:
            self.show_trajectory3()
        self.window.update()
                
    
    # btn1.pack()
    # btn2.pack()
    # btn3.pack()
    
    