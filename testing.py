from module import services, parser

arg1 = 'магадан'
arg2 = 'бухгалтер'

if services.get_req(arg1, arg2):
    id_area, text_req = services.get_req(arg1, arg2)
    filename = parser.get_result_for_bot(id_area, text_req, arg1)
    result = parser.load_result_from_file(filename)
    print(result)
    #print(count_vacancies, sum_salary_count, top_skills)
else:
    error = 'Неверно введен город, повторите ввод данных'
    print(error)