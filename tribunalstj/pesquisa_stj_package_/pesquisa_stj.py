from partes import partes
import pandas as pd
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

class RoboStj:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    def __init__(self, url='https://processo.stj.jus.br/processo/pesquisa/', headless=0):
        """
        url='https://processo.stj.jus.br/processo/pesquisa/' -> Vái para o site do STJ (CONSULTA PROCESSUAL)
        maximizar=True => vai deixar o navegador em tela cheia
        """
        if headless == 1:
            print('Executando com Headless')
            self.s = Service(ChromeDriverManager().install())
            self.options = ChromeOptions()
            self.options.add_argument("--headless")
            self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
            self.chrome = Chrome(service=self.s, chrome_options=self.options)
            self.chrome.maximize_window()
            self.get = self.chrome.get(url)
            self.wdw = WebDriverWait(driver=self.chrome, timeout=10, poll_frequency=0.5)
        elif headless == 0:
            self.options = ChromeOptions()
            self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
            self.s = Service(ChromeDriverManager().install())
            self.chrome = Chrome(service=self.s, chrome_options=self.options)
            self.get = self.chrome.get(url)
            self.wdw = WebDriverWait(driver=self.chrome, timeout=10, poll_frequency=0.5)


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
    
    def espera_enquanto_nao_tem_resposta_do_site(self, locator : tuple):
        """Essa função tentará recarregar a página em até 3 vezes esperando pelo elemento"""
        try:
            element = self.wdw.until(EC.element_to_be_clickable(locator))
            if element:
                return element
        except TimeoutException:
            print('Talvez a página tenha dado algum erro, vou atualiza-lá')
            sleep(2)
            try:
                self.chrome.refresh()
                element = self.wdw.until(EC.element_to_be_clickable(locator))
                if element:
                    print('Voltou!')
                    return element
            except TimeoutException:
                print('A página ainda não voltou, vou atualiza-lá')
                sleep(2)
                try:
                    self.chrome.refresh()
                    element = self.wdw.until(EC.element_to_be_clickable(locator))
                    if element:
                        print('Voltou!')
                        return element
                except TimeoutException:
                    print('Poxa, essa será a última vez que vou atualizar a página...')
                    sleep(2)
                    try:
                        self.chrome.refresh()
                        element = self.wdw.until(EC.element_to_be_clickable(locator))
                        if element:
                            print('Voltou!')
                            return element
                    except TimeoutException:
                        print("Olha, não foi possível. A página provavelmente caiu feio :(")
                        print("Infelizmente o programa vai ser finalizado...")
                        self.chrome.quit()
    
    
    ###############################################################################
    ############↓#######↓######### RECUPERA DADOS DO SITE #######↓###########↓#####
    ###############################################################################
    
    def faz_csv_detalhes(self, parte, processo, procs_p_rec=1, procs_rec=0, parte_partes=''):
        if procs_p_rec:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('\n\nRECUPERANDO DADOS DA ABA: \033[1;31mDETALHES\033[m')
            print(f"{procs_rec} processo(s) recuperados de {procs_p_rec} processo(s)")
            print(f"Recuperando processo {procs_rec + 1} de {procs_p_rec} processo(s)")
            print(f'\n\nPROCESSO: \033[1;33m{processo}\033[m')
            print(f'\nPARTE: \033[1;33m{parte}\033[m')

            if parte_partes:
                print(f'\nPARTE DE PARTE: \033[1;33m{parte_partes}\033[m')
                parte_partes = parte_partes.replace('/', '-')
            processo = processo.replace('/', '-')
            parte = parte.replace('/', '-')
            
            # VERIFICA SE JÁ EXISTE OS ARQUIVOS
            if os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}.xlsx'):
                print('\n\033[1;31mARQUIVO JÁ RECUPERADO EM UMA EXECUÇÃO ANTERIOR\033[m')
                return
            if os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}.xlsx'):
                print('\n\033[1;31mARQUIVO JÁ RECUPERADO EM UMA EXECUÇÃO ANTERIOR\033[m')
                return
            # VERIFICA SE JÁ EXISTE OS ARQUIVOS
            
            # clica na aba detalhes
            self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
            self.espera_elemento_disponivel_e_clica(locator=(By.CSS_SELECTOR, '#idSpanAbaDetalhes a'))
            
            self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
            colunas = self.espera_e_retorna_lista_de_elementos_text_from_id_esse_tribunal(locator=(By.CSS_SELECTOR, '.classSpanDetalhesLabel'))
            
            
            self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
            dados_detalhes = self.espera_e_retorna_lista_de_elementos_text(locator=(By.CSS_SELECTOR, '.classSpanDetalhesTexto'))
            
            df = pd.DataFrame([dados_detalhes], columns=colunas)
            
            if parte_partes:
                if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/'):
                    os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/')
                    df.to_excel(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}.xlsx', index=False)
                else:
                    df.to_excel(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{parte_partes.upper()}/{processo.upper()}.xlsx', index=False)
            else:
                if not os.path.exists(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/'):
                    os.makedirs(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/')
                    df.to_excel(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}.xlsx', index=False)
                else:
                    df.to_excel(f'DOWNLOADS/STJ - SUPERIOR TRIBUNAL DE JUSTICA/PARTES/{parte.upper()}/{processo.upper()}.xlsx', index=False)
            del df, colunas, dados_detalhes
            print(f'\n\nPROCESSO: \033[1;32m{processo} RECUPERADO!\033[m')
            
    def pesquisa_stj(self):
        if len(partes) >= 1:
            for parte in partes:
                url = 'https://processo.stj.jus.br/processo/pesquisa/'
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f'\n\n\033[0;31mPegando informações do site: STJ - SUPERIOR TRIBUNAL DE JUSTICA\n'
                    f'{url}\033[m')
                print(f'\n\nParte à pegar: \033[0;32m{parte}\033[m')
                
                self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                self.espera_elemento_e_envia_send_keys(locator=(By.CSS_SELECTOR, '#idParteNome'), string=parte)
                
                self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                self.espera_elemento_disponivel_e_clica(locator=(By.CSS_SELECTOR, '#idComboFoneticaPhonosParte_1'))

                self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                self.espera_elemento_disponivel_e_clica(locator=(By.CSS_SELECTOR, '#idBotaoPesquisarFormularioExtendido'))

                self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                qtd_partes_de_partes = self.espera_e_retorna_elemento_text((By.CSS_SELECTOR, '#idDivBlocoMensagem > div > b'))
                qtd_partes_de_partes_int = int(qtd_partes_de_partes)
                
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
                if qtd_partes_de_partes_int >= 1:
                    # lista das 'partes das partes'
                    self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                    lista_partes_de_partes_sel = self.espera_e_retorna_lista_de_elementos(locator=(By.CSS_SELECTOR, '.clsPessoaNome'))
                    
                    for parte_num in range(len(lista_partes_de_partes_sel)):
                        self.chrome.implicitly_wait(1)
                        nome_parte_parte = lista_partes_de_partes_sel[parte_num].text
                        lista_partes_de_partes_sel[parte_num].click()
                        
                        # lista de processos da parte
                        self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                        id_de_verificacao = self.chrome.find_element(By.CSS_SELECTOR, '#idSpanConteudoCentro > div:nth-child(2)').get_attribute('id')
                        
                        # se existir a div de mensagem que existe uma lista de processos
                        """
                        EXEMPLO: Listando processos relacionados a(s) parte(s) com nome WHIRLPOOL S.A..
                                            Pesquisa resultou em 7 registro(s)!
                        """
                        if 'idDivBlocoMensagem' == id_de_verificacao:
                            qtd_processos_recuperados = 0  # contador de processos recuperados
                            
                            self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                            qtd_processos_para_recuperar_str = self.espera_e_retorna_elemento_text((By.CSS_SELECTOR, '#idDivBlocoMensagem > div > b'))
                            
                            qtd_processos_para_recuperar = int(qtd_processos_para_recuperar_str)
                            
                            registros = self.espera_e_retorna_lista_de_elementos((By.CSS_SELECTOR, '.classSpanProcessoUF a'))
                            
                            while qtd_processos_recuperados != qtd_processos_para_recuperar:
                                if qtd_processos_para_recuperar > 40:  # se existir mais de 40, tem paginacao
                                    len_registros_for_range = len(registros)
                                    registros_range = range(len_registros_for_range)
                                    for registro_do_registro in registros_range:
                                        self.chrome.implicitly_wait(1)
                                        titulo_processo = registros[registro_do_registro].text
                                        registros[registro_do_registro].click()  # clica no processo
                                        self.faz_csv_detalhes(
                                            parte,
                                            titulo_processo,
                                            parte_partes=nome_parte_parte,
                                            procs_p_rec=qtd_processos_para_recuperar,
                                            procs_rec=qtd_processos_recuperados)
                                        qtd_processos_recuperados += 1
                                        self.chrome.back()
                                        self.chrome.refresh()
                                        del registros
                                        
                                        self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                                        registros = self.espera_e_retorna_lista_de_elementos((By.CSS_SELECTOR, '.classSpanProcessoUF a'))
                                    else:
                                        try:
                                            button_existe = self.chrome.find_element(By.CSS_SELECTOR, '#idDivBlocoPaginacaoTopo > div > span > span.classSpanPaginacaoImagensDireita > a').get_attribute('title')
                                            
                                            if button_existe == 'próxima página':
                                                self.chrome.refresh()
                                                self.espera_enquanto_nao_tem_resposta_do_site((By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                                                self.chrome.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)
                                                self.espera_elemento_disponivel_e_clica((By.CSS_SELECTOR, '#idDivBlocoPaginacaoBase > div > span > span.classSpanPaginacaoImagensDireita > a:nth-child(1)'))
                                                
                                                del registros
                                                registros = self.espera_e_retorna_lista_de_elementos((By.CSS_SELECTOR, '.classSpanProcessoUF a'))
                                        except Exception:
                                            if qtd_processos_recuperados == qtd_processos_para_recuperar:
                                                self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                                                page_atual = int(self.espera_e_retorna_conteudo_do_atributo_do_elemento_text('value', (By.CSS_SELECTOR, '#idDivBlocoPaginacaoTopo > div > span > span.classSpanPaginacaoPaginaTextoInterno > input[type=text]')))
                                                
                                                for voltar in range(page_atual):
                                                    self.chrome.back()
                                                else:
                                                    # atualiza a lista de partes
                                                    self.chrome.refresh()
                                                    qtd_processos_recuperados = 0
                                                    qtd_processos_para_recuperar = 0
                                                    
                                                    self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                                                    lista_partes_de_partes_sel = self.espera_e_retorna_lista_de_elementos(locator=(By.CSS_SELECTOR, '.clsPessoaNome'))
                                else: # se tem menos ou sao até 40 nao tem paginacao
                                    self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                                    registros = self.espera_e_retorna_lista_de_elementos((By.CSS_SELECTOR, '.classSpanProcessoUF a'))
                                    for registro_do_registro in range(len(registros)):
                                        self.chrome.implicitly_wait(1)
                                        titulo_processo = registros[registro_do_registro].text
                                        registros[registro_do_registro].click()
                                        self.faz_csv_detalhes(
                                                    parte,
                                                    titulo_processo,
                                                    parte_partes=nome_parte_parte,
                                                    procs_rec=qtd_processos_recuperados,
                                                    procs_p_rec=qtd_processos_para_recuperar
                                                    )
                                        qtd_processos_recuperados += 1
                                        
                                        self.chrome.back()
                                        self.chrome.refresh()
                                        del registros
                                        self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                                        registros = self.espera_e_retorna_lista_de_elementos((By.CSS_SELECTOR, '.classSpanProcessoUF a'))
                                    else:
                                        self.chrome.back()
                                        self.chrome.refresh()
                                        qtd_processos_recuperados = 0
                                        qtd_processos_para_recuperar = 0
                                        self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                                        lista_partes_de_partes_sel = self.espera_e_retorna_lista_de_elementos(locator=(By.CSS_SELECTOR, '.clsPessoaNome'))
                            else:
                                qtd_processos_recuperados = 0
                                qtd_processos_para_recuperar = 0
                                self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                                lista_partes_de_partes_sel = self.espera_e_retorna_lista_de_elementos(locator=(By.CSS_SELECTOR, '.clsPessoaNome'))
                        # se não houver uma div falando que tem uma lista de processos, existe somente um
                        else:
                            titulo_processo = self.espera_e_retorna_elemento_text((By.CSS_SELECTOR, '#idSpanClasseDescricao'))
                            self.faz_csv_detalhes(
                                                parte,
                                                titulo_processo,
                                                parte_partes=nome_parte_parte)
                            self.chrome.back()
                            self.chrome.refresh()
                            self.espera_enquanto_nao_tem_resposta_do_site(locator=(By.CSS_SELECTOR, '#idInterfaceVisualMenuLateralLinkNivel1_Pai1'))
                            lista_partes_de_partes_sel = self.espera_e_retorna_lista_de_elementos(locator=(By.CSS_SELECTOR, '.clsPessoaNome'))
                    else:
                        # returna para a pege para pesquisar a nova parte
                        self.chrome.get('https://processo.stj.jus.br/processo/pesquisa/')
                else:
                    print('Nenhuma parte encontrada!')
                    self.chrome.get('https://processo.stj.jus.br/processo/pesquisa/')
            else:
                self.chrome.quit()
                print(f'\n\n\033[0;31m === O ROBÔ FINALIZOU AS CONSULTAS DE {len(partes)} PARTES === \033[m\n\n')
        

if __name__ == '__main__':     
    executa = RoboStj(headless=0)
    executa.pesquisa_stj()