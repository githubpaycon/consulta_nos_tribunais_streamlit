from pprint import pprint
import requests
import pandas as pd
from pandas import DataFrame
from funcsforspo_l.fselenium.functions_selenium import cria_user_agent
from funcsforspo_l.fpython.functions_for_py import remover_acentos
import streamlit as st

class Stf:
    def __init__(self, parte):
        self.PARTE = parte


    def faz_dataframe_com_o_json(self, json):
        return pd.json_normalize(json)

    def faz_pesquisa_com_todos_os_valores(self, qtd_registros):
        headers = {
            'authority': 'digital.stf.jus.br',
            'accept': '*/*',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://portal.stf.jus.br',
            'referer': 'https://portal.stf.jus.br/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': cria_user_agent(),
        }

        params = {
            'nome': f'{self.PARTE}',
            'registrosPorPagina': str(qtd_registros),
            'pagina': '1',
        }

        response = requests.get(
            'https://digital.stf.jus.br/integracoes-processos/api/public/partes/processos',
            params=params,
            headers=headers,
        )
        
        response_json = response.json()
        return response_json


    def faz_pesquisa_recupera_qtd_processos(self):
        headers = {
            'authority': 'digital.stf.jus.br',
            'accept': '*/*',
            'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://portal.stf.jus.br',
            'referer': 'https://portal.stf.jus.br/',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': cria_user_agent(),
        }

        params = {
            'nome': f'{self.PARTE}',
            'registrosPorPagina': '20',
            'pagina': '1',
        }

        response = requests.get(
            'https://digital.stf.jus.br/integracoes-processos/api/public/partes/processos',
            params=params,
            headers=headers,
        )
        response_json = response.json()

        from pprint import pprint
        total_registros = response_json['totalDeRegistros']
        return total_registros
    
    def trata_dataframe(self, df) -> DataFrame:
        try:
            del df['id']
        except:...
        
        try:
            del df['pessoaId']
        except:...
        
        try:
            del df['processoId']
        except:...

        df = df.rename(columns={'pessoaNome': 'Parte'})
        df = df.rename(columns={'processoIdentificacao': 'Identificação'})
        df = df.rename(columns={'processoNumeroUnico': 'Número Único'})
        df = df.rename(columns={'processoDataAutuacao': 'Data Autuação'})
        df = df.rename(columns={'processoMeio': 'Meio'})
        df = df.rename(columns={'processoPublicidade': 'Publicidade'})
        df = df.rename(columns={'processoEmTramitacao': 'Trâmite?'})

        return df
        
    def executa_bot(self):
        qtd_processos = self.faz_pesquisa_recupera_qtd_processos()
        st.text(f'Foi encontrado {qtd_processos}')
        json = self.faz_pesquisa_com_todos_os_valores(qtd_processos)
        df = self.faz_dataframe_com_o_json(json['partes'])
        df = self.trata_dataframe(df)
        df.to_excel('EXTRACAO.xlsx', remover_acentos(self.PARTE), index=False)
