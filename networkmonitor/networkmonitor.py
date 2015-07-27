import autoremote
import subprocess
from datetime import datetime, timedelta
import sched, time
import platform

is_windows = any(platform.win32_ver())

lasthostips = None

hostips = {
    "192.168.1.11": None,
    "192.168.1.12": None,
    "192.168.1.13": None,
    "192.168.1.50": None,
    "192.168.1.51": None,
    "192.168.1.52": None,
    "192.168.1.53": None,
    "192.168.1.54": None,
    "192.168.1.55": None}

# check every X minutes
def timer(sc):
    scanhost()
    sc.enter(5, 1, timer, (sc,))

def isOnLine(ip=None):
    if is_windows:
        output = subprocess.Popen(["ping", "-n", "1", ip],stdout = subprocess.PIPE).communicate()[0]
        if ('received = 0' in output.lower()):
            return False
        else:
            return True
    else:
        output = subprocess.Popen(["ping", "-c", "1", ip],stdout = subprocess.PIPE).communicate()[0]
        if ('unreachable' in output.lower()):
            return False
        else:
            return True

def scanhost():
    global lasthostips
    for ip in hostips:
        if isOnLine (ip) == True:
            hostips[ip] = "Online"
        else:
            hostips[ip] = "Offline"
    if hostips != lasthostips:
        lasthostips = hostips
        for ip in hostips:
            print(ip + " : " + hostips[ip])
            if hostips[ip] == "Offline":
                ar = autoremote("[YOUR AUTOREMOTE URL]")   # Connect to AutoRemote server
                ar.send("notify Warning=:=" + ip + " : " + hostips[ip])			  # Send Message
    else:
        print("No Change!!!")

s = sched.scheduler(time.time, time.sleep)
s.enter(0, 1, timer, (s,))
s.run()