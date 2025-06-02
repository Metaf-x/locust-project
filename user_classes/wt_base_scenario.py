from locust import task, SequentialTaskSet, HttpUser, constant_pacing, events
from config.config import cfg, logger


class PurchaseFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)
    @task
    def uc_00_getHomePage(self) -> None:
        r00_01_response = self.client.get(
            '/WebTours/',
            name='REQ_00_0_getHtml',
            headers={
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate'
            }
        )
        print(r00_01_response.status_code)
        print(r00_01_response.text)

class WebToursBaseUserClass(HttpUser): # юзер-класс, принимающий в себя основные параметры теста
    wait_time = constant_pacing(cfg.pacing)
    host = cfg.url

    logger.info(f'WebToursBaseClass started. Host: {host}')
    tasks = [PurchaseFlightTicket]