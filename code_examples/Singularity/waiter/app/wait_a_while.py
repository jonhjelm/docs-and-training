import sys
import time

STATUSFILE = "/service/status.txt"
RESULTFILE = "/service/result.txt"

PROGRESS = '''<html>
  <head>
    <title>HPC job progress</title>
  </head>

  <body style="margin: 20px; padding: 20px;">
    <h1>HPC job progress</h1>
    <div>
    <h3>This is a waiter. It's waiting on the HPC cluster. It has waited {}/{} seconds.</h3>
    </div>
  </body>
</html>
'''


def main():
    seconds_to_wait = int(sys.argv[1])

    with open(RESULTFILE, 'w') as f:
        f.write('UNSET')

    for current_time in range(seconds_to_wait):
        status = make_progressbar(current_time, seconds_to_wait)
        with open(STATUSFILE, 'w') as f:
            f.write(str(status))
        time.sleep(1)

        if current_time == seconds_to_wait - 1:
            with open(RESULTFILE, 'w') as f:
                f.write('Done. I have waited {} seconds.'.format(seconds_to_wait))


def make_progressbar(current_time, total_time):
    return PROGRESS.format(current_time, total_time)


if __name__ == "__main__":
    main()
