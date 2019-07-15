#!/usr/bin/env python3
"""
Parse an Openfoam log file and write a status webpage.

Usage
-----
    python log_crawler.py LOGFILE STATFILE

Args
----
    LOGFILE:  log file to be parsed
    STATFILE: status html file to be written

This is a really basic log crawler, able to parse only two quantities, clock
time and simulation time, and display them in text mode.
The user can expand the script functionalities by:
- adding more items to rx_dict
- modifying the parse_logfile function
- modifying PROGRESS_BODY variable

Note that time_data variable will need more lists. Also, one can use library
such Matplotlib to create plots from time_data and include them in status
webpage. Keep in mind that, in this case, you should save your image as png,
encode it in base64 and then embed the code in <img> tag.

"""
import logging
import os
import sys
import re
import subprocess
import time

logging.basicConfig(format='%(asctime)s %(name)-15s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger("Log crawler")

# Head of the status webpage.
PROGRESS_HEAD = '''<html>
  <head>
    <title>Openfoam job progress</title>
    <script type="text/javascript">
      function abort() {
        notify_running_job("ABORT");
      }
    </script>
  </head>'''

# Body of the status webpage.
PROGRESS_BODY = '''<body style="margin: 20px; padding: 20px;">
    <h1>HPC job progress</h1>
    <div>
    <h3>Simulation in folder {} is going on.</h3>
    <p>Current simulation time is {} s, after {} s of clock time.</p>
    <p>Click the Abort button to stop the simulation early. Please click only once,
    it will take a while until the request is processed. (The status might even
    update once more before the job is aborted.)</p>
    <input type="button" value="Abort" onclick="abort()">
    </div>
  </body>
</html>
'''

# This dictionary contains pairs of keys and regex expressions.
# Keys are strings uses in this script to identify the quantity of interest.
# Regex elements describe the Openfoam output and include the group name of the
# quantity to be extracted from the processed string.
# See https://docs.python.org/3/library/re.html for details on python regex.
rx_dict = {
    'time': re.compile(r'^Time = (?P<time>(\d+.\d+e[+-]\d+)|(\d+[.\d+]*))'),
    'clock': re.compile(r'ExecutionTime = (?P<clock>\d+.\d+) s'),
}


def main():
    """Execute the assigned task."""
    # Command line parameters
    fn_log = os.path.abspath(sys.argv[1])
    fn_sta = os.path.abspath(sys.argv[2])
    logger.info(F'Log file: {fn_log}')
    logger.info(F'Status file: {fn_sta}')

    # Variables needed for parsing
    finished = False
    log_offset = 0

    # List of lists for quantities to retrieve
    # first list (column 0): clock time
    # second list (column 1): simulation time
    time_data = [[], []]

    while not finished:

        # Do nothing if the calculation has not been started yet
        if not os.path.isfile(fn_log):
            continue

        # Parse the new portion of the logfile
        log_offset = parse_logfile(fn_log, time_data, log_offset)

        # Write status webpage
        try:
            status = PROGRESS_HEAD + PROGRESS_BODY.format(
                os.path.dirname(fn_log),
                time_data[1][-1],  # last item of column 1 (simulation time)
                time_data[0][-1],  # last item of column 0 (clock time)
            )
            with open(fn_sta, 'w') as status_file:
                status_file.write(status)

        # In case time_data is still empty
        except IndexError:
            pass

        # Check if the simulation is finished
        finished = check_if_finished(fn_log)

        # Wait a few seconds before reading again the file
        time.sleep(3)

    return


def parse_line(line):
    """
    Parse a single line against regex in rx_dict.

    Returns
    -------
        a pair made by the found key and its retrieved value.

    """
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None


def parse_logfile(fn_log, data, offset=0):
    """
    Parse the Openfoam log file.

    Args
    ----
        fn_log: filename of the log file
        data: list of list of quantities
        offset: the start line for parsing

    Returns
    -------
        the start line of the next parsing.

    According to the key-values pairs defined in rx_dict, each line is parsed
    and the requested values are retrieved.

    For each time step, the last value of each quantity is retained if more
    than one iterations are carried out. This behaviour can be modified if
    needed, of course.

    The retrieved data are added to the data list, which is actually a list of
    lists. Each list represents a specific quantity, while each item is the
    quantity's value at a specific time step.

    The log file is parsed every three seconds, each time starting from the
    line specified in offset parameter.

    """
    # Retrieve the content of the logfile
    content = subprocess.check_output(['cat', fn_log])
    lines = content.decode('utf-8').splitlines(True)
    current_data = {}

    for index, line in enumerate(lines):

        # Process only new lines
        if index > offset:
            key, match = parse_line(line)

            # Save data in current_data dictionary
            if key == 'time':
                current_data[key] = match.group(key)
            if key == 'clock':
                current_data[key] = match.group(key)

                # In this case, a new time step will begin
                # which means we can change the offset
                # and save the retrieved data
                offset = index
                data[0].append(current_data['clock'])
                data[1].append(current_data['time'])

    return offset


def check_if_finished(fn_log):
    """
    Check if the simulation is finished.

    Returns
    -------
        True if simulation is finished, False otherwise

    Actually, it checks if the last line of the file matches
    a specific sentence.

    """
    with open(fn_log, 'r') as logfile:
        for line in logfile:
            pass
    re_test = re.compile('^Finalising parallel run')
    try:
        if re_test.match(line) is not None:
            return True
        else:
            return False
    except UnboundLocalError:
        return False


if __name__ == '__main__':
    main()
