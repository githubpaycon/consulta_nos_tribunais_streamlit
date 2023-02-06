from twocaptcha import TwoCaptcha
from twocaptcha.api import ApiException
from twocaptcha.api import NetworkException
from funcsforspo_l.fpython.functions_for_py import *
        
class CaptchaSolver:
    def captchasolver(self, captcha_key:str, type_captcha:dict, timeout:int=120):
        """

        Args:
            captcha_key (str): captcha_key
            type_captcha (dict): {
                                    'type': 'image',
                                    'content': image_for_2captcha
                                }

        Returns:
            bool: False if exception or str for captcha
        """
        solver = TwoCaptcha(captcha_key, defaultTimeout=timeout)
        
        if type_captcha['type'] == 'image':
            try:
                result = solver.normal(file=type_captcha['content'])
                if isinstance(result['code'], str):
                    return result['code']
                else:
                    return False
            except ApiException as e:
                e = str(e)
                if ('ERROR_ZERO_BALANCE' in e):
                    faz_log('Acabou os créditos no TwoCaptcha.')
                    return False
                if ('ERROR_NO_SLOT_AVAILABLE' in e):
                    faz_log('Captcha sobrecarregado... Tentando novamente daqui 7 segundos')
                    return False
                if ('ERROR_WRONG_USER_KEY' in e):
                    faz_log('Key 2captcha inválido...')
                    return False
                if ('ERROR_KEY_DOES_NOT_EXIST' in e):
                    faz_log('Key 2Captcha inexistente...')
                    return False
                if ('ERROR_ZERO_CAPTCHA_FILESIZE' in e):
                    faz_log('Erro na imagem ao enviar...')
                    return False
                if ('ERROR_TOO_BIG_CAPTCHA_FILESIZE' in e):
                    faz_log('Erro na imagem ao enviar...')
                    return False
                if ('ERROR_IMAGE_TYPE_NOT_SUPPORTED' in e):
                    faz_log('Erro na imagem ao enviar...')
                    return False
                if ('IP_BANNED' in e):
                    faz_log('IP local banido...')
                    faz_log('Aguardando 5 minutos...')
                    sleep(510)
                    return False
                if ('CAPCHA_NOT_READY' in e):
                    faz_log('Captcha não resolvido, tentando outra imagem...')
                    sleep(5)
                    return False
                else:
                    faz_log(repr(e), 'c*')
                    faz_log('Erro no TwoCaptcha, verifique o Log.')
            except NetworkException:
                return False