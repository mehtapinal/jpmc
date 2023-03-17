import socket
import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple
from flask import Flask, request, abort, render_template
from constants import LOCAL_HOST, DOCKER_HOST, PORT_8000, PORT_8080

class Loggerator:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('logs.db', check_same_thread=False)
        self.c = self.conn.cursor()

    def schema_setup(self) -> None:
        # Create table "logs"
        # Drop table logs to avoid duplicate data
        self.c.execute("drop table if exists logs")
        self.c.execute('''CREATE TABLE IF NOT EXISTS logs
                         (ip text, user text, date text, method text, url text, code text)''')

        self.conn.commit()

    def receive_logs_from_loggertor(self) -> None:
        client_socket = socket.socket()
        try:
            # Try to connect to the Docker host at host.docker.internal
            client_socket.connect((DOCKER_HOST, PORT_8080))
        except socket.gaierror:
            # If running locally, try to connect to 0.0.0.0
            client_socket.connect((LOCAL_HOST, PORT_8080))

        # Continuously receive data from the socket
        while True:
            data = client_socket.recv(1024).decode()
            # If no more data is received, break out of the loop
            if not data:
                break

            # Parse the received data and store the logs
            self.parse_logs(data.splitlines())

        client_socket.close()

    def parse_logs(self, lines: List[str]) -> None:
        # Loop through each log line in the list
        for line in lines:
            # Split the line into separate fields
            fields = line.split()

            # Check that the line has the expected number of fields
            if len(fields) == 11:
                # Extract relevant fields from the line
                remote_host = fields[0]
                remote_user = fields[2]
                timestamp = fields[3].lstrip('[') + ' ' + fields[4]
                timestamp = datetime.strptime(timestamp, '%d/%b/%Y %H:%M:%S')
                request_path = fields[7]
                request_method = fields[6].strip('"').lower()
                response_code = int(fields[9])

                # Insert the extracted fields into the SQLite database
                self.c.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?, ?)",
                               (remote_host, remote_user, timestamp, request_method, request_path, response_code))
                self.conn.commit()

    def get_count(self):
        val = self.c.execute("select * from logs")
        print(f"ds: {val.fetchall()}")

    def get_logs_request_builder(self, code: Optional[str] = None, method: Optional[str] = None,
                                 user: Optional[str] = None) \
            -> List[Tuple[str, str, str, str, str, str]]:
        query = 'SELECT * FROM logs'
        conditions = []
        if code:
            conditions.append(f'code = "{code}"')
        if method:
            conditions.append(f'method = "{method}"')
        if user:
            conditions.append(f'user = "{user}"')
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        query += ' ORDER BY date DESC'

        print(query)

        self.c.execute(query)
        results = self.c.fetchall()
        return results  # json.dumps(results, indent=4)


app = Flask(__name__)
loggerator = Loggerator()


@app.route('/logs', methods=['GET'])
def get_logs_request():
    """
    This function handles GET requests to the '/logs'
    """
    code = request.args.get('code')
    method = request.args.get('method')
    user = request.args.get('user')

    # TODO set pagination for better api response time

    # Validate query parameters
    valid_params = ['code', 'method', 'user']
    for key in request.args:
        if key not in valid_params:
            abort(400, f"Invalid query parameter: {key}")
    try:
        # Call the get_logs_request_builder method
        return loggerator.get_logs_request_builder(code, method, user)
    except Exception as e:
        # Catch exception if any
        abort(500, f"Internal app error: {e}")


@app.route('/', methods=['GET'])
def home_route():

    return render_template('home.html')


if __name__ == '__main__':
    loggerator.schema_setup()
    loggerator.receive_logs_from_loggertor()
    app.run(host=LOCAL_HOST, port=PORT_8000, debug=True)
