import numpy as np
import time
import os
import math

def task(bound):
    #np.random.seed((os.getpid() * int(time.time())) % 123456789)
    # bound should be > 50000
    x = sum([math.sqrt(i) for i in range(1, bound)])
    #r = abs(np.random.normal(1,1))
    #time.sleep(r)
    #write(r)
    return 0

def write(data):
    try:
        f = open("race.txt",'a')
        w_str = (
            f"{data}\n"
            f"{time.time()}\n"
            f"print('module name:', {__name__})\n"
            f"print('parent process:', {os.getppid()})\n"
            f"print('process id:', {os.getpid()})\n"
            )
        f.write(w_str)
        f.close()
    finally:
        pass

st          = time.time()
for i in range(144):
    task(10000000)
print(f"Time: {time.time()-st}")
