import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from time import sleep


url = 'https://processo.stj.jus.br/processo/pesquisa/'
s = Service(ChromeDriverManager().install())
options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome = Chrome(service=s, chrome_options=options)
chrome.maximize_window()
get = chrome.get(url)
wdw = WebDriverWait(driver=chrome, timeout=10, poll_frequency=0.5)
def espera_enquanto_nao_tem_resposta_do_site(driver, wdw, locator : tuple):
    """Essa função tentará recarregar a página em até 3 vezes esperando pelo elemento"""
    try:
        element = wdw.until(EC.element_to_be_clickable(locator))
        if element:
            return element
    except TimeoutException:
        print('Talvez a página tenha dado algum erro, vou atualiza-lá')
        sleep(2)
        try:
            driver.refresh()
            element = wdw.until(EC.element_to_be_clickable(locator))
            if element:
                print('Voltou!')
                return element
        except TimeoutException:
            print('A página ainda não voltou, vou atualiza-lá')
            sleep(2)
            try:
                driver.refresh()
                element = wdw.until(EC.element_to_be_clickable(locator))
                if element:
                    print('Voltou!')
                    return element
            except TimeoutException:
                print('Poxa, essa será a última vez que vou atualizar a página...')
                sleep(2)
                try:
                    driver.refresh()
                    element = wdw.until(EC.element_to_be_clickable(locator))
                    if element:
                        print('Voltou!')
                        return element
                except TimeoutException:
                    print("Olha, não foi possível. A página provavelmente caiu feio :(")
                    print("Infelizmente o programa vai ser finalizado...")
                    driver.quit()
        
        
espera_enquanto_nao_tem_resposta_do_site(chrome, wdw, (By.CSS_SELECTOR, 'h2'))
sleep(15)
espera_enquanto_nao_tem_resposta_do_site(chrome, wdw, (By.CSS_SELECTOR, 'h2'))