#coding:utf-8
from flask import Flask
from flask_script import Manager

app = Flask(__name__)
manage = Manager(app)

"""flask的Manager类似于django的manage 不过没有django的manage功能强大"""

@app.route('/login')
def login():
    return 'login'

if __name__ == '__main__':
    # app.run(debug=True)
    manage.run()