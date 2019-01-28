# -*- coding:utf-8 -*-
# coding=<utf8>
from todoes.models import Activity, Person
import datetime

def set_last_activity_model(login,url,url_not_to_track=[],url_one_record=[]):
    """
    Сохраняем последную деятельность пользователя на сайте - что и когда
    Если url = /tasks/, то есть просто обновляется страница с заявками, чтобы не плодить мусор в БД просто обновляется последнее аналогичное посещение
    """
    if url not in url_not_to_track and url not in url_one_record:
        la = Activity()
        la.login = login
        la.last_page = url
        la.timestamp =datetime.datetime.now()
        la.save()
    elif url in url_one_record:
        try:
            la = Activity.objects.filter(login=login,last_page=url)[0]
        except (Activity.DoesNotExist,IndexError):
            la = Activity()
            la.login = login
            la.last_page = url
            la.timestamp =datetime.datetime.now()
            la.save()
        else:
            la.timestamp =datetime.datetime.now()
            la.save()
def get_last_activities():
    """
    Получаем список последних действий пользователей - когда и что
    """
    class Act():
        def __init__(self,user,not_older_than_15,last_page,timestamp):
            self.not_older_than_15 = not_older_than_15
            self.user = user
            self.last_page = last_page
            self.timestamp = timestamp
    # получаем список пользователей
    users = Person.objects.all()
    # для каждого пользователя получаем его последний url и дату и добавляем их в возвращаемый [] и давно ли это было
    # первый элемент равен True, если последнее событие было в пределах последних 15 минут
    last_activities=[]
    for user in users:
        try:
            la = Activity.objects.filter(login=user.login)[0]
            last_activities.append(
                Act(not_older_than_15 = la.timestamp >=
                                    datetime.datetime.now() -
                                    datetime.timedelta(minutes=15) ,
                    user=user,
                    last_page=la.last_page,
                    timestamp=la.timestamp))
        except IndexError:
            pass
    return last_activities

def get_user_per_date_activities(person,date):
    """
    Получаем список действий пользователя за дату
    """
    last_activities=[]
    next_day = date + datetime.timedelta(1)
    try:
        queryset = Activity.objects.filter(login=person.login)
        last_activities = queryset.filter(timestamp__range=(date, next_day))
    except IndexError:
        pass
    return last_activities