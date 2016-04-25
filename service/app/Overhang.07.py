 #I have XYZ
 #I want an equation whos values I can optimze to match XYZ

import tensorflow as tf 
import numpy as np
import math

# input a list of XYZ val in KM/s
x_pos_data = [];
y_pos_data = [];
z_pos_data = [];
x_vel_data = [];
y_vel_data = [];
z_vel_data = [];
output = False
with open("../../data/cartesian/pluto-barycenter", "r") as f:
  
  lines = f.readlines()
  for line in lines:

    line = line.replace("\n", "")
  
    if line == "$$EOE":
      output = False

    if output:
      elements = line.split(",")
      dt = elements[1]
      x_pos_data.append(float(elements[2]))
      y_pos_data.append(float(elements[3]))
      z_pos_data.append(float(elements[4]))
      x_vel_data.append(float(elements[5]))
      y_vel_data.append(float(elements[6]))
      z_vel_data.append(float(elements[7]))

    if line == "$$SOE":
      output = True

# Change the data to numpy arrays
x_pos_data = np.array(x_pos_data, dtype=np.float32)
y_pos_data = np.array(y_pos_data, dtype=np.float32)
z_pos_data = np.array(z_pos_data, dtype=np.float32)
x_vel_data = np.array(x_vel_data, dtype=np.float32)
y_vel_data = np.array(y_vel_data, dtype=np.float32)
z_vel_data = np.array(z_vel_data, dtype=np.float32)

#R = tf.Variable(tf.random_uniform([1], -1.0, 1.0), dtype=tf.float32)  # semi-major axis
R = 39.48211675
lan = tf.Variable(tf.random_uniform([1], -1.0, 1.0), dtype=tf.float32) # latitude of acending node
WV = tf.Variable(tf.random_uniform([1], -1.0, 1.0), dtype=tf.float32)   # argument of periapsis
#V = tf.Variable(tf.random_uniform([1], -1.0, 1.0), dtype=tf.float32)   # true anomoly
#i = tf.Variable(tf.random_uniform([1], -1.0, 1.0), dtype=tf.float32)   # inclination
i = 17.14001206

x_pos = R * ((tf.cos(lan) * tf.cos(WV)) - (tf.sin(lan) * tf.sin(WV) * tf.cos(i)))

y_pos = R * ((tf.sin(lan) * tf.cos(WV)) + (tf.cos(lan) * tf.sin(WV) * tf.cos(i)))

z_pos = R * (tf.sin(i) * tf.sin(WV))

## Minimize the mean squared errors.
## Setup the training
loss = tf.reduce_mean(tf.square(x_pos - x_pos_data))
optimizer = tf.train.GradientDescentOptimizer(1.0)
train = optimizer.minimize(loss)

## Before starting, initialize the variables.  We will 'run' this first.
init = tf.initialize_all_variables()

## Launch the graph.
session = tf.Session()
session.run(init)

## Fit the line.
for step in xrange(2000):
    
    session.run(train)

print (step, R, session.run(lan)[0], session.run(WV)[0], i)
'''
print step
print "R : "+session.run(R)[0]
print "AS: "+session.run(lan)[0]
print "W : "+session.run(W)[0]
print "TA: "+session.run(V)[0]
print "i : "+session.run(i)[0]'''