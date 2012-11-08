#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, date, time, timedelta
from itertools import cycle

import pymongo
from bson import DBRef
from settings import DB_NAME


old_date = date(1900, 1, 1)
weekdays = range(1, 8)

feature_day = lambda days: timedelta(days=days)

def make_datetime(date_or_time):
    if isinstance(date_or_time, date):
        return datetime.combine(date_or_time, time())
    else:
        return datetime.combine(old_date, date_or_time)

db = pymongo.Connection()[DB_NAME]


if __name__ == '__main__':
    db.users.drop()
    db.alarms.drop()

    db.users.insert(
        [{'name': u'Иван Васильевич', 'phone': '1111111111'},
         {'name': u'Ахмед Абдуллин', 'phone': '2222222222'},
         {'name': u'Рахат Лукумов', 'phone': '3333333333'},
         {'name': u'Абдусариб Шишвамбеков', 'phone': '4444444444'},
         {'name': u'Илья Петров', 'phone': '5555555555'},
         {'name': u'Филин Сазанович', 'phone': '6666666666'},
         {'name': u'Гусейн Утконович', 'phone': '7777777777'},
         {'name': u'Федор Топорович', 'phone': '8888888888'},
         {'name': u'Эрнесто Чегеваров', 'phone': '9999999999'},
         {'name': u'Хулио Перес', 'phone': '0000000000'}
        ],
        safe=True
    )

    users = cycle(db.users.find())
    today = date.today()

    # На каждую минуту в течение года у нас есть 2 будильника с фиксированной датой
    for day in range(0, 365):
        for hour in range(0,24):
            for minute in range(0,60):
                db.alarms.insert([
                    {'time': make_datetime(time(hour, minute)),
                     'date': make_datetime(today + feature_day(day)),
                     'user': DBRef('users', users.next()['_id']),
                    },
                    {'time': make_datetime(time(hour, minute)),
                     'date': make_datetime(today + feature_day(day)),
                     'user': DBRef('users', users.next()['_id']),
                    },
                ])

    # И также на каждую минуту есть один периодический будильник
    for hour in range(0,24):
        for minute in range(0,60):
            for weekday in weekdays:
                db.alarms.insert(
                    {'time': make_datetime(time(hour, minute)),
                     'weekdays': [weekday],
                     'user': DBRef('users', users.next()['_id']),
                    }
                )

    db.alarms.ensure_index('time')
    db.alarms.ensure_index('date')
    db.alarms.ensure_index('weekdays')

