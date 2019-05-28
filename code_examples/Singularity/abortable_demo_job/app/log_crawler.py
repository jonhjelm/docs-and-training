import sys
import time
import os
import json
import logging
import shutil

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger("Log crawler")

PROGRESS_HEAD = '''<html>
  <head>
    <title>HPC job progress</title>
    <script type="text/javascript">
      function abort() {
        notify_running_job("ABORT");
      }
    </script>
  </head>'''

PROGRESS_BODY='''<body style="margin: 20px; padding: 20px;">
    <h1>HPC job progress</h1>
    <div>
    <h3>This is a demo HPC job.</h3>
    <p>Last status message from {}: {}</p>
    <p>Click the Abort button to stop the job early. Please click only once,
    it will take a while until the request is processed. (The status might even
    update once more before the job is aborted.)</p>
    <input type="button" value="Abort" onclick="abort()">
    </div>
  </body>
</html>
'''

PROGRESS_BODY_UNKNOWN='''<body style="margin: 20px; padding: 20px;">
    <h1>HPC job progress</h1>
    <div>
    <h3>This is a demo HPC job. Its status is currently unknown.</h3>
    <input type="button" value="Abort job" onclick="abort()">
    </div>
  </body>
</html>
'''


def main():
    fn_log = sys.argv[1]
    fn_status = sys.argv[2]

    crawl_log(fn_log, fn_status)


def crawl_log(fn_log, fn_status):
    """Monitors a log file and creates html status pages from it

    The log file is expected to grow only by one line at a time, with new lines
    added to the end of the file. Each line is expected to be either a json
    string containing the fields 'timestamp' and 'message', or the string
    'FINISHED', which triggers the crawler to stop.

    Note that this crawler is "memory-less", meaning that it cares only about
    the last, newest line added to the log file while all prior lines are
    disregarded.

    Args:
        fn_log (str): Filename of the log file to monitor
        fn_status (str): Filename to write the status output to
    """
    logger.info("Log crawler starting up")
    cached_stamp = 0
    should_stop = False
    while not should_stop:
        if not os.path.exists(fn_log):
            logger.info("Log file doesn't exist")
        else:
            # Check if "last modified" time of the log file has changed
            stamp = os.stat(fn_log).st_mtime
            if not stamp != cached_stamp:
                logger.info("Log file hasn't changed since last check")
            else:
                logger.info("Log file has changed")
                cached_stamp = stamp
                
                status = get_last_line(fn_log)
                # We can stop crawling the logs if the main app is done
                if status.strip() == "FINISHED":
                    should_stop = True
                    logger.info("Found FINISHED log, will stop now!")
                # Otherwise, parse json and write status from it
                else:
                    try:
                        log = json.loads(status)
                        write_status(log, fn_status)
                    except json.JSONDecodeError:
                        write_status_unknown(fn_status)

        time.sleep(1)
    
    logger.info("Log crawler terminating")


def get_last_line(fn):
    """Returns the last line of a file
    
    Args:
        fn (str): File name of the file to read from
    """
    with open(fn, 'r') as fin:
        for line in fin: 
            pass
        return line


def write_status(log, fn_status):
    """Writes a status html page using the information in 'log'

    Args:
        log (dict): Log containing the field 'timestamp' and 'message'
        fn_status (str): Filename to write the status html to
    """
    status = PROGRESS_HEAD + PROGRESS_BODY.format(
        log["timestamp"],
        log["message"],
    )
    # First write to a temporary file, then copy to actual status file. That
    # way, the status file won't be corrupt if the writing process takes a 
    # while.
    fn_status_new = fn_status + '.new'
    with open(fn_status_new, 'w') as fout:
        fout.write(status)
    shutil.copyfile(fn_status_new, fn_status)
    
    logger.info("Wrote status file")


def write_status_unknown(fn_status):
    """Writes a status html page when no actual status is known

    Args:
        fn_status (str): Filename to write the status html to
    """
    with open(fn_status, 'w') as fout:
        fout.write(PROGRESS_HEAD + PROGRESS_BODY_UNKNOWN)
    
    logger.info("Wrote unknown status")


if __name__ == "__main__":
    main()
