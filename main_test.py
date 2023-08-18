import math
from parallel_class import parallel_env
# pass in worker that is running task to have access to w/lock functions
def task(worker, args):
    # unpack args by searching dict.
    print("doing task")
    bound = args["bound"]
    #worker.set_rng_seed()
    a = [math.sqrt(i) for i in range(1, bound)]
    h = sum(a)
    i = sum(a)
    print((h,i))
    #r = abs(np.random.normal(1,1))
    #time.sleep(r)
    #worker.write_with_lock("test.txt",)
    #worker.place_data_queue(a,b)
    worker.place_data_queue(h,i)

if __name__ == "__main__":
    n    = 6
    #FIXME: currently breaks with large input args = {"bound":100000000}
    args = {"bound":100000000}
    num_workers = 16
    #data = parallel_env(n,num_workers,task,args,False).run()
    data   = parallel_env(n,num_workers,task,args).run()
    first  = data[0]
    second = data[1]
    #print(second)
    #print(first)
    print(len(first))
    #print(f"0:{first}\n1:{second}")

