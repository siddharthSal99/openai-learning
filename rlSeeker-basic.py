import gym
import numpy as np
import rlSeeker
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import time

MAX_EPS = 1000

class DQNAgent:
	def __init__(self,obs_space,act_space):
		pass

	def add_to_buffer(self, stateSet):
		pass

	def chooseAction(self):
		pass

	def learn(self):
		pass

# class QLearningAgent:




def main():
	env = gym.make("rlSeeker-v0")
	observation = env.reset()
	for _ in range(MAX_EPS):
		env.render()
		action = env.action_space.sample() # your agent here (this takes random actions)
		observation, reward, done, info = env.step(action)
		print action, observation, reward, done, info
		if done:
			observation = env.reset()
		time.sleep(0.1)
	env.close()

if __name__ == "__main__":
	main()
