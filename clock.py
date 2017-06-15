from apscheduler.schedulers.blocking import BlockingScheduler
from job.jobs import Jobs

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    job = Jobs()
    job.run()
    print('Timer is ticked...')

sched.start()