#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
import json
import urllib
import sys
import time
import os
import redis
import cgi
import cgitb; cgitb.enable() # Optional; for debugging only

response = {"success":False}
form = cgi.FieldStorage()
ids = None
db = None

if "ids" in form:
  ids = form["ids"].value

if "db" in form:
  db = form["db"].value

if ids != None and db != None:

  #set up the redis connection
  host = "127.0.0.1"
  port = 6379
  pool = redis.ConnectionPool(host=host, port=port, db=db)
  conn = redis.Redis(connection_pool=pool)

  #loop the ids and get the orbital elements
  data = {}
  ids = ids.split(",")
  for id in ids:
    data[id] = conn.lrange(id, 0, -1)

    data[id][8] = float(data[id][8])
    data[id][9] = float(data[id][9])
    data[id][10] = float(data[id][10])
    data[id][11] = float(data[id][11])
    data[id][12] = float(data[id][12])

  response["data"] = data
  response["success"] = True

print "Content-Type: application/json\n\n"
print json.dumps(response)