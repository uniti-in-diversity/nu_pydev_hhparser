import requests
import pprint
from collections import defaultdict
import json

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

def get_vacancies_url(count_pages, url, text_req, id_area):
    all_vacancies_urls = []
    for page in range(count_pages):
        params = {'text': text_req, 'area': id_area, 'page': page}
        result = requests.get(url, params=params).json()
        all_vacancies_urls.append([{'api_url': item['url']} for item in result['items']])
    return all_vacancies_urls

BASE_URL = 'https://api.hh.ru/'
url_vacancies = f'{BASE_URL}vacancies'
url_areas = f'{BASE_URL}areas'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}
all_areas_json = requests.get(url_areas, headers=headers).json()

while True:
    area_req = input('Введите регион поиска или город, можно в любом регистре: ').lower()
    name = find_key(all_areas_json, 'name')
    key = find_key(all_areas_json, 'id')
    try:
        count_area = find_area_intindex(name, area_req)
        break
    except ValueError:
        print('Город введен с ошибкой, повторите ввод:')

dict_area = find_id_area(count_area, key)
id_area = dict_area[1]
print('Выбран город', area_req, 'id -', id_area)
text_req = input('Введите ключевые слова для поска вакансии: ')
params = {'text': text_req, 'area': id_area}

result = requests.get(url_vacancies, headers=headers, params=params).json()
count_vacancies = result['found']
items_vacancies = result['items']
count_pages = result['pages']

#print('СТРАНИЦ', count_pages)
#print('ВАКАНСИЙ', count_vacancies)

allurls = get_vacancies_url(count_pages, url_vacancies, text_req, id_area)
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

#print(key_skills)
#print(count_url_skils)
#print(len(salary_list))

sum_salary_count = sum(salary_list)/len(salary_list)
sorted_key_skills = sorted(key_skills.items(), key=lambda x: int(x[1]), reverse=True)
filename = str(area_req)+'_'+str(text_req)

with open(filename+'.json', 'w', encoding='utf8') as file:
    json.dump(sorted_key_skills, file, ensure_ascii=False)

print('Всего вакансий', count_vacancies)
print('Средняя зарплата', sum_salary_count)
print('Отсортирвоанный список навыков:\n')
for sorted_skil in sorted_key_skills:
    print(sorted_skil)
