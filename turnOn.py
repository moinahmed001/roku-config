import subprocess
import time


print "Called turn_off at ", time.strftime('%d/%m/%Y %H:%M:%S')
subprocess.call('pm2 restart omx_stream1', shell=True)
subprocess.call('tvservice -p', shell=True)
subprocess.call('fbset -accel true', shell=True)
