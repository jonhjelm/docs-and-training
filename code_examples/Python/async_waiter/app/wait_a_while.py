"""Simple script which waits for a given amount of time.

While waiting, it regularly updates a status file.
Once finished waiting, it writes "FINISHED" into a result file.

In a more realistic scenario, this waiter would be replaced by a complex
calculation or similar.
"""
import sys
import time


def main():
    seconds_to_wait = int(sys.argv[1])
    statusfile = sys.argv[2]
    resultfile = sys.argv[3]

    with open(resultfile, 'w') as f:
        f.write('UNSET')

    for current_time in range(seconds_to_wait):
        status = "%d" % round(100*(current_time+1)/seconds_to_wait)
        with open(statusfile, 'w') as f:
            f.write(str(status))
        time.sleep(1)

        if current_time == seconds_to_wait - 1:
            with open(resultfile, 'w') as f:
                f.write('FINISHED')


if __name__ == "__main__":
    main()
