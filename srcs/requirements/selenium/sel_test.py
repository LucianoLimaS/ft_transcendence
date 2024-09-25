from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Configurando o WebDriver para o Selenium Server
driver = webdriver.Remote(
    command_executor='http://selenium:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME
)

# Exemplo de operação com o WebDriver
driver.get("http://app:8001")  # Acessa sua aplicação

print(driver.title)  # Imprime o título da página

driver.quit()  # Fecha o navegador
