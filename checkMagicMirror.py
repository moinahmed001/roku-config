# http://moinahmed.ddns.net:5000/

import requests
import os
import datetime

print(str(datetime.datetime.now()) + " running the file")
x = requests.get('http://moinahmed.ddns.net:5000')
print("Status code: " + str(x.status_code))
if x.status_code != 200:
    # restart MagicMirror
    print(datetime.datetime.now() + " restart MagicMirror")
    cmd = "python3 plug.py {0} {1}".format("pi","OFF")
    os.system(cmd)
    time.sleep(5)
    cmd_on = "python3 plug.py {0} {1}".format("pi","ON")
    os.system(cmd_on)
