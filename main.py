from flask import Flask, render_template

web = Flask(__name__)

@web.route('/')
def index():
    return render_template('index.html')


@web.route('/contacts/')
def contacts():
    return render_template('contacts.html')

if __name__ == "__main__":
    web.run(debug=True)