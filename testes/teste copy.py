from partes import partes
import pandas as pd
import os
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.request import urlopen


chrome = Chrome(ChromeDriverManager().install())
chrome.get('https://processo.stj.jus.br/processo/pesquisa/')
chrome.find_element(By.CSS_SELECTOR, '#idParteNome').send_keys('WHIRLPOOL')
chrome.find_element(By.CSS_SELECTOR, '#idBotaoPesquisarFormularioExtendido').click()
chrome.find_element(By.CSS_SELECTOR, '.clsLinhaPessoa:nth-child(11) .clsPessoaNome').click()

chrome.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)  # posicao onde acaba os processo
sleep(.5)
chrome.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)

chrome.find_element(By.CSS_SELECTOR, '#idDivBlocoPaginacaoBase > div > span > span.classSpanPaginacaoImagensDireita > a:nth-child(1)').click()
chrome.find_element(By.CSS_SELECTOR, '#idDivBlocoPaginacaoBase > div > span > span.classSpanPaginacaoImagensDireita > a:nth-child(1)').click()
chrome.find_element(By.CSS_SELECTOR, '#idDivBlocoPaginacaoBase > div > span > span.classSpanPaginacaoImagensDireita > a:nth-child(1)').click()

# voltando para clicar no proximo registro do registro
chrome.back()
chrome.back()
chrome.back()
chrome.back()
chrome.refresh()
print(len(chrome.find_elements(By.CSS_SELECTOR, '.clsPessoa ')))