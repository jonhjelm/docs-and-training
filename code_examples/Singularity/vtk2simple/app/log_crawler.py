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
    <title>Converting .vtk file to .simple format</title>
    <script type="text/javascript">
      function abort() {
        notify_running_job("ABORT");
      }
    </script>
  </head>'''

PROGRESS_BODY='''<body style="margin: 20px; padding: 20px;">
    <h1>File convertion status</h1>
    <div>
    <p> treating file {currfile} of {nfiles} </p>
    <p> inputfile: {inputfile} </p>
    <p> outputfile: {outputfile} </p>
    <p> ncells: {ncells} </p>
    <p> npoints: {npoints} </p>
    <p> conversionNeeded: {conversionNeeded} </p>
    <p>Last status message: {statusline}</p>
    </div>
  </body>
</html>
'''



PROGRESS_BODY_UNKNOWN='''<body style="margin: 20px; padding: 20px;">
    <h1>HPC job progress</h1>
    <div>
    <h3>This is a demo HPC job. Its status is currently unknown.</h3>
    </div>
  </body>
</html>
'''


def main():
    fn_log = sys.argv[1]
    fn_status = sys.argv[2]
    fn_result = sys.argv[3]
    
    crawl_log(fn_log, fn_status, fn_result)


def crawl_log(fn_log, fn_status, fn_result):
    """Monitors a log file and creates html status pages from it

    The log file is expected to grow only by one line at a time, with new lines
    added to the end of the file. 

    Args:
        fn_log (str): Filename of the log file to monitor
        fn_status (str): Filename to write the status output to
    """
    logger.info("Log crawler starting up")
    statusd = {}
    statusd['inputfile'] = "unknown"
    statusd['outputfile'] = "unknown"
    statusd['ncells'] = "unknown"
    statusd['npoints'] = "unknown"
    statusd['conversionNeeded'] = "unknown"
    statusd['statusline']="not yet started"
    cached_stamp = 0
    should_stop = False
    while not os.path.exists(fn_log):
#        logger.info("Log file doesn't exist")
        time.sleep(1)

    log_file = open(fn_log, 'r')
    while not should_stop:
#        logger.info("Log file has changed")
                
        status = log_file.readline()
        # We can stop crawling the logs if the main app is done
        if status.strip() == "FINISHED":
            should_stop = True
            logger.info("Found FINISHED log, will stop now!")
            # check if it is a new statusline
        elif  status[:1] == '#' :
            statusd['statusline'] = status[1:]
            # check if it sets a new variable
        else:
            key_value = status.strip().split(': ',1)
            if len(key_value)==2:
                statusd[key_value[0]]  = key_value[1]
                logger.info("Got " + key_value[0] + ":" + key_value[1] )
        write_status(statusd, fn_status)
#        time.sleep(1)
    with open(fn_result, 'w') as file:
        if 'outputlist' in statusd:
            file.write(statusd['outputlist'])
        else:
            #        file.write(statusd.outputfile)
            # strip quotation mark at start and end
            result = statusd['outputfile']
            if len(result) >= 2:
                if result[0] == '\"':
                    result = result[1:]
                    if result[-1] == '\"':
                        result = result[:-1]
            file.write(result)
    log_file.close()
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
        log (dict): Log containing all fields required
        fn_status (str): Filename to write the status html to
    """
    try:
        status = PROGRESS_HEAD + PROGRESS_BODY.format(**log)
    except KeyError:
        status = PROGRESS_HEAD + PROGRESS_BODY_UNKNOWN
    # First write to a temporary file, then copy to actual status file. That
    # way, the status file won't be corrupt if the writing process takes a 
    # while.
    fn_status_new = fn_status + '.new'
    with open(fn_status_new, 'w') as fout:
        fout.write(status)
    shutil.copyfile(fn_status_new, fn_status)
    
#    logger.info("Wrote status file")


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
