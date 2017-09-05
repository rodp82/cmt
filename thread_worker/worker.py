from utils import StoppableThread
import logging

logger = logging.getLogger(__name__)


class WorkerThread(StoppableThread):
    def __init__(self, name=None, run_freq=1, **kwargs):
        super(WorkerThread, self).__init__()
        self.name = name or self.__class__.__name__
        self.freq = run_freq

    def run(self):
        logging.info('Starting {}'.format(self.name))
        while not self.stopped:
            logging.info('looping')
            self.sleep(self.freq)
