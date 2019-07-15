#!/usr/bin/env python3
"""
Executes an Openfoam simulation.

The case is decomposed, run in parallel and reconstructed.
Background process of log crawling and notifications monitor are also started.

Please note that this script is meant to be executed in parallel (see below)
but there's no guarantee that it would work with executables different than
Openfoam.

Usage
-----
    mpirun -np NP python startup.py SOLVER FOLDER NP

Args
----
    NP:     number of processors
    SOLVER: Openfoam solver
    FOLDER: case folder

"""
import logging
import os
import subprocess
import sys

logging.basicConfig(format='%(asctime)s %(name)-15s %(levelname)-8s %(message)s', level=logging.INFO)
logger = logging.getLogger('Openfoam image')


def main():
    """Main program."""
    # Get the rank and the command line parameters
    # Please note that the rank is a string.
    rank = get_rank()
    solver = sys.argv[1]
    folder = os.path.abspath(sys.argv[2])
    np = sys.argv[3]

    # Go to case folder, if exists
    try:
        os.chdir(folder)
    except FileNotFoundError:
        logger.error(F'Folder {folder} not found.')
        exit()

    # Needed filenames
    fn_log = os.path.join(folder, solver)
    fn_log += '.log'
    fn_notification = '/service/notifications.txt'
    fn_status = '/service/status.html'
    fn_result = '/service/result.txt'

    # Preliminary operations started by the main process
    if rank == '0':

        # Write dummy value into result file
        logger.info('Writing dummy result')
        with open(fn_result, 'w') as resfile:
            resfile.write('UNSET')

        # Start log crawler
        logger.info('Starting log crawler')
        log_crawler_proc = subprocess.Popen(['/app/log_crawler.py', fn_log,
                                             fn_status])

        # Start notification monitor
        logger.info('Starting notifications monitor')
        monitor_proc = subprocess.Popen(['/app/notifications_monitor.py',
                                         folder, fn_notification])

        # Domain decomposition
        logger.info('Decomposing case')
        subprocess.run(['foamDictionary', 'system/decomposeParDict', '-entry',
                        'method', '-set', 'scotch'],
                       stdout=subprocess.DEVNULL, check=True)
        subprocess.run(['foamDictionary', 'system/decomposeParDict', '-entry',
                        'numberOfSubdomains', '-set', str(np)],
                       stdout=subprocess.DEVNULL, check=True)
        subprocess.run(['decomposePar', '-force'], stdout=subprocess.DEVNULL,
                       check=True)

    # Actual calculation
    try:
        with open(fn_log, 'w') as logfile:
            if rank == '0':
                logger.info('Running simulation')
            subprocess.run([solver, '-parallel', '-case', folder], check=True,
                           stdout=logfile, stderr=logfile)

    # Catch a solver error (i.e. Openfoam exits with errors)
    except subprocess.CalledProcessError:
        if rank == '0':
            logging.error('Simulation aborted due to solver error.')
            with open(fn_result, 'w') as resfile:
                resfile.write('Solver error.')

    # Final domain reconstruction
    if rank == '0':
        logger.info('Reconstructing domain')
        subprocess.run(['reconstructPar'], stdout=subprocess.DEVNULL)
        subprocess.run(['rm -rf processor*'], shell=True,
                       stdout=subprocess.DEVNULL)

    # Final tasks
    if rank == '0':
        monitor_proc.terminate()
        with open(fn_result, 'w') as resfile:
            resfile.write('Calculation ended.')

        # To avoid immediate abort in the next run, in case simulation was
        # stopped by the user
        subprocess.run(['foamDictionary', 'system/controlDict', '-entry',
                        'stopAt', '-set', 'endTime'],
                       stdout=subprocess.DEVNULL)

    return


def get_rank():
    """Obtain the rank, even if it is not an MPI execution."""
    try:
        return os.environ['PMIX_RANK']
    except KeyError:
        return '0'


if __name__ == "__main__":
    main()
