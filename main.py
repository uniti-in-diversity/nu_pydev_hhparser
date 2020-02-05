from flask import Flask, render_template, request
import bot_hhparser

web = Flask(__name__)

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
    if bot_hhparser.get_req(area, vacancy):
        id_area, text_req = bot_hhparser.get_req(area, vacancy)
        result = (bot_hhparser.get_result(id_area, text_req, area))
        return render_template('result.html', result=result)
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