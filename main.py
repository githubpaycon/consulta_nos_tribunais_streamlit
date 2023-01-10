'''
EXECUTE AQUI AS FUNÇÕES DE PESQUISA

pesquisa_stf()
pesquisa_stj()
pesquisa_tst()
'''

# STF
import os
from pesquisa_stf_package.pesquisa_stf import RoboStf
from pesquisa_stf_package.pesquisa_processos import RoboStfPegaDadosIndentificacao

# STJ
from pesquisa_stj_package.pesquisa_stj import RoboStj

# OUTRAS IMPORTAÇÕES
from partes import partes
from time import sleep
import time


def caso_de_erro(falha):
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    if not os.path.exists(f'ERROS'):
        os.makedirs(f'ERROS')
        with open('ERROS/erros.txt', 'a+') as file:
            file.write(f'{str(falha)}')
        sleep(1)
    else:
        with open('ERROS/erros.txt', 'a+') as file:
            file.write(f'\n{str(falha)}')
            sleep(1)
    print('\n\n\033[0;31mO ROBÔ FOI FINALIZADO PREMATURAMENTE!\n\nMOSTRE O ARQUIVO: erros.txt NA PASTA (ERROS) AO DESENVOLVEDOR\033[m\n\n')

def restart_program():
    import sys
    import os
    python = sys.executable
    os.execl(python, python, * sys.argv)


print(f'\033[1;32m===============================================\033[m')
print(f'\033[1;32m===== BEM-VINDO AO CONSULTA NOS TRIBUNAIS =====\033[m')
print(f'\033[1;32m===============================================\033[m')

print(f'\n\033[1;33mESCOLHA QUAL TRIBUNAL VOCÊ QUER RECUPERAR INFORMAÇÕES.\033[m\n')


print(f'\n\033[0;96mVocê vai procurar por {len(partes)} partes!\033[m\n')

print(f'')
print(f'STF -> \033[1;31m1\033[m')
print(f'STJ -> \033[1;31m2\033[m')
print(f'TST -> \033[1;31m3\033[m')
print(f'Listar partes que vou pesquisar (3 segundos para ver) -> \033[1;31m4\033[m\n')
tribunal = input('>>> ')
if tribunal == '1':
    try:
        inicio = time.time()
        robo_pega_tabela = RoboStf()
        robo_pega_tabela.pesquisa_stf()
        robo_pega_tabela.chrome.close()
        robo_pega_identificacao = RoboStfPegaDadosIndentificacao()
        robo_pega_identificacao.pega_dados_identificacao()
        robo_pega_identificacao.chrome.close()
        fim = time.time()
        result = (fim - inicio) / 60
        robo_pega_tabela.print_finalizado()
        print(f'O tempo de execução do bot foi de {result:.2f} minuto(s)')
    except Exception as falha:
        caso_de_erro(falha)

        
elif tribunal == '2':
    print(f'\033[0;96mVocê gostaria de ver o navegador?\033[m\n')
    print(f'NÃO -> \033[1;31m1\033[m')
    print(f'SIM -> \033[1;31m2\033[m')
    ver = input(f'\n>>> ')
    if ver == '1':
        try:
            inicio = time.time()
            robo_stj = RoboStj(headless='1')
            robo_stj.pesquisa_stj()
            fim = time.time()
            result = (fim - inicio) / 60
            print(f'O tempo de execução do bot foi de {result:.2f} minuto(s)')
            robo_stj.print_finalizado()
        except Exception as falha:
            caso_de_erro(falha)
    elif ver == '2':
        try:
            inicio = time.time()
            robo_stj = RoboStj(headless='2')
            robo_stj.pesquisa_stj()
            fim = time.time()
            result = (fim - inicio) / 60
            print(f'O tempo de execução do bot foi de {result:.2f} minuto(s)')
            robo_stj.print_finalizado()
        except Exception as falha:
            caso_de_erro(falha)
    else:
        print(f'NÃO ENTENDI O QUE VOCÊ DIGITOU [{tribunal}], VOU REINICIAR, E TENTE NOVAMENTE!')
        sleep(2)
        restart_program()
            
elif tribunal == '3':
    print('TST AINDA EM DESENVOLVIMENTO...')
    sleep(2)
    restart_program()
elif tribunal == '4':
    for parte in partes:
        print(parte)
    else:
        print()
        sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        restart_program()
else:
    print(f'NÃO ENTENDI O QUE VOCÊ DIGITOU [{tribunal}], TENTE NOVAMENTE!')
    sleep(1)
    restart_program()
    