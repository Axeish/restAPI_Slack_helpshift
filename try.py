import schedule
import time

def job(t):
    print ("I'm working...", t)
    return

schedule.every().day.at("18:15").do(job,'It is 01:00')
schedule.every().day.at("18:17").do(job,'It is 01:00')
schedule.every().day.at("18:20").do(job,'It is 01:00')
schedule.every().day.at("06:15").do(job,'It is 01:00')

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute
