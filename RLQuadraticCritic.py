import tensorflow as tf
import numpy as np
from tf.keras import layers

class RLSeekerCriticAgent:



class LinQuadLayer(layers.Layer):
	def __init__(self):
		super(LinQuadLayer,self).__init__()
		self.numOutputs = 1

	def call(self,inputs):
		if inputs.shape[0] < 1:
			raise ValueError("Cannot have layer input size less than 1")
		u,v = tf.meshgrid(inputs,inputs)
		quadLayer = u * v;
		r,c = quadLayer.shape
		quadLayer = (u * v).numpy();
		op = np.zeros([self.__triangle(inputs.shape[0])])
		for i in range(r):
			for j in range(i):
				op[i * inputs.shape[0] + j] = quadLayer[i][j]

		return tf.convert_to_tensor(op)

	def __triangle(self,N):
		return (N**2 + N)/2





