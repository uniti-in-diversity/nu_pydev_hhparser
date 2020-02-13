import requests
import datetime
import os
from collections import defaultdict
import json
import sqlite3
from module import base_orm

#FILEDB = 'hhdb.db'
BASE_URL = 'https://api.hh.ru/'
URL_vacancies = f'{BASE_URL}vacancies'
url_areas = f'{BASE_URL}areas'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}
all_areas_json = requests.get(url_areas, headers=headers).json()

def iter_dict(d, val, indices):
    for k, v in d.items():
        if k == val:
            yield indices + [k], v
        if isinstance(v, dict):
            yield from iter_dict(v, val.lower(), indices + [k])
        elif isinstance(v, list):
            yield from iter_list(v, val.lower(), indices + [k])

def iter_list(seq, key, indices):
    for k, v in enumerate(seq):
        if isinstance(v, dict):
            yield from iter_dict(v, key.lower(), indices + [k])
        elif isinstance(v, list):
            yield from iter_list(v, key.lower(), indices + [k])

def find_key(obj, key):
    if isinstance(obj, dict):
        yield from iter_dict(obj, key.lower(), [])
    elif isinstance(obj, list):
        yield from iter_list(obj, key.lower(), [])

def find_area_intindex(name, area_req):
    ncount = 0
    for n in name:
        ncount += 1
        nname = n[1]
        nname = nname.lower()
        if nname == area_req.lower():
            return ncount
    raise ValueError('Нет такого города')

def find_id_area(count, key):
    kcount = 0
    intid = count
    for k in key:
        kcount += 1
        if kcount == intid:
            return k

def get_intcount_area(arg1):
    '''
    arg1 передаем введеный город от юзера из бота
    получаем промежточный номер который передаем в другую функцию чтобы найти id города в hh
    можно проверять есть ли на hh такой город для поиска
    :param arg1:
    :return:
    '''
    area_req = arg1.lower()
    name = find_key(all_areas_json, 'name')
    try:
        count_area = find_area_intindex(name, area_req)
        return count_area
    except ValueError:
        #print('Город введен с ошибкой, повторите ввод:')
        return 0

def get_id_area(intcount_area):
    key = find_key(all_areas_json, 'id')
    dict_area = find_id_area(intcount_area, key)
    id_area = dict_area[1]
    return id_area

def get_req(arg1, arg2):
    '''
    :arg1 = из бота город
    :arg2 = из бота ключевая фраза
    :return = параметры для запроса к апи (текст, и город)
    '''
    intcount_area = get_intcount_area(arg1)
    #print(intcount_area)
    if intcount_area == 0:
        return False
    else:
        id_area = get_id_area(intcount_area)
        text_req = arg2
        return id_area, text_req

def get_vacancies_url(count_pages, url, text_req, id_area):
    all_vacancies_urls = []
    for page in range(count_pages):
        params = {'text': text_req, 'area': id_area, 'page': page}
        result = requests.get(url, params=params).json()
        all_vacancies_urls.append([{'api_url': item['url']} for item in result['items']])
    return all_vacancies_urls

#print('Выбран город', area_req, 'id -', id_area)
#text_req = input('Введите ключевые слова для поска вакансии: ')

def get_reqs_params(id_area, text_req):
    params = {'text': text_req, 'area': id_area}
    return params

def compare_file_create_date(filename):
    '''
    Сравнивает текущую дату с датой создания файла (без времени, только дата)
    :param filename: путь к файлу
    :return: True или False
    '''
    today = str(datetime.date.today())
    fd = os.path.getctime(filename)
    fd = str(datetime.datetime.fromtimestamp(fd))
    filedate = fd[0:10]
    if filedate == today:
        return True
    else:
        return False

def check_result_from_cache(id_area, text_req):
    '''
    Передаем ID региона и запрос, ищем в истории запросов по ключу,
    если находим возвращаем имя файла с результатом запроса.
    :return: str имя файла
    '''
    #data = {}
    key_h = text_req + '_' + id_area
    with open('request_history.json', encoding='utf-8') as file:
        data = json.load(file)
    result_filename = data.get(key_h)
    return result_filename
    #print(result_filename)

def load_result_from_file(result_filename):
    '''
    Выдача резльтатов по запросу из кэша (из файла с результатом ранее выполненого запроса)
    :param result_filename: имя файла с результатом запроса выполненного ранее.
    :return: dict результат запроса из файла ранее выполненного запроса
    '''
    # загружаем txt с результатом запроса в переменную
    with open(result_filename, 'r', encoding='utf-8') as file:
        result_data = file.read()
    #print('ИЗ ФУНКЦИИ', result_data)
    return result_data

def process_parsing(id_area, text_req, params, area_req):
    #conn = sqlite3.connect(FILEDB, check_same_thread=False)
    #cursor = conn.cursor()
    region = base_orm.Region(id_area, area_req)

    cursor.execute('INSERT INTO region (region_code, region_name) VALUES (?, ?)', (id_area, area_req))
    cursor.execute('INSERT INTO vacancy (vacancy_name, region_id) VALUES (?, ?)', (text_req, id_area))
    conn.commit()
    cursor.execute('SELECT id FROM vacancy where vacancy_name=? and region_id=?', (text_req, id_area))
    conn.commit()
    vacancy_id = cursor.fetchone()[0]
    #print('vacancy_id =', vacancy_id)
    #print('vacancy_id', vacancy_id)
    #print(type(vacancy_id))
    result = requests.get(URL_vacancies, headers=headers, params=params).json()
    count_vacancies = result['found']
    cursor.execute('UPDATE vacancy SET total_vacancy = ? where id=?', (count_vacancies, vacancy_id))
    conn.commit()
    count_pages = result['pages']
    #items_vacancies = result['items']
    #print('СТРАНИЦ', count_pages)
    #print('ВАКАНСИЙ', count_vacancies)
    allurls = get_vacancies_url(count_pages, URL_vacancies, text_req, id_area)
    count_url_skils = 0
    key_skills = defaultdict(int)
    salary_list = []
    for url_vacancy in allurls:
        for url in url_vacancy:
            url_req_vac = url['api_url']
            one_vacancy = requests.get(url_req_vac).json()
            for skil in one_vacancy['key_skills']:
                skill_name = skil['name']
                key_skills[skill_name] += 1
            salary = one_vacancy['salary']
            if salary is not None:
                salary_to = salary.get('to')
                if salary_to is not None:
                    salary_list.append(salary_to)
            count_url_skils += 1

    for key_skill in key_skills:
        cursor.execute('INSERT INTO vacancy_skills (vacancy_id, skill_name, count) VALUES (?, ?, ?)', (vacancy_id, key_skill, key_skills[key_skill]))
        conn.commit()

    sum_salary_count = int(sum(salary_list)/len(salary_list))
    cursor.execute('UPDATE vacancy SET avg_salary = ? where id=?', (sum_salary_count, vacancy_id))
    conn.commit()
    conn.close()
    #sorted_key_skills = sorted(key_skills.items(), key=lambda x: int(x[1]), reverse=True)
    #выгружаем результат ВСЕ НАВЫКИ в JSON формате
    #with open(filename+'.json', 'w', encoding='utf8') as file:
    #    json.dump(sorted_key_skills, file, ensure_ascii=False)

    #формируем строки для внесения в историю запросов
    #key_h - ключ словаря запрос_код региона, file_h = имя файла с результатом запроса
    filename = str(area_req) + '_' + str(text_req)
    key_h = text_req + '_' + id_area
    file_h = str(filename)+'.txt'
    #подгружаем json с историей запросов в словарь, добавляем новый запрос словарь
    with open('request_history.json', encoding='utf-8') as file:
        data = json.load(file)
    data[key_h] = file_h

    #выгружаем обратно в json обновленный словарь с историей запросов
    with open('request_history.json', mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
    return True

def prepare_result_for_bot(count_vacancies, sum_salary_count, top_skills, area_req, text_req):
    filename = str(area_req) + '_' + str(text_req) + '.txt'
    #Выгружаем в текстовик форматированный вывод
    with open(filename, 'w', encoding='utf8') as file:
       file.write('Кол-во вакансий: %s\n' % count_vacancies)
       file.write('Средняя зарплата: %s рублей\n' % sum_salary_count)
       file.write('Топ 20 навыков: %s\n' % top_skills)
    return filename


def get_result_from_db(id_area, text_req, qtop=20):
    conn = sqlite3.connect(FILEDB, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM vacancy where vacancy_name=? and region_id=?', (text_req, id_area))
    vacancy_id = cursor.fetchone()
    cursor.execute('select v.avg_salary, v.total_vacancy from vacancy v where v.id = ?', (vacancy_id))
    query_result = (cursor.fetchall())
    sum_salary_count, count_vacancies  = query_result[0]

    cursor.execute('SELECT id FROM vacancy where vacancy_name=? and region_id=?', (text_req, id_area))
    vacancy_id = cursor.fetchone()
    cursor.execute('select vs.skill_name, vs.count from vacancy v, vacancy_skills vs '
                   'where vs.vacancy_id = v.id and vs.vacancy_id = ?'
                   'ORDER BY vs.count DESC', (vacancy_id))
    all_skills = cursor.fetchall()
    top_skills = []
    if len(all_skills) < qtop:
        qtop = int(len(all_skills))
    for i in range(qtop):
        top_skills.append(all_skills[i])
    conn.close()
    return count_vacancies, sum_salary_count, top_skills


def get_result(id_area, text_req, area_req, telebot=False):
    '''
    Главная функция использующая все остальные.
    Передаются параметры для запроса. Проверяет в кэше, если был такой запрос, то выдает результат из базы.
    Если не было ранее такого запроса, парсит, пишет в базу, выдает результат.
    :param id_area: код региона
    :param text_req: ключевая фраза
    :param area_req: название региона поиска
    :param telebot: признак откуда запрос от бота или сайта
    :return: если для сайта то объекты, елси для бота то путь к текстововму файлу со сформированным сообщением
    '''
    if check_result_from_cache(id_area, text_req):
        count_vacancies, sum_salary_count, top_skills = get_result_from_db(id_area, text_req)
        if telebot:
            filename = prepare_result_for_bot(count_vacancies, sum_salary_count, top_skills, area_req, text_req)
            return filename
        else:
            return count_vacancies, sum_salary_count, top_skills
    else:
        params = get_reqs_params(id_area, text_req)
        process_parsing(id_area, text_req, params, area_req)
        count_vacancies, sum_salary_count, top_skills = get_result_from_db(id_area, text_req)
        if telebot:
            filename = prepare_result_for_bot(count_vacancies, sum_salary_count, top_skills, area_req, text_req)
            return filename
        else:
            return count_vacancies, sum_salary_count, top_skills


# arg1 = 'краснодар'
# arg2 = 'сисадмин'
#
# if get_req(arg1, arg2):
#     id_area, text_req = get_req(arg1, arg2)
#     filename = (get_result(id_area, text_req, arg1, True))
#     result = load_result_from_file(filename)
#     print(result)
#     #print(count_vacancies, sum_salary_count, top_skills)
# else:
#     error = 'Неверно введен город, повторите ввод данных'
#     print(error)