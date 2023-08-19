import math
from parallel_class import parallel_env
import numpy as np
import time
import os

def task(worker,b,c):
    worker.set_rng_seed()
    a = [math.sqrt(i) for i in range(1, b)]
    res1 = sum(a)
    res2 = sum(a)
    seconds = abs(np.random.normal(1,1))
    time.sleep(seconds)
    worker.write_with_lock(f"test.txt","writing with lock in {os.getpid()}")
    worker.place_data_queue(res1,res2)

if __name__ == "__main__":
    n    = 6
    args = (100000,'c')
    num_workers = 16
    data   = parallel_env(n,num_workers,task,args).run()
    first_res  = data[0]
    second_res = data[1]
    print(f"Results returned: {len(first_res)}")
