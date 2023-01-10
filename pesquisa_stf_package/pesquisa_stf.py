import pandas as pd
import time
import os
from partes import partes
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


class RoboStf:
    os.system('cls' if os.name == 'nt' else 'clear')  # clear the Terminal
    
    def __init__(self, url='https://portal.stf.jus.br/', maximizar=False):
        """
        url='https://portal.stf.jus.br/' -> Vái para o site do STF
        maximizar=True => vai deixar o navegador em tela cheia
        """
        if maximizar == True:
            self.driver_path = ChromeDriverManager().install()
            self.chrome = Chrome(self.driver_path)
            self.chrome.maximize_window()
            self.get = self.chrome.get(url)
            self.wdw = WebDriverWait(driver=self.chrome, timeout=10)
        else:
            self.driver_path = ChromeDriverManager().install()
            self.chrome = Chrome(self.driver_path)
            self.get = self.chrome.get(url)
            self.wdw = WebDriverWait(driver=self.chrome, timeout=10)

    def url_pag_inicial_processos(self):
        return self.chrome.current_url
            
    def espera_elemento_disponivel_e_clica(self, locator: tuple):
        # espera o item estar disponível quando disponível JA ENTRA NELE
        self.wdw.until(EC.element_to_be_clickable(locator))
        # clica no elemento
        self.chrome.find_element(*locator).click()
    
    def espera_elemento(self, locator: tuple):
        return self.wdw.until(EC.element_to_be_clickable(locator))
    
    def espera_elemento_e_envia_send_keys(self, string, locator: tuple):
        # espera o item estar disponível quando disponível JA ENTRA NELE
        self.wdw.until(EC.element_to_be_clickable(locator))
        # Envia string para o elemento
        self.chrome.find_element(*locator).send_keys(string)
    
    def pesquisa_stf(self):
        if len(partes) >= 1:
            for parte in partes:
                url = 'https://portal.stf.jus.br/'
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f'\n\n\033[0;31mPegando informações do site: STF - SUPREMO TRIBUNAL FEDERAL\n'
                    f'{url}\033[m')
                print(f'\n\nParte à pegar: \033[0;32m{parte}\033[m')
                self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#pesquisa-principal > div.col-md-12.col-xs-12.col-sm-12.pesquisa-processo.aba-pesquisa > select > option:nth-child(4)'))
                self.espera_elemento((By.CSS_SELECTOR, '#pesquisa-principal > div.col-md-12.col-xs-12.col-sm-12.pesquisa-processo.aba-pesquisa > select > option:nth-child(4)'))
                self.espera_elemento_e_envia_send_keys(string=parte, locator=(By.CSS_SELECTOR, '#pesquisaPrincipalParteAdvogado'))
                self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#btnPesquisar'))
                self.chrome.maximize_window()
                
                url_pag_inicial_processos = self.url_pag_inicial_processos()
                self.espera_elemento((By.CSS_SELECTOR, '#texto-pagina-interna > div > div > div.lista-processo-parte > div:nth-child(1) > h5'))
                print(self.chrome.find_element(By.CSS_SELECTOR, '#texto-pagina-interna > div > div > div.lista-processo-parte > div:nth-child(1) > h5').text, f'\n\n')
                self.espera_elemento((By.CSS_SELECTOR, '#quantidade'))
                qtd_processos = self.chrome.find_element(By.CSS_SELECTOR, '#quantidade').text
                qtd_processos = int(qtd_processos)
                
                def envia_validador_para_mudar_pagina():
                    self.wdw.until(EC.element_to_be_clickable(locator=(By.CSS_SELECTOR, "#item-proxima-pagina")))
                    return self.chrome.find_element(By.CSS_SELECTOR, "#item-proxima-pagina").get_attribute('class')
                
                if qtd_processos >= 1:
                    try:
                        def pega_colunas():
                            print(f'\n\nRecuperando colunas para fazer o arquivo \033[0;33m.csv\033[m da parte: \033[0;32m{parte}\033[m\n')
                            print('\033[1;33mEspere um momento...\033[m')
                            self.espera_elemento((By.CSS_SELECTOR,'th'))
                            pega_colunas_selen = self.chrome.find_elements(By.CSS_SELECTOR,'th')
                            pega_colunas_list = []
                            
                            for coluna in pega_colunas_selen:
                                pega_colunas_list.append(coluna.text.upper())
                            else:
                                return pega_colunas_list
                    except Exception as erro:
                        print(erro)
                        self.chrome.refresh()
                        colunas = pega_colunas()

                        
                    try:
                        def pega_identificacao():
                            '''COMO PEGA O QUE TERÁ EM TODAS AS PÁGINAS, NÁO PRECISA DE VALIDADOR PARA MUDAR DE PÁGINA'''
                            print('\n\nRecuperando informações de \033[0;32mIdentificação\033[m: \n\033[0;32m EX: AAA 0000000\033[m\n')
                            print('\033[1;33mEspere um momento...\033[m')

                            self.espera_elemento((By.CSS_SELECTOR, '#tabela_processos a'))
                            pega_id_cels_selen = self.chrome.find_elements(By.CSS_SELECTOR, '#tabela_processos a')
                            pega_id_cels_list = []
                            validador = envia_validador_para_mudar_pagina()
                            
                            while validador != 'disabled' or qtd_processos != len(pega_id_cels_list):
                                for item in pega_id_cels_selen:
                                    pega_id_cels_list.append(item.text)
                                else:
                                    self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#paginacao-proxima-pagina'))
                                    validador = envia_validador_para_mudar_pagina()
                                    self.espera_elemento((By.CSS_SELECTOR, '#tabela_processos a'))
                                    pega_id_cels_selen = self.chrome.find_elements(By.CSS_SELECTOR, '#tabela_processos a')
                            else:
                                self.chrome.get(url_pag_inicial_processos)
                                validador = envia_validador_para_mudar_pagina()
                                return pega_id_cels_list
                    except Exception as erro:
                        print(erro)
                        self.chrome.refresh()
                        identificacao = pega_colunas()

                    try:
                        def pega_partes_name():
                            print('\n\nRecuperando informações de \033[0;32mNome Das Partes\033[m: \n\033[0;32m EX: PARTE S.A\033[m')
                            print('\033[1;33mEspere um momento...\033[m')
                            
                            self.espera_elemento((By.CSS_SELECTOR, 'td:nth-child(2)'))
                            pega_nomes_partes_selen = self.chrome.find_elements(By.CSS_SELECTOR, 'td:nth-child(2)')
                            pega_nomes_partes_list = []
                            validador = envia_validador_para_mudar_pagina()
                            
                            while validador != 'disabled' or qtd_processos != len(pega_nomes_partes_list):
                                for item in pega_nomes_partes_selen:
                                    pega_nomes_partes_list.append(item.text)
                                else:
                                    self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#paginacao-proxima-pagina'))
                                    validador = envia_validador_para_mudar_pagina()
                                    self.espera_elemento((By.CSS_SELECTOR, 'td:nth-child(2)'))
                                    pega_nomes_partes_selen = self.chrome.find_elements(By.CSS_SELECTOR, 'td:nth-child(2)')
                            else:
                                self.chrome.get(url_pag_inicial_processos)
                                validador = envia_validador_para_mudar_pagina()
                                return pega_nomes_partes_list
                    except Exception as erro:
                        print(erro)
                        self.chrome.refresh()
                        partes_name = pega_colunas()
                    
                    try:
                        def pega_num_unico():
                            print('\n\nRecuperando informações de \033[0;32mNúmero Único\033[m: '
                                '\n\033[0;32m EX: 0000000-00.0000.0.00.0000 / Sem Número Único\033[m')
                            print('\033[1;33mEspere um momento...\033[m')
                            self.espera_elemento((By.CSS_SELECTOR, 'td:nth-child(3)'))
                            pega_num_unic_cels_selen = self.chrome.find_elements(By.CSS_SELECTOR, 'td:nth-child(3)')
                            pega_num_unic_cels_list = []                        
                            validador = envia_validador_para_mudar_pagina()
                            
                            while validador != 'disabled' or qtd_processos != len(pega_num_unic_cels_list):
                                for item in pega_num_unic_cels_selen:
                                    pega_num_unic_cels_list.append(item.text)
                                else:
                                    self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#paginacao-proxima-pagina'))
                                    validador = envia_validador_para_mudar_pagina()
                                    self.espera_elemento((By.CSS_SELECTOR, 'td:nth-child(3)'))
                                    pega_num_unic_cels_selen = self.chrome.find_elements(By.CSS_SELECTOR, 'td:nth-child(3)')
                            else:
                                self.chrome.get(url_pag_inicial_processos)
                                validador = envia_validador_para_mudar_pagina()
                                return pega_num_unic_cels_list
                    except Exception as erro:
                        print(erro)
                        self.chrome.refresh()
                        num_unico = pega_colunas()

                    try:
                        def pega_data_atuacao():
                            print('\n\nRecuperando informações de \033[0;32mData Autuação\033[m: '
                                '\n\033[0;32m EX: 23/03/1933\033[m')
                            print('\033[1;33mEspere um momento...\033[m')
                            self.espera_elemento((By.CSS_SELECTOR, 'td:nth-child(4)'))
                            pega_data_autuacao_selen = self.chrome.find_elements(By.CSS_SELECTOR, 'td:nth-child(4)')
                            pega_data_autuacao = []
                            validador = envia_validador_para_mudar_pagina()

                            while validador != 'disabled' or len(pega_data_autuacao) != qtd_processos:
                                for data in pega_data_autuacao_selen:
                                    pega_data_autuacao.append(data.text)
                                else:
                                    self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#paginacao-proxima-pagina'))
                                    validador = envia_validador_para_mudar_pagina()
                                    self.espera_elemento((By.CSS_SELECTOR, 'td:nth-child(4)'))
                                    pega_data_autuacao_selen = self.chrome.find_elements(By.CSS_SELECTOR, 'td:nth-child(4)')

                            else:
                                self.chrome.get(url_pag_inicial_processos)
                                validador = envia_validador_para_mudar_pagina()
                                return pega_data_autuacao
                    except Exception as erro:
                        print(erro)
                        self.chrome.refresh()
                        data_autuacao = pega_colunas()
                        
                    try:    
                        def pega_meio():
                            print('\n\nRecuperando informações de \033[0;32mMeio\033[m: '
                                '\n\033[0;32m EX: Eletrônico / Físico\033[m')
                            print('\033[1;33mEspere um momento...\033[m')
                            self.espera_elemento((By.CSS_SELECTOR, 'td:nth-child(5)'))
                            pega_meio_selen = self.chrome.find_elements(By.CSS_SELECTOR, 'td:nth-child(5)')
                            pega_meio = []
                            validador = envia_validador_para_mudar_pagina()
                            
                            while validador != 'disabled' or len(pega_meio) != qtd_processos:
                                for meio in pega_meio_selen:
                                    pega_meio.append(meio.text)
                                else:
                                    self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#paginacao-proxima-pagina'))
                                    validador = envia_validador_para_mudar_pagina()
                                    self.espera_elemento((By.CSS_SELECTOR, 'td:nth-child(5)'))
                                    pega_meio_selen = self.chrome.find_elements(By.CSS_SELECTOR, 'td:nth-child(5)')
                                    
                            else:
                                self.chrome.get(url_pag_inicial_processos)
                                validador = envia_validador_para_mudar_pagina()
                                return pega_meio
                    except Exception as erro:
                        print(erro)
                        self.chrome.refresh()
                        meio = pega_colunas()
                    
                    try:
                        def pega_publicidade():
                            print('\n\nRecuperando informações de \033[0;32mPublicidade\033[m: '
                                '\n\033[0;32m EX: Público\033[m')
                            print('\033[1;33mEspere um momento...\033[m')
                            self.espera_elemento((By.CSS_SELECTOR, 'td:nth-child(6)'))
                            pega_publicidade_selen = self.chrome.find_elements(By.CSS_SELECTOR, 'td:nth-child(6)')
                            pega_publicidade = []
                            validador = envia_validador_para_mudar_pagina()
                            
                            while validador != 'disabled' or len(pega_publicidade) != qtd_processos:
                                for publicidade in pega_publicidade_selen:
                                    pega_publicidade.append(publicidade.text)
                                else:
                                    self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#paginacao-proxima-pagina'))
                                    validador = envia_validador_para_mudar_pagina()
                                    self.espera_elemento((By.CSS_SELECTOR, 'td:nth-child(6)'))
                                    pega_publicidade_selen = self.chrome.find_elements(By.CSS_SELECTOR, 'td:nth-child(6)')
                            else:
                                self.chrome.get(url_pag_inicial_processos)
                                validador = envia_validador_para_mudar_pagina()
                                return pega_publicidade
                    except Exception as erro:
                        print(erro)
                        self.chrome.refresh()
                        publicidade = pega_colunas()
                    
                    try:
                        def pega_tramite():
                            print('\n\nRecuperando informações de \033[0;32mTrâmite\033[m: '
                                '\n\033[0;32m EX: Sim/Não\033[m')
                            print('\033[1;33mEspere um momento...\033[m')
                            self.espera_elemento((By.CSS_SELECTOR, 'td:nth-child(7)'))
                            pega_tramite_selen = self.chrome.find_elements(By.CSS_SELECTOR, 'td:nth-child(7)')
                            pega_tramite = []
                            validador = envia_validador_para_mudar_pagina()

                            while validador != 'disabled' or  len(pega_tramite) != qtd_processos:
                                for tramite in pega_tramite_selen:
                                    pega_tramite.append(tramite.text)
                                else:
                                    self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#paginacao-proxima-pagina'))
                                    validador = envia_validador_para_mudar_pagina()
                                    self.espera_elemento((By.CSS_SELECTOR, 'td:nth-child(7)'))
                                    pega_tramite_selen = self.chrome.find_elements(By.CSS_SELECTOR, 'td:nth-child(7)')
                            else:
                                self.chrome.get(url_pag_inicial_processos)
                                validador = envia_validador_para_mudar_pagina()
                                return pega_tramite
                    except Exception as erro:
                        print(erro)
                        self.chrome.refresh()
                        tramite = pega_colunas()

                    colunas = pega_colunas()
                    identificacao = pega_identificacao()
                    partes_name = pega_partes_name()
                    num_unico = pega_num_unico()
                    data_autuacao = pega_data_atuacao()
                    meio = pega_meio()
                    publicidade = pega_publicidade()
                    tramite = pega_tramite()
                    print('\n\nFazendo arquivo \033[0;32m.csv\033[m da parte \033[0;32m{parte}\033[m: ')
                    print(f'Localização do arquivo: DOWNLOADS/STF - SUPREMO TRIBUNAL FEDERAL/PARTES/{parte.upper()}/DADOS PRIMÁRIOS\n')
                    print('\033[1;33mEspere um momento...\033[m')
                    dados = {colunas[0]: identificacao, colunas[1]: partes_name, colunas[2]: num_unico, colunas[3]: data_autuacao, colunas[4]: meio, colunas[5]: publicidade, colunas[6]: tramite}
                    # pega_colunas [0 -> 'IDENTIFICAÇÃO', 1 -> 'PARTE', 2 -> 'NÚMERO ÚNICO', 3 -> 'DATA AUTUAÇÃO', 4 -> 'MEIO', 5 -> 'PUBLICIDADE', -> 6 'TRÂMITE']
                    
                    df = pd.DataFrame(dados)

                    # verifica se existem diretorios, senão, cria e loogo dps o pandas coloca o arq csv
                    parte = parte.replace('/', '-')
                    if not os.path.exists(f'DOWNLOADS/STF - SUPREMO TRIBUNAL FEDERAL/PARTES/{parte.upper()}/DADOS PRIMÁRIOS'):
                        os.makedirs(f'DOWNLOADS/STF - SUPREMO TRIBUNAL FEDERAL/PARTES/{parte.upper()}/DADOS PRIMÁRIOS/')
                        df.to_csv(f'DOWNLOADS/STF - SUPREMO TRIBUNAL FEDERAL/PARTES/{parte.upper()}/DADOS PRIMÁRIOS/{parte.upper()}.csv', index=False)
                        sleep(1)
                    else:
                        df.to_csv(f'DOWNLOADS/STF - SUPREMO TRIBUNAL FEDERAL/PARTES/{parte.upper()}/DADOS PRIMÁRIOS/{parte.upper()}.csv', index=False)
                        sleep(1)
                else:
                    print(f'Não existe processos atualmente nessa parte: \033[0;32m{parte}\033[m\n\n')
        
    def print_finalizado(self):
        print(f'\n\n\033[0;31m === O ROBÔ FINALIZOU AS CONSULTAS DE {len(partes)} PARTES === \033[m\n\n')
        
