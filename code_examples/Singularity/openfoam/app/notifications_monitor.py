#!/usr/bin/env python3
"""
Check for user input.

If an ABORT command is sent, the simulation is immediatly stopped writing the
last result.

Usage:
    python notification_monitor.py FOLDER NOTFILE

Args:
    FOLDER:  folder where case is executed
    NOTFILE: path to notification file

Other commands can be implemented just by adding new messages other than ABORT
and implementing the corresponding functions.

"""
import logging
import os
import subprocess
import sys
import time

logging.basicConfig(format='%(asctime)s %(name)-15s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger("Not. monitor")


def main():
    """Execute the assigned task."""
    # Command line parameters
    folder = os.path.abspath(sys.argv[1])
    fn_notifications = os.path.abspath(sys.argv[2])

    logger.info('Notification monitor started.')
    cached_stamp = 0

    while True:
        if os.path.exists(fn_notifications):
            stamp = os.stat(fn_notifications).st_mtime
            # Check if the notification file has been updated
            if stamp != cached_stamp:
                logger.info('New notification received')
                cached_stamp = stamp

                # Read the notification sent
                notification = subprocess.check_output(
                    ['tail', '-1', fn_notifications],
                ).strip().decode()
                os.remove(fn_notifications)

                # Process the notification sent
                if notification == 'ABORT':
                    logger.info('Received ABORT command.')
                    stop_simulation(folder)
                else:
                    logger.info(F'Ignoring unknown command {notification}')

        # Wait a little before checking again
        time.sleep(1)


def stop_simulation(folder):
    """
    Stop a simulation.

    Args:
        folder: folder where simulation is running

    """
    os.chdir(folder)
    subprocess.run(['foamDictionary', 'system/controlDict',
                    '-entry', 'stopAt', '-set', 'writeNow'],
                   stdout=subprocess.DEVNULL)
    return


if __name__ == "__main__":
    main()
