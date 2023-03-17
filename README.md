# Loggerator
This is a Flask app that receives logs from a remote server and stores them in an SQLite database. 
It also provides a REST API to query the logs based on different criteria.

## Requirements
Python 3
Flask
SQLite3
unittest

## Installation
Clone the repository: git clone https://github.com/yourusername/loggerator.git
Install dependencies: `pip install -r requirements.txt`
Run the app: `python app.py`

## Usage
### Receiving logs
The app expects logs to be sent to it via a socket connection. To simulate this, you can run the following command:


If we run with default setting(without count params) it will take about 10 mins to populate 800K records. 
To test the app quickly
bash
`docker run -p 8080:8080 gcr.io/hiring-278615/loggerator --count 500`

### Query Parameters
The /logs endpoint accepts the following query parameters:

code: HTTP response code (e.g. 200, 404, 500).
method: HTTP request method (e.g. GET, POST, PUT).
user: User who made the request.
These parameters are optional and can be combined in any way.

#### Example Usage

To get all logs, send a GET request to http://localhost:8000/logs.
To get all logs with response code 200, send a GET request to http://localhost:8000/logs?code=200.
To get all logs with response code 200 and request method POST, send a GET request to http://localhost:8000/logs?code=200&method=post.
To get all logs made by a user with username "jondoe", send a GET request to http://localhost:8000/logs?user=jondoe.


## Note
The schema_setup method drops the table logs if already exists and creates a new table with columns (ip, user, date, method, url, code).
parse_logs method gets the logs sent via a socket connection, parse each line and store the necessary information in the logs table.
get_count method prints the count of total logs stored in the database.
The Flask app runs on http://localhost:5000 by default.

In production schema changes will be handeled by db migrations

## Limitations:
The current code logic is like a PHASE 1 and covers basic functions mentioned in the assesement. 
If needed we can improve on following limitation that it currently has:

* The app is designed to handle a single socket connection at a time. If multiple Loggerator services are sending logs simultaneously, the app may not be able to handle the load.
* The app is not currently designed to handle large volumes of logs. If the database becomes too large, it may slow down or crash the app.
* The app does not currently support pagination, which may lead to slow response times for large numbers of logs.
* The app does not include any authentication or security features, which may make it vulnerable to attacks.

## Future Improvements:
* Pagination: As the amount of log data grows, it could become difficult to handle large amounts of data in a single response. Implementing pagination would allow users to retrieve logs in smaller, more manageable chunks.

* Filtering by date range: Currently, the app only allows filtering by user, code, and HTTP method. Adding the ability to filter by date range would be useful for users who need to retrieve logs from a specific time period.

* Authentication and authorization: Currently, there is no authentication or authorization mechanism in place. Adding user authentication and access control would help to prevent unauthorized access to the logs.

* Real-time updates: Currently, the app only retrieves logs from the loggertor server when it starts up. Adding the ability to receive real-time updates as new logs are generated would be a useful feature.

* Scalability: If the amount of log data continues to grow, it may become necessary to scale the app horizontally across multiple servers. Implementing a load balancer and/or caching layer could help to improve performance and ensure high availability.