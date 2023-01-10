import pandas as pd
import time
import os
from partes import partes
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

class RoboStfPegaDadosIndentificacao:
    os.system('cls' if os.name == 'nt' else 'clear')  # clear the Terminal
    
    def __init__(self, url='https://portal.stf.jus.br/', maximizar=False):
        """
        url='https://portal.stf.jus.br/' -> Vái para o site do STF
        maximizar=True => vai deixar o navegador em tela cheia
        """
        
        if maximizar == True:
            self.driver_path = ChromeDriverManager().install()
            self.chrome = Chrome(executable_path=self.driver_path)
            self.chrome.maximize_window()
            self.get = self.chrome.get(url)
            self.wdw = WebDriverWait(driver=self.chrome, timeout=60)

        else:
            self.driver_path = ChromeDriverManager().install()
            self.chrome = Chrome(executable_path=self.driver_path)
            self.get = self.chrome.get(url)
            self.wdw = WebDriverWait(driver=self.chrome, timeout=60)


    def url_pag_inicial_processos(self):
        return self.chrome.current_url
            
    def espera_elemento_disponivel_e_clica(self, locator: tuple):
        # espera o item estar disponível quando disponível JA ENTRA NELE
        self.wdw.until(EC.element_to_be_clickable(locator))
        # clica no elemento
        self.chrome.find_element(*locator).click()

    def espera_elemento_e_envia_send_keys(self, string, locator: tuple):
        # espera o item estar disponível quando disponível JA ENTRA NELE
        self.wdw.until(EC.element_to_be_clickable(locator))
        # Envia string para o elemento
        self.chrome.find_element(*locator).send_keys(string)
    
    def espera_elemento(self, locator: tuple):
        return self.wdw.until(EC.element_to_be_clickable(locator))
    
    def abre_pagina_muda_e_pesquisa_pelo_href(self, href : str):
        # abre uma aba em branco
        self.chrome.execute_script('window.open()')
        
        # verifica se abriu x numeros de janelas
        self.wdw.until(EC.number_of_windows_to_be(2))
        
        # pega todas as janelas
        windows = self.chrome.window_handles
        
        # muda para a ultima janela
        self.chrome.switch_to.window(windows[-1])
        
        # envia o seu href para essa nova janela
        self.chrome.get(href)
        
            
    def pega_dados_identificacao(self):
        def execucao_interna():
            try:
                if len(partes) >= 1:
                    for parte in partes:
                        import os
                        url='https://portal.stf.jus.br/'
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f'\n\n\033[0;31mPegando dados da IDENTIFICAÇÃO do site: STF - SUPREMO TRIBUNAL FEDERAL\n'
                            f'{url}\033[m')
                        print(f'\n\nParte à pegar: \033[0;32m{parte}\033[m')
                        self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#pesquisa-principal > div.col-md-12.col-xs-12.col-sm-12.pesquisa-processo.aba-pesquisa > select > option:nth-child(4)'))
                        self.espera_elemento((By.CSS_SELECTOR, '#pesquisa-principal > div.col-md-12.col-xs-12.col-sm-12.pesquisa-processo.aba-pesquisa > select > option:nth-child(4)'))
                        self.espera_elemento_e_envia_send_keys(string=parte, locator=(By.CSS_SELECTOR, '#pesquisaPrincipalParteAdvogado'))
                        self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#btnPesquisar'))
                        self.chrome.maximize_window()
                        self.espera_elemento((By.CSS_SELECTOR, '#texto-pagina-interna > div > div > div.lista-processo-parte > div:nth-child(1) > h5'))
                        print(self.chrome.find_element(By.CSS_SELECTOR, '#texto-pagina-interna > div > div > div.lista-processo-parte > div:nth-child(1) > h5').text, f'\n\n')
                        
                        self.espera_elemento((By.CSS_SELECTOR, '#quantidade'))
                        qtd_processos = self.chrome.find_element(By.CSS_SELECTOR, '#quantidade').text
                        qtd_processos = int(qtd_processos)
                        
                        def envia_validador_para_mudar_pagina():
                            self.wdw.until(EC.element_to_be_clickable(locator=(By.CSS_SELECTOR, "#item-proxima-pagina")))
                            return self.chrome.find_element(By.CSS_SELECTOR, "#item-proxima-pagina").get_attribute('class')
                        
                        if qtd_processos >= 1:
                            print('\n\nRecuperando informações de \033[0;32mIDENTIFICAÇÃO\033[m: ')
                            print('\033[1;33mEspere um momento...\033[m')
                            
                            # recebe o validador -> '' ou 'disabled'
                            validador = envia_validador_para_mudar_pagina()
                            
                            # contador para mudar de pagina quando finalizar os 20
                            ancoras_recuperadas = 0
                            
                            # nome da identificacao -> REA13412
                            id_para_csv = ''
                            
                            # Espera as ancoras aparecerem
                            self.espera_elemento((By.CSS_SELECTOR, '#tabela_processos a'))
                            
                            # recupera todas as ancoras de id
                            identificacoes_ancoras = self.chrome.find_elements(By.CSS_SELECTOR, '#tabela_processos a')
                            
                            # enquanto o validador (que pode ser '' ou 'disabled') for != de 'disabled'
                            # ou enquanto a quantidade de ancoras recuperadas for != da qtd_processos...
                            while validador != 'disabled' or ancoras_recuperadas != qtd_processos:
                                
                                # para cada ancora (int) nas quantidades de ancoras
                                for id_posit in range(len(identificacoes_ancoras)):
                                    
                                    # recupera o id para salvar o csv
                                    id_para_csv = identificacoes_ancoras[id_posit].text
                                    
                                    # da um tab para mover a tela até o elemento para recuperar (gambi)
                                    identificacoes_ancoras[id_posit].send_keys(Keys.TAB)
                                    
                                    # clica no id
                                    identificacoes_ancoras[id_posit].click()
                                    
                                    try:
                                        def tipo_processo_dados_csv1():
                                            # recurso extraordinario ...
                                            self.espera_elemento((By.CSS_SELECTOR, '#descricao-procedencia'))  # espera pela origem (elemento que mais demora)
                                            dados_csv1 = self.chrome.find_elements(By.CSS_SELECTOR, '.p-l-16')
                                            
                                            print('\n\nRecuperando: \033[0;32mTIPO DE PROCESSO\033[m')
                                            tipo_do_processo = dados_csv1[0].text
                                            
                                            print('\n\nRecuperando: \033[0;32mORIGEM DO PROCESSO\033[m')
                                            origem_do_processo = dados_csv1[1].text

                                            print('\n\nRecuperando: \033[0;32mRELATORES\033[m')
                                            relatores = [relator.text for relator in dados_csv1[2:]]
                                            
                                            return tipo_do_processo, origem_do_processo, relatores
                                    except Exception:
                                        self.chrome.refresh()
                                        tipo_do_precesso, origem_do_processo, relatores = tipo_processo_dados_csv1()

                                    try:
                                        def colunas_csv2():
                                            # colunas => 
                                            self.espera_elemento((By.CSS_SELECTOR, '.col-md-2'))
                                            colunas_csv2 = self.chrome.find_elements(By.CSS_SELECTOR, '.col-md-2')
                                            colunas = []
                                            adv = 1
                                            recte = 1
                                            recdo = 1
                                            for coluna in colunas_csv2: 
                                                if coluna.text == 'ADV.(A/S)':
                                                    print('\n\nRecuperando coluna: \033[0;32mADV.(A/S)\033[m')
                                                    colunas.append(f'{coluna.text} {adv}')
                                                    adv += 1
                                                elif coluna.text == 'RECTE.(S)':
                                                    print('\n\nRecuperando coluna: \033[0;32mRECTE.(S)\033[m')
                                                    colunas.append(f'{coluna.text} {recte}')
                                                    recte += 1
                                                elif coluna.text == 'RECDO.(A/S)':
                                                    print('\n\nRecuperando coluna: \033[0;32mRECDO.(A/S)\033[m')
                                                    colunas.append(f'{coluna.text} {recdo}')
                                                    recdo += 1
                                                else:
                                                    colunas.append(coluna.text)
                                            return colunas
                                    except Exception:
                                        self.chrome.refresh()
                                        colunas_processos = colunas_csv2()
                                                
                                                
                                    try:
                                        def dados_csv2():
                                            self.espera_elemento((By.CSS_SELECTOR, '#partes-resumidas .col-md-8'))
                                            dados = self.chrome.find_elements(By.CSS_SELECTOR, '#partes-resumidas .col-md-8')
                                            print('\n\nRecuperando: \033[0;32mDADOS DAS COLUNAS\033[m')
                                            dados_das_partes = [dado.text for dado in dados]
                                            return dados_das_partes
                                    except Exception:
                                        self.chrome.refresh()
                                        dados_das_partes = dados_csv2()
                                        
                                    tipo_do_precesso, origem_do_processo, relatores = tipo_processo_dados_csv1()
                                    colunas_processos = colunas_csv2()
                                    dados_das_partes = dados_csv2()
                                    
                                    df1 = pd.DataFrame({'TIPO DE PROCESSO': tipo_do_precesso, 'ORIGEM DO PROCESSO': origem_do_processo, 'RELATOR(ES / AS)': relatores})
                                    df2 = pd.DataFrame([dados_das_partes], columns=colunas_processos)
                                    
                                    frames = [df1, df2]
                                    
                                    result = pd.concat(frames)
                                    df = pd.DataFrame(result)
                                    
                                    parte = parte.replace('/', '-')
                                    if not os.path.exists(f'DOWNLOADS/STF - SUPREMO TRIBUNAL FEDERAL/PARTES/{parte.upper()}/IDENTIFICAÇÕES/{id_para_csv.upper()}'):
                                        os.makedirs(f'DOWNLOADS/STF - SUPREMO TRIBUNAL FEDERAL/PARTES/{parte.upper()}/IDENTIFICAÇÕES/{id_para_csv.upper()}')
                                        print(f'\n\nFazendo arquivo .csv do da identificação: \033[0;32m{id_para_csv.upper()}\033[m')
                                        df.to_csv(f'DOWNLOADS/STF - SUPREMO TRIBUNAL FEDERAL/PARTES/{parte.upper()}/IDENTIFICAÇÕES/{id_para_csv.upper()}/{id_para_csv.upper()}.csv', index=False)
                                    else:
                                        print(f'\n\nFazendo arquivo .csv do da identificação: \033[0;32m{id_para_csv.upper()}\033[m')
                                        df.to_csv(f'DOWNLOADS/STF - SUPREMO TRIBUNAL FEDERAL/PARTES/{parte.upper()}/IDENTIFICAÇÕES/{id_para_csv.upper()}/{id_para_csv.upper()}.csv', index=False)
                                        
                                    # ancora é recuperada com sucesso
                                    ancoras_recuperadas += 1
                                    
                                    # volta para a pagina das ancoras
                                    self.chrome.back()
                                    
                                    # atualiza a pagina
                                    self.chrome.refresh()
                                    
                                    # espera pelas ancoras
                                    self.espera_elemento((By.CSS_SELECTOR, '#tabela_processos a'))
                                    
                                    # recupera as ancoras para poder clicar
                                    identificacoes_ancoras = self.chrome.find_elements(By.CSS_SELECTOR, '#tabela_processos a')
                                else:
                                    # quando acabar de recuperar todas as ancoras dessa page

                                    # espera e clica no botão de próxima pagina
                                    self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#paginacao-proxima-pagina'))

                                    # envia o validador para saber se está na ultima pagina
                                    validador = envia_validador_para_mudar_pagina()
                                    
                                    # espera pelos a's
                                    self.espera_elemento((By.CSS_SELECTOR, '#tabela_processos a'))

                                    # recupera as ancoras quando disponível
                                    identificacoes_ancoras = self.chrome.find_elements(By.CSS_SELECTOR, '#tabela_processos a')
                                    
                                    # cai para o while
                            else:
                                # quando o validador (que pode ser '' ou 'disabled') for != de 'disabled'
                                # ou enquanto a quantidade de ancoras recuperadas for != da qtd_processos for falso
                                
                                # vai para a home
                                self.chrome.get(url)
                                
                                # limpa as ancoras recuperadas
                                ancoras_recuperadas = 0
                                
                                # o id é limpo 
                                id_para_csv = ''
                        else:
                            print(f'Não existe processos atualmente nessa parte: \033[0;32m{parte}\033[m\n\n')
                            sleep(1)
                    
            except Exception as erro:
                self.chrome.refresh()
                execucao_interna()
        execucao_interna()
    
    
    def caso_de_erro(self, falha):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        if not os.path.exists(f'../erros'):
            os.makedirs(f'../erros')
            with open('erros/erros.log', 'a+') as file:
                file.write(falha)
        else:
            with open('erros/erros.log', 'a+') as file:
                file.write(str(falha))
        print('\n\n\033[0;31mO ROBÔ FOI FINALIZADO PREMATURAMENTE!\n\nMOSTRE O ARQUIVO: erros.log NA PASTA erros AO DESENVOLVEDOR\033[m\n\n')
        quit()
        
    def print_finalizado(self):
        os.system('clear')
        print(f'\n\n\033[0;31m === O ROBÔ FINALIZOU AS CONSULTAS DE {len(partes)} PARTES === \033[m\n\n')

