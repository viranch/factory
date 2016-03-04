from Queue import Queue
from threading import Thread

class Factory:

    def __init__(self, worker, num_workers):
        self.q = Queue()
        self.worker_fn = worker
        self.workers = num_workers

    def worker(self):
        while True:
            item = self.q.get()
            output = self.worker_fn(item)
            self.results.append(output)
            self.q.task_done()

    def start_threads(self):
        for x in range(self.workers):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

    def put_jobs(self, jobs):
        for x in jobs:
            self.q.put(x)

    def work(self, jobs):
        self.results = []
        self.start_threads()
        self.put_jobs(jobs)
        self.q.join()
        return self.results
