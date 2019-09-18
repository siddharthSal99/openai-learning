import gym
import custom_env
env = gym.make("sid_cartpole-v0")
observation = env.reset()
for _ in range(1000):
	env.render()
	action = env.action_space.sample() # your agent here (this takes random actions)
	observation, reward, done, info = env.step(action)

	if done:
		observation = env.reset()
env.close()
