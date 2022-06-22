import numpy as np
from simulator3_simplified_vsersion_mapName import treasureHuntSimulator
from GUI import TreasureGUI
from time import sleep
import networkx as nx


if __name__=='__main__':
    simulator = treasureHuntSimulator(9,9,verbose=True,treasureNo=1,mapID=4)
    simulator.reset()
    done = simulator.done
    TGUI = TreasureGUI(simulator=simulator)
    TGUI.run()
    # while not done:
    g1 = nx.Graph()
    for i in range(9):
        for j in range(9):
            g1.add_node("{}_{}".format(i+1,j+1),pos=(i+1,j+1),probability=simulator.groupProbList[0][simulator.groupMap[i][j][0]-1])
    for i in range(9):
        for j in range(9):
            if i!=8:
                g1.add_edge("{}_{}".format(i+1,j+1),"{}_{}".format(i+2,j+1))
            if j!=8:
                g1.add_edge("{}_{}".format(i+1,j+1),"{}_{}".format(i+1,j+2))
    target=None
    groupProbList = simulator.groupProbList[0].copy()
    currentLocation="{}_{}".format(1,1)
    posDict=nx.get_node_attributes(g1,name="pos")
    probDict = nx.get_node_attributes(g1,name="probability")
    temp=input()
    while not done:
        sleep(0.5)
        if target == None:
            bIndex=np.where(groupProbList==max(groupProbList))[0][0]
            targets=[]
            for i in range(9):
                for j in range(9):
                    # if groupProbList[simulator.groupMap[i][j][0]-1] == groupProbList[bIndex]:
                    if probDict["{}_{}".format(i+1,j+1)] == groupProbList[bIndex]:
                        targets.append("{}_{}".format(i+1,j+1))
            if len(targets)==0:
                groupProbList[bIndex]=0
                for i in range(9):
                    for j in range(9):
                        # if groupProbList[simulator.groupMap[i][j][0]-1] == groupProbList[bIndex]:
                        if probDict["{}_{}".format(i+1,j+1)] == groupProbList[bIndex]:
                            targets.append("{}_{}".format(i+1,j+1))
            shortestPathLength=500
            print(groupProbList)
            print(targets)
            for i in targets:
                if nx.shortest_path_length(g1,currentLocation,i) < shortestPathLength:
                    shortestPathLength = nx.shortest_path_length(g1,currentLocation,i)
                    target=i
        else:
            path = nx.shortest_path(g1,currentLocation,target)
            print(path)
            cx= int(currentLocation.split("_")[0])
            cy= int(currentLocation.split("_")[1])
            for i in path[1:]:
                sleep(0.5)
                x = posDict[i][0]
                y = posDict[i][1]
                if cx+1==x:
                    simulator.moveAgent("R")
                    cx+=1
                elif cx-1==x:
                    simulator.moveAgent("L")
                    cx-=1
                elif cy+1==y:
                    simulator.moveAgent("U")
                    cy+=1
                elif cy-1==y:
                    simulator.moveAgent("D")
                    cy-=1
                else:
                    print("No connection")
                    exit()
                simulator.getObservation()
                TGUI.update()
            print("here1")
            simulator.moveAgent("G")
            currentLocation = "{}_{}".format(cx,cy)
            probDict[currentLocation]=0
            target=None
            done = simulator.done
        print("here2")
    np.save("greedyTrajectory3",[simulator.trajectoryL,simulator.treasureList,simulator.probList,simulator.trajectoryR,simulator.distribution_info])
    exit()

