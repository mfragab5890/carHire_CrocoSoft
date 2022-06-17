from flask_mysqldb import MySQL


# Setup Database function to connect to database and return mysql object
def setup_db(app):
    app.config.from_pyfile('config.py')
    # choose db host if local environment leave as local host if not use your URL
    app.config[ 'MYSQL_HOST' ] = 'localhost'
    # db username
    app.config[ 'MYSQL_USER' ] = 'root'
    # db password
    app.config[ 'MYSQL_PASSWORD' ] = 'tafiTAFI'
    # db name
    app.config[ 'MYSQL_DB' ] = 'car_hire'
    # connecting flask to my sql
    mysql = MySQL(app)
    return mysql

