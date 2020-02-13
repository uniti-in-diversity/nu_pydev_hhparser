import requests
import json

BASE_URL = 'https://api.hh.ru/'
#URL_vacancies = f'{BASE_URL}vacancies'
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

# def compare_file_create_date(filename):
#     '''
#     Сравнивает текущую дату с датой создания файла (без времени, только дата)
#     :param filename: путь к файлу
#     :return: True или False
#     '''
#     today = str(datetime.date.today())
#     fd = os.path.getctime(filename)
#     fd = str(datetime.datetime.fromtimestamp(fd))
#     filedate = fd[0:10]
#     if filedate == today:
#         return True
#     else:
#         return False

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