from flask_mysqldb import MySQL


# Setup Database function to connect to database and return mysql object
def setup_db(app):
    app.config.from_pyfile('config.py')
    # choose db host if local environment leave as local host if not use your URL
    app.config[ 'MYSQL_HOST' ] = 'localhost'
    # db username
    app.config[ 'MYSQL_USER' ] = 'root'
    # db password better stored as enviroment variable
    app.config[ 'MYSQL_PASSWORD' ] = 'tafiTAFI'
    # db name
    app.config[ 'MYSQL_DB' ] = 'car_hire'
    # connecting flask to my sql
    mysql = MySQL(app)
    return mysql


# db_execute function execute a sql statement(s) and return success state and message
def db_execute(mysql, statements):
    # Creating a connection cursor
    cursor = mysql.connection.cursor()
    # Executing SQL Statements
    if isinstance(statements, str):
        cursor.execute(statements)
    elif isinstance(statements, list):
        for statement in statements:
            cursor.execute(statement)
    try:
        # Saving the Actions performed on the DB
        mysql.connection.commit()
    except Exception as e:
        print(e)
        return {
            'success': False,
            'message': e,
        }
    else:
        return {
            'success': True,
            'message': 'Statement executed successfully'
        }
    finally:
        # Closing the cursor
        cursor.close()

