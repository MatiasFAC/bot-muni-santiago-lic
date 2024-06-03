import os
from time import sleep
from loguru import logger

env_main_web = os.environ.get('MAIN_WEB', 'https://tramites.munistgo.cl/reservahoralicencia/')
env_rut = os.environ.get('RUT', '19773246-6')
env_get_msg = os.environ.get('GET_MSG', 'http://api/msg/')
env_time_refresh_seconds = os.environ.get('TIME_REFRESH_SECONDS', '15')
env_selenium_server = os.environ.get('SELENIUM_SERVER', 'http://127.0.0.1:4444/wd/hub')
env = os.environ.get('ENV', 'prod') # prod, dev, test


### Var Web fullxpath
web_digite_su_rut = "/html/body/div/div/div[2]/div[2]/div[1]/div/div[3]/form/input"
web_ingresar = "/html/body/div/div/div[2]/div[2]/div[1]/div/div[3]/form/button"
web_reservar_licencia = "/html/body/form/div[4]/div[1]/div[2]/div[2]/div/div/div[3]/div[1]/div/div/div/div/table/tbody/tr[2]/td[2]/input"
web_modal_no_hay_horas = "/html/body/form/div[4]/div[2]/div/div"


def env_validations() -> None:
    global env_time_refresh_seconds

    logger.debug(f"env_main_web:             {env_main_web}")
    logger.debug(f"env_rut:                  {env_rut}")
    logger.debug(f"env_get_msg:              {env_get_msg}")
    logger.debug(f"env_time_refresh_seconds: {env_time_refresh_seconds}")
    logger.debug(f"env:                      {env}")
    
    try: # env_time_refresh_seconds
        numero = int(env_time_refresh_seconds)
        if numero > 0:
            
            env_time_refresh_seconds = numero
        else:
            logger.error("Invalid TIME_REFRESH_SECONDS has to be greater than 0. env_time_refresh_seconds not set.")
            exit(1)
    except ValueError:
        logger.error("Invalid TIME_REFRESH_SECONDS provided. env_time_refresh_seconds not set.")
        exit(1)

    if env not in ['prod', 'dev', 'test']:
        logger.error("Invalid ENV provided. env not set.")
        exit(1)


def loguro_config() -> None:
    if env == 'prod':
        logger.add("./log/{time:YYYY-MM-DD}.log", rotation="250 MB", level="WARNING")
    else:
        logger.add("./log/{time:YYYY-MM-DD}.log", rotation="250 MB", level="DEBUG")
    # logger.debug("This is a debug message")
    # logger.info("This is an info message")
    # logger.success("This is a success message")
    # logger.warning("This is a warning message")
    # logger.error("This is an error message")


def bot() -> bool:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import NoSuchElementException


    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # no graphical interface
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        if env == 'dev':
            service = Service("./chromedriver.exe")
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            driver = webdriver.Remote(command_executor=env_selenium_server, options=chrome_options)
        
        driver.get(env_main_web)

        # logger.debug(driver.title)
    except Exception as e:
        logger.error(f"Error creating driver. {e}")
        return False



    

    # Send RUT to input
    for i in range(3):
        try:
            element = driver.find_element(By.XPATH, web_digite_su_rut)
            element.send_keys(env_rut)
            break
        except NoSuchElementException:
            logger.warning(f"Element web_digite_su_rut not found. Try=N°{i+1}")
            if i == 2:
                logger.error("Element web_digite_su_rut not found.")
                driver.quit()
                return False
            sleep(0.5)
    
    # Click on Ingresar
    for i in range(3):
        try:
            element = driver.find_element(By.XPATH, web_ingresar)
            element.click()
            break
        except NoSuchElementException:
            logger.warning(f"Element web_ingresar not found. Try=N°{i+1}")
            if i == 2:
                logger.error("Element web_ingresar not found.")
                driver.quit()
                return False
            sleep(0.5)

    # Click on Reservar Licencia
    for i in range(3):
        try:
            element = driver.find_element(By.XPATH, web_reservar_licencia)
            element.click()
            break
        except NoSuchElementException:
            logger.warning(f"Element web_reservar_licencia not found. Try=N°{i+1}")
            if i == 2:
                logger.error("Element web_reservar_licencia not found.")
                driver.quit()
                return False
            sleep(0.5)
    
    # Check if there are no hours
    sleep(1)
    url_modal = driver.current_url
    logger.debug(url_modal)
    index = url_modal.find('Error=No%20existen%20horas%20disponibles')

    if index != -1:
        driver.quit()
        return False

    driver.quit()
    return True


def get_msg() -> None:
    import requests

    logger.info(f"Sending message to {env_get_msg}.")
    try:
        requests.get(env_get_msg, params={'msg', 'https://tramites.munistgo.cl/reservahoralicencia/'})
    except Exception as e:
        logger.error(f"Error sending message to {env_get_msg}. {e}")


def main():
    if bot():
        logger.success("Bot executed successfully")
        get_msg()
    else:
        logger.error("Bot failed")


if __name__ == '__main__':
    loguro_config()
    env_validations()
    

    if env == 'prod':
        while True:
            main()
            sleep(int(env_time_refresh_seconds))
    else:
        main()