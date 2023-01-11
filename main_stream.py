import pandas as pd
from src.app.stf import Stf
import streamlit as st
from src.base.base import InvalidSessionIdException
import os
from funcsforspo_l.fpython.functions_for_py import *
from src.utils.utils import to_excel_for_download_button, verifica_colunas_stf
import plotly.express as px


# -- CONFIGURATIONS -- #
st.set_page_config(
    page_title="Consulta nos Tribunais",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://api.whatsapp.com/send?phone=5511985640273',
        'Report a bug': "https://api.whatsapp.com/send?phone=5511985640273",
        'About': "#### Trabalhando por um futuro melhor (e mais automatizado) com muito amor, inteligência e vontade! [Isso é a Paycon Automation](https://payconautomacoes.com.br/)"
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
CHOICE = bar.selectbox('Escolha uma Ferramenta', ['Extração dos Dados', 'Analise Dos Dados Extraidos'])
# -- SIDEBAR --

# -- DELETE EXTRACTION --
try:
    os.remove('EXTRACAO.xlsx')
except FileNotFoundError:
    pass
# -- DELETE EXTRACTION --

# -- CONFIGURATIONS -- #


# ================================ #
# ====== EXTRAÇÃO DOS DADOS ====== #
# ================================ #
if CHOICE == 'Extração dos Dados':
    st.markdown('# Consulta nos Tribunais')
    st.markdown('### Faça consultas nos principais tribunais do Brasil!')
    st.markdown('#### Tribunais disponíveis atualmente:')
    st.markdown('* STF - Supremo Tribunal Federal')
    st.markdown('---')

    tribunal = st.selectbox('Escolha o Tribunal:', ['STF - Supremo Tribunal Federal', 'STJ - Superior Tribunal de Justiça', 'TST - Tribunal Superior do Trabalho'])

    if tribunal == 'STF - Supremo Tribunal Federal':
        parte_tipo = st.radio('Escolha entre as formas de procura:', ['Uma única parte', 'Várias partes ao mesmo tempo'])
        
        if parte_tipo == 'Uma única parte':
            st.markdown('<p class="p">* Insira uma parte válida!</p>', True)
            parte = st.text_input('Parte:')
            if parte:
                stf_button = st.button('Pesquisar no STF', 'stf')

                if stf_button:
                    with st.expander('Execução do robô...'):
                        try:
                            stf = Stf(True, False, parte)
                            stf.executa_bot()
                            st.success('Robô finalizado!')
                        except InvalidSessionIdException:
                            st.warning('Ocorreu um erro inesperado, reexecute a pesquisa.')
                    try:
                        df_xlsx = to_excel_for_download_button('EXTRACAO.xlsx')
                        st.download_button(label='📥 Baixar a Extração...',
                                            data=df_xlsx ,
                                            file_name= 'extraction.xlsx')
                    except (FileNotFoundError, FileExistsError):
                        st.warning('O Robô foi executado, no entanto pode ter ocorrido um erro e não existe a tabela de extração')
        if parte_tipo == 'Várias partes ao mesmo tempo':
            st.markdown('<p class="p">* Insira um arquivo .xlsx com uma coluna <b>PARTES</b> contendo as partes!</p>', True)
            parte = st.file_uploader('Arquivo:', type='xlsx')
            if parte is not None:
                df_partes =pd.read_excel(parte, 0)
                try:
                    partes_list = df_partes['PARTES']
                    st.markdown('Partes encontradas:')
                    for part in partes_list:
                        st.markdown(f'<center><b>{part}</b></center>', True)
                        

                    stf_button = st.button('Pesquisar no STF', 'stf')
                    if stf_button:
                        with st.expander('Execução do robô...'):
                            try:
                                stf = Stf(True, False, parte)
                                stf.executa_bot()
                                st.success('Robô finalizado!')
                            except InvalidSessionIdException:
                                st.warning('Ocorreu um erro inesperado, reexecute a pesquisa.')
                        try:
                            df_xlsx = to_excel_for_download_button('EXTRACAO.xlsx')
                            st.download_button(label='📥 Baixar a Extração...',
                                                data=df_xlsx ,
                                                file_name= 'extraction.xlsx')
                        except (FileNotFoundError, FileExistsError):
                            st.warning('O Robô foi executado, no entanto pode ter ocorrido um erro e não existe a tabela de extração')

                except KeyError:
                    st.error(f'Não foi encontrada a coluna **PARTES** e sim essa(s): {list(df_partes.columns)}. Remova o arquivo e envie outro com a devida coluna.')
    else:
        st.warning('Ainda em desenvolvimento...', icon='🧑‍💻')

if CHOICE == 'Analise Dos Dados Extraidos':
    df = None
    st.warning('Ainda em Desenvolvimento...', icon='🧑‍💻')
    st.markdown('# Analise Dos Dados da Extração')
    st.markdown('### Verifique por exemplo quantos processos estão em tramite, quais os meios, etc...')
    
    tribunal = st.selectbox('Tribunal que deseja anlisar os dados...', ['STF', 'TRT'])
    if tribunal == 'STF':
        with st.expander('Envio do arquivo...', True):
            file = st.file_uploader('Arquivo da extração:')
            if not file is None:
                df = pd.read_excel(file)
                if verifica_colunas_stf(df) == False:
                    st.error(f"Foi encontrada alguma coluna que não faz parte da extração do STF... As colunas válidas são {transforma_lista_em_string(['PARTE', 'IDENTIFICACAO', 'NUMERO UNICO', 'DATA AUTUACAO', 'MEIO', 'PUBLICIDADE', 'TRAMITE'])}")
                else:
                    st.success('Prontinho, você pode recolher essa aba e ver os gráficos...')
                    
        with st.expander('Gráficos...'):
            try:
                print(df)
                choice = st.selectbox('Escolha a forma de visualização', ['Tabela', 'Métricas', 'Pizza'])
                if choice == 'Tabela':
                    st.dataframe(df)
                if choice == 'Métricas':
                    c1, c2, c3 = st.columns(3)
                    
                    c1.metric('Partes Totais Encontradas', len(list(set(df['PARTE']))))
                    c2.metric('Meio Eletrônico', len(df['PARTE'].loc[df['MEIO'] == 'Eletrônico']))
                    c3.metric('Meio Físico', len(df['PARTE'].loc[df['MEIO'] == 'Físico']))
                    c1.metric('Em trâmite', len(df['PARTE'].loc[df['TRAMITE'] == 'Sim']))
                    c2.metric('Não em trâmite', len(df['PARTE'].loc[df['TRAMITE'] == 'Não']))
                if choice == 'Pizza':
                    st.subheader('Quantidade de processos em trâmite')
                    values = st.selectbox('Valores', list(df.columns), index=2) # index é o default
                    names = st.selectbox('Nomes', list(df.columns), index=1)
                    tamanho_hole = st.slider('Tamanho do Furo', min_value=0.001, max_value=1.0)
                    partes = st.multiselect('Partes', list(df['PARTE']), key='2', default=list(df['PARTE'])[10])
                    if not len(partes) == 0:
                        df = df.loc[df['PARTE'].isin(partes)]

                    fig = px.pie(df, values=values, names=names, hole=tamanho_hole) 
                    st.plotly_chart(fig, True)

            except Exception as e:
                print(e)
                print(repr(e))
                st.warning('Arquivo ainda não enviado...')
