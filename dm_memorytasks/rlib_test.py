import gymnasium as gym
from ray.rllib.algorithms.impala import ImpalaConfig
import numpy as np

import dm_memorytasks

class PsychLab(gym.Env):
    def __init__(self, env_config):

        # Initialize the PsychLab environment with the provided config
        env_settings = dm_memorytasks.EnvironmentSettings(seed=123, level_name='spot_diff_extrapolate')
        
        self.env = dm_memorytasks.load_from_docker(name='gcr.io/deepmind-environments/dm_memorytasks:v1.0.1', settings=env_settings)        
        self.action_spec = self.env.action_spec()
        observation_spec = self.env.observation_spec()

        self.action_space = gym.spaces.Dict({
            'STRAFE_LEFT_RIGHT': gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32),
            'MOVE_BACK_FORWARD': gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32),
            'LOOK_LEFT_RIGHT': gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32),
            'LOOK_DOWN_UP': gym.spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
        })
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=observation_spec['RGB_INTERLEAVED'].shape, dtype=int)
        
    def reset(self, *, seed=None, options=None):
        # Reset the PsychLab environment and return the initial observation
        timestep = self.env.reset()
        return timestep.observation['RGB_INTERLEAVED'], {}
    
    def step(self, action):
        # Step the PsychLab environment with the given action
        # and return the next observation, reward, done, and info
        timestep = self.env.step(action)
        print('goblin')
        print(timestep)
        return timestep.observation['RGB_INTERLEAVED'], timestep.reward, False, timestep.last(),{}

# Create an RLlib Algorithm instance
config = ImpalaConfig()
# config = config.training(lr=0.0003, train_batch_size=512)  
# config = config.resources(num_gpus=0, num_learner_workers=1)

# Build a Algorithm object from the config and run 1 training iteration.
algo = config.build(env=PsychLab)

# Train for n iterations and report results (mean episode rewards).
for i in range(5):
    results = algo.train()
    print(f"Iter: {i}; avg. reward={results['episode_reward_mean']}")