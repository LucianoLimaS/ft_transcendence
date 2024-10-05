#!/usr/bin/env python3

from prometheus_client import start_http_server, Summary, Counter
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

# Métrica do tempo de execução dos testes
REQUEST_TIME = Summary('selenium_test_duration_seconds', 'Duration of Selenium tests')
# Contador de testes realizados
TESTS_RUN = Counter('selenium_tests_run_total', 'Total number of Selenium tests run')
# Contador de falhas nos testes
TESTS_FAILED = Counter('selenium_tests_failed_total', 'Total number of Selenium tests failed')

@REQUEST_TIME.time()
def run_selenium_test():
    TESTS_RUN.inc()  # Incrementa o contador de testes realizados
    driver = None  # Inicializa a variável driver
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Executar sem interface gráfica
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Conectar ao Selenium Grid na porta 4444
        driver = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            options=options
        )
        
        driver.set_page_load_timeout(10)  # Timeout para carregar a página
        driver.get('http://nginx:80')  # Ajuste a URL se necessário
        time.sleep(5)  # Simulação de tempo de teste
    except WebDriverException as e:
        print(f"Error occurred: {e}")
        TESTS_FAILED.inc()  # Incrementa o contador de falhas
    finally:
        if driver is not None:  # Verifica se o driver foi inicializado
            driver.quit()

if __name__ == '__main__':
    print("Iniciando o exporter...")
    start_http_server(8003, addr='0.0.0.0')
    print("Servidor de métricas disponível em http://localhost:8003")
    while True:
        run_selenium_test()
        time.sleep(10)  # Intervalo entre os testes
