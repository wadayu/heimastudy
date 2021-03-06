from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

import pymysql
pymysql.install_as_MySQLdb()

from ihome import create_app,db

app = create_app('deve')

manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    # print (app.url_map)
    manager.run()
