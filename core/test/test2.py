from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime

def prova():
    print(datetime.datetime.now().strftime("%A, %d. %B %Y %H:%M:%S"))
    print(2)

def main():
    scheduler = BackgroundScheduler()

    try:

        scheduler.add_job(prova, 'cron', hour='10', minute='*', second='*/2', id='prova')

        scheduler.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        scheduler.shutdown()


if __name__ == "__main__":
    main()
