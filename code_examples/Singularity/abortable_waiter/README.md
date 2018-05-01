# Full-featured Singularity example: an abortable waiter

Code layout:
1. Start script
   * Checks MPI variables
   * Starts job on every node
   * Starts log crawler and notifications monitor only on first node
2. The actual job: a waiter
   * does nothing but waiting
   * writes simple stuff to a log file
3. Log crawler
   * reads the waiter log files regularly and creates html status reports
   * the status reports contain controls to gracefully abort the job
4. Notifications monitor
   * Monitors `/service/notifications.txt` (checks for existence regulary)
   * Reacts to incoming messages