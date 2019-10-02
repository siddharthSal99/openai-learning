"""
Classic cart-pole system implemented by Rich Sutton et al.
Copied from http://incompleteideas.net/sutton/book/code/pole.c
permalink: https://perma.cc/C9ZM-652R
"""

import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np

class RLSeeker(gym.Env):
	"""
	Description:
		A pole is attached by an un-actuated joint to a cart, which moves along a track. The pendulum starts upright, and the goal is to prevent it from falling over by increasing and reducing the cart's velocity.
	Source:
		This environment corresponds to the version of the cart-pole problem described by Barto, Sutton, and Anderson
	Observation:
		Type: Box(4)
		Num	Observation                 Min         Max
		0	Cart Position             -4.8            4.8
		1	Cart Velocity             -Inf            Inf
		2	Pole Angle                 -24 deg        24 deg
		3	Pole Velocity At Tip      -Inf            Inf

	Actions:
		Type: Discrete(2)
		Num	Action
		0	Push cart to the left
		1	Push cart to the right

		Note: The amount the velocity that is reduced or increased is not fixed; it depends on the angle the pole is pointing. This is because the center of gravity of the pole increases the amount of energy needed to move the cart underneath it
	Reward:
		Reward is 1 for every step taken, including the termination step
	Starting State:
		All observations are assigned a uniform random value in [-0.05..0.05]
	Episode Termination:
		Pole Angle is more than 12 degrees
		Cart Position is more than 2.4 (center of the cart reaches the edge of the display)
		Episode length is greater than 200
		Solved Requirements
		Considered solved when the average reward is greater than or equal to 195.0 over 100 consecutive trials.
	"""

	metadata = {
		'render.modes': ['human', 'rgb_array'],
		'video.frames_per_second' : 50
	}

	def __init__(self,curr_loc = np.array([9,9]),
				goal_loc = np.array([3.5,2.5]),
				living_reward = -10,
				goal_reward = 10,
				xLim = np.array([-10,10]),
				yLim = np.array([-10,10]),
				discrete_step = 0.5):


		self.xLim  = xLim
		self.yLim = yLim

		self.goal_reward = goal_reward
		self.living_reward = living_reward
		self.goal_loc = goal_loc
		self.curr_loc = curr_loc
		self.discrete_step = discrete_step
		self.xStates = np.arange(self.xLim[0],self.xLim[1],self.discrete_step)
		self.yStates = np.arange(self.yLim[0],self.yLim[1],self.discrete_step)

		self.action_space = spaces.Discrete(4) #['North', 'South','East','West']
		self.action_list = {'North':np.array([0,discrete_step]),
							'South':np.array([0,-discrete_step]),
							'East':np.array([discrete_step,0]),
							'West':np.array([-discrete_step,0])
							}
		self.observation_space = spaces.Discrete(2)
		self.noise = 0.1
		self.viewer = None



	def step(self, action):
		if action not in self.action_space:
			raise ValueError('Invalid action')
		if action == 0:
			#implement noise here
			self.curr_loc = self.curr_loc + self.action_list['North']
		elif action == 1:
			self.curr_loc = self.curr_loc + self.action_list['South']
		elif action == 2:
			self.curr_loc = self.curr_loc + self.action_list['East']
		elif action == 3:
			self.curr_loc = self.curr_loc + self.action_list['West']
		self.__checkBounds()
		reward = 0;
		if self.__atGoal():
			reward = self.goal_reward
		else:
			reward = self.living_reward

		return self.curr_loc, reward, self.__atGoal(), {}


	def reset(self):
		self.curr_loc[0] = np.random.choice(self.xStates,1)
		self.curr_loc[1] = np.random.choice(self.yStates,1)
		self.goal_loc[0] = np.random.choice(self.xStates,1)
		self.goal_loc[1] = np.random.choice(self.yStates,1)
		return self.curr_loc



	def render(self, mode='human'):
		screen_width = 600
		screen_height = 400

		world_width = (self.xLim[1] - self.xLim[0])*1.25

		scale = screen_width/world_width
		agentRad = 1 * scale
		if self.viewer is None:
			from gym.envs.classic_control import rendering
			self.viewer = rendering.Viewer(screen_width,screen_height)
			agent = rendering.make_circle(radius = agentRad, res = 30)
			self.agenttrans = rendering.Transform()
			agent.add_attr(self.agenttrans)
			agent.set_color(0.6,0,0)
			pos = self.curr_loc
			agentX = pos[0]*scale + screen_width / 2
			agentY = pos[1]*scale + screen_height / 2
			self.agenttrans.set_translation(agentX, agentY)
			self.viewer.add_geom(agent)



			self.goal = rendering.make_circle(radius = agentRad, res = 30)
			self.goaltrans = rendering.Transform()
			self.goal.add_attr(self.goaltrans)
			goalX = self.goal_loc[0]*scale + screen_width / 2
			goalY = self.goal_loc[1]*scale + screen_height / 2
			self.goal.set_color(0,1,0)
			self.goaltrans.set_translation(goalX, goalY)
			self.viewer.add_geom(self.goal)

			return self.viewer.render(return_rgb_array = mode=='rgb_array')


		# carty = 100 # TOP OF CART
		# polewidth = 10.0
		# polelen = scale * (2 * self.length)
		# cartwidth = 50.0
		# cartheight = 30.0

		# if self.viewer is None:
		# 	from gym.envs.classic_control import rendering
		# 	self.viewer = rendering.Viewer(screen_width, screen_height)
		# 	l,r,t,b = -cartwidth/2, cartwidth/2, cartheight/2, -cartheight/2
		# 	axleoffset =cartheight/4.0
		# 	cart = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
		# 	self.carttrans = rendering.Transform()
		# 	cart.add_attr(self.carttrans)
		# 	self.viewer.add_geom(cart)
		# 	l,r,t,b = -polewidth/2,polewidth/2,polelen-polewidth/2,-polewidth/2
		# 	pole = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
		# 	pole.set_color(.8,.6,.4)
		# 	self.poletrans = rendering.Transform(translation=(0, axleoffset))
		# 	pole.add_attr(self.poletrans)
		# 	pole.add_attr(self.carttrans)
		# 	self.viewer.add_geom(pole)
		# 	self.axle = rendering.make_circle(polewidth/2)
		# 	self.axle.add_attr(self.poletrans)
		# 	self.axle.add_attr(self.carttrans)
		# 	self.axle.set_color(.5,.5,.8)
		# 	self.viewer.add_geom(self.axle)
		# 	self.track = rendering.Line((0,carty), (screen_width,carty))
		# 	self.track.set_color(0,0,0)
		# 	self.viewer.add_geom(self.track)

		# 	self._pole_geom = pole

		# if self.state is None: return None

		# # Edit the pole polygon vertex
		# pole = self._pole_geom
		# l,r,t,b = -polewidth/2,polewidth/2,polelen-polewidth/2,-polewidth/2
		# pole.v = [(l,b), (l,t), (r,t), (r,b)]

		# x = self.state
		# cartx = x[0]*scale+screen_width/2.0 # MIDDLE OF CART
		# self.carttrans.set_translation(cartx, carty)
		# self.poletrans.set_rotation(-x[2])

		# return self.viewer.render(return_rgb_array = mode=='rgb_array')

	def close(self):
		if self.viewer:
			self.viewer.close()
			self.viewer = None

	def __checkBounds(self):
		xBoundLower = self.curr_loc[0] < self.xLim[0]
		xBoundUpper = self.curr_loc[0] > self.xLim[1]
		yBoundLower = self.curr_loc[1] < self.yLim[0]
		yBoundUpper = self.curr_loc[1] > self.yLim[1]
		if xBoundUpper:
			self.curr_loc[0] = self.xLim[1]
		elif xBoundLower:
			self.curr_loc[0] = self.xLim[0]

		if yBoundUpper:
			self.curr_loc[1] = self.yLim[1]
		elif yBoundLower:
			self.curr_loc[1] = self.yLim[0]

	def __atGoal(self):
		return min(self.curr_loc == self.goal_loc)







