import time
import schedule
import backup
import json

def setSchedule(config):
    print("set backup schedule...")
    if config['schedule']['mode'] == 'perMinute':
        schedule.every(config['schedule']['perMinute']).minutes.do(backup.main, config)
    elif config['schedule']['mode'] == 'everyDayAt':
        for atTime in config['schedule']['everyDayAt']:
            schedule.every().day.at(atTime).do(backup.main, config)

if __name__ == "__main__":
    with open('config.json', encoding='utf8') as configFile:
        config = json.loads(configFile.read())
    setSchedule(config)
    backup.main()
    while True:
        schedule.run_pending()
        time.sleep(1)