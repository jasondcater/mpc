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
with open("../../data/cartesian/earth-moon-barycenter-KM", "r") as f:
  
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
orb_obj_x_vel_data = np.array(orb_obj_x_vel_data, dtype=np.float32)
orb_obj_y_vel_data = np.array(orb_obj_y_vel_data, dtype=np.float32)
orb_obj_z_vel_data = np.array(orb_obj_z_vel_data, dtype=np.float32)

# Setup variables which we want to solve for

# These variable will need to be added solved for as well,
# but for now we will solve only the Kepler elements.
mean_anomoly = 1.917 #for Earth in radians on Apr 23rd 2016
orbit_time   = 3.1558149 * math.pow(10, 7);  #in seconds
date_of_periapsis = 9703507.0
semi_major_axis = 1.00000261

#Sun = 1.32712440018 * math.pow(10, 20) #gravitation param for Sun

#Pluto = 8.71 * math.pow(10, 11)

#print (4*math.pow(math.pi,2)*math.pow(semi_major_axis, 3))/math.pow(orbit_time, 2)
#3.96405884282e-14

Sun = 1.98894729428839 * math.pow(10, 30) #mass in kg
Earth = 5.97378250603408 * math.pow(10, 24) #mass in kg
G = math.pow(6.6725985, -11);
Mu = G * (Sun + Earth)

#Earth = 3.986004418 * math.pow(10, 14) #gravitational param for Earth

#AU = 149597870.700 #in KM
#Mu = Earth
#Earth = 3.986004418 * math.pow(10, 14) #gravitational param for Earth

#semi_major_axis = tf.Variable([], dtype=tf.float32)
#eccentricity    = tf.Variable([], dtype=tf.float32)
#inclination     = tf.Variable([], dtype=tf.float32)
#arg_of_periapsis= tf.Variable([], dtype=tf.float32)
#ascending_node  = tf.Variable([], dtype=tf.float32)

radius_data = []
velocity_data = []
energy_data = []

for index in range(0, len(orb_obj_x_data)):

  xPos = float(orb_obj_x_data[index])
  yPos = float(orb_obj_y_data[index])
  zPos = float(orb_obj_z_data[index])
  xVel = float(orb_obj_x_vel_data[index])
  yVel = float(orb_obj_y_vel_data[index])
  zVel = float(orb_obj_z_vel_data[index])

  #radius
  R = math.sqrt(math.pow(xPos, 2.0) + math.pow(yPos, 2.0) + math.pow(zPos, 2.0))

  #velocity 
  V = math.sqrt(math.pow(xVel, 2.0) + math.pow(yVel, 2.0) + math.pow(zVel, 2.0))

  #angular momentum
  H = R * V

  #energy 
  E = (math.pow(V, 2) / 2) - (Mu/R)

  a = -(Mu/(2*E))
  a = 1 / (2/ R - math.pow(V, 2) / Mu)
  #var a = 1/(2 / R - V*V / Mu); //  semi-major axis


  print R, V, a

