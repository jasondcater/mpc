import os
import time
import sys
import redis

#set up the redis connection
host = "127.0.0.1"
port = 6379
pool = redis.ConnectionPool(host=host, port=port, db=1)
conn = redis.Redis(connection_pool=pool)

def setList(key, lst):
    if conn.exists(key):
        index = 0
        while index < len(lst):
            entry = lst[index].rstrip().lstrip()
            conn.lset(key, index, entry)
            index += 1
    else:
        index = 0
        while index < len(lst):
            entry = lst[index].rstrip().lstrip()
            lst[index].replace(" ", "")
            conn.rpush(key, entry)
            index += 1

#rebuild the meta data for DB1 in redis
def setMeta():
    meta = [
        "Designation",
        "Provential Designation",
        "Perihelion",
        "Aphelion",
        "EMoid",
        "Visual Magnitude",
        "Epoch",
        "Mean Anomoly",
        "Argument of Perihelion",
        "Ascending Node",
        "Inclination",
        "Eccentricity",
        "Semimajor Axis",
        "Oppositions",
        "Reference"
    ]
    setList("meta", meta)

#clear out DB1 in redis
def clear():
    keys = conn.keys("*")
    for key in keys:
        conn.delete(key)

#reset the DB1
clear()
setMeta()

#open up the Amors.txt file for reading
with open(os.getcwd()+"/../../data/Amors.txt", "r+") as f:
    lines = f.readlines()

#loop the lines in the Amors.txt file
count = 2
while count < len(lines):
                                                   # This column discribes the field headers from MPC
    designation            = lines[count][0:27]    # Designation (and name)
    provential_designation = lines[count][27:40]   # Prov. Des.
    perihelion             = lines[count][40:48]   # q (in AU)
    aphelion               = lines[count][48:55]   # Q (in AU)
    e_moid                 = lines[count][55:65]   # EMoid (minimum distance between the orbit of the earth and the minor planet)
    visual_magnitude       = lines[count][65:72]   # H (Visual Magnitude)
    epoch                  = lines[count][72:82]   # Epoch
    mean_anomoly           = lines[count][82:89]   # M (Mean anomoly for each Epoch)

    arg_of_perihelion      = lines[count][89:95]   # Peri. (Argument of Perihelion in Deg)
    ascending_node         = lines[count][95:102]  # Node  (Longitude of Ascending Node in Deg)
    inclination            = lines[count][102:107] # Incl. (Inclination in Deg)
    eccentricity           = lines[count][107:115] # e (Orbital Eccentricity)
    semiajor_axis          = lines[count][115:122] # a (Semimajor Axis in AU)
    oppositions            = lines[count][122:131] # Opps. (Oppositions, arc length in days is given in parentheses)
    reference              = lines[count][131:142] # Ref. (Reference to the published orbit)

    redisData = [

        designation,
        provential_designation,
        perihelion,
        aphelion,
        e_moid,
        visual_magnitude,
        epoch,
        mean_anomoly,
        arg_of_perihelion,
        ascending_node,
        inclination,
        eccentricity,
        semiajor_axis,
        oppositions,
        reference
    ]

    setList(provential_designation.rstrip().lstrip(), redisData);

    count = count + 1