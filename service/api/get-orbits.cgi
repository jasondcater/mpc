#!/usr/bin/python
import json
import urllib
import sys
import time
import os
import redis
import cgi
import cgitb; cgitb.enable() # Optional; for debugging only

#set up the redis connection
host = "127.0.0.1"
port = 6379
pool = redis.ConnectionPool(host=host, port=port, db=1)
conn = redis.Redis(connection_pool=pool)

response = {"success":False}
form = cgi.FieldStorage()
ids = None

if "ids" in form:
    ids = form["ids"].value

if ids != None:

    #loop the ids and get the orbital elements
    data = {}
    ids = ids.split(",")
    for id in ids:
        data[id] = conn.lrange(id, 0, -1)

    response["data"] = data
    response["success"] = True

print "Content-Type: application/json\n\n"
print json.dumps(response)