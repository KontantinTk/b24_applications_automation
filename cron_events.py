from b24auto import config
from ApplicationWatcher import ApplicationWatcher

last_bitrix_datetime_string = config.get_datetime_from_file()

next_datetime = config.datetime_from_bitrix(last_bitrix_datetime_string)
now_datetime = config.get_now_datetime_for_Moscow()

if now_datetime > next_datetime:
    config.write_to_log("Trying to get portals")
    aw = ApplicationWatcher()
    aw.start()
    aw.end()
else:
    # config.write_to_log("Couldn't get portals!")
    pass