#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

#Generate X,Y,Z elements from Kepler Elements
import datetime
import time
import math
import json
import cgi
import cgitb; cgitb.enable() # Optional; for debugging only

#START FUNCTIONS

def calcMeanAnomaly(semi_maj_axis, date_of_periapsis, orbit_time, day):

  d = datetime.datetime.strptime(date_of_periapsis, "%d/%m/%Y %H:%M:%S")
  perihelion = time.mktime(d.timetuple())

  d = datetime.datetime.now() + datetime.timedelta(days=day)
  now = time.mktime(d.timetuple())

  #Time in seconds since the J2000 Epoch
  deltaT = now - perihelion
  
  n = (2*math.pi) / orbit_time
  mean_anomaly = n * deltaT

  #returns in radians
  return mean_anomaly % (2*math.pi)

def calcEccentricAnomaly(eccentricity, mean_anomaly, accruacy):

  delta = math.pow(10, -(accruacy))
  max_iteration = 30
  index = 0

  e = eccentricity
  M = mean_anomaly
  E = M

  # Function F of E = E - e * sin(E) - M
  F = (E - e*math.sin(E) - M)

  while math.fabs(F) > delta and index < max_iteration:

    E = E - (F / (1.0 - e*math.cos(E)))
    F = E - e*math.sin(E) - M
    index = index + 1

  #return in radians
  return E

def calcTrueAnomaly(eccentricity, eccentric_anomaly):

  Y = math.sqrt(1.0 + eccentricity) * math.sin(eccentric_anomaly/2)
  X = math.sqrt(1.0 - eccentricity) * math.cos(eccentric_anomaly/2)
  phi = 2 * math.atan2(Y, X)
  return phi

def calcDistance(semi_maj_axis, eccentricity, eccentric_anomaly):

  # a(1 - e * cos(E))
  dist = semi_maj_axis * (1 - eccentricity * math.cos(eccentric_anomaly));
  return dist

def calcPostion(distance, right_ascension, arg_of_periapsis, true_anomaly, inclination):

  wv = arg_of_periapsis + true_anomaly
  ra = right_ascension
  incl = inclination

  xPos = ((math.cos(ra) * math.cos(wv)) - (math.sin(ra) * math.sin(wv) * math.cos(incl)))
  xPos = xPos * distance

  yPos = ((math.sin(ra) * math.cos(wv)) + (math.cos(ra) * math.sin(wv) * math.cos(incl)))
  yPos = yPos * distance

  zPos = (math.sin(incl) * math.sin(wv))
  zPos = zPos * distance

  return [float(xPos), float(yPos), '{:.20f}'.format(zPos)]

#END FUNCTIONS

response = {"success":False}
form = cgi.FieldStorage()

if "a" in form:
  a = form["a"].value

if "e" in form:
  e = form["e"].value

if "i" in form:
  i = form["i"].value

if "w" in form:
  w = form["w"].value

if "r" in form:
  r = form["r"].value

if "o" in form:
  o = form["o"].value

if "p" in form:
  p = form["p"].value

if a != None:# and e != None and i != None and w != None and r != None o != None and p != None:

  semi_maj_axis = float(a)
  eccentricity = float(e)
  inclination = float(i) * (math.pi/180.0)
  arg_of_periapsis = float(w) * (math.pi/180.0)
  ascending_node = float(r) * (math.pi/180.0)
  orbit_time = float(o)
  date_of_periapsis = p

  returnData = []

  data = []
  
  for index in range(0, 30000):

    mean_anomaly = calcMeanAnomaly(semi_maj_axis, date_of_periapsis, orbit_time, index)
    data.append("mean_anomaly : "+ str(mean_anomaly))
    
    eccentric_anomaly = calcEccentricAnomaly(eccentricity, mean_anomaly, 10)
    data.append("eccentric_anomaly : "+ str(eccentric_anomaly))

    true_anomaly = calcTrueAnomaly(eccentricity, eccentric_anomaly)
    data.append("true_anomaly : "+ str(eccentric_anomaly))

    distance = calcDistance(semi_maj_axis, eccentricity, eccentric_anomaly)
    data.append("distance : "+ str(distance))  

    position = calcPostion(distance, ascending_node, arg_of_periapsis, true_anomaly, inclination)
    data.append("position : "+ str(position))

    returnData.append([index, float(position[0]), float(position[1]), float(position[2]), float(true_anomaly), float(distance)])

  response["data"] = returnData
  response["success"] = True

print "Content-Type: application/json\n\n"
print json.dumps(response)


