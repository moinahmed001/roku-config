import schedule
import time
import sys
import os
import subprocess
import datetime
from appFunctions import *

debug = False

def job(device, switch):
    print(getDateTime(datetime.datetime.now()) + " Running the job function for device: '" + device + "' to turn " + switch)

    cmd = "python3 checkStatus.py {0}".format(device)
    currentSwitchStatus = subprocess.check_output(cmd, shell=True).decode("utf-8")
    print(currentSwitchStatus)

    if currentSwitchStatus.upper() == "ON" and switch.upper() == "ON":
        # its already on!
        print("scheduler: Its already on!")
    elif currentSwitchStatus.upper() == "OFF" and switch.upper() == "OFF":
        # its already off!
        print("scheduler: Its already off!")
    else:
        cmd = "python3 plug.py {0} {1}".format(device,switch.upper())
        os.system(cmd)
        job(device, switch)

def checkEveryOtherMin():
    print("Running the check at "+ getDateTime(datetime.datetime.now()))
    if debug:
        results = [{'deviceName': 'living', 'routineTime': '2020-12-25 01:10', 'switch': "on"}, {'deviceName': 'living', 'routineTime': '2020-02-05 07:09', 'switch': "off"}]
    else:
        now = datetime.datetime.now()
        currentDate = getDateTime(now)
        print("currentDate: " + currentDate)
        results = fetch_routine_data(currentDate)

    print(results)

    for result in results:
        device = result["deviceName"]
        switch = result["switch"]

        job(device, switch)


schedule.every().hour.at(":00").do(checkEveryOtherMin)
schedule.every().hour.at(":29").do(checkEveryOtherMin)
schedule.every().hour.at(":30").do(checkEveryOtherMin)
schedule.every().hour.at(":59").do(checkEveryOtherMin)

# schedule.every().minute.do(checkEveryOtherMin)

if debug:
    # testing purpose
    schedule.every().hour.at(":20").do(checkEveryOtherMin)
    schedule.every().hour.at(":21").do(checkEveryOtherMin)
    schedule.every().hour.at(":22").do(checkEveryOtherMin)
    schedule.every().minute.do(checkEveryOtherMin)

    # checkEveryOtherMin()

print("starting file")
while True:
    schedule.run_pending()
    time.sleep(1)
