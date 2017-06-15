from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def jobrun():
    page = requests.get('https://obscure-bastion-79958.herokuapp.com/job/')
    print('Timer is ticked...')

sched.start()