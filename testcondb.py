import sqlite3

#data = 'астрахань'
conn = sqlite3.connect('hhdb.db', check_same_thread=False)
cursor = conn.cursor()

#cursor.execute('select s.skill_name, vs.count from vacancy v, skills s, vacancy_skills vs where vs.vacancy_id = v.id and vs.skill_id = s.id and vs.vacancy_id = 1 ORDER BY vs.count DESC')
#print(cursor.fetchall())
#
# id_area = 60
# text_req = 'бухгалтер'
# area_req = 'астрахань'
# cursor.execute('SELECT id FROM vacancy where vacancy_name=? and region_id=?', (text_req, id_area))
# id = int(cursor.fetchone()[0])
# print(id)

vacancy_id = 2
cursor.execute('select v.avg_salary, v.total_vacancy from vacancy v where v.id = ?', ([vacancy_id]))
result = (cursor.fetchall())
print(result)
print(type(result))

sum_salary_count, count_vacancies  = result[0]
# count_vacancies = result[1]
print(sum_salary_count, count_vacancies)

