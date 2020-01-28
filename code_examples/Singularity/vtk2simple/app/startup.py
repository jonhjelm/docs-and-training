#!/usr/local/bin/python3
import argparse

import subprocess
import sys
import os
import string
import random
import shutil
import logging
import time
import json

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger("Startup")


def main():
    # Input arguments
    filepath = sys.argv[1]

    # Pre-defined files for communication with the "outside world"
    fn_status = '/service/status.html'
    fn_result = '/service/result.txt'
    fn_notifications = '/service/notifications.txt'

    # Write dummy value into result file
    logger.info("Writing dummy result")
    with open(fn_result, 'w') as fout:
        fout.write("UNSET")

    # Define files for the main app in a unique folder
    ID = generate_id('/home')
    unique_folder = os.path.join('/home', ID)
    os.mkdir(unique_folder)
    fn_log = os.path.join(unique_folder, 'main_log.txt')
    fn_abort = os.path.join(unique_folder, 'main_abort.txt')
    logger.info("Created unique folder {}".format(unique_folder))

    # 1: Start log crawler as a background process
    # The log crawler monitors a single log file and creates status html pages
    # from it
    # The log crawler will automatically terminate when it reads the finishing
    # log from the main application
    logger.info("Starting log crawler")
    log_crawler_script = '/app/log_crawler.py'
    command = ['python', log_crawler_script, fn_log, fn_status, fn_result]
    proc_log = subprocess.Popen(command)

    # 2: Start the notifications monitor as a background process
    # It monitors the notifications file (which is written to when messages are
    # sent to the HPC service running this Singularity image) and translates
    # messages into comands to the main application. Here, this is done simply
    # by creating a specific file the main app looks for. Only a single command
    # (abort) is supported.
    # The notifications monitor does _not_ terminate by itself.
    logger.info("Starting notifications monitor")
    not_monitor_script = '/app/notifications_monitor.py'
    command = ['python', not_monitor_script, fn_notifications, fn_abort]
    proc_not = subprocess.Popen(command)

    # 3: Start the main application as a foreground process
    # The main application will write to the log file monitored by the crawler,
    # and it will write its final result into the result file.
    # It will also check periodically for the existence of 'fn_abort' and quit
    # if this file exists. (This is a cheap way of sending a command to the
    # main app.)
    # The main app receives the parameter filepath given to
    # this SOAP method.
    logger.info("Starting vtk2simple")
    try:
        json.loads(filepath)
        command = ['python', '/app/vtk2simple.py', '--filelist', filepath, '--logfile', fn_log]
    except:
        command = ['python', '/app/vtk2simple.py', '--filename', filepath, '--logfile', fn_log]
#    command = ['echo', '/app/vtk2simple.py', '--filename', filepath, '--logfile', fn_log]
    subprocess.call(command)
    logger.info("Main app finished, terminating processes")

    # 4: Terminate notifications monitor and remove log folders
    # As the main app is finished at this point, we can safely terminate the
    # notifications monitor. Notify the log parser that the appliication is finished
    # letting it write to the results file. Terminate the log parser if it has not
    # exited within 5 seconds
    with open(fn_log, 'a') as file:
        file.write("FINISHED")
    for i in range (5):
        if proc_log.poll() == None:
            time.sleep(1)
    proc_log.terminate()
    proc_not.terminate()
    shutil.rmtree(unique_folder)

    # (Optional) 5: Process end result
    # In case the final result of the main application (see step 3) is _not_
    # just a simple file, we should call another script here which processes
    # this end result and writes into the /service/result.txt file.


def generate_id(folder, size=16, chars=string.ascii_uppercase + string.digits):
    """Generates a random ID string which guaranteed not to exist in a folder"""
    while True:
        ID = ''.join(random.choice(chars) for _ in range(size))
        if not os.path.exists(os.path.join(folder, ID)):
            break
    return ID


if __name__ == "__main__":
    main()
