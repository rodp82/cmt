import logging
import threading
import signal

logger = logging.getLogger(__name__)


class QuitEvent(object):
    """
    Sets up a threading event and uses the signal class to trigger the event.set() method on ctrl-c trigger
    """
    default_signals = [signal.SIGINT, signal.SIGTERM]

    def __init__(self):
        # create a threading event
        self._quit_event = threading.Event()

        # set the handler function to handle the signals
        for _sig in self.default_signals:
            signal.signal(_sig, self._quit_handler)

    def get_quit_event(self):
        return self._quit_event

    def _quit_handler(self, signum, frame):
        logger.info('Signal {} received, stopping.'.format(signum))
        self._quit_event.set()


class StoppableThread(threading.Thread):
    """
    Stoppable Thread.

    When implementing children, make use of the stopped property in the
    run() method to know when to stop and return from run() cleanly.
    """

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.join()
        return False

    def stop(self):
        logger.info('stopping thread class : {0}'.format(self.__class__.__name__))
        self._stop_event.set()

    @property
    def stopped(self):
        return self._stop_event.is_set()

    def sleep(self, seconds):
        self._stop_event.wait(seconds)
