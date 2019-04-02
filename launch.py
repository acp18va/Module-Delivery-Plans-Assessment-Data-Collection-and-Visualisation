import os
import signal
import subprocess


os.chdir("webapp")
os.system("pip install npm")
os.system("ls")
proc = subprocess.Popen("npm run dev >> out &", shell=True, preexec_fn=os.setsid)
#
# # p = os.system("npm run dev >> out &")
os.chdir("..")
os.chdir("adc")
os.system("python3 application.py")
os.system("sleep 59")
os.killpg(proc.pid, signal.SIGTERM)

# os.system("ps -ef")
# os.kill(17892,15)