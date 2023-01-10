from logging import exception
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

class RoboStj:
    os.system('clear')
    def __init__(self, url='https://consultaprocessual.tst.jus.br/consultaProcessual/', headless='2'):
        """
        url='https://consultaprocessual.tst.jus.br/consultaProcessual/' -> Vái para o site do TST (CONSULTA PROCESSUAL)
        headless = 1 -> não mostra o navegador
        """
        if headless == '1':
            self.url = url
            self.driver_path = ChromeDriverManager().install()
            self.options = ChromeOptions()
            self.options.add_argument("--headless")
            self.options.add_argument("user-data-dir=selenium")
            self.chrome = Chrome(self.driver_path, chrome_options=self.options)
            self.chrome.maximize_window()
            self.get = self.chrome.get(url)
            self.wdw = WebDriverWait(driver=self.chrome, timeout=30)
        elif headless == '2':
            self.url = url
            self.driver_path = ChromeDriverManager().install()
            self.chrome = Chrome(self.driver_path)
            self.get = self.chrome.get(url)
            self.wdw = WebDriverWait(driver=self.chrome, timeout=60)
        else:
            self.url = url
            self.driver_path = ChromeDriverManager().install()
            self.chrome = Chrome(self.driver_path)
            self.get = self.chrome.get(url)
            self.wdw = WebDriverWait(driver=self.chrome, timeout=60)

    
    
    ###############################################################################
    ############↓#######↓######### RECUPERA DADOS DO SITE #######↓###########↓#####
    ###############################################################################
    
    
 
    def pesquisa_stj(self):
        if len(partes) >= 1:
            for parte in partes:
                import os
                print(f'\n\n\033[0;31mPegando informações do site: TST - TRIBUNAL SUPERIOR DO TRABALHO\n'
                    f'{self.url}\033[m')
                print(f'\n\nParte à pegar: \033[0;32m{parte}\033[m')

                try:
                    def executa():
                        espera_elemento_estar_na_tela_para_clicar(driver=self.chrome, wdw=self.wdw, locator=(By.CSS_SELECTOR, '#empregadorForm\:nomParte'))
                        espera_elemento_e_envia_send_keys(driver=self.chrome, wdw=self.wdw, locator=(By.CSS_SELECTOR, '#empregadorForm\:nomParte'), string=parte)
                        espera_elemento_disponivel_e_clica(driver=self.chrome, wdw=self.wdw, locator=(By.CSS_SELECTOR, 'body > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(9) > td > form > table > tbody > tr:nth-child(2) > td:nth-child(2) > input:nth-child(2)'))
                        
                        # verifica se existe paginacao
                        paginacao = espera_e_retorna_elemento_text(self.chrome, self.wdw, (By.CSS_SELECTOR, '.pagebanner'))
                        
                        # se mostra todos os itens na tela
                        if 'exibindo todos itens' in paginacao:
                            
                            # recupera n unico processo -> #processo [href^="resumo"]
                            ancoras_n_processos = espera_e_retorna_lista_de_elementos(self.chrome, self.wdw, (By.CSS_SELECTOR, '#processo [href^="resumo"]'))
                            try:
                                def pega_dados_ancoras():
                                    for ancora in range(len(ancoras_n_processos)):
                                        self.chrome.implicitly_wait(1)
                                        n_unico = ancoras_n_processos[ancora].text
                                        ancoras_n_processos[ancora].click()
                                        
                                        def faz_csv_dados_processo(parte, n_unico):
                                            
                                            # espera pelo elemento que mais demora
                                            espera_por_varios_elementos(self.chrome, self.wdw, (By.CSS_SELECTOR, 'img'))
                                            
                                            colunas = espera_e_retorna_lista_de_elementos_text(self.chrome, self.wdw, (By.CSS_SELECTOR, '.dadosProcesso b'))
                                            colunas_tratadas = [coluna.split(':')[0] for coluna in colunas]
                                            cont = 1
                                            colunas_para_csv = []
                                            for coluna in colunas_tratadas:
                                                colunas_para_csv.append(f'{coluna} col{cont}')
                                                cont += 1
                                            dados = espera_e_retorna_lista_de_elementos_text(self.chrome, self.wdw, (By.CSS_SELECTOR, '.dadosProcesso+ .dadosProcesso , .dadosProcesso font'))

                                            df = pd.DataFrame([dados], columns=colunas_para_csv)
                
                                            parte = parte.replace('/', '-')
                                            if not os.path.exists(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/'):
                                                os.makedirs(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/')
                                                df.to_csv(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/dados_fundamentais.csv', index=False)
                                            else:
                                                df.to_csv(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/dados_fundamentais.csv', index=False)
            
                                        def faz_csv_historico_processo(parte, n_unico):
                                            # espera pelo elemento que mais demora
                                            espera_por_varios_elementos(self.chrome, self.wdw, (By.CSS_SELECTOR, 'img'))
                                            data = espera_e_retorna_lista_de_elementos_text(self.chrome, self.wdw, (By.CSS_SELECTOR, '.historicoProcesso > font'))
                                            dados = espera_e_retorna_lista_de_elementos_text(self.chrome, self.wdw, (By.CSS_SELECTOR, '.historicoProcesso .historicoProcesso td font'))

                                            csv_structure = {'DATA': data, 'HISTÓRICO' : dados}
                                            df = pd.DataFrame(csv_structure)
                
                                            parte = parte.replace('/', '-')
                                            if not os.path.exists(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/'):
                                                os.makedirs(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/')
                                                df.to_csv(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/histórico do processo.csv', index=False)
                                            else:
                                                df.to_csv(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/histórico do processo.csv', index=False)
                                            
                                            
                                        faz_csv_dados_processo(parte, n_unico)
                                        faz_csv_historico_processo(parte, n_unico)
                                        
                                        self.chrome.back()
                                        self.chrome.refresh()
                                        ancoras_n_processos = espera_e_retorna_lista_de_elementos(self.chrome, self.wdw, (By.CSS_SELECTOR, '#processo [href^="resumo"]'))
                                    else:
                                        self.chrome.get(self.url)
                                pega_dados_ancoras()
                            except Exception:
                                self.chrome.refresh()
                                pega_dados_ancoras()
                        # caso tenha paginacao (tenha processos para muitas pages) não mostrará (exibindo todos itens)
                        else:
                            # pegando paginacao
                            lista_de_ancoras_paginacao = espera_e_retorna_lista_de_elementos(self.chrome, self.wdw, (By.CSS_SELECTOR, '.pagelinks a'))
                            btn_prox = ''
                            for a in lista_de_ancoras_paginacao:
                                if a.text == 'Próxima':
                                    btn_prox = a

                            try:
                                def pega_dados_ancoras_paginada():
                                    for ancora in range(len(ancoras_n_processos)):
                                        self.chrome.implicitly_wait(1)
                                        n_unico = ancoras_n_processos[ancora].text
                                        ancoras_n_processos[ancora].click()
                                        
                                        def faz_csv_dados_processo(parte, n_unico):
                                            
                                            # espera pelo elemento que mais demora
                                            espera_por_varios_elementos(self.chrome, self.wdw, (By.CSS_SELECTOR, 'img'))
                                            
                                            colunas = espera_e_retorna_lista_de_elementos_text(self.chrome, self.wdw, (By.CSS_SELECTOR, '.dadosProcesso b'))
                                            colunas_tratadas = [coluna.split(':')[0] for coluna in colunas]
                                            cont = 1
                                            colunas_para_csv = []
                                            for coluna in colunas_tratadas:
                                                colunas_para_csv.append(f'{coluna} col{cont}')
                                                cont += 1
                                            dados = espera_e_retorna_lista_de_elementos_text(self.chrome, self.wdw, (By.CSS_SELECTOR, '.dadosProcesso+ .dadosProcesso , .dadosProcesso font'))

                                            df = pd.DataFrame([dados], columns=colunas_para_csv)
                
                                            parte = parte.replace('/', '-')
                                            if not os.path.exists(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/'):
                                                os.makedirs(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/')
                                                df.to_csv(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/dados_fundamentais.csv', index=False)
                                            else:
                                                df.to_csv(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/dados_fundamentais.csv', index=False)
            
                                            
                                        def faz_csv_historico_processo(parte, n_unico):
                                            # espera pelo elemento que mais demora
                                            espera_por_varios_elementos(self.chrome, self.wdw, (By.CSS_SELECTOR, 'img'))
                                            data = espera_e_retorna_lista_de_elementos_text(self.chrome, self.wdw, (By.CSS_SELECTOR, '.historicoProcesso > font'))
                                            dados = espera_e_retorna_lista_de_elementos_text(self.chrome, self.wdw, (By.CSS_SELECTOR, '.historicoProcesso .historicoProcesso td font'))

                                            csv_structure = {'DATA': data, 'HISTÓRICO' : dados}
                                            df = pd.DataFrame(csv_structure)
                
                                            parte = parte.replace('/', '-')
                                            if not os.path.exists(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/'):
                                                os.makedirs(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/')
                                                df.to_csv(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/histórico do processo.csv', index=False)
                                            else:
                                                df.to_csv(f'DOWNLOADS/TST - TRIBUNAL SUPERIOR DO TRABALHO/PARTES/SISTEMA ANTIGO/{parte.upper()}/{n_unico}/DADOS/histórico do processo.csv', index=False)
                                            
                                            
                                        faz_csv_dados_processo(parte, n_unico)
                                        faz_csv_historico_processo(parte, n_unico)
                                        
                                        self.chrome.back()
                                        self.chrome.refresh()
                                        ancoras_n_processos = espera_e_retorna_lista_de_elementos(self.chrome, self.wdw, (By.CSS_SELECTOR, '#processo [href^="resumo"]'))
                                    else:
                                        # depois que esgotar as ancoras desse site...
                                        if btn_prox:
                                            btn_prox.click()
                                            self.chrome.refresh()
                                            ancoras_n_processos = espera_e_retorna_lista_de_elementos(self.chrome, self.wdw, (By.CSS_SELECTOR, '#processo [href^="resumo"]'))
                                        else:
                                            self.chrome.get(self.url)
                                pega_dados_ancoras_paginada()
                            except Exception:
                                self.chrome.refresh()
                                pega_dados_ancoras_paginada()
                    executa()        
                except Exception:
                    self.chrome.refresh()
                    executa()
                    # if not os.path.exists(f'erros'):
                    #     os.makedirs(f'erros')
                    #     self.chrome.save_screenshot('erros/erro.png')
                    #     self.chrome.quit()
                    # else:
                    #     self.chrome.save_screenshot('erros/erro.png')
                    #     self.chrome.quit()
                    # print('\n\n\033[0;31mO ROBÔ FOI FINALIZADO PREMATURAMENTE!\n\nMOSTRE O ARQUIVO: erros.log NA PASTA erros AO DESENVOLVEDOR\033[m\n\n')
                    # quit()
         
    def caso_de_erro(self, falha):
        import os
        if not os.path.exists(f'erros'):
            os.makedirs(f'erros')
            with open('erros/erros.log', 'a+') as file:
                file.write(falha)
            sleep(1)
        else:
            with open('erros/erros.log', 'a+') as file:
                file.write(str(falha))
                sleep(1)
        print('\n\n\033[0;31mO ROBÔ FOI FINALIZADO PREMATURAMENTE!\n\nMOSTRE O ARQUIVO: erros.log NA PASTA erros AO DESENVOLVEDOR\033[m\n\n')
        quit()
        
    def print_finalizado(self):
        print(f'\n\n\033[0;31m === O ROBÔ FINALIZOU AS CONSULTAS DE {len(partes)} PARTES === \033[m\n\n')

if __name__ == '__main__':     
    executa = RoboStj()
    executa.pesquisa_stj()