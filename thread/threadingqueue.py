import threading
import queue
import time
from collections import defaultdict

class JobManager(object):
    """docstring for ThreadQueue"""
    def __init__(self,nthreads,jobs):
        self.nthreads=nthreads
        self.request=queue.Queue(nthreads)
        self.result=queue.Queue(2*nthreads)
        self.jobs=jobs
        self.threads=[]
        self.insert_done=False
        self.init_threads()

    def init_threads(self):
        for i in range(self.nthreads):
            t=threading.Thread(target=self.process_job,args=(i,),name=str(i))
            t.setDaemon(True)
            self.threads.append(t)
        self.threads.append(threading.Thread(target=self.insert_que_to_threads))
        for t in self.threads:
            t.start()
        print('init_threads done')

    def pull(self):
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

    def process_job(self,th):
        while True:
            try:
                i=self.request.get(timeout=1)
            except queue.Empty:
                break
            self.result.put(i)
        print('consume task',th,'done')

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
    jm=JobManager(2,jobs)
    print('start')
    for i in jm.pull():
        print('pull',i)
    print("Hi")



if __name__ == '__main__':
    main()