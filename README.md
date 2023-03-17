# Log App Server
This is a Flask app that receives logs from a remote server and stores them in an SQLite database. 
It also provides a REST API to query the logs based on different criteria.

## Tech Stack
* Python 3
* Flask
* SQLite3
* unittest

## Usage
### Receiving logs
*** Be sure, to have the loggerater container running on PORT 8080 *** 
This app expects to listen to logs via a socket connection. To simulate this, you can run the following command:
`docker run -p 8080:8080 gcr.io/hiring-278615/loggerator --count 500`

#### Note: 
If we run with default setting(without count params) it will take about 10 mins to populate 800K records. 
To test the app quickly
bash
`docker run -p 8080:8080 gcr.io/hiring-278615/loggerator --count 500`

## Installation
### Local Setup
1. Clone the repository: `git clone https://github.com/mehtapinal/jpmc.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`

### Docker Setup
1. Clone the repository: `git clone https://github.com/mehtapinal/jpmc.git`
    cd projects
2. Build the Docker image
    `docker build -t log-app-server .`
3. Run the Docker image
    `docker run -p 8000:8000 --name log-app-server log-app-server`

## Testing:
To run  unit tests: `pytest test.py`

### Query Parameters
The /logs endpoint accepts the following query parameters:

* code (optional): The code associated with the log.
* method (optional): The method associated with the log.
* user (optional): The user associated with the log.
* page (optional, default=1): The page number of the logs to return.
* limit (optional, default=50): The number of logs to return per page.

#### Example Usage

* To retrieve all logs, send a GET request to http://localhost:8000/logs.
* To retrieve all logs with response code 200, send a GET request to http://localhost:8000/logs?code=200.
* To retrieve all logs with response code 200 and request method POST, send a GET request to http://localhost:8000/logs?code=200&method=post.
* To retrieve all logs made by a user with username "jondoe", send a GET request to http://localhost:8000/logs?user=jondoe.
* To retrieve all logs with different limit/page, send a GET request to http://localhost:8000/logs?limit=300&page=2


## Design Architecture:
This app consists of a Flask-based web application that receives and logs web server access logs. It parses logs received from a separate logging service and stores them in a SQLite database.
The schema_setup method drops the table logs if already exists and creates a new table with columns (ip, user, date, method, url, code).
parse_logs method gets the logs sent via a socket connection, parse each line and store the necessary information in the logs table.

Pagination: As the amount of log data grows, it could become difficult to handle large amounts of data in a single response. 
Implementing pagination would allow users to retrieve logs in smaller, more manageable chunks.


## Limitations:
The current code logic is like a PHASE 1 and covers basic functions mentioned in the assesement. 
If needed we can improve on following limitation that it currently has:

* The app is designed to handle a single socket connection at a time. If multiple Loggerator services are sending logs simultaneously, the app may not be able to handle the load.
* The app is not currently designed to handle large volumes of logs. If the database becomes too large, it may slow down or crash the app.
* The app currently uses sqllite as its database which has limited scalability. The reason for my choice: It fits the current MVP/needs and don't want to over-engineer it.
* The app does not currently support pagination, which may lead to slow response times for large numbers of logs.
* The app does not include any authentication or security features, which may make it vulnerable to attacks.

## Future Improvements:
* Filtering by date range: Currently, the app only allows filtering by user, code, and HTTP method. Adding the ability to filter by date range would be useful for users who need to retrieve logs from a specific time period.
* Authentication and authorization: Currently, there is no authentication or authorization mechanism in place. Adding user authentication and access control would help to prevent unauthorized access to the logs.
* Real-time updates: Currently, the app only retrieves logs from the loggertor server when it starts up. Adding the ability to receive real-time updates as new logs are generated would be a useful feature.
* Scalability: If the amount of log data continues to grow, it may become necessary to scale the app horizontally across multiple servers. Implementing a load balancer and/or caching layer could help to improve performance and ensure high availability.
