import multiprocessing as mp
import queue as q
import numpy as np
import time
import os

class parallel_env:
    def __init__(self,num_jobs,num_workers,f,fargs,num_data_items=None):
        self.num_jobs    = num_jobs
        # function
        self.f = f
        # dict of function arguments
        self.fargs = fargs
        # global lock for write synchronization
        self.lock  = mp.Lock()
        self.data_queue = mp.Queue()
        self.num_data_items = num_data_items

        if num_jobs == 0 or num_workers == 0 \
           or num_jobs < 0 or num_workers < 0:
            print("Zero jobs or workers delegated\nExiting.")
            exit()
        elif num_jobs < num_workers:
            self.num_workers = num_jobs
        else:
            self.num_workers = num_workers

        jobs_to_assign = self.num_jobs
        jobs_per_worker = [0]*self.num_workers
        for i in range(self.num_jobs):
            jobs_per_worker[i % self.num_workers]+=1
            jobs_to_assign -= 1
            if jobs_to_assign == 0:
                break
        self.jobs_per_worker=jobs_per_worker

    def run(self):
        worker_processes = []
        data = []
        for n in self.jobs_per_worker:
            w = worker(self.lock,self.data_queue)
            w.fill_job_queue(n,self.f,self.fargs)
            worker_processes.append(mp.Process(target=w.run_job))
        tick = time.time()
        for wp in worker_processes:
            wp.start()
        if self.num_data_items is not None:
            for wp in worker_processes:
                t_list = []
                for i in range(self.num_data_items):
                    t = self.data_queue.get()
                    t_list.append(t)
                data.append(t_list)
        for wp in worker_processes:
            # join all and block main thread until all finish.
            wp.join()
        tock = time.time()
        print(f"Total run time: {tock-tick} s")
        if self.num_data_items is not None:
            #fixme split list into individual lists
            return self.unpack_data(data)
        else:
            return 0

    def unpack_data(self,data):
        num_data_points = len(data[0])
        data_points_to_return = []
        for i in range(num_data_points):
            data_points_to_return.append( [data[j][i] for j in range(len(data))] )
        return data_points_to_return

class worker:
    def __init__(self,lock=None,queue=None):
        self.job_q  = q.Queue()
        self.lock   = lock
        self.data_queue = queue

    def fill_job_queue(self,n,f,fargs):
        for i in range(n):
            self.job_q.put(job(f,fargs))

    #FIXME: bug ehere, race condition
    def place_data_queue(self,*args):
        for i in range(len(args)):
            self.data_queue.put(args[i])

    def run_job(self):
        while not self.job_q.empty():
            job_to_run = self.job_q.get()
            job_to_run.f(self,job_to_run.fargs)
            print("finished a job")

    def write_with_lock(self,fname,data):
        ### Use a lock to ensure that only one process prints to standard output at a time
        self.lock.acquire()
        try:
            with open(fname, 'a') as f:
                f.write(str(data)+"\n")
        finally:
            self.lock.release()
    def set_rng_seed(self):
        # any process forked from the main process inherits seed used by np.
        np.random.seed((os.getpid() * int(time.time())) % 123456789)



# if only a struct
class job:
    def __init__(self,f,fargs):
        self.f = f
        self.fargs = fargs
