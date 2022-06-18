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


# db_execute function execute a sql statement(s) insert, update and delete then return success state and message
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


# db_select function execute a sql select statement then return success state and results
def db_select(mysql, statement):
    # Creating a connection cursor
    cursor = mysql.connection.cursor()

    try:
        # Executing SQL Select Statements
        cursor.execute(statement)
        results = cursor.fetchall()
    except Exception as e:
        print(e)
        return {
            'success': False,
            'message': e,
        }
    else:
        return {
            'success': True,
            'message': 'Statement executed successfully',
            'results': results,
        }
    finally:
        # Closing the cursor
        cursor.close()


def db_create_all(mysql):
    # create customers table
    customers = '''CREATE TABLE IF NOT EXISTS customers (
    ID int NOT NULL AUTO_INCREMENT,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255) NOT NULL,
    Email varchar(255) NOT NULL,
    Phone varchar(255) NOT NULL,
    Birthday DATE,
    Address varchar(255),
    City varchar(255),
    PRIMARY KEY (ID),
    CONSTRAINT UC_Customer UNIQUE (Email, Phone)
    )
    '''

    # create vehicles types table
    vehicles_types = '''CREATE TABLE IF NOT EXISTS vehicles_types (
    ID int NOT NULL AUTO_INCREMENT,
    Name varchar(255) NOT NULL,
    MaxPassengers int NOT NULL,
    PRIMARY KEY (ID),
    CONSTRAINT UC_Customer UNIQUE (Name)
    )
    '''

    # create vehicles table
    vehicles = '''CREATE TABLE IF NOT EXISTS vehicles (
    ID int NOT NULL AUTO_INCREMENT,
    Make varchar(255) NOT NULL,
    Model varchar(255) NOT NULL,
    Year int NOT NULL,
    Color varchar(255) NOT NULL,
    Plate varchar(255) NOT NULL,
    TypeId int NOT NULL,
    DayPrice int NOT NULL,
    PRIMARY KEY (ID),
    CONSTRAINT UC_Customer UNIQUE (Plate),
    FOREIGN KEY (TypeId) REFERENCES vehicles_types(ID)
    )
    '''

    # create bookings table
    bookings = '''CREATE TABLE IF NOT EXISTS bookings (
    ID int NOT NULL AUTO_INCREMENT,
    VehicleId int NOT NULL,
    CustomerId int NOT NULL,
    Created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Created_by varchar(255) NOT NULL,
    HireDate DATE NOT NULL,
    ReturnDate DATE NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (VehicleId) REFERENCES vehicles(ID),
    FOREIGN KEY (CustomerId) REFERENCES customers(ID)
    )
    '''

    # create invoices table
    invoices = '''CREATE TABLE IF NOT EXISTS invoices (
    ID int NOT NULL AUTO_INCREMENT,
    VehicleId int NOT NULL,
    CustomerId int NOT NULL,
    Duration int NOT NULL,
    Price int NOT NULL,
    ReceivedDate TIMESTAMP NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (VehicleId) REFERENCES vehicles(ID),
    FOREIGN KEY (CustomerId) REFERENCES customers(ID)
    )
    '''
    db_execute(mysql, [ customers, vehicles_types, vehicles, bookings, invoices ])
