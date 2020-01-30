from flask import Flask, render_template

web = Flask(__name__)

@web.route('/')
def index():
    context = {
    'title':'HeadHanter Парсер',
    'button_name':'Парсить вакансии'
    }
    return render_template('index.html', **context)

@web.route('/form/')
def form():
    return render_template('form.html')



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