import math
import parallel_class as pc
# pass in worker that is running task to have access to w/lock functions
def task(worker, args):
    # unpack args by searching dict.
    bound = args["bound"]
    #worker.set_rng_seed()
    print("inside running task...")
    x = sum([math.sqrt(i) for i in range(1, bound)])
    #r = abs(np.random.normal(1,1))
    #time.sleep(r)
    #worker.write_with_lock("test.txt",x)

if __name__ == "__main__":
    n    = 144
    args = {"bound":10000000}
    num_workers = 8
    a = pc.parallel_env(n,num_workers,task,args)
    a.run()

