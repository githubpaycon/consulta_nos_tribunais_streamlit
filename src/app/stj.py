from funcsforspo_l.fpython.functions_for_py import *
from funcsforspo_l.fselenium.functions_selenium import *
import pytz
from src.base.base import *

class Stj(Bot):
    def __init__(self, headless, download_files, parte:str, tipo_de_parte:list) -> None:
        self.URL = 'https://processo.stj.jus.br/processo/pesquisa/'
        self.PARTE = parte
        self.TIPO_PARTE = tipo_de_parte
        
        # -- COLUNAS DF -- #
        self.processo_uf = []
        self.num_registro = []
        self.data_autucacao = []
        self.processo_eletronico = []
        self.link = []
        # -- COLUNAS DF -- #

        
        super().__init__(headless, download_files)
        
    def pesquisa(self):
        faz_log_st(f'Pesquisando pela parte {self.PARTE}')
        try:
            self.DRIVER.get(self.URL)
        except WebDriverException:
            faz_log_st('Ocorreu um erro no Driver, pesquise novamente...')
            self.DRIVER.close()
        
        # -- RECUPERA OS DADOS -- #
        faz_log_st('Preenchendo os dados')
        
        # Preenche a parte do tipo da parte, Autor, Réu, Outros
        for tipo_parte in self.TIPO_PARTE:
            if 'Autor' in tipo_parte:
                espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#idParteAutorTemp'))
            if 'Réu' in tipo_parte:
                espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#idParteReuTemp'))
            if 'Autor' in tipo_parte:
                espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#idParteOutrosTemp'))
        
        # Envia a parte no input
        espera_elemento_e_envia_send_keys(self.WDW, self.PARTE.strip(), (By.CSS_SELECTOR, '#idParteNome'))

        # Clica em Igual
        espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#idComboFoneticaPhonosParte_1'))

        # Clica em Consultar
        espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#idBotaoPesquisarFormularioExtendido'))
        
        # Marca todos
        espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#idBotaoMarcarTodos'))

        # clica em pesquisar marcados
        espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#idBotaoPesquisarMarcados'))

        qtd_registros = espera_e_retorna_elemento_text(self.WDW, (By.CSS_SELECTOR, '#idDivBlocoMensagem > div > b'))
        faz_log_st(f'Foram encontrados {qtd_registros}')
        
        while True:
            registros = espera_e_retorna_lista_de_elementos(self.WDW, (By.CSS_SELECTOR, '#idBlocoInternoLinhasProcesso > div~div'))

            for num, registro in enumerate(registros):
                # faz_log_st(f'Indo para o registro {num}')

                processo_uf = registro.find_element(By.CSS_SELECTOR, 'span>span>span>span>a').text
                num_registro = registro.find_element(By.CSS_SELECTOR, 'span>span>span>span~span>a').text
                data_autucacao = registro.find_element(By.CSS_SELECTOR, 'span>span>span~span>span[title="data de autuação"]').text
                processo_eletronico = registro.find_element(By.CSS_SELECTOR, 'span>span>span~span>span[class="clsBlocoProcessoColuna clsBlocoProcessoColuna4 clsLinhaProcessosFisicoEletronico"]').text
                link = registro.find_element(By.CSS_SELECTOR, 'span>span>span>span>a').get_attribute('href')

                # insert in list for dataframe
                self.processo_uf.append(processo_uf)
                self.num_registro.append(num_registro)
                self.data_autucacao.append(data_autucacao)
                self.processo_eletronico.append(processo_eletronico)
                self.link.append(link)
                print(processo_uf, num_registro, data_autucacao, processo_eletronico, link)
            else:
                try:
                    page_atual = pega_somente_numeros(espera_e_retorna_conteudo_do_atributo_do_elemento_text(self.WDW, 'value', (By.CSS_SELECTOR, 'span.classSpanPaginacaoPaginaTextoInterno> input')))
                    page_a_recuperar = pega_somente_numeros(espera_e_retorna_elemento_text(self.WDW, (By.CSS_SELECTOR, 'span.classSpanPaginacaoPaginaTextoInterno')))
                    qtd_a_recuperar = int(page_a_recuperar) - int(page_atual) 
                    
                    faz_log_st(f'Página que foi extraida: {page_atual} | Quantidade de páginas para extrair: {qtd_a_recuperar}')
                    
                    if page_atual != page_a_recuperar:
                        espera_elemento_disponivel_e_clica(self.WDW3, (By.CSS_SELECTOR, 'span.classSpanPaginacaoImagensDireita > a:nth-child(1) > span'))
                        continue
                    else:
                        faz_log_st('Acabou as páginas')
                        break                        
                except (TimeoutException, NoSuchElementException):
                    faz_log_st('Acabou as páginas')
                    break
        
    def faz_dataframe(self):
        faz_log_st('Fazendo tabela excel...')
        
        dict_df = {
            'PROCESSO / UF':self.processo_uf,
            'NUMERO REGISTRO':self.num_registro,
            'DATA AUTUACAO':self.data_autucacao,
            'PROCESSO ELETRONICO':self.processo_eletronico,
            'LINK DO PROCESSO':self.link
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