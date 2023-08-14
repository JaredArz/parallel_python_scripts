def run_in_batch(n,batch_size,jq):
    tasks_to_run = n
    while tasks_to_run >= 1:
        if tasks_to_run < batch_size:
            batch_size = tasks_to_run
        procs = []
        for i in range(batch_size):
            #print(f"starting proc {i}")
            procs.append(jq.get())
            procs[-1].start()
        for job in procs:
            print("joined")
            job.join()
        for job in procs:
            job.close()
        tasks_to_run -= batch_size
    return 0


def w_thread(wq, kill_thread):
    while True:
        if wq.empty():
            time.sleep(1e-3)
        else:
            msg = wq.get()
        if kill_thread():
            print("Exiting loop.")
            break
    print("w_thread signing off.")
    return 0
def queue_data_to_write(wq,data):
     wq.put(data)
     wq.join()


