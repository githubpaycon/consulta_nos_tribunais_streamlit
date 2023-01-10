from time import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By




def url_atual(driver):
    """
    ### Essa função retorna a url atual
    """
    return driver.current_url

def print_url_atual(driver):
    """
    ### Essa função printa a url atual
    """
    print(driver.current_url)

        
def espera_elemento_disponivel_e_clica(driver, wdw, locator: tuple):
    """
    ### Essa função espera o elemento ficar disponível (clicavel) e clica assim que disponível
    #### Parâmetros
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    
    # espera o item estar disponível quando disponível JA ENTRA NELE
    wdw.until(EC.element_to_be_clickable(locator))
    # clica no elemento
    driver.find_element(*locator).click()

def espera_elemento_estar_na_tela_para_clicar(driver, wdw, locator: tuple):
    """
    ### Essa função espera o elemento ficar disponível (visibility_of_element_located) e clica assim que disponível
    #### Parâmetros
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    
    # espera o item estar disponível quando disponível JA ENTRA NELE
    wdw.until(EC.visibility_of_element_located(locator))
    # clica no elemento
    driver.find_element(*locator).click()

def espera_elemento(driver, wdw, locator: tuple):
    """### Essa função espera o elemento ficar disponível (clicavel) e retorna o valor padrão do until
    #### Parâmetros
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')"""
    
    return wdw.until(EC.element_to_be_clickable(locator))

def espera_elemento_e_envia_send_keys(driver, wdw, string, locator: tuple):
    """
    ### Essa função espera o elemento (clicavel) e envia a sua string para ele
    ### O elemento deve ser um tipo de input ou textarea para entrada de dados com o user
    ### Parâmetros
    #### * string -> String ou número que deseja enviar para o elemento
    #### * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    
    # espera o item estar disponível quando disponível JA ENTRA NELE
    wdw.until(EC.element_to_be_clickable(locator))
    
    # Envia string para o elemento
    driver.find_element(*locator).send_keys(string)
    
def espera_e_retorna_lista_de_elementos(driver, wdw, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
    """
    ### Essa função espera os elementoS ficarem disponíveis (clicaveis) e retorna A LISTA DE ELEMENTOS
    #### Parâmetros
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    
    wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_elements(*locator)

def espera_e_retorna_lista_de_elementos_text_from_id(driver, wdw, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
    """
    ### Essa função espera os elementoS ficarem disponíveis (clicaveis) e retorna A LISTA DE ELEMENTOS COM UM NÚMERO DE IDENTIFICAÇÃO NO FINAL
    ### EX -> [ADV 1, ADV2, JUR 3, OPS 4]
    ## ESSA FUNÇÃO ADICIONA STRINGS VAZIAS (SEM ID)!
    #### Parâmetros
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    
    wdw.until(EC.element_to_be_clickable(locator))
    webelements = driver.find_elements(*locator)
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
    
def espera_e_retorna_lista_de_elementos_text_from_id_esse_tribunal(driver, wdw, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
    """
    ### Essa função espera os elementoS ficarem disponíveis (clicaveis) e retorna A LISTA DE ELEMENTOS COM UM NÚMERO DE IDENTIFICAÇÃO NO FINAL
    ### EX -> [ADV col1, ADV col2, JUR col3, OPS col4]
    ## AQUI ELE ACHA A COLUNA SEM NADA QUE É A COLUNA COM OS VOLUMES
    ## ESSA FUNÇÃO ADICIONA STRINGS VAZIAS (SEM ID)!
    #### Parâmetros
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    
    wdw.until(EC.element_to_be_clickable(locator))
    webelements = driver.find_elements(*locator)
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

def espera_e_retorna_lista_de_elementos_text(driver, wdw, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
    """
    ### Essa função espera os elementoS ficarem disponíveis (clicaveis) e retorna A LISTA DOS TEXTOS DOS ELEMENTOS
    #### Parâmetros
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    
    ### FORMA DE UTILIZAÇÃO
    #### minha_lista_de_textos_dos_elementos = espera_e_retorna_lista_de_elementos_text(
    #### (By.CSS_SELECTOR, '.class_elements')
    #### )
    """
    
    wdw.until(EC.element_to_be_clickable(locator))
    elements = driver.find_elements(*locator)
    return [element.text for element in elements]

def espera_e_retorna_conteudo_do_atributo_do_elemento_text(driver, wdw, atributo, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
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
    
    wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_element(*locator).get_attribute(atributo)

def espera_e_retorna_conteudo_dos_atributos_dos_elementos_text(driver, wdw, atributo, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
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
    
    wdw.until(EC.element_to_be_clickable(locator))
    atributos = driver.find_elements(*locator)
    elementos_atributos = [atributo_selen.get_attribute(atributo) for atributo_selen in atributos]
    return elementos_atributos
        
def espera_e_retorna_elemento_text(driver, wdw, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
    """
    ### Essa função espera o elemento ficar disponível (clicavel) e retorna o texto dele
    #### Parâmetros
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_element(*locator).text
    
def espera_abrir_n_de_janelas_e_muda_para_a_ultima_janela(driver, wdw, num_de_janelas: int=2):
    # verifica se abriu x numeros de janelas
    print(f'Você está na janela -> {driver.current_window_handle}')
    wdw.until(EC.number_of_windows_to_be(num_de_janelas))
    print(f'Agora, você tem {len(driver.window_handles)} janelas abertas')
    todas_as_windows = driver.window_handles
    driver.switch_to.window(todas_as_windows[-1])
    print(f'Agora, você está na janela -> {driver.current_window_handle}')
    
    
def espera_por_varios_elementos(driver, wdw, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
    """
    ### Essa função espera o elemento ficar disponível (clicavel) e retorna o texto dele
    #### Parâmetros
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    return wdw.until(EC.visibility_of_all_elements_located(locator))
    
def find_window_to_title_contain(driver, title_contain_switch: str): # quero que pelo menos um pedaco do titulo que seja str
    """
    ### Essa função muda de janela quando o título tiver pelo menos algo igual ao parametro enviado
    #### Ex -> Minha janela = janela
    
    para cada janela em ids das janelas
    muda para a janela
    se a janela for ao menos de um pedaço do titulo que passei
        em title_contain_switch
    para de executar
    """
    window_ids = driver.window_handles # ids de todas as janelas

    for window in window_ids:
        driver.switch_to_window(window)  
        if title_contain_switch in driver.title:
            break
    else:
        print(f'Janela não encontrada!\n'
            f'Verifique o valor enviado {title_contain_switch}')
    
def fecha_janela_atual(driver):
    driver.close()
    
    
def clica_tab_do_teclado(driver, locator : tuple=(By.CSS_SELECTOR, 'body')):
    """
    Lista de teclas
    
    ADD	ALT	ARROW_DOWN
    ARROW_LEFT	ARROW_RIGHT	ARROW_UP
    BACKSPACE	BACK_SPACE	CANCEL
    CLEAR	COMMAND	CONTROL
    DECIMAL	DELETE	DIVIDE
    DOWN	END	ENTER
    EQUALS	ESCAPE	F1
    F10	F11	F12
    F2	F3	F4
    F5	F6	F7
    F8	F9	HELP
    HOME	INSERT	LEFT
    LEFT_ALT	LEFT_CONTROL	LEFT_SHIFT
    META	MULTIPLY	NULL
    NUMPAD0	NUMPAD1	NUMPAD2
    NUMPAD3	NUMPAD4	NUMPAD5
    NUMPAD6	NUMPAD7	NUMPAD8
    NUMPAD9	PAGE_DOWN	PAGE_UP
    PAUSE	RETURN	RIGHT
    SEMICOLON	SEPARATOR	SHIFT
    SPACE	SUBTRACT	TAB
    
    """
    driver.find_element(*locator).send_keys(Keys.TAB)

    
def restart_all_program():
    import sys
    import os
    python = sys.executable
    os.execl(python, python, *sys.argv)