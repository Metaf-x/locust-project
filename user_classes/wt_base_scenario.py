from locust import task, SequentialTaskSet, HttpUser, FastHttpUser, constant_pacing, events
from config.config import cfg, logger
import sys, re
from utils.assertion import check_http_response
from utils.non_test_methods import open_csv_field
import random

COMMON_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate'
}

class PurchaseFlightTicket(SequentialTaskSet):

    test_users_csv_file_path = './test_data/user_data_test.csv'

    def on_start(self) -> None:

        @task
        def uc_01_getHomePage(self) -> None:

            self.test_users_data = open_csv_field(self.test_users_csv_file_path)

            self.client.get(
                '/WebTours/',
                name='REQ_01_1_/WebTours/',
                headers=COMMON_HEADERS,
                #debug_stream=sys.stderr
            )

            self.client.get(
                '/cgi-bin/welcome.pl?signOff=true',
                name='REQ_01_2_/cgi-bin/welcome.pl?signOff=true',
                headers=COMMON_HEADERS,
                allow_redirects=False,
                #debug_stream=sys.stderr
            )

            with self.client.get(
                '/cgi-bin/nav.pl?in=home',
                name='REQ_01_3_/cgi-bin/nav.pl?in=home',
                headers=COMMON_HEADERS,
                allow_redirects=False,
                catch_response=True,
                # debug_stream=sys.stderr
            ) as req_01_3_response:
                check_http_response(req_01_3_response, "name=\"userSession\"")
            self.userSession = re.search(r'name=\"userSession\" value=\"(.*)\"/>', req_01_3_response.text).group(1)

        @task
        def uc_01_getLogin(self) -> None:

            self.user_data_row = random.choice(self.test_users_data)

            userName = self.user_data_row['username']
            password = self.user_data_row['password']
            req_body_02_01 = f"userSession={self.userSession}&username={userName}&password={password}&login.x=0&login.y=0&JSFormSubmit=off"

            with self.client.post(
                '/cgi-bin/login.pl',
                name='REQ_02_1_/cgi-bin/login.pl',
                headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'content-type': 'application/x-www-form-urlencoded'
                },
                data=req_body_02_01,
                    catch_response=True,
                # debug_stream=sys.stderr
            ) as req_02_1_response:
                check_http_response(req_02_1_response, "User password was correct")

            with self.client.get(
                '/cgi-bin/login.pl?intro=true',
                name='REQ_02_2_/cgi-bin/login.pl?intro=true',
                headers=COMMON_HEADERS,
                # debug_stream=sys.stderr
            ) as req_02_2_response:
                check_http_response(req_02_2_response, f"Welcome, <b>{userName}</b>")

        @task
        def uc_01_getLogout(self) -> None:

            self.client.get(
                '/cgi-bin/welcome.pl?signOff=1',
                name='REQ_03_1_/cgi-bin/welcome.pl?signOff=1',
                headers=COMMON_HEADERS,
            )

            self.client.get(
                '/cgi-bin/nav.pl?in=home',
                name='REQ_03_2_/cgi-bin/cgi-bin/nav.pl?in=home',
                headers=COMMON_HEADERS,
            )

        uc_01_getHomePage(self)
        uc_01_getLogin(self)
        uc_01_getLogout(self)

    @task
    def fixTest(self):
        pass

class WebToursBaseUserClass(FastHttpUser):
    wait_time = constant_pacing(cfg.pacing)
    host = cfg.url

    logger.info(f'WebToursBaseClass started. Host: {host}')
    tasks = [PurchaseFlightTicket]