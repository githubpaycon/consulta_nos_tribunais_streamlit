from selenium.webdriver.support import expected_conditions as EC

def url_atual(driver):
    """
    ### Essa função retorna a url atual
    """
    return driver.current_url


def print_url_atual(driver):
    """
    ### Essa função mostra na tela (print) a url atual
    """
    print(driver.current_url)

        
def espera_elemento_disponivel_e_clica(driver, wdw, locator: tuple):
    """
    ### Essa função espera o elemento ficar disponível (element_to_be_clickable | clicavel) e clica assim que disponível
    #### Parâmetros
    * driver -> Seu webdriver -> chrome, firefox
    * wdw -> o WebDriverWait que servirá para fazer a espera do elemento -> wdw = WebDriverWait(your_webdriver, timeout=10) 
    * locator -> Tupla para recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    
    # espera o item estar disponível quando disponível.
    wdw.until(EC.element_to_be_clickable(locator), message='O tempo limite para achar o WebElement foi finalizado!')
    # clica no elemento assim que disponível
    driver.find_element(*locator).click()


def espera_elemento(wdw, locator: tuple):
    """
    ### Essa função espera o elemento ficar disponível (element_to_be_clickable) e retorna o valor padrão do until (True or False)
    #### Parâmetros
    * wdw -> o WebDriverWait que servirá para fazer a espera do elemento -> wdw = WebDriverWait(your_webdriver, timeout=10) 
    * locator -> Tupla para recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    
    return wdw.until(EC.element_to_be_clickable(locator), message='O tempo limite para achar o WebElement foi finalizado!')


def espera_elemento_e_envia_send_keys(driver, wdw, string, locator: tuple):
    """
    ### Essa função espera o elemento (element_to_be_clickable) e envia a string enviada por você para o elemento
    ### O elemento deve ser um tipo de input ou textarea para entrada de dados com o usuário
    ### Parâmetros
    #### * string -> String ou número que deseja enviar para o elemento
    #### * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    #### * driver -> Seu webdriver -> chrome, firefox
    #### * wdw -> o WebDriverWait que servirá para fazer a espera do elemento -> wdw = WebDriverWait(your_webdriver, timeout=10) 
    """
    
    # espera o item estar disponível quando disponível JA ENTRA NELE
    wdw.until(EC.element_to_be_clickable(locator))
    
    # Envia string para o elemento
    driver.find_element(*locator).send_keys(string)
    
    
def espera_e_retorna_lista_de_elementos(driver, wdw, locator: tuple):
    """
    ### Essa função espera os elementoS ficarem disponíveis (element_to_be_clickable) e retorna A LISTA DE ELEMENTOS
    #### Parâmetros
    * driver -> Seu webdriver -> chrome, firefox
    * wdw -> o WebDriverWait que servirá para fazer a espera do elemento -> wdw = WebDriverWait(your_webdriver, timeout=10) 
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_elements(*locator)


def espera_e_retorna_lista_de_elementos_text_from_id(driver, wdw, locator: tuple):
    """
    ### Essa função espera os elementoS ficarem disponíveis (element_to_be_clickable) e retorna A LISTA DE ELEMENTOS COM UM NÚMERO DE IDENTIFICAÇÃO NO FINAL
    ### EX -> [ADV 1, ADV 2, JUR 3, OPS 4]
    ## ESSA FUNÇÃO NÃO ADICIONA ID EM STRINGS VAZIAS!
    #### Parâmetros
    * driver -> Seu webdriver -> chrome, firefox
    * wdw -> o WebDriverWait que servirá para fazer a espera do elemento -> wdw = WebDriverWait(your_webdriver, timeout=10) 
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
    
    
def espera_e_retorna_lista_de_elementos_text_from_id_esse_tribunal(driver, wdw, locator: tuple):
    """
    ### Essa função espera os elementoS ficarem disponíveis (element_to_be_clickable) e retorna A LISTA DE ELEMENTOS COM UM NÚMERO DE IDENTIFICAÇÃO NO FINAL
    ### EX -> [ADV col1, ADV col2, JUR col3, OPS col4]
    ### ESSA FUNÇÃO ENCONTRA STRINGS VAZIAS E ADICIONA ESSE TEXTO NELA: STRING_VAZIA col{?}
    #### Parâmetros
    * driver -> Seu webdriver -> chrome, firefox
    * wdw -> o WebDriverWait que servirá para fazer a espera do elemento -> wdw = WebDriverWait(your_webdriver, timeout=10) 
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    
    wdw.until(EC.element_to_be_clickable(locator))
    webelements = driver.find_elements(*locator)
    id = 1
    elementos_com_id = []
    for element in webelements:
        if element.text == ' ':
            elementos_com_id.append(f'STRING_VAZIA col{id}')
        else:
            elementos_com_id.append(f'{element.text} col{id}')
        id += 1
    else:
        return elementos_com_id


def espera_e_retorna_lista_de_elementos_text(driver, wdw, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
    """
    ### Essa função espera os elementoS ficarem disponíveis (element_to_be_clickable) e retorna A LISTA DOS TEXTOS DOS ELEMENTOS
    #### Parâmetros
    * driver -> Seu webdriver -> chrome, firefox
    * wdw -> o WebDriverWait que servirá para fazer a espera do elemento -> wdw = WebDriverWait(your_webdriver, timeout=10) 
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    
    ### FORMA DE UTILIZAÇÃO
    #### textos_dos_elementos = espera_e_retorna_lista_de_elementos_text((By.CSS_SELECTOR, '.class_elements'))
    #### retorna uma lista
    """
    
    wdw.until(EC.element_to_be_clickable(locator))
    elements = driver.find_elements(*locator)
    return [element.text for element in elements]


def espera_e_retorna_conteudo_do_atributo_do_elemento_text(driver, wdw, atributo : str, locator: tuple):
    """
    ### Essa função espera o elemento ficar disponível (element_to_be_clickable) e retorna o conteudo do atributo escolhido
    #### Parâmetros
    * driver -> Seu webdriver -> chrome, firefox
    * wdw -> o WebDriverWait que servirá para fazer a espera do elemento -> wdw = WebDriverWait(your_webdriver, timeout=10) 
    * atributo -> 'href' 'class' 'onclick'...
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    
    wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_element(*locator).get_attribute(atributo)


def espera_e_retorna_conteudo_dos_atributos_dos_elementos_text(driver, wdw, atributo, locator: tuple=("BY_SELECTOR", "WEBELEMENT")):
    """
    ### Essa função espera o elemento ficare disponível (element_to_be_clickable) e retorna uma lista dos conteúdos dos atributos escolhidos
    #### Parâmetros
    * driver -> Seu webdriver -> chrome, firefox
    * wdw -> o WebDriverWait que servirá para fazer a espera do elemento -> wdw = WebDriverWait(your_webdriver, timeout=10) 
    * atributo -> 'href' 'class' 'onclick'...
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    
    wdw.until(EC.element_to_be_clickable(locator))
    atributos = driver.find_elements(*locator)
    elementos_atributos = [atributo_selen.get_attribute(atributo) for atributo_selen in atributos]
    return elementos_atributos
        
        
def espera_e_retorna_elemento_text(driver, wdw, locator: tuple):
    """
    ### Essa função espera o elemento ficar disponível (element_to_be_clickable) e retorna o texto dele
    #### Parâmetros
    * driver -> Seu webdriver -> chrome, firefox
    * wdw -> o WebDriverWait que servirá para fazer a espera do elemento -> wdw = WebDriverWait(your_webdriver, timeout=10) 
    * locator -> A forma de se recuperar um elemento -> (By.CSS_SELECTOR, 'html')
    """
    wdw.until(EC.element_to_be_clickable(locator))
    return driver.find_element(*locator).text
    
    
def espera_abrir_n_de_janelas_e_muda_para_a_ultima_janela(driver, wdw, num_de_janelas: int=2):
    """
    ### Essa função espera a quantidades de janelas enviadas por ti, e muda para a ultima janela aberta
    
    #### Parâmetros
    * driver -> Seu webdriver -> chrome, firefox
    * wdw -> o WebDriverWait que servirá para fazer a espera do elemento -> wdw = WebDriverWait(your_webdriver, timeout=10) 
    * num_de_janelas -> quantidade de janelas que você espera ter abertas
    """
    # verifica se abriu x numeros de janelas
    print(f'Você está na janela de id -> {driver.current_window_handle}')
    wdw.until(EC.number_of_windows_to_be(num_de_janelas))
    print(f'Agora, você tem {len(driver.window_handles)} janelas abertas')
    todas_as_windows = driver.window_handles
    driver.switch_to.window(todas_as_windows[-1])
    print(f'Agora, você está na janela de id -> {driver.current_window_handle}')
    
    
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
    """
    Fecha a janela / aba atual do navegador utilizado
    """
    driver.close()


def restart_all_program():
    """
    Essa função simplesmente reinicia o código todo
    """
    import sys
    import os
    python = sys.executable
    os.execl(python, python, *sys.argv)