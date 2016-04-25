#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
import json
import cgi
import cgitb; cgitb.enable() # Optional; for debugging only

with open("../../data/cartesian/pluto-barycenter", "r") as f:
  lines = f.readlines()

returnData = []
output = False
for line in lines:
  
  line = line.replace("\n", "")
  
  if line == "$$EOE":
    output = False

  if output:
    elements = line.split(",")
    dt = elements[1]
    x = float(elements[2])
    y = float(elements[3])
    z = float(elements[4])

    returnData.append([dt, x, y, z])

  if line == "$$SOE":
    output = True

response = {"success":True, "data": returnData}
print "Content-Type: application/json\n\n"
print json.dumps(response)