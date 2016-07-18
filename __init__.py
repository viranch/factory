from Queue import Queue
from threading import Thread, current_thread
import sys, traceback


class StopWorker(Exception): pass


class Factory:

    def __init__(self, worker, num_workers=None):
        self.jobs_q = Queue()
        self.worker_fn = worker
        self.workers = num_workers
        self.results_q = Queue()

    def do_job(self, item):
        if item is None:
            # stop worker once all is done
            raise StopWorker()
        try:
            return self.worker_fn(item)
        except Exception as e:
            exc_info = sys.exc_info()
            return Exception(current_thread().getName(), exc_info)

    def worker(self):
        while True:
            item = self.jobs_q.get()
            try:
                output = self.do_job(item)
                self.results_q.put(output)
            except StopWorker:
                break
            finally:
                self.jobs_q.task_done()

    def start_threads(self):
        for x in range(self.workers):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

    def put_jobs(self, jobs):
        for x in jobs:
            self.jobs_q.put(x)

    def stop_threads(self):
        for x in range(self.workers):
            self.jobs_q.put(None)
        self.jobs_q.join()

    def start_workers(self, jobs):
        if self.workers is None:
            self.workers = len(jobs)
        self.start_threads()
        self.put_jobs(jobs)

    def handle_exc(self, exc):
        print 'Exception in thread {0}:'.format(exc.args[0])
        traceback.print_exception(*exc.args[1])
        print ''

    def work(self, jobs):
        self.start_workers(jobs)

        results = []
        for x in range(len(jobs)):
            result = self.results_q.get()
            self.results_q.task_done()
            if isinstance(result, Exception):
                self.handle_exc(result)
            else:
                results.append(result)

        self.close()

        return results

    def work_async(self, jobs):
        self.start_workers(jobs)

        for x in range(len(jobs)):
            result = self.results_q.get()
            self.results_q.task_done()
            if isinstance(result, Exception):
                self.handle_exc(result)
            else:
                yield result

    def close(self):
        self.stop_threads()
