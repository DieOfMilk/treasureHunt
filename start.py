import numpy as np
from simulator1 import treasureHuntSimulator

if __name__=='__main__':
    simulator = treasureHuntSimulator(5,5,verbose=True)
    simulator.reset()
    done = simulator.done
    simulator.showGrid()
    while not done:
        action=input("please enter the action")
        simulator.moveAgent(action)
        done = simulator.done
    exit()


