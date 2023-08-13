import multiprocessing as mp
import queue as q
import threading as tx
import numpy as np
import time
import os
import math 
from typing import Callable
from dataclasses import dataclass

def main():
    lock        = mp.Lock()
    n           = 144
    argsv = (10000000,lock)
    run_threads = []
    for i in range(mp.cpu_count()):
        j=q.Queue()
        fill_job_queue(int(n/mp.cpu_count()),j,task,argsv)
        t = tx.Thread(target=run_thread,args=(j,),daemon=True)
        run_threads.append(t)
    print("Threads allocated")
    print("Starting threads")
    st          = time.time()
    for t in run_threads:
        t.start()
    for t in run_threads:
        t.join()
    print(f"Time: {time.time()-st}")

def run_thread(jq):
    while not jq.empty():
        job=jq.get()
        job.start()
        job.join()
        job.close()
        print("finished job")
    
def task(bound,l):
    print("stat running")
    np.random.seed((os.getpid() * int(time.time())) % 123456789)
    # bound should be > 50000
    x = sum([math.sqrt(i) for i in range(1, bound)])
    r = abs(np.random.normal(1,1))
    time.sleep(r)
    write(r,l)
    
def fill_job_queue(m,jq,f,argsv):
    print(m)
    for i in range(m):
        job = mp.Process(target=f,args=argsv)
        jq.put(job)

def write(data,l):
    #use a lock to ensure that only one process prints to standard output at a time
    l.acquire()
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
        l.release()

if __name__ == "__main__":
    main()
