import sys
import time
import datetime
import json
import os
import logging

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger("Waiter")


def main():
    seconds_to_wait = int(sys.argv[1])
    fn_log = sys.argv[2]
    fn_result = sys.argv[3]
    fn_abort = sys.argv[4]
    logger.info("Waiter starting up, will wait {} seconds".format(seconds_to_wait))
    
    for current_time in range(seconds_to_wait):
        # Perform part of "complicated computation"
        time.sleep(1)
        
        # Write log
        write_log(fn_log, current_time, seconds_to_wait)

        # Check if we should abort
        if os.path.exists(fn_abort):
            write_final_log(fn_log)
            write_result(fn_result, current_time, aborted=True)
            return 0
    
    write_final_log(fn_log)
    write_result(fn_result, seconds_to_wait)


def write_log(fn_log, elapsed_time, total_time):
    log = {
        'timestamp': str(datetime.datetime.now()),
        'elapsed_time': str(elapsed_time),
        'total_time': str(total_time),
    }
    with open(fn_log, 'a') as fout:
        json.dump(log, fout)
        fout.write("\n")
    logger.info("Log written: {}/{} seconds waited".format(elapsed_time, total_time))


def write_final_log(fn_log):
    with open(fn_log, 'a') as fout:
        fout.write("FINISHED\n")
    logger.info("Final log written")


def write_result(fn, seconds_waited, aborted=False):
    with open(fn, 'w') as f:
        if aborted:
            f.write('Done. My waiting was aborted after {} seconds.'.format(seconds_waited))
        else:
            f.write('Done. I have waited {} seconds.'.format(seconds_waited))
    logger.info("Result written")


if __name__ == "__main__":
    main()
