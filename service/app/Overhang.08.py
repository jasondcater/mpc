 #I have XYZ
 #I want an equation whos values I can optimze to match XYZ
import tensorflow as tf
import numpy as np
import math
import datetime
import time

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

radius_data = []
velocity_data = []
angular_momentum_data = []
true_anomaly_data = []

# Setup constant parameters for the calulation
G = 6.6725985 * math.pow(10, -11)
mass_of_sun = 1.989 * math.pow(10, 30)
mass_of_earth = 5.972 * math.pow(10, 24)
mass_of_pluto = 1.30900 * math.pow(10, 22)
Mu = G * (mass_of_sun + mass_of_pluto)

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

  # these two equations produce similar results
  # but the second is more accurate
  # h = math.sqrt(math.pow(h_x, 2) + math.pow(h_y, 2) + math.pow(h_z, 2))
  H = R * V
  angular_momentum_data.append(H)

  # dot product of r*v
  q = x_pos*x_vel + y_pos*y_vel + z_pos*z_vel

  # true anomaly
  TAx = math.pow(H, 2) / (R*Mu) - 1
  TAy = H*q / (R*Mu)
  TA = math.atan2(TAy, TAx)
  true_anomaly_data.append(TA)

# Change the data to numpy arrays
radius_data = np.array(radius_data, dtype=np.float32)
velocity_data = np.array(velocity_data, dtype=np.float32)
angular_momentum_data = np.array(angular_momentum_data, dtype=np.float32)
true_anomaly_data = np.array(true_anomaly_data, dtype=np.float32)


'''
#lan = tf.Variable(tf.random_uniform([1], -1.0, 1.0), dtype=tf.float32) # longitude of acending node
lan = 110.30393684 * math.pi/180
#W = tf.Variable(tf.zeros([1]), dtype=tf.float32)   # argument of periapsis
#i = tf.Variable(tf.zeros([1]), dtype=tf.float32)   # inclination
i = 17.14001206 * math.pi/180

def computeAvgDiff(w_var, radius_data, true_anomaly_data, x_pos_data):

  diff = 0
  for index in range(0, len(x_pos_data)):

    actual_rad = radius_data[index]
    actual_ta  = true_anomaly_data[index]
    actual_x   = x_pos_data[index]

    x_pos = actual_rad * (math.cos(lan) * math.cos(w_var + actual_ta)) - (math.sin(lan) * math.sin(w_var + actual_ta) * math.cos(i))

    diff += math.fabs(actual_x - x_pos)

  diff = diff/len(x_pos_data)
  return diff

W = 1.0
last_diff = computeAvgDiff(W, radius_data, true_anomaly_data, x_pos_data)
multi = -2
toggle = True
lim = 1.0
W = 2.0

while lim > 0.1:
  
  diff = computeAvgDiff(W, radius_data, true_anomaly_data, x_pos_data)

  if diff > last_diff:
    if toggle:
      toggle = False
    else:
      toggle = True
    multi = multi - 1

  if toggle:
    W = W + math.pow(10, multi)
  else:
    W = W - math.pow(10, multi)

  lim = math.fabs(diff - last_diff)

  print diff, lim, W
  last_diff = diff

'''  

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
learning_rate = tf.train.exponential_decay(starter_learning_rate, global_step, 1000, 0.96, staircase=True)

#R = tf.Variable(tf.random_uniform([1], -1.0, 1.0), dtype=tf.float32)  # semi-major axis
lan = tf.constant((110.30393684 * math.pi/180), name="lan")
W = tf.Variable(tf.zeros([1]), dtype=tf.float32)   # argument of periapsis
#V = tf.Variable(tf.random_uniform([1], -1.0, 1.0), dtype=tf.float32)   # true anomoly
#i = tf.Variable(tf.random_uniform([1], -1.0, 1.0), dtype=tf.float32)   # inclination

#W = tf.constant(1.56908, name="i")
i = tf.constant(17.14001206, name="i")

x_pos = radius_data * (tf.cos(lan) * tf.cos(W + true_anomaly_data)) - (tf.sin(lan) * tf.sin(W + true_anomaly_data) * tf.cos(i))
y_pos = radius_data * (tf.sin(lan) * tf.cos(W + true_anomaly_data)) + (tf.cos(lan) * tf.sin(W + true_anomaly_data) * tf.cos(i))
z_pos = radius_data * (tf.sin(i) * tf.sin(W + true_anomaly_data))

#rad = tf.sqrt( tf.pow(x_pos, 2)+ tf.pow(y_pos, 2) + tf.pow(z_pos, 2))

# Minimize the mean squared errors.
# Setup the training
loss = tf.reduce_mean(tf.square(x_pos - x_pos_data))
#loss = tf.square(x_pos - x_pos_data)
#loss = tf.reduce_mean(tf.square(y_pos - y_pos_data))
#loss = tf.reduce_mean(tf.square(rad - radius_data))
optimizer = tf.train.GradientDescentOptimizer(1.0)
train = optimizer.minimize(loss)

## Before starting, initialize the variables.  We will 'run' this first.
init = tf.initialize_all_variables()

## Launch the graph.
session = tf.Session()
session.run(init)

d = datetime.datetime.now()
then = time.mktime(d.timetuple())

## Fit the line.
for step in xrange(300):
    
    session.run(train)
    if step % (300/30) == 0:
      
      d = datetime.datetime.now()
      now = time.mktime(d.timetuple())
      
      print((now - then), step, session.run(W)[0])

print(step, session.run(W)[0])