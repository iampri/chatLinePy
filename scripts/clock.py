from apscheduler.schedulers.blocking import BlockingScheduler
from job.jobs import Jobs

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def run():
    job = Jobs()
    res = job.run()
    print('Timer is ticked...')

sched.start()