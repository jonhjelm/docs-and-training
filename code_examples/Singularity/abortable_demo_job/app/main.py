import sys
import time
import datetime
import json
import os
import logging

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger("Main")


def main():
    filepath = sys.argv[1]
    text_input = sys.argv[2]
    fn_log = sys.argv[3]
    fn_result = sys.argv[4]
    fn_abort = sys.argv[5]
    logger.info("Main app starting up.")

    # In its current form, the main app doesn't do much. It simply reports the
    # arguments it got as its status. It does so with a delay such that the
    # status can be displayed during the workflow execution.

    write_log(fn_log, "HPC app started successfully.")

    # Check if we should abort, if not, wait a bit
    if os.path.exists(fn_abort):
        write_final_log(fn_log)
        write_result(fn_result, current_time, aborted=True)
        return 0
    time.sleep(8)

    message = "Filepath parameter was: {}".format(filepath)
    write_log(fn_log, message)

    # Check if we should abort, if not, wait a bit
    if os.path.exists(fn_abort):
        write_final_log(fn_log)
        write_result(fn_result, current_time, aborted=True)
        return 0
    time.sleep(8)

    message = "Text-input parameter was: {}".format(text_input)
    write_log(fn_log, message)

    # Check if we should abort, if not, wait a bit
    if os.path.exists(fn_abort):
        write_final_log(fn_log)
        write_result(fn_result, current_time, aborted=True)
        return 0
    time.sleep(8)

    message = "Nothing more to do, will shut down soon."
    write_log(fn_log, message)

    # Check if we should abort, if not, wait a bit
    if os.path.exists(fn_abort):
        write_final_log(fn_log)
        write_result(fn_result, current_time, aborted=True)
        return 0
    time.sleep(8)

    write_final_log(fn_log)
    write_result(fn_result)


def write_log(fn_log, message):
    """Writes a message with a timestamp as a json string to a log file."""
    log = {
        'timestamp': str(datetime.datetime.now()),
        'message': message,
    }
    with open(fn_log, 'a') as fout:
        json.dump(log, fout)
        fout.write("\n")
    logger.info("Log written")


def write_final_log(fn_log):
    """Writes the final log which indicates that the application is finished."""
    with open(fn_log, 'a') as fout:
        fout.write("FINISHED\n")
    logger.info("Final log written")


def write_result(fn, aborted=False):
    with open(fn, 'w') as f:
        if aborted:
            f.write('Done. The app has been aborted.')
        else:
            f.write('Done.')
    logger.info("Result written")


if __name__ == "__main__":
    main()
