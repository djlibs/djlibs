# -*- coding:utf-8 -*-
# coding=<utf8>
__version__ = '0.0.1а'

import re
from user_settings.functions import get_full_section
from ConfigParser import NoSectionError
languages = {'ru': 'RUS/',
             }


class Link:
    def __init__(self, name, link):
        self.name = name
        self.href = link
        self.id = id(self)
        # обрабатываем ссылки, где есть запрос параметров, типа
        # '/api/snmp/show_router_mapping_by_id/{0}/'
        params = re.findall('{[^}]+}', self.href)
        # print params
        self.onclick = 'var link=\\"'+link+'\\";'
        script_end = ''
        for idx, param in enumerate(params):
            # получаем параметры из урла, запрашиваем значения у
            # пользователя и заменяем их в урле
            question = param[1:-1]
            self.onclick +=\
                ("var a"+str(idx)+'=prompt(\\"'+question+':\\");')
            script_end +=\
                ('link=link.replace(\\"'+param+'\\",a'+str(idx)+");")
        self.onclick += script_end
        self.onclick +=\
            ('document.getElementById(\\"'+str(self.id) +
             '\\").href = link;')


class Module:
    def __init__(self, name):
        self.links = []
        self.name = name
        self.active = False
        self.id = None


class ModuleGroup:
    def __init__(self):
        self.__modules = []
        self.__module_id = 0

    def append(self, item):
        item.id = self.__module_id
        self.__modules.append(item)
        self.__module_id += 1

    def __iter__(self):
        return self.__modules.__iter__()


def add_module_menu(fn):
    """
     Декоратор, который добавляет в словарь данные для отображения
     меню модулей под ключём module_menu
     Пример того, что должна возвращать функция, которую декорируют:
     return (decorate_or_not,
            ('all_bills.html',
                {'form_name':(form_param1,form_param2),},
                {'cashs':cashs, 'cashlesss':cashlesss},
                request,
                app))
    """
    def wrapped(*args, **kwargs):
        decorate, result = fn(*args, **kwargs)
        if not decorate:
            return decorate, result
        template, forms_dict, context, request, app = result
        modules = collect_modules()
        context['modules'] = modules
        return decorate, (template, forms_dict, context, request, app)
    return wrapped


def collect_modules():
    """
    Собирает данные о модулях, которые установлены в системе.
    Не факт, что включены
    """
    modules = ModuleGroup()
    import os
    import os.path
    import imp
    cur_dir = os.getcwd()
    for record in os.listdir('.'):
        if os.path.isdir(record):
            temp_dir = os.path.join(cur_dir, record)
            # если это модуль
            if 'todoes_module' in os.listdir(temp_dir):
                module = Module(record)
                # если в этом модуле есть ссылки - импортируем
                if '__settings__.py' in os.listdir(temp_dir):
                    foo = imp.load_source('module.'+record,
                                          os.path.join(temp_dir,
                                                       '__settings__.'
                                                       'py'))
                    module.links = foo.links
                    # module.links = foo.Module().links
                else:
                    module.links = [Link('Нет ссылок', '/'), ]
                modules.append(module)
    # для каждого модуля надо проверить, есть ли он в настройках
    # если нет - то можно его подключить и добавить в настройки,
    # если есть показываем статус из настроек. Данные для модуля
    # будем брать из файла todoes_module. Если в нём не правильные
    # данные - выдаём про него отдельное сообщение
    try:
        connected_modules = [x.option for x in get_full_section(
            'modules') if x.value]
    except NoSectionError:
        connected_modules = []
    for module in modules:
        if module.name in connected_modules:
            module.active = True
    return modules
