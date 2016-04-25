import tensorflow as tf 
import numpy as np
import math

G = 6.6725985 * math.pow(10, -11)
mass_of_sun = 1.989 * math.pow(10, 30)
mass_of_earth = 5.972 * math.pow(10, 24)
Mu = G * (mass_of_sun + mass_of_earth)

x_pos = -125518862.0595397 * 1000
y_pos = -81708230.33866683 * 1000
z_pos = -20745.43524889275 * 1000

x_vel = 15.75982787007057 * 1000
y_vel = -25.06821930929441 * 1000
z_vel = 0.0008466672110731821 * 1000

# radius
R = math.sqrt(math.pow(x_pos, 2.0) + math.pow(y_pos, 2.0) + math.pow(z_pos, 2.0))

# velocity
V = math.sqrt(math.pow(x_vel, 2.0) + math.pow(y_vel, 2.0) + math.pow(z_vel, 2.0))

# another way to calculate the semi-major axis
# using the energy of the syste
#en = (math.pow(V, 2)/2) - (Mu/R)
#a_sub = -(Mu/(2*en))

# semi-major axis
a = 1 / ((2/R) - (math.pow(V, 2)/Mu))

# angular momentun, cross product of position and velocity
h_x = y_pos*z_vel - z_pos*y_vel
h_y = z_pos*x_vel - x_pos*z_vel
h_z = x_pos*y_vel - y_pos*x_vel

# these two equations produce similar results
# but the second is more accurate
# h = math.sqrt(math.pow(h_x, 2) + math.pow(h_y, 2) + math.pow(h_z, 2))
H = R * V

# eccentricity
p = math.pow(H, 2) / Mu
E = math.sqrt(1 - p/a)

# inclination
i = math.acos(h_z/H)

# longitude of ascending node
lan = 0
if i != 0:
 lan = math.atan2(h_x,-h_y)

# dot product of R * V
q = x_pos*x_vel + y_pos*y_vel + z_pos*y_vel 

# true anomoly
TAx = H*H / (R*Mu) - 1
TAy = H*q / (R*Mu)
TA = math.atan2(TAy, TAx)

# argument of periapsis
#Cw = (x_pos * math.cos(lan) + y_pos * math.sin(lan))/R
Cw = (x_pos * math.cos(lan) + y_pos * math.sin(lan))
Sw = z_pos / math.sin(i)
W = math.atan2(Sw, Cw) - TA

print R, V, a
