import tensorflow as tf 
import numpy as np
import math

# input a list of XYZ val
orb_obj_x_data = [];
orb_obj_y_data = [];
orb_obj_z_data = [];
orb_obj_x_vel_data = [];
orb_obj_y_vel_data = [];
orb_obj_z_vel_data = [];
output = False
with open("../../data/cartesian/earth-moon-barycenter", "r") as f:
  
  lines = f.readlines()
  for line in lines:

    line = line.replace("\n", "")
  
    if line == "$$EOE":
      output = False

    if output:
      elements = line.split(",")
      dt = elements[1]
      orb_obj_x_data.append(float(elements[2]))
      orb_obj_y_data.append(float(elements[3]))
      orb_obj_z_data.append(float(elements[4]))
      orb_obj_x_vel_data.append(float(elements[5]))
      orb_obj_y_vel_data.append(float(elements[6]))
      orb_obj_z_vel_data.append(float(elements[7]))

    if line == "$$SOE":
      output = True

#Change the data to numpy arrays
orb_obj_x_data = np.array(orb_obj_x_data, dtype=np.float32)
orb_obj_y_data = np.array(orb_obj_y_data, dtype=np.float32)
orb_obj_z_data = np.array(orb_obj_z_data, dtype=np.float32)
orb_obj_x_vel_data = np.array(orb_obj_x_data, dtype=np.float32)
orb_obj_y_vel_data = np.array(orb_obj_y_data, dtype=np.float32)
orb_obj_z_vel_data = np.array(orb_obj_z_data, dtype=np.float32)

# Setup variables which we want to solve for

# These variable will need to be added solved for as well,
# but for now we will solve only the Kepler elements.
mean_anomoly = 1.917 #for Earth in radians on Apr 23rd 2016
orbit_time   = 3.1558149 * math.pow(10, 7);  #in seconds
date_of_periapsis = 9703507.0
semi_major_axis = 1.00000261

#mu = 1.32712440018 * math.pow(10, 20) #gravitation param for Sun
mu = 3.986004418 * math.pow(10, 14) #gravitational param for Earth

#semi_major_axis = tf.Variable([], dtype=tf.float32)
#eccentricity    = tf.Variable([], dtype=tf.float32)
#inclination     = tf.Variable([], dtype=tf.float32)
#arg_of_periapsis= tf.Variable([], dtype=tf.float32)
#ascending_node  = tf.Variable([], dtype=tf.float32)

radius_data = []
velocity_data = []
energy_data = []

for index in range(0, len(orb_obj_x_data)):

  #Compute the radius and velocity for each point
  radius_data.append(math.sqrt(math.pow(orb_obj_x_data[index], 2) + \
    math.pow(orb_obj_y_data[index], 2) + math.pow(orb_obj_z_data[index], 2)))
  velocity_data.append(math.sqrt(math.pow(orb_obj_x_data[index], 2) + \
    math.pow(orb_obj_y_data[index], 2) + math.pow(orb_obj_z_data[index], 2)))

  # Compute the specific energy
  energy_data.append( (math.pow(velocity_data[index], 2) / 2) - \
    (mu/radius_data[index]) )

# Change the data to numpy arrays
radius_data = np.array(radius_data, dtype=np.float32)
velocity_data = np.array(velocity_data, dtype=np.float32)
energy_data = np.array(energy_data, dtype=np.float32)

for index in range(0, len(energy_data)):

  a = -(mu/(2*energy_data[index]))
  print energy_data[index], a, -(mu/(2*a))

'''
# Setup the error functions
#Look for a value of semi-major axis that will equal the energy
semi_major_axis_var = tf.Variable(1.1, dtype=tf.float32)

## a = -(mu/(2*energy)) , solve for energy
## energy = -(mu/(2*a))

energy_var = -(mu/(2*semi_major_axis_var))

## Minimize the mean squared errors.
## Setup the training
loss = tf.reduce_mean(tf.square(energy_var - energy_data))
optimizer = tf.train.GradientDescentOptimizer(math.pow(10, -31))
train = optimizer.minimize(loss)

## Before starting, initialize the variables.  We will 'run' this first.
init = tf.initialize_all_variables()

## Launch the graph.
session = tf.Session()
session.run(init)

## Run the training
for step in xrange(200):
    
    print session.run(semi_major_axis_var), semi_major_axis_train    
    session.run(train)#
'''
