import logging

from contextlib2 import ExitStack
from utils.thread_utils import QuitEvent
from thread_worker.worker import WorkerThread

logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] [%(asctime)s] |%(threadName)-10s| {%(pathname)s:%(lineno)d} %(message)s')
logger = logging.getLogger(__name__)


def main():
    # Get a quit event to handle graceful closing of application
    quit_event = QuitEvent().get_quit_event()

    # Create a list of threads to run
    threads = [
        WorkerThread(),
        WorkerThread(run_freq=2, name='Thread One'),
        WorkerThread(run_freq=5, name='Thread Two')
    ]

    with ExitStack() as stack:
        # Use context manager to kick off the WorkerThread.run() function via the StoppableThread.__enter()__ function
        running_threads = [stack.enter_context(thread) for thread in threads]
        logger.info('Started {} threads'.format(len(running_threads)))

        # Loop until quit_event is triggered
        while not quit_event.is_set():
            logger.info('waiting')
            quit_event.wait(1)

        logger.info('Closing main application')

    # on exiting with statement, the __exit__ function on StoppableThread is triggered, stopping the threads


main()
