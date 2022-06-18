# Car Hire managment system

## Project Description
This is a web application where client can make car rental reservations for customers and do CRUD operations on customers, vehicles, bookings, invoices and vehicles types
## Getting Started

### Installing Dependencies

#### Python 3.10

Install the latest version of python for your platform.

#### Virtual Environment

working within a virtual environment keeps dependencies for the project separate and organized.

#### PIP Dependencies

Once we have your virtual environment setup and running, install dependencies by running:
```bash
pip install -r requirements.txt
```

This will install all of the required packages
##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [Flask-mysqldb](https://flask-mysqldb.readthedocs.io/en/latest/) is the Python DBAPI that handle mysql db connection. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
create your own database using mysql use name 'car_hire' or change the MYSQL_DB in models.py with your db name

## Running the server

From within the `\` directory first ensure you are working using your created virtual environment.
```bash
python -m venv venv
venv\Scripts\activate
pip install requirements
```
First import our app to flask, execute:
```bash
$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "true"
$env:FLASK_CONFIG = "instance"
```
To run the server, execute:

```bash
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `__init__.py` file in flaskr folder.
## Tests:
### Postman
- Go to url `https://web.postman.co/`
- login and open workspace
- upload Crocosoft postman collection from `/Crocosoft.postman_collection.json`
- test each endpoint with your data.

## API References

### Getting Started

##### Base URL: 
Currently hosted locally at http://127.0.0.1:5000/.

### Error Handling:

Errors are returned as JSON objects in the following format:
```bash
{
    "success": False,
    "error": 400,
    "message": "Bad Request!!!! Please make sure the data you entered is correct"
}
```
The API will return error types when requests fail, example:
```bash
400: Bad Request
404: Resource Not Found
422: Not Processable
405: Method Not Allowed
```
### Endpoints
#### customer end points.

##### GET '/customers'

- Function:get customer by id
- Requested Arguments: customer id
- Returns an object with query result

##### POST '/customers'

- Function: create new customer
- Requested Arguments: lastname, firstname, email, phone are essential, birthday, address, city are optional
- Returns an object with success, custom message

##### PATCH '/customers/<int:customer_id>'

- Function: update customer data
- Requested Arguments: customer_id, and any field needs updating but at least one must be given 
- Returns an object with success, custom message
- 
##### DELETE '/customers/<int:customer_id>'

- Function: delete customer
- Requested Arguments: customer_id
- Returns an object with success, custom message