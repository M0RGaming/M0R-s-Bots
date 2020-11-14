import subprocess
import atexit
import os
import signal

def kill_child():
    if child1_pid is None:
        pass
    else:
        os.kill(child1_pid, signal.SIGTERM)
    if child2_pid is None:
        pass
    else:
        os.kill(child2_pid, signal.SIGTERM)

child1 = subprocess.Popen(["python3", "ArtaeumRaidTool.py", "stdout"])
child2 = subprocess.Popen(["python3", "SimpleVote.py", "stdout"])


global child1_pid
global child2_pid
child1_pid = child1.pid
child2_pid = child2.pid

atexit.register(kill_child)

child1.wait(); child2.wait()