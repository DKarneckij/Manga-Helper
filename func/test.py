from time import sleep
import warnings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import gspread

warnings.filterwarnings("ignore")

async def test():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Looping at ", current_time)

scheduler = AsyncIOScheduler(timezone="America/New_York")
scheduler.add_job(test, 'cron', hour= 19, minute= '*')
scheduler.start()
            

