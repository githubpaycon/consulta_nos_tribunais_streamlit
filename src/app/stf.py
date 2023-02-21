from funcsforspo_l.fpython.functions_for_py import *
from funcsforspo_l.fselenium.functions_selenium import *
import pytz
from src.base.base import *

class Stf(Bot):
    def __init__(self, headless, download_files, partes:list|str) -> None:
        self.URL_CLEAR = 'https://portal.stf.jus.br/processos/listarPartes.asp?termo='  # após o termo=, colocar a parte
        self.PARTES = partes
        
        # -- COLUNAS DF -- #
        self.identificacao_col = []
        self.num_unico_col = []
        self.parte_col = []
        self.data_autuacao_col = []
        self.meio_col = []
        self.publicidade_col = []
        self.tramite_col = []
        # -- COLUNAS DF -- #

        
        super().__init__(headless, download_files)
        
    def pesquisa(self):
        if isinstance(self.PARTES, str):
            parte = self.PARTES
            faz_log_st(f'Pesquisando pela parte {parte}')
            try:
                self.DRIVER.get(f'{self.URL_CLEAR}{parte}')
            except WebDriverException:
                faz_log_st('Ocorreu um erro no Driver, pesquise novamente...')
                self.DRIVER.close()
            
            # -- RECUPERA OS DADOS -- #
            try:
                espera_elemento(self.WDW3, (By.CSS_SELECTOR, 'div[class*="conteudo-404"]'))
                faz_log_st('Não existem processos!')
                self.DRIVER.close()
                return
            except TimeoutException:
                try:
                    page_atual = espera_e_retorna_conteudo_do_atributo_do_elemento_text(self.WDW, 'data-pagina', (By.CSS_SELECTOR, 'a[class="paginacao-ir-para-pagina"]'))
                    qtd_processos = espera_e_retorna_elemento_text(self.WDW, (By.CSS_SELECTOR, '#quantidade'))
                    faz_log_st(f'Quantidade de Processos {qtd_processos}')

                    processos_pagination = True

                    for i in range(20):
                        self.DRIVER.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
                    for i in range(20):
                        self.DRIVER.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_UP)


                    processos = espera_e_retorna_lista_de_elementos(self.WDW, (By.CSS_SELECTOR, '#card_processos>div'))
                    while processos_pagination:
                        faz_log_st(f'Pagina atual {page_atual}')
                        for processo in processos:
                            identificacao = processo.find_element(By.CSS_SELECTOR, 'div >h6>span').text
                            num_unico = processo.find_element(By.CSS_SELECTOR, 'div >h6~h6>span').text
                            parte = processo.find_element(By.CSS_SELECTOR, 'div[class="item__descricao item__partes"]').text
                            data_autuacao = processo.find_element(By.CSS_SELECTOR, 'div~div>div>div~div>div~div[class="item__descricao"]').text
                            meio = processo.find_element(By.CSS_SELECTOR, 'div~div>div>div~div~div>div~div[class="item__descricao"]').text
                            publicidade = processo.find_element(By.CSS_SELECTOR, 'div~div>div>div~div~div~div>div~div[class="item__descricao"]').text
                            tramite = processo.find_element(By.CSS_SELECTOR, 'div~div>div>div~div~div~div~div>div~div[class="item__descricao"]').text

                            self.identificacao_col.append(identificacao)
                            self.num_unico_col.append(num_unico)
                            self.parte_col.append(parte)
                            self.data_autuacao_col.append(data_autuacao)
                            self.meio_col.append(meio)
                            self.publicidade_col.append(publicidade)
                            self.tramite_col.append(tramite)
                        else:
                            faz_log_st('Verificando se tem mais paginas...')
                            for i in range(20):
                                self.DRIVER.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)

                            botao_next_ativo = espera_e_retorna_conteudo_do_atributo_do_elemento_text(self.WDW, 'class', (By.CSS_SELECTOR, '#item-proxima-pagina'))
                            if not botao_next_ativo == 'disabled':
                                espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#paginacao-proxima-pagina'))
                                processos = espera_e_retorna_lista_de_elementos(self.WDW, (By.CSS_SELECTOR, '#card_processos>div'))
                                page_atual = espera_e_retorna_conteudo_do_atributo_do_elemento_text(self.WDW, 'data-pagina', (By.CSS_SELECTOR, 'a[class="paginacao-ir-para-pagina"]'))
                            else:
                                faz_log_st('Sem mais processos nessa parte...')
                                processos_pagination = False
                        # -- RECUPERA OS DADOS -- #
                except (TimeoutException, NoSuchElementException):
                    faz_log_st(self.DRIVER.get_screenshot_as_base64())
                    faz_log_st(self.DRIVER.page_source)
                    faz_log_st('Não existe processos para a parte - ou o site está fora do ar...')
                    self.identificacao_col.append('Não existe processos para a parte - ou o site está fora do ar...')
                    self.num_unico_col.append('Não existe processos para a parte - ou o site está fora do ar...')
                    self.parte_col.append(parte)
                    self.data_autuacao_col.append('Não existe processos para a parte - ou o site está fora do ar...')
                    self.meio_col.append('Não existe processos para a parte - ou o site está fora do ar...')
                    self.publicidade_col.append('Não existe processos para a parte - ou o site está fora do ar...')
                    self.tramite_col.append('Não existe processos para a parte - ou o site está fora do ar...')
                except Exception as e:
                        faz_log_st(self.DRIVER.get_screenshot_as_base64())
                        faz_log_st(self.DRIVER.page_source)
                        st.exception(e) 
        
    def faz_dataframe(self):
        faz_log_st('Fazendo tabela excel...')
        dict_df = {
            'PARTE': self.parte_col,
            'IDENTIFICACAO': self.identificacao_col,
            'NUMERO UNICO': self.num_unico_col,
            'DATA AUTUACAO': self.data_autuacao_col,
            'MEIO': self.meio_col,
            'PUBLICIDADE': self.publicidade_col,
            'TRAMITE': self.tramite_col,
        }
        df = pd.DataFrame(dict_df)
        try:
            df.to_excel('EXTRACAO.xlsx', sheet_name=datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%d.%m.%Y %H_%M_%S"), index=False)
        except PermissionError:
            faz_log_st('Feche a tabela, aguardando 10 segundos...')
            sleep(10)
            df.to_excel('EXTRACAO.xlsx', sheet_name=datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%d.%m.%Y %H_%M_%S"), index=False)
        self.DRIVER.close()

    def executa_bot(self):
        self.pesquisa()
        self.faz_dataframe()