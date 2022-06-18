from flask_cors import CORS
import dateutil.parser
import babel
from flask import Flask, jsonify, abort, request
from models import setup_db, db_create_all, db_execute, db_select


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # initiate CORS
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # initiate mysql connection
    mysql = setup_db(app)

    # db initialization
    with app.app_context():
        db_create_all(mysql)

    # ----------------------------------------------------------------------------#
    # Filters.
    # ----------------------------------------------------------------------------#

    def format_datetime(value, format='medium'):
        if isinstance(value, str):
            date = dateutil.parser.parse(value)
        else:
            date = value

        if format == 'full':
            format = "EEEE MMMM, d, y 'at' h:mma"
        elif format == 'medium':
            format = "EE MM, dd, y h:mma"
        return babel.dates.format_datetime(date, format, locale='en')

    app.jinja_env.filters[ 'datetime' ] = format_datetime

    # ----------------------------------------------------------------------------#
    # Controllers.
    # ----------------------------------------------------------------------------#

    # Check if server and database is running for testing purpose only
    @app.route('/check', methods=[ 'GET' ])
    def server_check():
        try:
            return jsonify({
                'success': True,
                'message': 'Server running',
            })
        except Exception as e:
            print(e)
            abort(400)

    # add new customer, this API requires body with firstname, lastname, email, phone
    # and optional birthday, address, City.
    @app.route('/customers/', methods=[ 'POST' ])
    def add_customer():
        body = request.get_json()
        firstname = body.get('firstname', None)
        lastname = body.get('lastname', None)
        email = body.get('email', None)
        phone = body.get('email', None)
        birthday = body.get('birthday', None)
        address = body.get('address', None)
        city = body.get('city', None)
        if firstname and lastname and email and phone:
            add_customer_query = f'''insert into customers 
            (LastName, FirstName, Email, Phone, Birthday, Address, City) 
            VALUES ({lastname}, {firstname}, {email}, {phone}, {birthday}, {address}, {city},)
            '''
            try:
                with app.app_context():
                    result = db_execute(mysql, add_customer_query)
                    if result.success:
                        return {
                            'success': True,
                            'message': 'Customer Added Successfully'
                        }
                    else:
                        return {
                            'success': False,
                            'message': 'Failed To Add Customer, Check Data And Try Again'
                        }
            except Exception as e:
                print(e)
                return {
                    'success': False,
                    'message': e,
                }

    # update customer
    @app.route('/customers/<int:customer_id>', methods=[ 'PATCH' ])
    def update_customer(customer_id):
        pass

    # update customer
    @app.route('/customers/<int:customer_id>', methods=[ 'DELETE' ])
    def delete_customer(customer_id):
        pass

    # get customer by id
    @app.route('/customers/<int:customer_id>', methods=[ 'GET' ])
    def get_customer(customer_id):
        customer_query = f'''SELECT * FROM customers where ID = {customer_id}'''
        print(customer_query)
        try:
            with app.app_context():
                data = db_select(mysql, customer_query)
            if data[ 'results' ]:
                return jsonify(data)
            else:
                return jsonify({
                    'success': False,
                    'message': 'No Record Found',
                })
        except Exception as e:
            print(e)
            abort(400)

    # ----------------------------------------------------------------------------#
    # Error Handlers.
    # ----------------------------------------------------------------------------#
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": 'Not found!!! : please check your Data or maybe your request is currently not available.'
        }), 404

    @app.errorhandler(422)
    def not_processable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'Unprocessable!!! : The request was well-formed but was unable to be followed'
        }), 422

    @app.errorhandler(405)
    def not_allowed_method(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method Not Allowed!!!: Your request method not supported by that API '
        }), 405

    @app.errorhandler(400)
    def not_good_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request!!!! Please make sure the data you entered is correct'
        }), 400

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error!!!: Please try again later or reload request. '
        }), 500

    return app
