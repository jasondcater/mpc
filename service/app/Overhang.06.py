import tensorflow as tf 
import numpy as np
import math
import time

# input a list of XYZ val in KM/s
orb_obj_x_data = [];
orb_obj_y_data = [];
orb_obj_z_data = [];
orb_obj_x_vel_data = [];
orb_obj_y_vel_data = [];
orb_obj_z_vel_data = [];
output = False
with open("../../data/cartesian/pluto-KM", "r") as f:
  
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

# Change the data to numpy arrays
orb_obj_x_data = np.array(orb_obj_x_data, dtype=np.float32)
orb_obj_y_data = np.array(orb_obj_y_data, dtype=np.float32)
orb_obj_z_data = np.array(orb_obj_z_data, dtype=np.float32)
orb_obj_x_vel_data = np.array(orb_obj_x_vel_data, dtype=np.float32)
orb_obj_y_vel_data = np.array(orb_obj_y_vel_data, dtype=np.float32)
orb_obj_z_vel_data = np.array(orb_obj_z_vel_data, dtype=np.float32)

# Setup constant parameters for the calulation
G = 6.6725985 * math.pow(10, -11)
mass_of_sun = 1.989 * math.pow(10, 30)
mass_of_earth = 5.972 * math.pow(10, 24)
mass_of_pluto = 1.30900 * math.pow(10, 22)
Mu = G * (mass_of_sun + mass_of_pluto)

radius_data = []
velocity_data = []
energy_data = []
angular_momentum_data = []

for index in range(0, len(orb_obj_x_data)):

  x_pos = orb_obj_x_data[index] * 1000
  y_pos = orb_obj_y_data[index] * 1000
  z_pos = orb_obj_z_data[index] * 1000
  
  x_vel = orb_obj_x_vel_data[index] * 1000
  y_vel = orb_obj_y_vel_data[index] * 1000
  z_vel = orb_obj_z_vel_data[index] * 1000

  # radius
  R = math.sqrt(math.pow(x_pos, 2.0) + math.pow(y_pos, 2.0) + \
    math.pow(z_pos, 2.0))
  radius_data.append(R)

  # velocity
  V = math.sqrt(math.pow(x_vel, 2.0) + math.pow(y_vel, 2.0) + \
    math.pow(z_vel, 2.0))
  velocity_data.append(V)

  # Energy
  E = (math.pow(V, 2)/2) - (Mu/R)
  energy_data.append(E)

  # angular momentum, cross product of position and velocity
  h_x = y_pos*z_vel - z_pos*y_vel
  h_y = z_pos*x_vel - x_pos*z_vel
  h_z = x_pos*y_vel - y_pos*x_vel

  # these two equations produce similar results
  # but the second is more accurate
  # h = math.sqrt(math.pow(h_x, 2) + math.pow(h_y, 2) + math.pow(h_z, 2))
  H = R * V
  angular_momentum_data.append(H)

AU = 149597870.7
a = 39.48211675 * AU * 1000

def computeAvgDiff(a, energy_data):
  
  diff = 0
  for index in range(0, len(energy_data)):
    actual_e = energy_data[index]
    test_e = -(Mu/(2*a))
    diff += actual_e - test_e

  return math.fabs(diff/len(energy_data))

a = 0.1
exp = 10
direction = True
lowest_diff = last_diff = computeAvgDiff(a, energy_data)

for index in range(0, 10000):
  
  if direction:
    a += math.pow(10, exp) # up
  else:
    a -= math.pow(10, exp) # down

  diff = computeAvgDiff(a, energy_data)

  if diff > last_diff:
    exp -= 1
    if direction:
      direction = False
    else:
      direction = True

  last_diff = diff

  if diff < lowest_diff:
    lowest_diff = diff

print "var pluto=", [a/AU/1000, 0.24882730, 17.14001206, 238.92903833, (224.06891629-110.30393684), 110.30393684], ";"
