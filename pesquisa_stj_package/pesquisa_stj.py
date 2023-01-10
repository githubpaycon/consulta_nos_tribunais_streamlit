from partes import partes
import pandas as pd
import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

class RoboStj:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    def __init__(self, url='https://processo.stj.jus.br/processo/pesquisa/', headless='2'):
        """
        url='https://processo.stj.jus.br/processo/pesquisa/' -> Vái para o site do STJ (CONSULTA PROCESSUAL)
        maximizar=True => vai deixar o navegador em tela cheia
        """
        if headless == '1':
            self.driver_path = ChromeDriverManager().install()
            self.options = ChromeOptions()
            self.options.add_argument("--headless")
            self.chrome = Chrome(self.driver_path, chrome_options=self.options)
            self.chrome.maximize_window()
            self.get = self.chrome.get(url)
            self.wdw = WebDriverWait(driver=self.chrome, timeout=10)
        elif headless == '2':
            self.driver_path = ChromeDriverManager().install()
            self.chrome = Chrome(self.driver_path)
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
    
    def faz_csv_detalhes(self, parte, processo, parte_partes=''):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n\nRECUPERANDO DADOS DA ABA: \033[1;31mDETALHES\033[m')
        print(f'\n\nPROCESSO: \033[1;33m{processo}\033[m')
        
        processo = processo.replace('/', '-')
        parte = parte.replace('/', '-')
        if parte_partes:
            parte_partes = parte_partes.replace('/', '-')
        
        # clica na aba detalhes
        self.espera_elemento_disponivel_e_clica(locator=(By.CSS_SELECTOR, '#idSpanAbaDetalhes a'))
        

        self.espera_elemento(locator=(By.CSS_SELECTOR, '.classSpanDetalhesLabel'))
        colunas = self.espera_e_retorna_lista_de_elementos_text_from_id_esse_tribunal(locator=(By.CSS_SELECTOR, '.classSpanDetalhesLabel'))
        
        self.espera_elemento(locator=(By.CSS_SELECTOR, '.classSpanDetalhesTexto'))
        dados_detalhes = self.espera_e_retorna_lista_de_elementos_text(locator=(By.CSS_SELECTOR, '.classSpanDetalhesTexto'))
        
        df = pd.DataFrame([dados_detalhes], columns=colunas)
        
        if parte_partes:
            if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/DETALHES/'):
                os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/DETALHES/')
                df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/DETALHES/{dados_detalhes[0].upper()}.csv', index=False, encoding='utf-8')
            else:
                df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/DETALHES/{dados_detalhes[0].upper()}.csv', index=False, encoding='utf-8')
        else:
            if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/DETALHES/'):
                os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/DETALHES/')
                df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/DETALHES/{dados_detalhes[0].upper()}.csv', index=False, encoding='utf-8')
            else:
                df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/DETALHES/{dados_detalhes[0].upper()}.csv', index=False, encoding='utf-8')
            
    def faz_csv_fases(self, parte, processo, parte_partes=''):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n\nRECUPERANDO DADOS DA ABA: \033[1;31mFASES\033[m')
        print(f'\n\nPROCESSO: \033[1;33m{processo}\033[m')
        
        processo = processo.replace('/', '-')
        parte = parte.replace('/', '-')
        if parte_partes:
            parte_partes = parte_partes.replace('/', '-')
        
        # clica na aba Fases
        self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#idSpanAbaFases a'))

        colunas_fase_data =  self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classSpanFaseData'))
        colunas_fase_hora = self.espera_e_retorna_lista_de_elementos_text_from_id_esse_tribunal((By.CSS_SELECTOR, '.classSpanFaseHora'))
        colunas_data_hora_zip = zip(colunas_fase_data, colunas_fase_hora)
        colunas_fase = [col for col in colunas_data_hora_zip]
        dados_da_fases = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classSpanFaseTexto'))
        csv_structure = {'DATA E HORA': colunas_fase, 'DADOS' : dados_da_fases}
        df = pd.DataFrame(csv_structure)

        if parte_partes:
            if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/FASES/'):
                os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/FASES/')
                df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/FASES/{processo.upper()}.csv', index=False, encoding='utf-8')
            else:
                df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/FASES/{processo.upper()}.csv', index=False, encoding='utf-8')
        else:
            if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/FASES/'):
                os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/FASES/')
                df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/FASES/{processo.upper()}.csv', index=False, encoding='utf-8')
            else:
                df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/FASES/{processo.upper()}.csv', index=False, encoding='utf-8')
    
    def faz_csv_peticoes(self, parte, processo, parte_partes=''):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n\nRECUPERANDO DADOS DA ABA: \033[1;31mPETIÇÕES\033[m')
        print(f'\n\nPROCESSO: \033[1;33m{processo}\033[m')

        processo = processo.replace('/', '-')
        parte = parte.replace('/', '-')
        if parte_partes:
            parte_partes = parte_partes.replace('/', '-')
        
        
        self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#idSpanAbaPeticoes a'))
        
        div_tem_nao_tem_dados = self.chrome.find_element(By.CSS_SELECTOR, '#idDivPeticoes > div.classDivConteudoPesquisaProcessual > div').get_attribute('id')

            
     
        if div_tem_nao_tem_dados == 'idDivLinhaSemPeticoes':
            print('Não existe petições!')
        elif div_tem_nao_tem_dados == 'idDivCabecalhoPeticoes':
            numero_peticao = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classDivLinhaPeticoes .classSpanLinhaPeticoesNum'))
            protocolo = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classDivLinhaPeticoes .classSpanLinhaPeticoesProtocolo'))
            tipo = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classDivLinhaPeticoes .classSpanLinhaPeticoesTipo'))
            processamento = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classDivLinhaPeticoes .classSpanLinhaPeticoesProcessamento'))
            peticionario = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.classDivLinhaPeticoes .classSpanLinhaPeticoesQuem'))
            
            csv_structure = {'PETIÇÃO Nº': numero_peticao, 
                             'PROTOCOLO' : protocolo, 
                             'TIPO' : tipo, 
                             'PROCESSAMENTO' : processamento, 
                             'PETICIONÁRIO' : peticionario}
            
            df = pd.DataFrame(csv_structure)

            if parte_partes:
                if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/PETIÇÕES/'):
                    os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/PETIÇÕES/')
                    df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/PETIÇÕES/{processo.upper()}.csv', index=False, encoding='utf-8')
                else:
                    df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/PETIÇÕES/{processo.upper()}.csv', index=False, encoding='utf-8')
            else:
                if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/PETIÇÕES/'):
                    os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/PETIÇÕES/')
                    df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/PETIÇÕES/{processo.upper()}.csv', index=False, encoding='utf-8')
                else:
                    df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/PETIÇÕES/{processo.upper()}.csv', index=False, encoding='utf-8')
        
    def faz_csv_pautas(self, parte, processo, parte_partes):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n\nRECUPERANDO DADOS DA ABA: \033[1;31mPAUTAS\033[m')
        print(f'\n\nPROCESSO: \033[1;33m{processo}\033[m')
        
        processo = processo.replace('/', '-')
        parte = parte.replace('/', '-')
        if parte_partes:
            parte_partes = parte_partes.replace('/', '-')
        
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

            if parte_partes:
                if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/PAUTAS/'):
                    os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/PAUTAS/')
                    df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/PAUTAS/{processo.upper()}.csv', index=False, encoding='utf-8')
                else:
                    df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/PAUTAS/{processo.upper()}.csv', index=False, encoding='utf-8')
            if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/PAUTAS/'):
                os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/PAUTAS/')
                df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/PAUTAS/{processo.upper()}.csv', index=False, encoding='utf-8')
            else:
                df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/PAUTAS/{processo.upper()}.csv', index=False, encoding='utf-8')
                
    def faz_csv_decisoes(self, parte, processo, parte_partes):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n\nRECUPERANDO DADOS DA ABA: \033[1;31mDECISÕES\033[m')
        print(f'\n\nPROCESSO: \033[1;33m{processo}\033[m')
        # tratando nome processo
        processo = processo.replace('/', '-')
        if parte_partes:
            parte = parte.replace('/', '-')
        
        self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#idSpanAbaDecisoes > a'))
        
        # tenta pegar dessa classe -> clsDecisoesIntTeorRevistaLinhaTodosDocumentos
        self.chrome.implicitly_wait(1)
        classes_de_validacao = []
        div_content_clsDecisoesIntTeorRevistaLinhaTodosDocumentos = self.chrome.find_elements(By.CSS_SELECTOR, '#idDivDecisoes > div.classDivConteudoPesquisaProcessual > div')
        for atributo in div_content_clsDecisoesIntTeorRevistaLinhaTodosDocumentos:
            classes_de_validacao.append(atributo.get_attribute('class'))
        
        for classe_de_validacao in classes_de_validacao: 
            if classe_de_validacao == 'classDivLinhaDecisoesDocumentos':
                decisoes = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.clsDecisoesIntTeorRevistaBloco'))
                for decisao in decisoes:
                    nome_arquivo_e_coluna_decisao = decisao.split('\n')[0].replace('/', '-')  # recupera a string antes do \n
                    dados_decisao = decisao.split('\n')[1:]
                    
                    df = pd.DataFrame({f'{nome_arquivo_e_coluna_decisao}': dados_decisao})
                    # verifica se existem diretorios, senão, cria e loogo dps o pandas coloca o arq csv
                    
                    if parte_partes:
                        if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/DECISOES/NÃO MONOCRATICAS/'):
                            os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/DECISOES/NÃO MONOCRATICAS/')
                            df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/DECISOES/NÃO MONOCRATICAS/{processo.upper()}.csv', index=False, encoding='utf-8')
                        else:
                            df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}/DECISOES/NÃO MONOCRATICAS/{processo.upper()}.csv', index=False, encoding='utf-8')
                    else:
                        if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/DECISOES/NÃO MONOCRATICAS/'):
                            os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/DECISOES/NÃO MONOCRATICAS/')
                            df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/DECISOES/NÃO MONOCRATICAS/{nome_arquivo_e_coluna_decisao.upper()}.csv', index=False, encoding='utf-8')
                        else:
                            df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/DECISOES/NÃO MONOCRATICAS/{nome_arquivo_e_coluna_decisao.upper()}.csv', index=False, encoding='utf-8')
            elif classe_de_validacao == 'clsDecisoesMonocraticasBlocoExterno':
                div_content_clsDecisoesMonocraticasTopoLink = self.chrome.find_element(By.CSS_SELECTOR, '.clsDecisoesMonocraticasBlocoExterno > div > div > a').get_attribute('class')
                if div_content_clsDecisoesMonocraticasTopoLink == 'clsDecisoesMonocraticasTopoLink':
                    decisoes_monocratica = self.espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.clsDecisoesMonocraticasBlocoInterno'))
                    for decisao_monocratica in decisoes_monocratica:
                        nome_arquivo_e_coluna_decisao_monocratica = decisao_monocratica.split('\n')[0].replace('/', '-')  # recupera a string antes do \n
                        dados_decisao_monocratica = decisao_monocratica.split('\n')[1:]                        

                        df = pd.DataFrame({f'{nome_arquivo_e_coluna_decisao_monocratica}': dados_decisao_monocratica})
                        # verifica se existem diretorios, senão, cria e loogo dps o pandas coloca o arq csv
                        if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/DECISOES/MONOCRATICAS/'):
                            os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/DECISOES/MONOCRATICAS/')
                            df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/DECISOES/MONOCRATICAS/{nome_arquivo_e_coluna_decisao_monocratica.upper()}.csv', index=False, encoding='utf-8')
                        else:
                            df.to_csv(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}/DECISOES/MONOCRATICAS/{nome_arquivo_e_coluna_decisao_monocratica.upper()}.csv', index=False, encoding='utf-8')
            elif classe_de_validacao == 'classDivLinhaRegistroNaoEncontrado':
                print('Não há decisões.')
        # tenta pegar dessa classe -> clsDecisoesMonocraticasTopoLink
        self.chrome.implicitly_wait(1)  
    
    def executa_criacao_de_csvs(self, parte, processo, parte_partes):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'\n\nCRIANDO ARQUIVO CSV DO PROCESSO: \033[1;31m{processo}\033[m')
        self.faz_csv_detalhes(parte, processo, parte_partes)
        self.faz_csv_fases(parte, processo, parte_partes)
        self.faz_csv_decisoes(parte, processo, parte_partes)
        self.faz_csv_peticoes(parte, processo, parte_partes)
        self.faz_csv_pautas(parte, processo, parte_partes)
 
    def pesquisa_stj(self):
        if len(partes) >= 1:
            for parte in partes:
                url = 'https://processo.stj.jus.br/processo/pesquisa/'
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f'\n\n\033[0;31mPegando informações do site: STJ - SUPERIOR TRIBUNAL DE JUSTICA\n'
                    f'{url}\033[m')
                print(f'\n\nParte à pegar: \033[0;32m{parte}\033[m')
                self.espera_elemento_e_envia_send_keys(locator=(By.CSS_SELECTOR, '#idParteNome'), string=parte)
                self.espera_elemento_disponivel_e_clica(locator=(By.CSS_SELECTOR, '#idComboFoneticaPhonosParte_1'))
                self.espera_elemento_disponivel_e_clica(locator=(By.CSS_SELECTOR, '#idBotaoPesquisarFormularioExtendido'))
                qtd_registros_text = self.espera_e_retorna_elemento_text((By.CSS_SELECTOR, '#idDivBlocoMensagem > div > b'))
                qtd_registros = int(qtd_registros_text)
                
                # 1A LISTA DE PARTES DA PARTE
                """
                EXEMPLO: 0 = MARCADOR
                    0   WHIRLPOOL S A
                    0   WHIRLPOOL S/A
                    0   WHIRLPOOL S/A
                    0   WHIRLPOOL S/A
                    0   WHIRLPOOL S.A
                    0   WHIRLPOOL S.A
                    0   WHIRLPOOL S.A
                    0   WHIRLPOOL S.A.
                """
                if qtd_registros >= 1:
                    self.espera_elemento((By.CSS_SELECTOR, '.clsPessoaNome'))
                    
                    # lista das 'partes das partes'
                    lista_de_partes_s_o = self.espera_e_retorna_lista_de_elementos(locator=(By.CSS_SELECTOR, '.clsPessoaNome'))
                    
                    for parte_num in range(len(lista_de_partes_s_o)):
                        self.chrome.implicitly_wait(1)
                        nome_parte_parte = lista_de_partes_s_o[parte_num].text
                        lista_de_partes_s_o[parte_num].click()
                        
                        # lista de processos da parte
                        id_de_verificacao = self.chrome.find_element(By.CSS_SELECTOR, '#idSpanConteudoCentro > div:nth-child(2)').get_attribute('id')
                        
                        # se existir a div de mensagem que existe uma lista de processos
                        """
                        EXEMPLO: Listando processos relacionados a(s) parte(s) com nome WHIRLPOOL S.A..
                                            Pesquisa resultou em 7 registro(s)!
                        """
                        if 'idDivBlocoMensagem' == id_de_verificacao:
                            id_de_verificacao_se_tem_paginacao = self.chrome.find_element(By.CSS_SELECTOR, '#idSpanConteudoCentro > div:nth-child(3)').get_attribute('id')
                            
                            # verifica se existe paginacao na lista de processos
                            """
                            EXEMPLO:
                                página 1 de 2 páginas
                            """
                            if id_de_verificacao_se_tem_paginacao == 'idDivBlocoPaginacaoTopo':
                                qtd_processos_recuperados = 0
                                qtd_processos_para_recuperar = self.espera_e_retorna_elemento_text((By.CSS_SELECTOR, '#idDivBlocoMensagem > div > b'))
                                qtd_processos_para_recuperar = int(qtd_processos_para_recuperar)
                                
                                page_atual = int(self.espera_e_retorna_conteudo_do_atributo_do_elemento_text('value', (By.CSS_SELECTOR, '#idDivBlocoPaginacaoTopo > div > span > span.classSpanPaginacaoPaginaTextoInterno > input[type=text]')))
                                pages_para_percorrer_text = self.espera_e_retorna_elemento_text((By.CSS_SELECTOR, '#idDivBlocoPaginacaoTopo > div > span > span.classSpanPaginacaoPaginaTextoInterno'))
                                peges_para_percorrer_list =[int(caractere) for caractere in pages_para_percorrer_text.split() if caractere.isdigit()]
                                pages_para_percorrer = str(peges_para_percorrer_list).strip('[]')
                                pages_para_percorrer = int(pages_para_percorrer)
                                
                                registros = self.espera_e_retorna_lista_de_elementos((By.CSS_SELECTOR, '.classSpanProcessoUF a'))
                                while qtd_processos_recuperados != qtd_processos_para_recuperar:
                                    for registro_do_registro in range(len(registros)):
                                        self.chrome.implicitly_wait(1)
                                        titulo_processo = registros[registro_do_registro].text
                                        registros[registro_do_registro].click()  # clica no processo
                                        self.executa_criacao_de_csvs(parte, titulo_processo, parte_partes=nome_parte_parte)
                                        qtd_processos_recuperados += 1
                                        self.chrome.back()
                                        self.chrome.refresh()
                                        registros = self.espera_e_retorna_lista_de_elementos((By.CSS_SELECTOR, '.classSpanProcessoUF a'))
                                    else:
                                        try:
                                            self.espera_elemento((By.CSS_SELECTOR, '#idDivBlocoPaginacaoTopo > div > span > span.classSpanPaginacaoImagensDireita > a'))
                                            button_existe = self.chrome.find_element(By.CSS_SELECTOR, '#idDivBlocoPaginacaoTopo > div > span > span.classSpanPaginacaoImagensDireita > a').get_attribute('title')
                                            
                                            if button_existe == 'próxima página':
                                                sleep(.5)
                                                self.chrome.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)
                                                self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#idDivBlocoPaginacaoBase > div > span > span.classSpanPaginacaoImagensDireita > a:nth-child(1)'))
                                                registros = self.espera_e_retorna_lista_de_elementos((By.CSS_SELECTOR, '.classSpanProcessoUF a'))
                                        except Exception:
                                            page_atual = int(self.espera_e_retorna_conteudo_do_atributo_do_elemento_text('value', (By.CSS_SELECTOR, '#idDivBlocoPaginacaoTopo > div > span > span.classSpanPaginacaoPaginaTextoInterno > input[type=text]')))
                                            
                                            for voltar in range(page_atual):
                                                self.chrome.back()
                                            else:
                                                # atualiza a lista de partes
                                                self.chrome.refresh()
                                                lista_de_partes_s_o = self.espera_e_retorna_lista_de_elementos(locator=(By.CSS_SELECTOR, '.clsPessoaNome'))
                                else:
                                    lista_de_partes_s_o = self.espera_e_retorna_lista_de_elementos(locator=(By.CSS_SELECTOR, '.clsPessoaNome'))
                            else:  # se não houver paginação...
                                registros = self.espera_e_retorna_lista_de_elementos((By.CSS_SELECTOR, '.classSpanProcessoUF a'))
                                for registro_do_registro in range(len(registros)):
                                    self.chrome.implicitly_wait(1)
                                    titulo_processo = registros[registro_do_registro].text
                                    registros[registro_do_registro].click()          
                                    self.executa_criacao_de_csvs(parte, titulo_processo)
                                    self.chrome.back()
                                    self.chrome.refresh()
                                    registros = self.espera_e_retorna_lista_de_elementos((By.CSS_SELECTOR, '.classSpanProcessoUF a'))
                                else:
                                    self.chrome.back()
                                    self.chrome.refresh()
                                    lista_de_partes_s_o = self.espera_e_retorna_lista_de_elementos(locator=(By.CSS_SELECTOR, '.clsPessoaNome'))
                        # se não houver uma div falando que tem uma lista de processos, existe somente um
                        else:
                            titulo_processo = self.espera_e_retorna_elemento_text((By.CSS_SELECTOR, '#idSpanClasseDescricao'))
                            self.executa_criacao_de_csvs(parte, titulo_processo)
                            self.chrome.back()
                            self.chrome.refresh()
                            lista_de_partes_s_o = self.espera_e_retorna_lista_de_elementos(locator=(By.CSS_SELECTOR, '.clsPessoaNome'))
                    else:
                        # returna para a pege para pesquisar a nova parte
                        self.chrome.get('https://processo.stj.jus.br/processo/pesquisa/')
                else:
                    print('Nenhuma parte encontrada!')
                    self.chrome.get('https://processo.stj.jus.br/processo/pesquisa/')
         
    def caso_de_erro(self, falha):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
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