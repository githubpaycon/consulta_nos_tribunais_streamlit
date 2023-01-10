'''
EXECUTE AQUI AS FUNÇÕES DE PESQUISA

pesquisa_stf()
pesquisa_stj()
pesquisa_tst()
'''

# STJ
from pesquisa_stj_package_.pesquisa_stj import RoboStj
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

print(f'\n\033[1;33mRECUPERANDO INFORMAÇÕES DO TRIBUNAL STJ - SUPREMO TRIBUNAL DE JUSTIÇA.\033[m\n')



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
    