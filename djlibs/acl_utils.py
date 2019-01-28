# -*- coding:utf-8 -*-
# coding=<utf8>
from user_settings.settings import admins
from djlib.error_utils import FioError, ErrorMessage, add_error
from django.http import HttpResponse, Http404, HttpResponseRedirect
# временно, надо сделать независимым от приложения
from todoes.models import Task, RegularTask
task_types = {'one_time':Task,'regular':RegularTask}


def acl(request,task_type,task_id):
    user = request.user.username
    task = task_types[task_type].objects.get(id = task_id)
    if user in task.acl.split(';') or user in admins or not task.acl:
        return True
    else:
        return False
#TODO: убрать. Это должно быть по умолчанию. Перенсё в multilanguage
def for_admins(fn):
    """
     Декоратор для "видов", которые содержат инфу, которую должны видеть только админы. Добавляет в словарь dict['admin']=True
    """
    def wrapped(*args,**kwargs):
        # print "in shows_errors "+str(args[0].path)+" before calling function"
        decorate_or_not, result = fn(*args,**kwargs)
        # raise TypeError
        if not decorate_or_not:
            return decorate_or_not, result
        template,forms_dict,dict,request,app=result
        user = request.user.username
        if user in admins:
            # print "adding error to dict"
            dict['admin']=True
        # print "for path "+args[0].path+" dict['admin']="+str(dict['admin'])
        return decorate_or_not, (template,forms_dict,dict,request,app)
    return wrapped
def admins_only(fn):
    """
     Декоратор для "видов", которые могут видеть только админы. В противном случае перенаправляет к /
    """
    def wrapped(*args,**kwargs):
        # raise ImportError
        request = args[0]
        user = request.user.username
        if user not in admins:
            add_error(u"Эта страница доступна только для администраторов: %s " % (request.path,),request)
            request.session.modified = True
            return (False,(HttpResponseRedirect('/')))
        # print "in shows_errors "+str(args[0].path)+" before calling function"
        decorate_or_not, result = fn(*args,**kwargs)
        # raise TypeError
        if not decorate_or_not:
            return decorate_or_not, result
        template,forms_dict,dict,request,app=result
        return decorate_or_not, (template,forms_dict,dict,request,app)
    return wrapped

def add_permission(to='', for_whom='',
                   acl_field='acl', acl_separator=u';'):
    """
    Добавляет разрешение для объекта for_whom на просмотр
    объекта, определяемоего при помощи строки to. По умолчанию для
    хранения информации о правах
    доступа к to используется поле acl_field. В качестве разделителя
    значений в поле acl_field используется acl_separator

    Возращаемые значения:

   'CHANGING_ERROR' - ошибка произошла до попытки установить новое
                        значение
    'SAVING_ERROR' - ошибка произошла при попытке установить новое
                    значение или сохранить его
    'OK' - всё ок

    Parameters
    ----------
    to : django.db.models.Model
        Экзмепляр модели, содержащий параметр acl_field, доступ к
        которому надо обеспечить
    for_whom : string
        Определитель (например, логин) того, кому надо
        предоставить доступ
    acl_field : string
        Назавание поля объекта to, в котором хранится информация о
        правах доступа к нему. По умолчанию - 'acl'
    acl_separator : string
        Разделитель значений в поле acl_field. По умолчанию ";"
    """
    try:
        old_acl = to.__getattribute__(acl_field)
        tmp = [a for a in old_acl.split(acl_separator) if a]
        tmp.append(str(for_whom))
        new_acl = acl_separator.join(tmp)
    except:
        return 'CHANGING_ERROR'
    try:
        c.__setattr__(acl_field,new_acl)
        c.save()
    except:
        return 'SAVING_ERROR'
    return 'OK'
def remove_permission(to='', for_whom='',
                   acl_field='acl', acl_separator=u';'):
    """
    Убирает разрешение для объекта for_whom на просмотр
    объекта, определяемоего при помощи строки to. По умолчанию для
    хранения информации о правах
    доступа к to используется поле acl_field. В качестве разделителя
    значений в поле acl_field используется acl_separator

    Возращаемые значения:

   'CHANGING_ERROR' - ошибка произошла до попытки установить новое
                        значение
    'SAVING_ERROR' - ошибка произошла при попытке установить новое
                    значение или сохранить его
    'OK' - всё ок

    Parameters
    ----------
    to : django.db.models.Model
        Экзмепляр модели, содержащий параметр acl_field, доступ к
        которому надо обеспечить
    for_whom : string
        Определитель (например, логин) того, кому надо
        предоставить доступ
    acl_field : string
        Назавание поля объекта to, в котором хранится информация о
        правах доступа к нему. По умолчанию - 'acl'
    acl_separator : string
        Разделитель значений в поле acl_field. По умолчанию ";"
    """
    try:
        old_acl = to.__getattribute__(acl_field)
        tmp = set([a for a in old_acl.split(acl_separator) if a])
        tmp.remove(str(for_whom))
        new_acl = acl_separator.join(tmp)
    except:
        return 'CHANGING_ERROR'
    try:
        to.__setattr__(acl_field,new_acl)
        to.save()
    except:
        return 'SAVING_ERROR'
    return 'OK'