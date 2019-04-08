from rq import use_connection
from datetime import datetime
from rq_scheduler import Scheduler
from count_words import count_words_at_url

use_connection()
scheduler = Scheduler()



def schedule():
    scheduler.schedule(
        scheduled_time=datetime.utcnow(),  # Time for first execution
        func=count_words_at_url,                     # Function to be queued
        interval=2,                   # Time before the function is called again, in seconds
        # Repeat this number of times (None means repeat forever)
        repeat=2
    )


def cron():
    scheduler.cron(
        '* * * * *',  # Time for first execution
        func=count_words_at_url,                     # Function to be queued
        # Repeat this number of times (None means repeat forever)
        repeat=None
    )
cron()
