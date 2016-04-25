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

# Setup constant parameters for the calulation
G = 6.6725985 * math.pow(10, -11)
mass_of_sun = 1.989 * math.pow(10, 30)
mass_of_earth = 5.972 * math.pow(10, 24)
Mu = G * (mass_of_sun + mass_of_earth)

radius_data = []
velocity_data = []
ang_vel_data = []
energy_data = []

for index in range(0, len(x_pos_data)):

  x_pos = x_pos_data[index]
  y_pos = y_pos_data[index]
  z_pos = z_pos_data[index]
  
  x_vel = x_vel_data[index]
  y_vel = y_vel_data[index]
  z_vel = z_vel_data[index]

  # radius
  R = math.sqrt(math.pow(x_pos, 2.0) + math.pow(y_pos, 2.0) + \
    math.pow(z_pos, 2.0))
  radius_data.append(R)

  # velocity
  V = math.sqrt(math.pow(x_vel, 2.0) + math.pow(y_vel, 2.0) + \
    math.pow(z_vel, 2.0))
  velocity_data.append(V)

  # semi-major axis
  #a = 1 / ((2/R) - (math.pow(V, 2)/Mu))

  # angular velocity 
  H = R * V

  # energy
  E = (math.pow(V, 2)/2) - (Mu/R)
  energy_data.append(E)

  #a = -(Mu/(2*E))
  #e = -(Mu/(2*a))
  #print a

## SETUP FOR TENSORFLOW
## Rearrange the Energy equation so the semi-major axis is the variable
a_var = tf.Variable(tf.zeros([1]), dtype=tf.float32)
E_var = -(Mu/2*a_var)

def exponential_decay(learning_rate, global_step, decay_steps, decay_rate, staircase=False, name=None):
  with ops.op_scope([learning_rate, global_step, decay_steps, decay_rate],
                   name, "ExponentialDecay") as name:
    learning_rate = ops.convert_to_tensor(learning_rate, name="learning_rate")
    dtype = learning_rate.dtype
    global_step = math_ops.cast(global_step, dtype)
    decay_steps = math_ops.cast(decay_steps, dtype)
    decay_rate = math_ops.cast(decay_rate, dtype)
    p = global_step / decay_steps
    if staircase:
      p = math_ops.floor(p)
    return math_ops.mul(learning_rate, math_ops.pow(decay_rate, p), name=name)
    return math_ops.mul(learning_rate, math_ops.pow(decay_rate, p), name=name)

global_step = tf.Variable(0, trainable=False)
starter_learning_rate = 0.1
learning_rate = tf.train.exponential_decay(starter_learning_rate, global_step, 10, 0.96, staircase=True)

# Minimize the mean squared errors.
# Setup the training
loss = tf.reduce_mean(tf.square(E_var - energy_data))
optimizer = tf.train.GradientDescentOptimizer(learning_rate)
train = optimizer.minimize(loss)

# Before starting, initialize the variables.  We will 'run' this first.
init = tf.initialize_all_variables()

# Launch the graph.
session = tf.Session()
session.run(init)

for step in xrange(100):
  print session.run(a_var)
  session.run(train)