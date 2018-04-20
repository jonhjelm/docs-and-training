import sys
import time

STATUSFILE = "/service/status.txt"
RESULTFILE = "/service/result.txt"
NOTIFICATIONS = "/service/notifications.txt"

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
    <h3>This is a waiter. It's waiting on the HPC cluster. It has waited {}/{} seconds.</h3>
    <input type="button" value="Abort" onclick="abort()">
    </div>
  </body>
</html>
'''


def main():
    seconds_to_wait = int(sys.argv[1])

    with open(RESULTFILE, 'w') as f:
        f.write('UNSET')

    for current_time in range(seconds_to_wait):
        # 1: Check if there is an abort command
        try:
            with open(NOTIFICATIONS) as f:
                notifications = f.readlines()
        except FileNotFoundError:
            notifications = []

        if len(notifications) > 0 and notifications[-1].strip() == "ABORT":
            write_result(current_time, True)
            return 0

        # 2: Write current status
        status = make_progressbar(current_time, seconds_to_wait)
        with open(STATUSFILE, 'w') as f:
            f.write(str(status))
        time.sleep(1)

    write_result(seconds_to_wait)


def write_result(seconds_waited, aborted=False):
    with open(RESULTFILE, 'w') as f:
        if aborted:
            f.write('Done. My waiting was aborted after {} seconds.'.format(seconds_waited))
        else:
            f.write('Done. I have waited {} seconds.'.format(seconds_waited))


def make_progressbar(current_time, total_time):
    return PROGRESS_HEAD + PROGRESS_BODY.format(current_time, total_time)


if __name__ == "__main__":
    main()
