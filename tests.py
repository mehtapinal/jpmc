import unittest
import datetime
from app import app, Loggerator

loggerator = Loggerator()


class TestLogs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        loggerator.schema_setup()

        cls.logs = [
            '127.0.0.1 - frank [10/Oct/2000 13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326',
            '127.0.0.1 - berries [10/Jan/2008 13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 400 2326',
            '127.0.0.1 - mango [12/Mar/2013 13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 404 2326',
            '127.0.0.1 - lemon [1/Jul/2016 13:55:36 -0700] "post /apache_pb.gif HTTP/1.0" 301 2326',
            '127.0.0.1 - jackson [10/Dec/2018 13:55:36 -0700] "post /apache_pb.gif HTTP/1.0" 404 2326',
            '127.0.0.1 - test [10/Oct/2020 13:55:36 -0700] "get /apache_pb.gif HTTP/1.0" 404 2326',
            '127.0.0.1 - - [10/Oct/2000 13:55:36 -0700] "post /missing.gif HTTP/1.0" 404 296'
        ]
        loggerator.parse_logs(cls.logs)

    def test_schema_setup(self):
        """
        Validate schemas are created as expected
        """
        loggerator.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs'")
        result = loggerator.c.fetchone()
        self.assertIsNotNone(result)

    def test_get_all_logs_request(self):
        # test getting logs with no query parameters returns all logs
        response = app.test_client().get('/logs')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # loggerator.c.execute("SELECT * FROM logs")
        # loggerator.conn.commit()
        # result = loggerator.c.fetchall()
        # print(result)

        self.assertEqual(len(data), 7)

    def test_get_logs_request_with_params(self):
        """Test that the get_logs_request function correctly filters logs based on multiple query parameters.
        """
        # test getting logs with query parameters
        response = app.test_client().get('/logs?code=404&method=get')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)

    def test_get_logs_request_with_code_param(self):
        """Test that the get_logs_request function correctly filters logs based on multiple query parameters.
        """
        # test getting logs with query parameters
        response = app.test_client().get('/logs?code=404')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 4)

    def test_get_logs_request_with_method_param(self):
        """Test that the get_logs_request function correctly filters logs based on multiple query parameters.
        """
        # test getting logs with query parameters
        response = app.test_client().get('/logs?method=post')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 3)

    def test_get_logs_request_with_user_param(self):
        """Test that the get_logs_request function correctly filters logs based on multiple query parameters.
        """
        # test getting logs with query parameters
        response = app.test_client().get('/logs?user=jackson')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # print((data[3]))
        # self.assertEqual(data[0][1] == 'jackson')
        self.assertEqual(len(data), 1)

    def test_bad_request(self):
        """
        test bad request returns 400
        """
        response = app.test_client().get('/logs?bad=request')
        self.assertEqual(response.status_code, 400)

    def test_parse_logs(self):
        """
        Test logs are pasrsed as expected
        """
        # ensure that the parse_logs function correctly extracts data from log lines
        loggerator.c.execute("SELECT * FROM logs")
        data = loggerator.c.fetchall()
        self.assertEqual(len(data), 7)
        self.assertEqual(data[0][0], '127.0.0.1')
        self.assertEqual(data[0][1], 'frank')
        self.assertIsInstance(datetime.datetime.strptime(data[0][2], '%Y-%m-%d %H:%M:%S'), datetime.datetime)
        self.assertEqual(data[0][3], 'get')
        self.assertEqual(data[0][4], '/apache_pb.gif')
        self.assertEqual(data[0][5], '200')

    def test_malformed_date(self):
        """
        Test that the parse_logs function correctly handles log lines with malformed timestamp
        """
        log = ['127.0.0.1 - frank [bad_date 13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326']
        with self.assertRaises(ValueError):
            loggerator.parse_logs(log)

    def test_date_sorted_desc(self):
        """
        Test that the parse_logs correctly returns as DATE desc
        """
        response = app.test_client().get('/logs')
        self.assertEqual(response.status_code, 200)
        results = response.get_json()
        # Verify that the first row corresponds to the date string '10/Oct/2008 13:55:36 -0700'
        expected_date_str = '2020-10-10 13:55:36'
        # expected_date = datetime.datetime.strptime(expected_date_str, '%d/%b/%Y %H:%M:%S')
        # actual_date_str = results[0][2]
        # print(actual_date_str)
        # actual_date = datetime.datetime.strptime(actual_date_str, '%Y-%m-%d %H:%M:%S')
        self.assertEqual(expected_date_str, results[0][2])
        # assert actual_date == expected_date, f"Expected date {expected_date} does not match actual date {actual_date}"

    @classmethod
    def tearDownClass(cls):
        # close the in-memory database and delete it
        loggerator.c.execute("drop table if exists logs")
        loggerator.conn.commit()


if __name__ == '__main__':

    unittest.main()
