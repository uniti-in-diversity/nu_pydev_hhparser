from flask import Flask, render_template, request
from app.module import services
from app.module import parser
import logging

web = Flask(__name__)

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('webapp_debug.log', 'a', 'utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
root_logger.addHandler(handler)

@web.route('/')
def index():
    context = {
    'title':'HeadHanter Парсер',
    'button_name':'Парсить вакансии'
    }
    return render_template('index.html', **context)

@web.route('/form/', methods=['POST'])
def post_form():
    vacancy = request.form['vacancy']
    area = request.form['area']
    if services.get_req(area, vacancy):
        id_area, text_req = services.get_req(area, vacancy)
        count_vacancies, sum_salary_count, top_skills = parser.get_result(id_area, text_req, area)
        return render_template('result.html', count_vacancies=count_vacancies, sum_salary_count=sum_salary_count, top_skills=top_skills)
    else:
        error = 'Неверно введен город, повторите ввод данных'
        return render_template('form.html', error=error)

@web.route('/form/', methods=['GET'])
def get_form():
    return render_template('form.html')

@web.route('/result/')
def result():
    return render_template('result.html')

@web.route('/contacts/')
def contacts():
    context = {
        'name': 'Декин Максим',
        'email': "maxim.dekin@gmail.com",
        'phone': +79257777777,
        'telegram':'@unitiindiversity',
        'about':'DevOps инженер, python developer'
    }
    return render_template('contacts.html', **context)

if __name__ == "__main__":
    web.run(debug=True)