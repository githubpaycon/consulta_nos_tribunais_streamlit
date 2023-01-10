if __name__ == '__main__':
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\033[0;31mEXECUTE O main.py\033[m')
    quit()

from time import sleep


partes = []

with open('partes.txt', 'r') as file:
    for part in file.readlines():
        if ',' in part[-2::]:
            print(f'\n\n\033[0;31mA parte {part} é inválida, pois possui uma vírgula (",") no final da parte\033[m')
            sleep(1)
        else:
            
            part = part[:-1]  # remove a quebra de linha dada pelo enter (\n)
            partes.append(part)
