# -*- coding: utf-8 -*-
from datetime import datetime, time
from celery import Celery
from celery.utils.log import get_task_logger
from initialize_db import db, make_datetime

celery = Celery('tasks', broker='amqp://guest@localhost//')
celery.config_from_object('celeryconfig')

logger = get_task_logger(__name__)


@celery.task
def find():
    now = datetime.now()

    alarms = db.alarms.find(
        {'time': make_datetime(time(now.hour, now.minute)),
         '$or': [
             {'date': make_datetime(now.date())},
             {'weekdays': now.weekday()}
         ]})

    for alarm in alarms:
        call.delay(alarm['user'])

@celery.task
def call(user):
    user = db.dereference(user)
    logger.info(u"Звоним товарищу %s по номеру %s" % (user['name'], user['phone']))
