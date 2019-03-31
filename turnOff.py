import subprocess
import time


print "Called turn_off at ", time.strftime('%d/%m/%Y %H:%M:%S')
subprocess.call('fbset -accel false', shell=True)
subprocess.call('tvservice -o', shell=True)
