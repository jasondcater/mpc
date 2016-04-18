#!/usr/bin/python
import json
import urllib
import sys
import time

#add python support for cgi
import cgi
import cgitb; cgitb.enable() # Optional; for debugging only

form = cgi.FieldStorage()
objectIds = None
if "objectIds" in form:
	objectIds = form["objectIds"].value

response = {"sup":objectIds}
print "Content-Type: application/json\n\n"
print json.dumps(response)