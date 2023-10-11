import gymnasium as gym
from stable_baselines3 import A2C
import numpy as np
import pygame

import dm_memorytasks

_FRAMES_PER_SECOND = 30

ACTION_LIST = [
    {'STRAFE_LEFT_RIGHT': 0, 'MOVE_BACK_FORWARD': 0, 'LOOK_LEFT_RIGHT': -1, 'LOOK_DOWN_UP': 0},
    {'STRAFE_LEFT_RIGHT': 0, 'MOVE_BACK_FORWARD': 0, 'LOOK_LEFT_RIGHT': 1, 'LOOK_DOWN_UP': 0},
    {'STRAFE_LEFT_RIGHT': 0, 'MOVE_BACK_FORWARD': 0, 'LOOK_LEFT_RIGHT': 0, 'LOOK_DOWN_UP': 1},
    {'STRAFE_LEFT_RIGHT': 0, 'MOVE_BACK_FORWARD': 0, 'LOOK_LEFT_RIGHT': 0, 'LOOK_DOWN_UP': -1},
    {'STRAFE_LEFT_RIGHT': -1, 'MOVE_BACK_FORWARD': 0, 'LOOK_LEFT_RIGHT': 0, 'LOOK_DOWN_UP': 0},
    {'STRAFE_LEFT_RIGHT': 1, 'MOVE_BACK_FORWARD': 0, 'LOOK_LEFT_RIGHT': 0, 'LOOK_DOWN_UP': 0},
    {'STRAFE_LEFT_RIGHT': 0, 'MOVE_BACK_FORWARD': 1, 'LOOK_LEFT_RIGHT': 0, 'LOOK_DOWN_UP': 0},
    {'STRAFE_LEFT_RIGHT': 0, 'MOVE_BACK_FORWARD': -1, 'LOOK_LEFT_RIGHT': 0, 'LOOK_DOWN_UP': 0},
]

class PsychLab(gym.Env):
    def __init__(self, env_config):

        # Initialize the PsychLab environment with the provided config
        env_settings = dm_memorytasks.EnvironmentSettings(seed=123, level_name='spot_diff_extrapolate')
        
        self.env = dm_memorytasks.load_from_docker(name='gcr.io/deepmind-environments/dm_memorytasks:v1.0.1', settings=env_settings)        
        self.action_spec = self.env.action_spec()
        observation_spec = self.env.observation_spec()

        self.action_space = gym.spaces.Discrete(8)
        self.rgb_spec = observation_spec['RGB_INTERLEAVED']
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=self.rgb_spec.shape, dtype=np.uint8)

        pygame.init()
        try:
            pygame.mixer.quit()
        except NotImplementedError:
            pass
        pygame.display.set_caption('Memory Tasks SB3')

        self.screen = pygame.display.set_mode(
        (int(640), int(480)))

        self.surface = pygame.Surface((self.rgb_spec.shape[1], self.rgb_spec.shape[0]))
        
    def reset(self, *, seed=None, options=None):
        # Reset the PsychLab environment and return the initial observation
        timestep = self.env.reset()

        frame = np.swapaxes(timestep.observation['RGB_INTERLEAVED'], 0, 1)
        pygame.surfarray.blit_array(self.surface, frame)
        pygame.transform.smoothscale(self.surface, self.screen.get_size(), self.screen)

        pygame.display.update()

        return timestep.observation['RGB_INTERLEAVED'], {}
    
    def step(self, action):
        # Step the PsychLab environment with the given action
        # and return the next observation, reward, done, and info
        timestep = self.env.step(ACTION_LIST[action])

        frame = np.swapaxes(timestep.observation['RGB_INTERLEAVED'], 0, 1)
        pygame.surfarray.blit_array(self.surface, frame)
        pygame.transform.smoothscale(self.surface, self.screen.get_size(), self.screen)

        pygame.display.update()

        return timestep.observation['RGB_INTERLEAVED'], timestep.reward, False, timestep.last(),{}

env = PsychLab({})
model = A2C("CnnPolicy", env, verbose=1)
model.learn(total_timesteps=1000000, log_interval=4)