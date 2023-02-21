import pandas as pd
import pytz
from src.app.trt.trt2 import TrtSCOAT
from src.app.tst import Tst
from src.exceptions.exceptions import NenhumValorEncontradoStjException
from src.app.stf import Stf
from src.app.stj import Stj
import streamlit as st
from src.base.base import InvalidSessionIdException
import os
from funcsforspo_l.fregex.functions_re import *
from funcsforspo_l.fpython.functions_for_py import *
from src.utils.utils import to_excel_for_download_button, verifica_colunas_stf
import plotly.express as px

from src.widgets.widgets import *


# -- CONFIGURATIONS = START -- #
# timezone = pytz.timezone('America/Sao_Paulo')
# date = datetime.now(tz=timezone).strftime('%d/%m/%Y %H:%M:%S')

VERSION_APP = f'V3.0.0'

st.set_page_config(
    page_title="Consulta nos Tribunais",
    page_icon="justice.png",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://api.whatsapp.com/send?phone=5511985640273',
        'Report a bug': "https://api.whatsapp.com/send?phone=5511985640273",
        'About': f"###### Trabalhando por um futuro melhor (e mais automatizado) com muito amor, inteligência e vontade! Isso é a [Paycon Automações](https://payconautomacoes.com.br/)! | Versão: {VERSION_APP}"
    }
)


st.markdown("""<style type="text/css">
.p {
    color:red;
}
</style>""", True)

# -- SIDEBAR --
bar = st.sidebar
bar.markdown('# Escolha uma ferramenta...')
CHOICE = bar.selectbox('Escolha uma Ferramenta', ['Extração dos Dados', 'Conversar com IA'])
# -- SIDEBAR --

# -- DELETE EXTRACTION --
try:
    os.remove('EXTRACAO.xlsx')
except Exception:
    pass
cria_dir_no_dir_de_trabalho_atual('output')
# -- DELETE EXTRACTION --

# -- CONFIGURATIONS = END-- #

st.image('sucess_logo_paycon.png', width=150)

if CHOICE == 'Extração dos Dados':
    st.title('Consulta nos Tribunais')
    st.header('Captura de processos automaticamente nos tribunais principais tribunais do Brasil')
    st.text('Para consultar nos tribunais, basta apenas escolher o tribunal, enviar o nome da parte e aguardar o resultado em .xlsx')
    st.markdown('###### Tribunais disponíveis atualmente:')
    st.markdown('* STF - Supremo Tribunal Federal')
    st.markdown('* STJ - Superior Tribunal de Justiça')
    st.markdown('* TRT - Captura de Processos Trabalhistas')
    st.markdown('---')
    tribunal = st.selectbox('Escolha o Tribunal:', ['STF - Supremo Tribunal Federal', 'STJ - Superior Tribunal de Justiça', 'Captura de Processos Trabalhistas'])

    if tribunal == 'STF - Supremo Tribunal Federal':
        stf_widget()
    elif tribunal == 'STJ - Superior Tribunal de Justiça':
        stj_widget()
    elif tribunal == 'TST - Tribunal Superior do Trabalho':
        tst_widget()
    elif tribunal == 'Captura de Processos Trabalhistas':
        captura_de_processos_trabalhistas_widget()
    else:
        st.warning('Que pena! Estamos fazendo essa parte! Quem sabe amanhã não aparece aqui esse robô... 👀👀')
if CHOICE == 'Conversar com IA':
    conversar_com_ia()
if CHOICE == 'Consulta CNPJ':
    consulta_cnpj()
