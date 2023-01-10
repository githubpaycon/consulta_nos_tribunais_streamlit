from tqdm import tqdm
import time
import os

processos_a_recuperar = 40
for processo in tqdm(range(processos_a_recuperar)):
    print(f"Recuperando {processo} de {processos_a_recuperar} processo(s)")
    time.sleep(1)
    os.system('cls')