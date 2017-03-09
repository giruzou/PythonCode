import threading
import queue
import time
from collections import defaultdict

class ThreadQueue(object):
    """docstring for ThreadQueue"""
    def __init__(self,nthreads,jobs):
        self.nthreads=nthreads
        self.ret=defaultdict(list)
        self.request=queue.Queue(nthreads)
        self.result=queue.Queue(2*nthreads)
        self.jobs=jobs
        self.threads=[]
        self.consume_done=[False]*nthreads
        self.insert_done=False
        self.init_threads()

    def init_threads(self):
        for i in range(self.nthreads):
            t=threading.Thread(target=self.consume_task,args=(i,),name=str(i))
            t.setDaemon(True)
            self.threads.append(t)
        self.threads.append(threading.Thread(target=self.insert_que_to_threads))
        for t in self.threads:
            t.start()
        print('init_threads done')
        return None

    def pull_result(self):
        while True:
            print('begin pull')
            if self.insert_done and self.result.empty():
                print(self.result.empty(),'empty')
                for i in range(self.nthreads):
                    self.threads[i].join()
                break
            try:
                que=self.result.get()
                print('que=',que)
            except queue.Empty:
                break
            yield(que)
        print('break pull')
        return None

    def consume_task(self,th):
        while True:
            try:
                i=self.request.get(timeout=1)
            except queue.Empty:
                break
            self.result.put(i)
        print('consume task',th,'done')
        self.consume_done[th]=True
        return None

    def insert_que_to_threads(self):
        while not self.jobs.empty():
            job=self.jobs.get()
            self.request.put(job)
        print('put job done')
        self.insert_done=True
        

def main():
    
    jobs=queue.Queue()
    for i in range(30):
        jobs.put(i)
    tq=ThreadQueue(2,jobs)
    print('start')
    for i in tq.pull_result():
        print(i)
    print("Hi")



if __name__ == '__main__':
    main()