from turtle import done
import gym
import numpy as np
import networkx as nx
from simulator2_simple_version import treasureHuntSimulator

class treasureHunt(gym.Env):
    metadata={'render.modes':['human']}
    def __init__(self,row,col):
        self.simulator = treasureHuntSimulator(row,col)
        self.observation_space = gym.spaces.Dict({
            "prob":gym.spaces.Box(0,1,shape=(row*col,),dtype=np.float),
            # "dig":gym.spaces.Box(1,5,shape=(row*col,),dtype=np.int32),
            "agentPosition":gym.spaces.Box(0,1,shape=(row*col,),dtype=np.int32)
        })
        self.action_space = gym.spaces.Discrete(5)
    def reset(self):
        self.simulator.reset()
        obs = self.simulator.getObservation()
        return obs
    def step(self,action):
        if action==0:
            tempAction="G"
        elif action==1:
            tempAction="L"
        elif action==2:
            tempAction="R"
        elif action==3:
            tempAction="U"
        elif action==4:
            tempAction="D"
        self.simulator.moveAgent(tempAction)
        obs = self.simulator.getObservation()
        reward = self.simulator.getScore()
        done = self.simulator.getDone()
        info = {}
        return obs, reward, done, info 