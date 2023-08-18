import multiprocessing as mp
import queue as q
import numpy as np
import time
import os
import threading as tx


class parallel_env:
    def __init__(self,num_jobs,num_workers,f,fargs,data_handling=True):
        self.num_jobs    = num_jobs
        print(f"num jobs:{self.num_jobs}")
        self.f = f
        # dict of function arguments
        self.fargs = fargs
        # global lock for write synchronization
        self.lock       = mp.Lock()
        self.data_queue = mp.Queue()
        # using a list to store all data from f()
        self.data_temp  = []
        self.data_handling = data_handling

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
        print(f"jobs per worker:{self.jobs_per_worker}")

    def run(self):
        #need status of processes in consumer thread
        worker_processes = []
        consumer_thread = tx.Thread(target = self.consume)

        for n in self.jobs_per_worker:
            w = worker(self.lock,self.data_queue)
            w.fill_job_queue(n,self.f,self.fargs)
            worker_processes.append(mp.Process(target=w.run_job))
        tick = time.time()
        for wp in worker_processes:
            print("starting procs")
            wp.start()
        if self.data_handling:
            print("starting thread")
            consumer_thread.start()
        for wp in worker_processes:
            # join all and block main thread until all finish.
            print("joining procs")
            wp.join()


        for wp in worker_processes:
            print(wp.is_alive())

        self.data_queue.put("Kill Thread")
        print("joining thread")
        consumer_thread.join()
        print("thread exited")
        tock = time.time()
        print(f"Total run time: {tock-tick} s")
        if self.data_handling:
            print(f"data temp: {self.data_temp}")
            return self.unpack_data(self.data_temp)
        else:
            return 0

    def unpack_data(self,data):
        num_data_points = len(data[0])
        data_points_to_return = []
        for i in range(num_data_points):
            data_points_to_return.append( [data[j][i] for j in range(len(data))] )
        return data_points_to_return

    def consume(self):
        while True:
            data = self.data_queue.get()
            if data == "Kill Thread":
                break
            else:
                self.data_temp.append(data)

class worker:
    #FIXME: lock and queue optional
    def __init__(self,lock=None,queue=None):
        self.job_q      = q.Queue()
        self.lock       = lock
        self.data_queue = queue

    def fill_job_queue(self,n,f,fargs):
        # Placing an unrestricted tuple onto the queue for an unrestricted
        # function can lead to a deadlock. Either a consumer thread needs to act as relief
        # (currently implemented) or a temporary file needs to managed and data reconstructed 
        for i in range(n):
            self.job_q.put(job(f,fargs))

    def place_data_queue(self,*args):
        self.data_queue.put(args)

    def run_job(self):
        #time.sleep(1)
        while not self.job_q.empty():
            print("starting job")
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
