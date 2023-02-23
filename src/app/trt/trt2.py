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
            verifica_se_baixou_o_arquivo('downloads', '.pdf', sleep_time=0)
            os.replace(arquivos_com_caminho_absoluto_do_arquivo(DOWNLOAD_DIR)[0], arquivo_com_caminho_absoluto('output', 'certidao_trt2.pdf'))

    def executa_bot(self):
        try:
            self.pesquisa()
        except Exception as e:
            st.exception(e)
            self.DRIVER.close()
            
