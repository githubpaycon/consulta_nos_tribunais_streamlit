from funcsforspo_l.fpython.functions_for_py import *
from funcsforspo_l.fselenium.functions_selenium import *
from funcsforspo_l.fpdf.focr.orc import faz_ocr_em_pdf_offline
from src.utils.captcha.captcha import CaptchaSolver
import pytz
import os
from src.base.base import *

class TrtSCOAT(Bot):
    """Certidão de Reclamação Trabalhista Solicitação da Certidão Online de Ações Trabalhistas"""
    def __init__(self, headless, download_files, cnpj:str) -> None:
        self.URL = 'https://aplicacoes10.trt2.jus.br/certidao_trabalhista_eletronica/public/index.php/index/solicitacao'  # após o termo=, colocar a parte
        self.CNPJ = cnpj
        
        # -- COLUNAS DF -- #
        self.processos = []
        self.KEY_CAPTCHA:str = st.secrets["KEY_CAPCHA"]
        # -- COLUNAS DF -- #

        super().__init__(headless, download_files)
        
    def pesquisa(self):
        if isinstance(self.CNPJ, str):
            self.DRIVER.get(self.URL)
            espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#tipoDocumentoPesquisado-2'))
            espera_elemento_e_envia_send_keys(self.WDW, self.CNPJ, (By.CSS_SELECTOR, '#numeroDocumentoPesquisado'))
            espera_elemento_e_envia_send_keys(self.WDW, self.CNPJ, (By.CSS_SELECTOR, '#nomePesquisado'))

            while True:
                img = espera_e_retorna_conteudo_do_atributo_do_elemento_text(self.WDW, 'src', (By.CSS_SELECTOR, '#captcha-element > table > tbody > tr:nth-child(1) > td:nth-child(1) > img'))
                captcha_type = {
                    'type': 'image',
                    'content': img
                }
                captcha_text = CaptchaSolver().captchasolver(self.KEY_CAPTCHA, captcha_type)
                espera_input_limpa_e_envia_send_keys(self.WDW, captcha_text, (By.CSS_SELECTOR, '#captcha-input'))
                espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#submit'))
                try:
                    espera_elemento(self.WDW3, (By.CSS_SELECTOR, '#certidoes-ul-erros > li'), True)
                    continue
                except Exception:
                    break

            espera_elemento_disponivel_e_clica(self.WDW120, (By.CSS_SELECTOR, '#main-content button'))
            if verifica_se_baixou_o_arquivo('downloads', '.pdf'):
                file = arquivos_com_caminho_absoluto_do_arquivo('downloads')[0]
                dados = faz_ocr_em_pdf_offline(path_pdf=file)
                processos = re.findall(r'\d{20}', string=dados)
                qtd_processos = re.findall(r'Total de Processos: \d+', dados)
                qtd_processos = qtd_processos[-1]
                faz_log_st(qtd_processos)
                for i in processos:
                    self.processos.append(str(i))
            
    def faz_dataframe(self):
        faz_log_st('Fazendo tabela excel...')
        dict_df = {
            'PROCESSOS': self.processos
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