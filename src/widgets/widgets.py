from funcsforspo_l.fregex.functions_re import *
from funcsforspo_l.fpython.functions_for_py import *
import streamlit as st
from src.app.stf import *
from src.app.stj import *
from src.app.trt.trt2 import *
from src.app.trt.trt4 import *
from src.app.tst import *
from src.utils.utils import to_excel_for_download_button
import requests
import openai
from openai.error import AuthenticationError

# TST #
def tst_widget():
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

# STJ #
def stj_widget():
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

# STF #
def stf_widget():
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

# TRTs #
def captura_de_processos_trabalhistas_widget():
    """Robô de captura de processos trabalhistas no TRT
    """
    st.markdown('##### Olá! Esse bot captura todos os processos de trabalhistas nos tribunais indicados.')
    tribs = st.multiselect('Selecione os Tribunais:', ['TRT2', 'TRT4'], help='Os tribunais válidos até hoje são: TRT2; TRT4')  # depois de finalizar um, o bot vai jogar os dados para uma pasta, dps, que executar o outro tmb vai jogar na pasta os arquivos de extracao
    if len(tribs) == 0:
        pass
    else:

        if 'TRT4' in tribs:
            st.warning('Atenção, a execução do TRT4 pode ocorrer alguns erros...')

        cnpj = st.text_input('CNPJ:', help='Você pode enviar CNPJs com ou sem formatação.')
        try:
            cnpj = formata_cpf_e_cnpj(pega_somente_numeros(cnpj))
            button = st.button('Procurar...')
            if button:
                with st.expander('Execução do bot:'):
                    if 'TRT2' in tribs:
                        TrtSCOAT(headless=False, download_files=True, cnpj=cnpj).executa_bot()
                    if 'TRT4' in tribs:
                        TRT4CertidaoTrabalhista(headless=False, download_files=True, cnpj=cnpj).executa_bot()
                if len(arquivos_com_caminho_absoluto_do_arquivo('output')) != 0:
                    st.balloons()
                    st.success('Robô finalizado!')
                    zip_dirs(['output'], 'extracao.zip')
                    with st.expander('Nosso merchan 🫰🏽'):
                        st.warning('Caso você queira coisas mais específicas ou até mesmo um bot que se qualifique com seus objetivos, basta falar conosco, automatizamos praticamente qualquer ação em um computador hehehe.')
                    with open('extracao.zip', 'rb') as f:
                        st.download_button(
                            label='📥 Baixar a Arquivos...',
                            data=f.read(),
                            file_name=f'extracao.zip', 
                            help='Baixará um arquivo ZIP com a(s) certidão(dões) contendo todos os processos encontrados.')
                        limpa_diretorio('output')
                else:
                    st.warning('Algo deu errado na execução...')

        except IndexError:
            st.error('CNPJ não preenchido!')


## OPENAI SECTION ##
def conversar_com_ia():
    st.markdown('# Converse com o ChatGPT!')
    with st.expander('🖐🏽 Ajuda! 🖐🏽'):
        st.markdown('Caso você não tenha a chave da API, basta seguir os passo a baixo:')
        st.markdown('* Vá para esse link: [OPENAI LOGIN](https://platform.openai.com/signup/)')
        st.markdown('* Preferencialmente eu gosto de clicar em "Continue with Google". **Faça login com o Google.**')
        st.markdown('* Clique no menu superior direito. (na sua foto);')
        st.markdown('* Clique em "View API Keys"')
        st.markdown('* Clique em "Create new secret key"')
        st.markdown('* Copie-a e guarde em um lugar seguro **ELA NÃO PODE SER EXIBIDA NOVAMENTE!**;')
        st.markdown('* Por fim, cole-a abaixo')
        st.markdown('### Para a sua segurança, não salvamos suas credenciais! 😉')
        st.markdown('##### Você pode salvar a sua chave de API pelo gerenciador de senhas do Google!')
    api_key = st.text_input('Insira a chave da API:', type='password')
    
    if api_key == None or api_key == '':
        pass
    else:
        temperature = st.slider('Nível de Criatividade:', value=1.0, min_value=0.0, max_value=2.0, step=0.1, help='Quanto maior o nível de criatividade, maior a chance de uma resposta vir com problemas, e quanto menor o nível, maior a recionalidade da IA.')
        prompt_insert = st.text_input('Sua mensagem para a IA:', help='Se quiser um texto bem formatado, basta enviar no final "em markdown"')
        go = st.button('Enviar')
        if go:
            try:
                openai.api_key = api_key

                prompt = prompt_insert
                model_engine = "text-davinci-003"

                response = openai.Completion.create(
                    prompt=prompt,
                    model=model_engine,
                    max_tokens=1000,
                    temperature=temperature,
                    n=1,
                    # stop=['---']
                )

                result_final = ''
                for result in response.choices:
                    result_final += result.text.strip()
                
                st.markdown(result_final)
            except AuthenticationError:
                st.error('A chave de API enviada não é válida, tente outra...', icon='🗝️')


## API RECEITA ## 
def consulta_cnpj():
    st.markdown('# Faça consultas em um CNPJ')
    st.markdown('##### Recupere vários dados de um CNPJ.')
    cnpj = pega_somente_numeros(st.text_input('Numero do CNPJ', help='Envie com ou sem pontuação.'))
    pesquisar = st.button('Pesquisar...')
    if pesquisar:
        response = requests.get(f'https://receitaws.com.br/v1/cnpj/{cnpj}')
        print(response)
        print(response.content)
        json = response.json()
        if response.status_code != 200:
            if json['status'] == 'ERROR':
                print(json['message'])
                st.error(json['message'])
            print('Muitas requisições foram feitas, aguarde...')
        else:
            
            
            
            # recupera a atividade principal:
            atividade_principal = ''
            for i in json['atividade_principal']:
                if len(json['atividade_principal']) > 1:
                    atividade_principal += f'{i["text"]};'
                else:
                    atividade_principal = i["text"]
                    
            # Recupera a 
            data_situacao = json['data_situacao']
            fantasia = json['fantasia']
            complemento = json['complemento']
            tipo = json['tipo']
            nome = json['nome']
            telefone = json['telefone']
            email = json['email']
            
            # atividades secundarias
            atividade_secundaria = ''
            for i in json['atividades_secundarias']:
                if len(json['atividades_secundarias']) > 1:
                    atividade_secundaria += f'{i["text"]};'
                else:
                    atividade_secundaria = i["text"]
            
            # Quadro societário
            
            qsa = json['qsa']
            list_qsa = []
            for i in qsa:
                list_qsa.append(i["nome"])
                
            situacao = json['situacao']
            bairro = json['bairro']
            logradouro = json['logradouro']
            numero = json['numero']
            cep = json['cep']
            municipio = json['municipio']
            abertura = json['abertura']

            st.text(f"""
                    Atividade Principal
            {atividade_principal}      {atividade_principal}
            """)
            st.text(atividade_principal)
            st.text(atividade_principal)
            st.text(atividade_principal)
            st.text(atividade_principal)
            st.text(atividade_principal)



