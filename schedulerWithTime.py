import schedule
import time
import sys
import os
import subprocess
from appFunctions import *

done = False

def job():
    global done
    print("I'm working...")
    device = sys.argv[1]
    switch = sys.argv[2]

    cmd = "python3 checkStatus.py {0}".format(device)
    currentStatus = subprocess.check_output(cmd, shell=True).decode("utf-8")
    print(currentStatus)

    if currentStatus == "on" and switch == "on":
        # its already on!
        print("scheduler: Its already on!")
        done = True
        return schedule.CancelJob
    elif currentStatus == "off" and switch == "off":
        # its already off!
        print("scheduler: Its already off!")
        done = True
        return schedule.CancelJob
    else:
        cmd = "python3 plug.py {0} {1}".format(device,switch)
        os.system(cmd)
        job()

hourMin = sys.argv[3]
schedule.every().day.at(hourMin).do(job)

while done is False:
    schedule.run_pending()
    time.sleep(1)
