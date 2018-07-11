import logging
import time
import threading
import signal


logger = logging.getLogger('periodtask.tasklist')


class TaskList:
    def __init__(self, *args):
        self.tasks = args
        self.last_checked = None
        self.stopped = False
        self.orig_sigint_handler = None
        self.orig_sigterm_handler = None

    def _tick(self):
        now = int(time.time())
        for task in self.tasks:
            task.check_subprocesses()
            for sec in range(self.last_checked + 1, now + 1):
                task.check_for_second(sec)
        self.last_checked = now

    def start(self):
        logger.info('tasklist started')

        def handler(num, frame):
            self._stop()
        self.orig_sigint_handler = signal.getsignal(signal.SIGINT)
        self.orig_sigterm_handler = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)

        self.last_checked = int(time.time()) - 1
        while not self.stopped:
            self._tick()
            time.sleep(1)

    def _stop(self, check_subprocesses=True):
        signal.signal(signal.SIGINT, self.orig_sigint_handler)
        signal.signal(signal.SIGTERM, self.orig_sigterm_handler)
        self.stopped = True
        for task in self.tasks:
            task.stop(check_subprocesses)
        for thread in threading.enumerate():
            if thread != threading.main_thread():
                thread.join()
