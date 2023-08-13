import multiprocessing as mp
import numpy as np
import time
import os


def main():
    procs = []
    for i in range(5):
        secs = np.random.randint(1,25)
        p = mp.Process(target=foo,args=(secs,)) 
        procs.append(p)
        p.start()
    for job in procs:
        job.join()
        print("joined")
    for job in procs:
        print("closed")
        job.close()
    print("done")
        

def foo(secs):
    info(f"{secs}")
    time.sleep(secs)
    return None

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    print('\n\n')

if __name__ == "__main__":
    main()
