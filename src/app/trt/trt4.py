
from src.base.base import *

class TRT4CertidaoTrabalhista(Bot):
    """Certidão de Reclamação Trabalhista Solicitação da Certidão Online de Ações Trabalhistas"""
    def __init__(self, headless, download_files, cnpj:str) -> None:
        self.URL = 'https://pje.trt4.jus.br/certidoes/trabalhista/emissao'  # após o termo=, colocar a parte
        self.CNPJ = cnpj
        self.KEY_CAPTCHA:str = st.secrets["KEY_CAPCHA"]

        super().__init__(headless, download_files)
        
    def pesquisa(self):
        limpa_diretorio(DOWNLOAD_DIR)
        faz_log('Indo para o site')
        self.DRIVER.get(self.URL)
        espera_elemento_e_envia_send_keys(self.WDW, self.CNPJ, (By.CSS_SELECTOR, 'input[aria-label="CNPJ da parte"]'))
        faz_log('capturando captcha')
        captcha_iframe_link = espera_e_retorna_conteudo_do_atributo_do_elemento_text(self.WDW5, 'src', (By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]'))
        sitekey = re.findall(r'&k=\w+', captcha_iframe_link)[-1].replace('&k=', '')
        captcha_type = {
                    'type': '2captcha',
                    'sitekey': sitekey,
                }
        g_recaptcha_response = CaptchaSolver().captchasolver(self.KEY_CAPTCHA, captcha_type)

        espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, '#g-recaptcha-response'), in_dom=True)
        # deixa o textarea visivel
        self.DRIVER.execute_script('document.getElementById("g-recaptcha-response").setAttribute("style", "width: 250px; height: 40px; border: 1px solid rgb(193, 193, 193); margin: 10px 25px; padding: 0px; resize: none; display: visibility;");')
        self.DRIVER.find_element(By.CSS_SELECTOR, '#g-recaptcha-response').send_keys(g_recaptcha_response)            
        
        # executa o script de callback
        faz_log('resolvendo captcha')
        try:
            self.DRIVER.execute_script(f"___grecaptcha_cfg.clients[0].H.H.callback('{g_recaptcha_response}')")
        except JavascriptException:
            self.DRIVER.execute_script(f"___grecaptcha_cfg.clients[0].S.S.callback('{g_recaptcha_response}')")
            
        
        faz_log('Clicando para ir para a certidao')
        espera_elemento_disponivel_e_clica(self.WDW3, (By.CSS_SELECTOR, 'button[type="submit"]'))
        sleep(2)
        faz_log('Clicando para baixar...')
        espera_elemento_disponivel_e_clica(self.WDW10, (By.CSS_SELECTOR, 'button~button'))
        espera_elemento_disponivel_e_clica(self.WDW10, (By.CSS_SELECTOR, 'button~button'))

        faz_log('Verificando se o baixou o arquivo...')
        verifica_se_baixou_o_arquivo(DOWNLOAD_DIR, '.pdf', sleep_time=1)
        sleep(1)
        os.replace(arquivos_com_caminho_absoluto_do_arquivo(DOWNLOAD_DIR)[0], arquivo_com_caminho_absoluto('output', 'certidao_trt4.pdf'))

    def executa_bot(self):
        try:
            self.pesquisa()
        except Exception as e:
            st.exception(e)
            self.DRIVER.close()