import multiprocessing as mp

def run_in_batch(func,fargs,total_iters):
    al = []

    #   not to the best way to parallelize since
    #   batches are sequential, that is, even if an open
    #   core is available, it wont run till the slowest
    #   process finishes. good enough for now though.
    sims_to_run = total_iters
    batch_size=16
    #pbar = tqdm(total=sims_to_run,ncols=80)
    while sims_to_run >= 1:
        if sims_to_run < batch_size:
            batch_size = sims_to_run
        a = mp.Queue()  # parallel-safe queue
        processes = []
        #   create processes and start them
        for _ in range(batch_size):
            sim = mp.Process(target=func, args=(None, fargs, a))
            processes.append(sim)
            sim.start()
        #   waits for solution to be available
        for sim in processes:
            ai = a.get()  #will block
            al.append(ai)
        #   wait for all processes to wrap-up before continuing
        for sim in processes:
            sim.join()
        #pbar.update(batch_size)
        sims_to_run -= batch_size
        for sim in processes:
            sim.close()
    return al
