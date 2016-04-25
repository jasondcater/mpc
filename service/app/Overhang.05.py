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

AU = 149597870.7
a = 39.48211675 * AU * 1000

def computeAvgDiff(a, energy_data):
  for index in range(0, len(energy_data)):
    actual_e = energy_data[index]
    test_e = -(Mu/(2*a))
    diff = math.fabs(actual_e - test_e)
    diff = diff/len(energy_data)
  return diff

last_diff = computeAvgDiff(a, energy_data)
multi = 10
toggle = True
while last_diff > 0.1:
  
  diff = computeAvgDiff(a, energy_data)

  if diff > last_diff:
    if toggle:
      toggle = False
    else:
      toggle = True
    multi = multi - 1

  if toggle:
    a = a + math.pow(10, multi)
  else:
    a = a - math.pow(10, multi)

  last_diff = diff

  print diff
  time.sleep(0.1)

print
print a
print math.fabs(149597870.7 * 1000 - a)/1000/AU
# a == semi-major axis
#def computeEnergyError(a, energy_data):
#  total_error = 0;
#  for index in range(0, len(energy_data)):
#    actual_e = energy_data[index]
#    test_e = -(Mu/(2*a))
#    total_error += (actual_e - test_e) ** 2
#  return total_error / float(len(energy_data))
#
#test_a = 148956620419.0
##test_a = 149000000000.0
#
#print computeEnergyError(test_a, energy_data)

#y - (-(Mu/(2*a)))

#y - (-(1/(2*x)))



#test_a = 148056620419.0
#print computeEnergyError(test_a, energy_data, Mu)

#def stepGradient(a_current, energy_data, learningRate, Mu):
#  
#  e_gradient = 0
#  
#  for index in range(0, len(energy_data)):
#    e_gradient += (-Mu/(2* math.pow(a_current, 2)))
#
#
#  print e_gradient
#  new_a = a_current - (learningRate * e_gradient)
#  
#  return new_a
#
#test_a = 148956620419.0
#test_a = 148900000000.0
#
#for index in range(0, 10):
#  test_a = stepGradient(test_a, energy_data, 10000000, Mu)
#  print test_a
#
#print "\n"
#print 148956620419.0
#
#

#test_a = 148056620419.0
#test_a = 148056620419.0
#test_a = 150000000000.0

#mult = 7
#learningRate = math.pow(10, mult)
#for index in range(0, 100):
#  test_a = stepGradient(test_a, energy_data, learningRate, Mu)
#  print test_a
#  #if test_a < 0:
#  #  mult = mult - 1;
#  #  learningRate = math.pow(10, mult)
#  #print test_a, (prev_test-test_a)
#  #prev_test = test_a
#
#
#print "\n"
#print 148056620419.0
#''''
'''
def stepGradient(b_current, m_current, points, learningRate):
    b_gradient = 0
    m_gradient = 0
    N = float(len(points))
    for i in range(0, len(points)):
        b_gradient += -(2/N) * (points[i].y - ((m_current*points[i].x) + b_current))
        m_gradient += -(2/N) * points[i].x * (points[i].y - ((m_current * points[i].x) + b_current))
    new_b = b_current - (learningRate * b_gradient)
    new_m = m_current - (learningRate * m_gradient)
    return [new_b, new_m]


# y = mx + b
# m is slope, b is y-intercept
def computeErrorForLineGivenPoints(b, m, points):
    totalError = 0
    for i in range(0, len(points)):
        totalError += (points[i].y - (m * points[i].x + b)) ** 2
    return totalError / float(len(points))
'''
  #-(1/(2*x))
  #derivitive 

  #1/(2* math.pow(x, 2))

  #print R, test

  # Unit Vector      K = < 0, 0, 1 >
  # Angular Momemtum H = < h_x, h_y, h_z >
  # Node Vector      N = K * H = < -h_y, h_x, 0 >

