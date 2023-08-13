import multiprocessing as mp
import queue as q
import threading as tx
import numpy as np
import time
import os
import math
from typing import Callable
from dataclasses import dataclass

#FIXME:
# [] need better job class
# [] 
# [] better way of keeping lock global for entire 'divide and conquer'
# [] more options for managing data, file out, queue store, of job function

@dataclass
class job:
    ### function types can be annotated using typing.Callable.
    # Callable[[int], str] signifies a function that takes a
    # single parameter of type int and returns a str.
    # The python runtime does not enforce these types, left
    ### to be empty for now
    f : Callable[[None],None]
    args : tuple

def main():
    n    = 144
    args = (10000000)
    num_workers = mp.cpu_count()
    divide_and_conquer(n,num_workers,task,args)

# for a known amount of jobs to run that can be represented as a single
# function call with static arguments, divide_and_conquere will distribute
# these jobs evenly across an arbitrary number of worker processes and 
# collect the results. Jobs are assumed to be independent of eachother.
def divide_and_conquer(num_jobs, num_workers,func,fargs):
    if num_jobs == 0 or num_workers == 0:
        print("Either 0 jobs or workers delegated\nExiting.")
        exit()
    elif num_jobs < num_workers:
       num_workers = num_jobs

    jobs_to_assign = num_jobs
    jobs_per_worker [0 for n in range(num_workers)]
    for i in range(num_jobs):
        jobs_per_worker[i]+=1
        jobs_to_assign -= 1
        if jobs_to_assign == 0:
            break

    # create job queue with n number of jobs
    # for each job
    lock        = mp.Lock()
    worker_processes = []
    for n in jobs_per_worker:
        jq = q.Queue()
        # FIXME: reassign args and maybe add lock
        fill_job_queue(n,jq,task,args)
        proc = mp.Process(target=worker_process,args=(jq,))
        worker_processes.append(proc)
    print("Jobs allocated.\nStarting all workers.")
    tick = time.time()
    for p in worker_processes:
        p.start()
    for p in worker_processes:
        # join all and block main thread until all finish.
        p.join()
    tock = time.time()
    print(f"Execution time: {tick-tock} s")

def worker_process(jq):
    while not jq.empty():
        job = jq.get()
        #FIXME: more dynamic way of assigning args to function?
        job.f(job.args[0],job.args[1])
        print("finished job")

def task(bound,l):
    print("inside running task...")
    np.random.seed((os.getpid() * int(time.time())) % 123456789)
    # bound should be > 50000
    x = sum([math.sqrt(i) for i in range(1, bound)])
    r = abs(np.random.normal(1,1))
    time.sleep(r)
    write(r,l)
    return 0

def fill_job_queue(n,jq,f,args):
    for i in range(n):
        jq.put(job(f,args))

def write_with_lock(data,l):
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
