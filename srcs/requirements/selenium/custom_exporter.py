import os
import logging
from prometheus_client import start_http_server, Summary, Counter
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import requests

# Desativando a telemetria do Selenium
os.environ["SELENIUM_REMOTE_SESSION_ID"] = ""

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Métricas
REQUEST_TIME = Summary('selenium_test_duration_seconds', 'Duration of Selenium tests')
TESTS_RUN = Counter('selenium_tests_run_total', 'Total number of Selenium tests run')
TESTS_FAILED = Counter('selenium_tests_failed_total', 'Total number of Selenium tests failed')

@REQUEST_TIME.time()
def run_selenium_test():
    """Executa um teste com Selenium e coleta métricas."""
    TESTS_RUN.inc()
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')

        driver = webdriver.Chrome(options=options)
        driver.get('http://localhost:4444')  # Acesse a interface do Selenium Grid
        logging.info(f"Title of the page: {driver.title}")

        if "Selenium Grid" not in driver.title:
            logging.error("Título da página não corresponde ao esperado.")
            TESTS_FAILED.inc()

    except WebDriverException as e:
        logging.error(f"Error occurred: {e}")
        TESTS_FAILED.inc()
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        TESTS_FAILED.inc()
    finally:
        if driver is not None:
            driver.quit()

if __name__ == '__main__':
    logging.info("Iniciando o servidor de métricas...")
    start_http_server(8003, addr='0.0.0.0')
    logging.info("Servidor de métricas disponível em http://localhost:8003")

    try:
        while True:
            run_selenium_test()
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Encerrando o servidor de métricas...")
