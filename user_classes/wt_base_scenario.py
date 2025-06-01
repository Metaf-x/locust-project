from locust import task, SequentialTaskSet, HttpUser, constant_pacing, events
from config.config import cfg, logger


class PurchaseFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)
    @task()
    def uc_00_getHomePage(self) -> None:
        pass 

class WebToursBaseUserClass(HttpUser): # юзер-класс, принимающий в себя основные параметры теста
    wait_time = constant_pacing(5)
    host = 'URL тестируемого приложения из переменных среды'

    tasks = [PurchaseFlightTicket]