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
CHOICE = bar.selectbox('Escolha uma Ferramenta', ['Extração dos Dados']) # , 'Analise Dos Dados Extraidos'
# -- SIDEBAR --

# -- DELETE EXTRACTION --
try:
    os.remove('EXTRACAO.xlsx')
except Exception:
    pass
# -- DELETE EXTRACTION --

# -- CONFIGURATIONS = END-- #

# TrtSCOAT(False, True, '40.432.544/0001-47').executa_bot()

# ================================ #
# ====== EXTRAÇÃO DOS DADOS ====== #
# ================================ #
st.image('sucess_logo_paycon.png', width=150)
if CHOICE == 'Extração dos Dados':
    st.title('Consulta nos Tribunais')
    st.header('Captura de processos automaticamente nos tribunais principais tribunais do Brasil')
    st.text('Para consultar nos tribunais, basta apenas escolher o tribunal, enviar o nome da parte e aguardar o resultado em .xlsx')
    st.markdown('###### Tribunais disponíveis atualmente:')
    st.markdown('* STF - Supremo Tribunal Federal')
    st.markdown('* STJ - Superior Tribunal de Justiça')
    st.markdown('* TRT2 - Solicitação de Ações Trabalhistas')
    st.markdown('---')
    tribunal = st.selectbox('Escolha o Tribunal:', ['STF - Supremo Tribunal Federal', 'STJ - Superior Tribunal de Justiça', 'TRT2 - Solicitação da Certidão Online de Ações Trabalhistas'])

    if tribunal == 'STF - Supremo Tribunal Federal':
        st.markdown('<p class="p">* Insira uma parte válida!</p>', True)
        parte = st.text_input('Parte:').strip()
        stf_button = st.button('Pesquisar no STF', 'stf')
        if stf_button:
            if parte == '':
                st.warning('Parte não foi preenchida! ☹️')
            else:
                with st.expander('Execução do robô...'):
                    try:
                        stf = Stf(True, False, parte)
                        stf.executa_bot()
                        st.balloons()
                        st.success('Robô finalizado!')
                        df_xlsx = to_excel_for_download_button('EXTRACAO.xlsx')
                        st.download_button(label='📥 Baixar a Extração...',
                                            data=df_xlsx ,
                                            file_name=f'extraction_STF_{parte.lower().strip()}.xlsx')
                    except InvalidSessionIdException:
                        st.warning('Ocorreu um erro inesperado, reexecute a pesquisa.')

    elif tribunal == 'STJ - Superior Tribunal de Justiça':
        st.markdown('<p class="p">* Insira uma parte válida!</p>', True)
        tipo_de_parte = st.multiselect('Gostaria que a parte fosse:', ['Autor', 'Réu', 'Outros...'], default=['Autor', 'Réu', 'Outros...'])
        parte = st.text_input('Parte:').strip()
        stj_button = st.button('Pesquisar no STJ', 'stj')

        if stj_button:
            if parte == '' or parte == None:
                st.warning('Parte não foi preenchida! ☹️')
            elif len(tipo_de_parte) == 0:
                st.warning('Nenhum tipo de parte selecionad(a)! ☹️')
            else:
                st.warning('Olha, dependendo da quantidade de processos que a parte tiver, acho melhor pegar um café e uma bolacha (ou biscoito? 🤔) ☕🍪')
                with st.expander('👀 Veja aqui... 👀'):
                    st.snow()
                    st.warning('Alô você!')
                    st.warning('Gostaria de fazer pesquisas mais criteriosas, buscando por campos específicos? Com extrações de mais dados em uma única planilha Excel, e quem sabe, fazer essa extração, todo mês, ou cada semana ou ainda, todos os dias! Basta entrar em contato conosco que fazemos uma ferramenta para você! Basta entrar em contato pelo link ao lado: [Nosso WhatsApp](https://api.whatsapp.com/send?phone=5511985640273&text=Oi%20quero%20automatizar%20tarefas%20da%20minha%20empresa) 😏')
                    
                with st.expander('Execução do robô...'):
                    try:
                        stj = Stj(headless=False, download_files=False, parte=parte, tipo_de_parte=tipo_de_parte)
                        stj.executa_bot()
                        st.balloons()
                        st.success('Robô finalizado!')
                        df_xlsx = to_excel_for_download_button('EXTRACAO.xlsx')
                        st.download_button(label='📥 Baixar a Extração...',
                                            data=df_xlsx,
                                            file_name=f'extraction_STJ_{parte.lower().strip()}.xlsx')
                    except InvalidSessionIdException:
                        st.warning('Ocorreu um erro inesperado, reexecute a pesquisa.')
                    except NenhumValorEncontradoStjException:
                        st.warning(f'😱 Não foi possível encontrar nenhum registro para a perte informada "{parte}".')

    elif tribunal == 'TST - Tribunal Superior do Trabalho':
        st.markdown('<p class="p">* Insira uma parte válida!</p>', True)
        st.warning('Atenção: O TST geralmente fica fora do ar nas pesquisas... Não é culpa nossa. 😐')
        parte = st.text_input('Parte:').strip()
        tst_button = st.button('Pesquisar no TST', 'tst')

        if tst_button:
            if parte == '' or parte == None:
                st.warning('Parte não foi preenchida! ☹️')
            else:
                st.warning('Olha, dependendo da quantidade de processos que a parte tiver, acho melhor pegar um café e uma bolacha (ou biscoito? 🤔) ☕🍪')
                with st.expander('👀 Veja aqui... 👀'):
                    st.snow()
                    st.warning('Alô você!')
                    st.warning('Gostaria de fazer pesquisas mais criteriosas, buscando por campos específicos? Com extrações de mais dados em uma única planilha Excel, e quem sabe, fazer essa extração, todo mês, ou cada semana ou ainda, todos os dias! Basta entrar em contato conosco que fazemos uma ferramenta para você! Basta entrar em contato pelo link ao lado: [Nosso WhatsApp](https://api.whatsapp.com/send?phone=5511985640273&text=Oi%20quero%20automatizar%20tarefas%20da%20minha%20empresa) 😏')
                    
                with st.expander('Execução do robô...'):
                    try:
                        tst = Tst(headless=False, download_files=False, parte=parte)
                        tst.executa_bot()
                        st.balloons()
                        st.success('Robô finalizado!')
                        df_xlsx = to_excel_for_download_button('EXTRACAO.xlsx')
                        st.download_button(label='📥 Baixar a Extração...',
                                            data=df_xlsx,
                                            file_name=f'extraction_TST_{parte.lower().strip()}.xlsx')
                    except InvalidSessionIdException:
                        st.warning('Ocorreu um erro inesperado, reexecute a pesquisa.')
                    except NenhumValorEncontradoStjException:
                        st.warning(f'😱 Não foi possível encontrar nenhum registro para a perte informada "{parte}".')
    elif tribunal == 'TRT2 - Solicitação da Certidão Online de Ações Trabalhistas':
        st.markdown('#### Alô você! Esse bot captura todos os processos de Ações Trabalhistas no estado de São Paulo! Basta enviar o CNPJ!')
        cnpj = st.text_input('CNPJ:', help='Você pode enviar CNPJs com ou sem formatação.')
        try:
            cnpj = formata_cpf_e_cnpj(pega_somente_numeros(cnpj))
            button = st.button('Procurar...')
            if button:
                        with st.expander('Execução do bot:'):
                            TrtSCOAT(True, True, cnpj).executa_bot()
                        st.balloons()
                        st.success('Robô finalizado!')
                        df_xlsx = to_excel_for_download_button('EXTRACAO.xlsx')
                        st.download_button(
                            label='📥 Baixar a Extração...',
                            data=df_xlsx,
                            file_name=f'extraction_trt2_{cnpj}.xlsx',
                            help='Baixa uma planilha .xlsx com todos os processos em uma só coluna. Se desejar mais informações, recomendo a outra opção...')
                        certidao = None
                        with open(arquivo_com_caminho_absoluto('downloads', 'certidao.pdf'), 'rb') as f:
                            certidao = f.read()
                        st.download_button(
                            label='📥 Baixar a Certidão...',
                            data=certidao,
                            file_name=f'certidao_{cnpj}.pdf', 
                            help='Baixará o PDF da certidão que foi emitida no TRT2')
                        st.warning('Escolha uma das formas de download...')
                        
        except IndexError:
            st.error('CNPJ não preenchido!')
        except NameError:
            st.error('CNPJ Inválido')

    else:
        st.warning('Que pena! Estamos fazendo essa parte! Quem sabe amanhã não aparece aqui esse robô... 👀👀')
