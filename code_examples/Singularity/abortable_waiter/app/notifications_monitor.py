import os
import time
import sys
import logging

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger("Not. monitor")


def main():
    fn_notifications = sys.argv[1]
    fn_abort = sys.argv[2]

    monitor(fn_notifications, fn_abort)


def monitor(fn_notifications, fn_abort):
    """
    """
    logger.info("Notifications monitor starting up")
    cached_stamp = 0
    while True:
        if not os.path.exists(fn_notifications):
            logger.info("Notifications file doesn't exist")
        else:
            # Check if "last modified" time of the file has changed
            stamp = os.stat(fn_notifications).st_mtime
            if not stamp != cached_stamp:
                logger.info("Notifications file hasn't changed since last check")
            else:
                logger.info("Notifications file has changed")
                cached_stamp = stamp
                
                command = get_last_line(fn_notifications).strip()
                
                if command == "ABORT":
                    logger.info("Received abort command")
                    # Abort the main app by creating a specific file
                    open(fn_abort, 'a').close()
                else:
                    logger.info("Ignoring unknown command {}".format(command))

        time.sleep(1)


def get_last_line(fn):
    """Returns the last line of a file

    Returns an empty string if the file is empty.
    
    Args:
        fn (str): File name of the file to read from
    """
    with open(fn, 'r') as fin:
        i = -1
        for i, line in enumerate(fin): 
            pass
        if i >= 0:
            return line
        else:
            return ''


if __name__ == "__main__":
    main()