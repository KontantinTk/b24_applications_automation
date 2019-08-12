import re
from datetime import datetime, timedelta
import json
import os


class ConfigProvider(object):
    config_data = None

    @classmethod
    def get_config(cls):
        if cls.config_data is None:
            cls.config_data = ConfigProvider.get_new_config()

        return cls.config_data

    @staticmethod
    def get_new_config():
        with open(os.path.dirname(os.path.abspath(__file__))+"/configs/main.json", "r") as read_file:
            data = json.load(read_file)
            return data


def get_datetime_string_from_text(text):
    return re.search(r'\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}', text)[0]


def datetime_from_bitrix(datetime_bitrix_string):
    try:
        return datetime.strptime(datetime_bitrix_string, '%d.%m.%Y %H:%M:%S')
    except:
        now_datetime = get_now_datetime()
        update_datetime_file(now_datetime.strftime('%d.%m.%Y %H:%M:%S'))
        return now_datetime


def update_datetime_file(_string_datetime):
    fh = open(ConfigProvider.get_config()['path_to_next_date'], 'w')
    fh.write(str(_string_datetime))
    fh.close()


def get_datetime_from_file():
    fh = open(ConfigProvider.get_config()['path_to_next_date'], 'r')
    string_datetime_from_file = fh.readline()
    fh.close()
    return string_datetime_from_file


def get_now_datetime():
    return datetime.now()


def get_now_datetime_for_Moscow():
    return get_now_datetime() + timedelta(hours=1)


def write_to_log(*additions):
    fh = open('/home/b24_applications_automation/logs/request_log.txt', 'a+')
    now_datetime = get_now_datetime_for_Moscow()

    # Log record length is 52
    fh.write('## Record start.\n')
    fh.write("Date is {}\n".format(now_datetime))

    if additions:
        for i, addition in enumerate(additions):
            fh.write("{}) {}\n".format(i + 1, addition))

    fh.write('## Record end.\n\n')
    fh.close()
