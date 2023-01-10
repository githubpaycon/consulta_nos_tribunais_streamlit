from partes import partes
import pandas as pd
import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from functions_selenium import *
from time import sleep


os.system('clear')

driver_path = ChromeDriverManager().install()
chrome = Chrome(driver_path)
get = chrome.get('https://consultaprocessual.tst.jus.br/consultaProcessual')
wdw = WebDriverWait(driver=chrome, timeout=60)


if len(partes) >= 1:
    for parte in partes:
        url = 'https://consultaprocessual.tst.jus.br/consultaProcessual/consultaTstNumUnica.do?consulta=Consultar&conscsjt=&numeroTst=&digitoTst=&anoTst=&orgaoTst=5&tribunalTst=&varaTst='
        import os
        print(f'\n\n\033[0;31mPegando informações do site: TST - TRIBUNAL SUPERIOR DO TRABALHO\n'
            f'{url}\033[m')
        print(f'\n\nParte à pegar: \033[0;32m{parte}\033[m')
        
        # aceita os cookies
        # espera_elemento_disponivel_e_clica(driver=chrome, wdw=wdw, locator=(By.CSS_SELECTOR, '#portlet_com_liferay_iframe_web_portlet_IFramePortlet_INSTANCE_KgY5 > div > div.portlet-content-container > div > div > div > p > a'))

        try:
            def executa():
                espera_elemento_estar_na_tela_para_clicar(driver=chrome, wdw=wdw, locator=(By.CSS_SELECTOR, '#empregadorForm\:nomParte'))
                espera_elemento_e_envia_send_keys(driver=chrome, wdw=wdw, locator=(By.CSS_SELECTOR, '#empregadorForm\:nomParte'), string=parte)
                espera_elemento_disponivel_e_clica(driver=chrome, wdw=wdw, locator=(By.CSS_SELECTOR, 'body > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(9) > td > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > input:nth-child(2)'))
                
                # verifica se existe paginacao
                paginacao = espera_e_retorna_elemento_text(chrome, wdw, (By.CSS_SELECTOR, '.pagebanner'))
                
                # se mostra todos os itens na tela
                if 'exibindo todos itens' in paginacao:
                    
                    # recupera n unico processo -> #processo [href^="resumo"]
                    ancoras_n_processos = espera_e_retorna_lista_de_elementos(chrome, wdw, (By.CSS_SELECTOR, '#processo [href^="resumo"]'))

                    for ancora in range(len(ancoras_n_processos)):
                        chrome.implicitly_wait(1)
                        n_unico = ancoras_n_processos[ancora].text
                        ancoras_n_processos[ancora].click()
                        
                        def faz_csv_dados_processo(parte, n_unico):
                            
                            # espera pelo elemento que mais demora
                            espera_por_varios_elementos(chrome, wdw, (By.CSS_SELECTOR, 'img'))
                            
                            colunas = espera_e_retorna_lista_de_elementos_text(chrome, wdw, (By.CSS_SELECTOR, '.dadosProcesso b'))
                            colunas_tratadas = [coluna.split(':')[0] for coluna in colunas]
                            cont = 1
                            colunas_para_csv = []
                            for coluna in colunas_tratadas:
                                colunas_para_csv.append(f'{coluna} col{cont}')
                                cont += 1
                            dados = espera_e_retorna_lista_de_elementos_text(chrome, wdw, (By.CSS_SELECTOR, '.dadosProcesso+ .dadosProcesso , .dadosProcesso font'))

                            print(colunas_para_csv)
                            print()
                            print(dados)
                            
                        def faz_csv_historico_processo(parte, n_unico):
                            # espera pelo elemento que mais demora
                            espera_por_varios_elementos(chrome, wdw, (By.CSS_SELECTOR, 'img'))
                            data = espera_e_retorna_lista_de_elementos_text(chrome, wdw, (By.CSS_SELECTOR, '.historicoProcesso > font'))
                            print(data)
                            dados = espera_e_retorna_lista_de_elementos_text(chrome, wdw, (By.CSS_SELECTOR, '.historicoProcesso .historicoProcesso td font'))
                            print(dados)
                            
                        faz_csv_dados_processo(parte, n_unico)
                        faz_csv_historico_processo(parte, n_unico)
                        
                        chrome.back()
                        chrome.refresh()
                        ancoras_n_processos = espera_e_retorna_lista_de_elementos(chrome, wdw, (By.CSS_SELECTOR, '#processo [href^="resumo"]'))
            executa()        
        except Exception:
            chrome.refresh()
            executa()
            if not os.path.exists(f'erros'):
                os.makedirs(f'erros')
                chrome.save_screenshot('erros/erro.png')
                chrome.quit()
            else:
                chrome.save_screenshot('erros/erro.png')
                chrome.quit()
            print('\n\n\033[0;31mO ROBÔ FOI FINALIZADO PREMATURAMENTE!\n\nMOSTRE O ARQUIVO: erros.log NA PASTA erros AO DESENVOLVEDOR\033[m\n\n')
            quit()
        
