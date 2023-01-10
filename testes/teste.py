
  
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


class RoboStj:
    os.system('cls' if os.name == 'nt' else 'clear')  # clear the Terminal
    
    def __init__(self, url='https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=201901562697&totalRegistrosPorPagina=40&aplicacao=processos', maximizar=False):
        """
        url='https://processo.stj.jus.br/processo/pesquisa/' -> Vái para o site do STJ (CONSULTA PROCESSUAL)
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

    def url_atual(self):
        """
        ### Essa função retorna a url atual
        """
        return self.chrome.current_url
            
    def espera_elemento_disponivel_e_clica(self, locator: tuple):
        """
        ### Essa função espera o elemento ficar disponível (clicavel) e clica assim que disponível
        #### Parâmetros
        * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
        """
        
        # espera o item estar disponível quando disponível JA ENTRA NELE
        self.wdw.until(EC.element_to_be_clickable(locator))
        # clica no elemento
        self.chrome.find_element(*locator).click()
    
    def espera_elemento(self, locator: tuple):
        """### Essa função espera o elemento ficar disponível (clicavel) e retorna o valor padrão do until
        #### Parâmetros
        * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')"""
        
        return self.wdw.until(EC.element_to_be_clickable(locator))
    
    def espera_elemento_e_envia_send_keys(self, string, locator: tuple):
        """
        ### Essa função espera o elemento (clicavel) e envia a sua string para ele
        ### O elemento deve ser um tipo de input ou textarea para entrada de dados com o user
        ### Parâmetros
        #### * string -> String ou número que deseja enviar para o elemento
        #### * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
        """
        
        # espera o item estar disponível quando disponível JA ENTRA NELE
        self.wdw.until(EC.element_to_be_clickable(locator))
        
        # Envia string para o elemento
        self.chrome.find_element(*locator).send_keys(string)
        
    def espera_e_retorna_lista_de_elementos(self, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
        """
        ### Essa função espera os elementoS ficarem disponíveis (clicaveis) e retorna A LISTA DE ELEMENTOS
        #### Parâmetros
        * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
        """
        if locator == ("BY_SELECTOR", "WEBELEMENT"):
            print('Adicione um locator!!!!')
            return
        self.wdw.until(EC.element_to_be_clickable(locator))
        return self.chrome.find_elements(*locator)

    def espera_e_retorna_lista_de_elementos_text_from_id(self, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
        """
        ### Essa função espera os elementoS ficarem disponíveis (clicaveis) e retorna A LISTA DE ELEMENTOS COM UM NÚMERO DE IDENTIFICAÇÃO NO FINAL
        ### EX -> [ADV 1, ADV2, JUR 3, OPS 4]
        ## ESSA FUNÇÃO ADICIONA STRINGS VAZIAS (SEM ID)!
        #### Parâmetros
        * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
        """
        if locator == ("BY_SELECTOR", "WEBELEMENT"):
            print('Adicione um locator!!!!')
            return
        self.wdw.until(EC.element_to_be_clickable(locator))
        webelements = self.chrome.find_elements(*locator)
        id = 1
        elementos_com_id = []
        for element in webelements:
            if element.text == ' ':
                elementos_com_id.append(element.text)
            else:
                elementos_com_id.append(f'{element.text} {id}')
            id += 1
        else:
            return elementos_com_id
        
    def espera_e_retorna_lista_de_elementos_text_from_id_esse_tribunal(self, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
        """
        ### Essa função espera os elementoS ficarem disponíveis (clicaveis) e retorna A LISTA DE ELEMENTOS COM UM NÚMERO DE IDENTIFICAÇÃO NO FINAL
        ### EX -> [ADV col1, ADV col2, JUR col3, OPS col4]
        ## AQUI ELE ACHA A COLUNA SEM NADA QUE É A COLUNA COM OS VOLUMES
        ## ESSA FUNÇÃO ADICIONA STRINGS VAZIAS (SEM ID)!
        #### Parâmetros
        * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
        """
        if locator == ("BY_SELECTOR", "WEBELEMENT"):
            print('Adicione um locator!!!!')
            return
        self.wdw.until(EC.element_to_be_clickable(locator))
        webelements = self.chrome.find_elements(*locator)
        id = 1
        elementos_com_id = []
        for element in webelements:
            if element.text == ' ':
                elementos_com_id.append(f'VOLUME(S) col{id}')
            else:
                elementos_com_id.append(f'{element.text} col{id}')
            id += 1
        else:
            return elementos_com_id
    
    def espera_e_retorna_lista_de_elementos_text(self, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
        """
        ### Essa função espera os elementoS ficarem disponíveis (clicaveis) e retorna A LISTA DOS TEXTOS DOS ELEMENTOS
        #### Parâmetros
        * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
        
        ### FORMA DE UTILIZAÇÃO
        #### minha_lista_de_textos_dos_elementos = espera_e_retorna_lista_de_elementos_text(
        #### (By.CSS_SELECTOR, '.class_elements')
        #### )
        """
        if locator == ("BY_SELECTOR", "WEBELEMENT"):
            print('Adicione um locator!!!!')
            return
        self.wdw.until(EC.element_to_be_clickable(locator))
        elements = self.chrome.find_elements(*locator)
        return [element.text for element in elements]

    def espera_e_retorna_conteudo_do_atributo_do_elemento_text(self, atributo, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
        """
        ### Essa função espera o elemento ficare disponível (clicaveis) e retorna o conteudo do atributo escolhido
        #### Parâmetros
        * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
        * atributo -> 'href' 'class' 'onclick'...
        
        ### FORMA DE UTILIZAÇÃO
        #### minha_lista_de_textos_dos_elementos = espera_e_retorna_lista_de_elementos_text(
        #### (By.CSS_SELECTOR, '.class_elements')
        #### )
        """
        if locator == ("BY_SELECTOR", "WEBELEMENT"):
            print('Adicione um locator!!!!')
            return
        self.wdw.until(EC.element_to_be_clickable(locator))
        return self.chrome.find_element(*locator).get_attribute(atributo)
    
    def espera_e_retorna_conteudo_dos_atributos_dos_elementos_text(self, atributo, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
        """
        ### Essa função espera o elemento ficare disponível (clicaveis) e retorna o conteudo do atributo escolhido
        #### Parâmetros
        * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
        * atributo -> 'href' 'class' 'onclick'...
        
        ### FORMA DE UTILIZAÇÃO
        #### minha_lista_de_textos_dos_elementos = espera_e_retorna_lista_de_elementos_text(
        #### (By.CSS_SELECTOR, '.class_elements')
        #### )
        """
        if locator == ("BY_SELECTOR", "WEBELEMENT"):
            print('Adicione um locator!!!!')
            return
        self.wdw.until(EC.element_to_be_clickable(locator))
        atributos = self.chrome.find_elements(*locator)
        elementos_atributos = [atributo_selen.get_attribute(atributo) for atributo_selen in atributos]
        return elementos_atributos
            
    def espera_e_retorna_elemento_text(self, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
        """
        ### Essa função espera o elemento ficar disponível (clicavel) e retorna o texto dele
        #### Parâmetros
        * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
        """
        self.wdw.until(EC.element_to_be_clickable(locator))
        return self.chrome.find_element(*locator).text
        
    def espera_abrir_n_de_janelas_e_muda_para_a_ultima_janela(self, num_de_janelas: int=2):
        # verifica se abriu x numeros de janelas
        print(f'Você está na janela -> {self.chrome.current_window_handle}')
        self.wdw.until(EC.number_of_windows_to_be(num_de_janelas))
        print(f'Agora, você tem {len(self.chrome.window_handles)} janelas abertas')
        todas_as_windows = self.chrome.window_handles
        self.chrome.switch_to.window(todas_as_windows[-1])
        print(f'Agora, você está na janela -> {self.chrome.current_window_handle}')
        
    def find_window_to_title_contain(self, title_contain_switch: str): # quero que pelo menos um pedaco do titulo que seja str
        """
        ### Essa função muda de janela quando o título tiver pelo menos algo igual ao parametro enviado
        #### Ex -> Minha janela = janela
        
        para cada janela em ids das janelas
        muda para a janela
        se a janela for ao menos de um pedaço do titulo que passei
            em title_contain_switch
        para de executar
        """
        window_ids = self.chrome.window_handles # ids de todas as janelas

        for window in window_ids:
            self.chrome.switch_to_window(window)  
            if title_contain_switch in self.chrome.title:
                break
        else:
            print(f'Janela não encontrada!\n'
                f'Verifique o valor enviado {title_contain_switch}')
        
    def fecha_janela_atual(self):
        self.chrome.close()
    
    ###############################################################################
    ############↓#######↓######### RECUPERA DADOS DO SITE #######↓###########↓#####
    ###############################################################################
    

    # def faz_csv_detalhes(self, parte, processo):
    #     processo = processo.replace('/', '|')
        
    #     # clica na aba detalhes
    #     self.espera_elemento_disponivel_e_clica(locator=(By.CSS_SELECTOR, '#idSpanAbaDetalhes a'))
        
    #     # espera pelos 
    #     self.espera_elemento(locator=(By.CSS_SELECTOR, '.classSpanDetalhesLabel'))
    #     colunas = self.espera_e_retorna_lista_de_elementos_text_from_id_esse_tribunal(locator=(By.CSS_SELECTOR, '.classSpanDetalhesLabel'))
        
    #     # espera pelos 
    #     self.espera_elemento(locator=(By.CSS_SELECTOR, '.classSpanDetalhesTexto'))
    #     dados_detalhes = self.espera_e_retorna_lista_de_elementos_text(locator=(By.CSS_SELECTOR, '.classSpanDetalhesTexto'))
        
    #     df = pd.DataFrame([dados_detalhes], columns=colunas)
        
    #     if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/DETALHES/'):
    #         os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/DETALHES/')
    #         df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/DETALHES/{dados_detalhes[0].upper()}.csv', index=False)
    #         sleep(1)
    #     else:
    #         df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/DETALHES/{dados_detalhes[0].upper()}.csv', index=False)
    #         sleep(1)
    
    # def faz_csv_fases(self, parte, processo):
    #     processo = processo.replace('/', '|')
        
    #     # clica na aba Fases
    #     self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#idSpanAbaFases a'))

    #     colunas_fase_data =  self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classSpanFaseData'))
    #     colunas_fase_hora = self.espera_e_retorna_lista_de_elementos_text_from_id_esse_tribunal((By.CSS_SELECTOR, '.classSpanFaseHora'))
    #     colunas_data_hora_zip = zip(colunas_fase_data, colunas_fase_hora)
    #     colunas_fase = [col for col in colunas_data_hora_zip]
    #     dados_da_fases = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classSpanFaseTexto'))
    #     csv_structure = {'DATA E HORA': colunas_fase, 'DADOS' : dados_da_fases}
    #     df = pd.DataFrame(csv_structure)

        
    #     if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/FASES/'):
    #         os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/FASES/')
    #         df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/FASES/{processo.upper()}.csv', index=False)
    #         sleep(1)
    #     else:
    #         df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/FASES/{processo.upper()}.csv', index=False)
    #         sleep(1)
    
    # def faz_csv_peticoes(self, parte, processo):
    #     processo = processo.replace('/', '|')
    #     self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#idSpanAbaPeticoes a'))
        
    #     div_tem_nao_tem_dados = self.chrome.find_element(By.CSS_SELECTOR, '#idDivPeticoes > div.classDivConteudoPesquisaProcessual > div').get_attribute('id')

            
     
    #     if div_tem_nao_tem_dados == 'idDivLinhaSemPeticoes':
    #         print('Não existe petições!')
    #     elif div_tem_nao_tem_dados == 'idDivCabecalhoPeticoes':
    #         numero_peticao = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classDivLinhaPeticoes .classSpanLinhaPeticoesNum'))
    #         protocolo = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classDivLinhaPeticoes .classSpanLinhaPeticoesProtocolo'))
    #         tipo = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classDivLinhaPeticoes .classSpanLinhaPeticoesTipo'))
    #         processamento = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classDivLinhaPeticoes .classSpanLinhaPeticoesProcessamento'))
    #         peticionario = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classDivLinhaPeticoes .classSpanLinhaPeticoesQuem'))
            
    #         csv_structure = {'PETIÇÃO Nº': numero_peticao, 
    #                          'PROTOCOLO' : protocolo, 
    #                          'TIPO' : tipo, 
    #                          'PROCESSAMENTO' : processamento, 
    #                          'PETICIONÁRIO' : peticionario}
            
    #         df = pd.DataFrame(csv_structure)

            
    #         if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/PETIÇÕES/'):
    #             os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/PETIÇÕES/')
    #             df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/PETIÇÕES/{processo.upper()}.csv', index=False)
    #         else:
    #             df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/PETIÇÕES/{processo.upper()}.csv', index=False)
            
    
    def faz_csv_pautas(self, parte, processo):
        processo = processo.replace('/', '|')
        
        self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#idSpanAbaPautas a'))
        
        # verifica se ha pautas
        div_tem_ou_nao_pautas = self.chrome.find_element(By.CSS_SELECTOR, '#idDivPautas > div.classDivConteudoPesquisaProcessual > div > div').get_attribute('id')
        
        if div_tem_ou_nao_pautas == 'idDivLinhaSemPautas':
            print('Não há pautas.')
        elif div_tem_ou_nao_pautas == 'idCabecalhoPautas':
            data_da_secao_dado = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.clsLinhaPautasDataJulgamento'))
            hora_sessao_dado = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.clsLinhaPautasHoraJulgamento'))
            orgao_julgamento_dado = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.clsLinhaPautasOrgaoJulgamento'))

            csv_structure = {'DATA DA SESSÃO': data_da_secao_dado, 
                             'HORA DA SESSÃO' : hora_sessao_dado, 
                             'ORGÃO JULGAMENTO' : orgao_julgamento_dado
                             }
            
            df = pd.DataFrame(csv_structure)

        
            if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/PAUTAS/'):
                os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/PAUTAS/')
                df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/PAUTAS/{processo.upper()}.csv', index=False)
            else:
                df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTIÇA/PARTES/{parte.upper()}/{processo.upper()}/PAUTAS/{processo.upper()}.csv', index=False)

                
            
    def pesquisa_stj(self):
        if len(partes) >= 1:
            for parte in partes:
                self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#idProcessoDetalheBotoesBloco2'))
                nome_precesso = self.espera_e_retorna_elemento_text((By.CSS_SELECTOR, '#idSpanClasseDescricao'))
                self.faz_csv_pautas(parte, nome_precesso)
        else:
            ...       
                
executa = RoboStj()
executa.pesquisa_stj()