from module import services
import requests
import json
import sqlite3
from collections import defaultdict
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

FILEDB = 'hhdb.db'
BASE_URL = 'https://api.hh.ru/'
URL_vacancies = f'{BASE_URL}vacancies'
url_areas = f'{BASE_URL}areas'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}
all_areas_json = requests.get(url_areas, headers=headers).json()

engine = create_engine('sqlite:///hhdb_orm.sqlite', echo=True)
Base = declarative_base()

class Region(Base):
    __tablename__ = 'region'
    region_code = Column(Integer, primary_key=True)
    region_name = Column(String)

    def __init__(self, region_code, region_name):
        self.region_code = region_code
        self.region_name = region_name

    def __repr__(self):
        return "<Region('%s','%s')>" % (self.region_code, self.region_name)

class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    vacancy_name = Column(String)
    region_id = Column(Integer, ForeignKey('region.region_code'))
    avg_salary = Column(Integer)
    total_vacancy = Column(Integer)

    def __init__(self, vacancy_name, region_id, avg_salary, total_vacancy):
        self.vacancy_name = vacancy_name
        self.region_id = region_id
        self.avg_salary = avg_salary
        self.total_vacancy = total_vacancy

    def __repr__(self):
        return "<Vacancy('%s','%s', %s, %s)>" % (self.vacancy_name, self.region_id, self.avg_salary, self.total_vacancy)

class Vacancy_skills(Base):
    __tablename__ = 'vacancy_skills'
    id = Column(Integer, primary_key=True)
    vacancy_id = Column(Integer, ForeignKey('vacancy.id'))
    skill_name = Column(String)
    count = Column(Integer, default=0)

    def __init__(self, vacancy_id, skill_name, count):
        self.vacancy_id = vacancy_id
        self.skill_name = skill_name
        self.count = count

    def __repr__(self):
        return "<Vacancy_skills('%s','%s', %s)>" % (self.vacancy_id, self.skill_name, self.count)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def process_parsing(id_area, text_req, params, area_req):
    #conn = sqlite3.connect(FILEDB, check_same_thread=False)
    #cursor = conn.cursor()
    region = Region(id_area, area_req)
    vacancy = Vacancy(text_req, id_area, None, None)
    session.add(region)
    session.add(vacancy)
    session.commit()

    #cursor.execute('INSERT INTO region (region_code, region_name) VALUES (?, ?)', (id_area, area_req))
    #cursor.execute('INSERT INTO vacancy (vacancy_name, region_id) VALUES (?, ?)', (text_req, id_area))
    #conn.commit()
    #cursor.execute('SELECT id FROM vacancy where vacancy_name=? and region_id=?', (text_req, id_area))
    vacancy_id = session.query(Vacancy).filter(Vacancy.vacancy_name == text_req and Vacancy.region_id == id_area).all()
    for vac_id in vacancy_id:
        print(vac_id.region_id)
    #print('это ваканси айди ->', vacancy_id)
    exit()
    #conn.commit()
    #vacancy_id = cursor.fetchone()[0]
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
    allurls = services.get_vacancies_url(count_pages, URL_vacancies, text_req, id_area)
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

