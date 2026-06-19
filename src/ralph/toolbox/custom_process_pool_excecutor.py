from concurrent.futures import ProcessPoolExecutor

class RalphPoolExecutor(ProcessPoolExecutor):

    def __init__(self, max_workers):
        super().__init__(max_workers)
        self.max_workers = max_workers
        self._running_workers = 0

    def submit(self, *args, **kwargs):
        future = super().submit(*args, **kwargs)
        self._running_workers += 1
        future.add_done_callback(self._worker_is_done)
        return future

    def _worker_is_done(self, future):
        self._running_workers -= 1

    def get_pool_usage(self):
        return self._running_workers
