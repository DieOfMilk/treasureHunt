from gym.envs.registration import register

register(
    id='treasureHunt-v0',
    entry_point='gym_treasureHunt.envs:treasureHuntSimulator',
    kwargs={'row':9,'col':9,'verbose':False}
)