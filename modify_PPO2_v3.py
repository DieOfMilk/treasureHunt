
import numpy as np
import os
import gym
import gym_treasureHunt
from datetime import datetime
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2






if __name__=='__main__':
    startTime = datetime.now()
    log_dir = './log'
    env = gym.make("treasureHunt-v0", row=9, col=9, verbose=False)
    temp = env
    # env = DummyVecEnv([lambda: env]) 
    # env = VecNormalize(env, norm_obs=False, norm_reward=False, clip_obs=1.)
    # 
    # ipdb.set_trace()
    
    save_path = os.path.join('./log',"test")
    save_path = os.path.join(save_path,'model')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    model = PPO2(MlpPolicy, env, verbose=1, learning_rate=0.01,save_path=save_path)
    model.learn(total_timesteps = 5000)
    model.save(save_path)
    env.close()
    endTime = datetime.now()
    processTime = endTime-startTime
    print(processTime)
    print("Successfully translated")
    exit()
