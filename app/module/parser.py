from app.module import services
from app.module import base_orm


def prepare_result_for_bot(count_vacancies, sum_salary_count, top_skills, area_req, text_req):
    '''
    :return: имя файла с текстом для сообщения
    '''
    filename = str(area_req) + '_' + str(text_req) + '.txt'
    # Выгружаем в текстовик форматированный вывод
    with open(filename, 'w', encoding='utf8') as file:
       file.write('Кол-во вакансий: %s\n' % count_vacancies)
       file.write('Средняя зарплата: %s рублей\n' % sum_salary_count)
       file.write('Топ 20 навыков: %s\n' % top_skills)
    return filename

def get_result(id_area, text_req, area_req):
    '''
    Главная функция
    Передаются параметры для запроса. Проверяет в кэше, если был такой запрос, то выдает результат из базы.
    Если не было ранее такого запроса, парсит, пишет в базу, выдает результат.
    :param id_area: код региона
    :param text_req: ключевая фраза
    :param area_req: название региона поиска
    :return: если для сайта то объекты кол-во вакансий, средняя зп, топ 20 навыков
    '''
    if services.check_result_from_cache(id_area, text_req):
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

