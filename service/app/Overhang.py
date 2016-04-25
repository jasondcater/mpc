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

