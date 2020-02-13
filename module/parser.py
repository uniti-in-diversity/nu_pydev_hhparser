import json
from module import base_orm, services

#BASE_URL = 'https://api.hh.ru/'
#URL_vacancies = f'{BASE_URL}vacancies'
#url_areas = f'{BASE_URL}areas'
#headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}
#all_areas_json = requests.get(url_areas, headers=headers).json()

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
    return result_data

def prepare_result_for_bot(count_vacancies, sum_salary_count, top_skills, area_req, text_req):
    filename = str(area_req) + '_' + str(text_req) + '.txt'
    #Выгружаем в текстовик форматированный вывод
    with open(filename, 'w', encoding='utf8') as file:
       file.write('Кол-во вакансий: %s\n' % count_vacancies)
       file.write('Средняя зарплата: %s рублей\n' % sum_salary_count)
       file.write('Топ 20 навыков: %s\n' % top_skills)
    return filename


def get_result(id_area, text_req, area_req):
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
        count_vacancies, sum_salary_count, top_skills = base_orm.get_result_from_db(id_area, text_req)
        return count_vacancies, sum_salary_count, top_skills
    else:
        params = services.get_reqs_params(id_area, text_req)
        base_orm.process_parsing(id_area, text_req, params, area_req)
        count_vacancies, sum_salary_count, top_skills = base_orm.get_result_from_db(id_area, text_req)
        return count_vacancies, sum_salary_count, top_skills

def get_result_for_bot(id_area, text_req, area_req):
    '''
    :param id_area: код региона
    :param text_req: ключевая фраза
    :param area_req: название региона поиска
    :return: путь к файлу с результатом парсинга в текстовом формате для отправки в телегу
    '''
    count_vacancies, sum_salary_count, top_skills = get_result(id_area, text_req, area_req)
    filename = prepare_result_for_bot(count_vacancies, sum_salary_count, top_skills, area_req, text_req)
    return filename


# arg1 = 'краснодар'
# arg2 = 'сисадмин'
#
# if services.get_req(arg1, arg2):
#     id_area, text_req = services.get_req(arg1, arg2)
#     filename = get_result_for_bot(id_area, text_req, arg1)
#     result = load_result_from_file(filename)
#     print(result)
#     #print(count_vacancies, sum_salary_count, top_skills)
# else:
#     error = 'Неверно введен город, повторите ввод данных'
#     print(error)


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