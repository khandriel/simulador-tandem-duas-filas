import sys
from randomNumberGenerator import NextRandom
import time

count = 10000
fila1 = []
fila2 = []
tempo_global = 0
times1 = []
times2 = []
clientes_perdidos1 = 0
clientes_perdidos2 = 0
primeira_chegada = True
tempo_primeira_chegada = 1.5

def CHEGADA1():
    global fila1, clientes_perdidos1, primeira_chegada

    if primeira_chegada and tempo_global < tempo_primeira_chegada:
        return
    primeira_chegada = False

    if len(fila1) < K1:
        fila1.append(tempo_atendimento1())
    else:
        clientes_perdidos1 += 1

def SAIDA1():
    global fila1, fila2, clientes_perdidos2

    if fila1:
        # Cliente sai da fila 1 e vai para a fila 2
          # Geramos o tempo de atendimento para a fila 2
        if len(fila2) < K2:
            fila2.append(fila1.pop(0))
        else:
            clientes_perdidos2 += 1
            fila1.pop(0) 

def SAIDA2():
    global fila2
    if fila2:
        fila2.pop(0)  # Cliente conclui o atendimento na fila 2

def NextEvent():
    return NextRandom() < 0.5

def tempo_chegada1():
    return int(min_chegada1 + (max_chegada1 - min_chegada1) * NextRandom())

def tempo_atendimento1():
    return int(min_atendimento1 + (max_atendimento1 - min_atendimento1) * NextRandom())

def tempo_atendimento2():
    return int(min_atendimento2 + (max_atendimento2 - min_atendimento2) * NextRandom())

def inicializar_simulacao(args):
    global num_servidores1, K1, times1, min_chegada1, max_chegada1, min_atendimento1, max_atendimento1
    global num_servidores2, K2, times2, min_atendimento2, max_atendimento2

    if len(args) != 9:
        sys.exit(1)

    # Configuração da primeira fila (G/G/2/3)
    _, config1, min_chegada1_str, max_chegada1_str, min_atendimento1_str, max_atendimento1_str = args[:6]
    partes1 = config1.split("/")
    
    if len(partes1) != 4 or partes1[0] != "G" or partes1[1] != "G":
        sys.exit(1)

    num_servidores1 = int(partes1[2])
    K1 = int(partes1[3])

    min_chegada1 = int(min_chegada1_str)
    max_chegada1 = int(max_chegada1_str)
    min_atendimento1 = int(min_atendimento1_str)
    max_atendimento1 = int(max_atendimento1_str)

    times1 = [0] * (K1 + 1)

    # Configuração da segunda fila (G/G/1/5)
    config2, min_atendimento2_str, max_atendimento2_str = args[6:]
    partes2 = config2.split("/")
    
    if len(partes2) != 4 or partes2[0] != "G" or partes2[1] != "G":
        sys.exit(1)

    num_servidores2 = int(partes2[2])
    K2 = int(partes2[3])

    min_atendimento2 = int(min_atendimento2_str)
    max_atendimento2 = int(max_atendimento2_str)

    times2 = [0] * (K2 + 1)

def simulador():
    global tempo_global, count

    servidores1 = [0] * num_servidores1
    servidores2 = [0] * num_servidores2

    while count > 0:
        evento_chegada = NextEvent()

        if evento_chegada:
            CHEGADA1()
        else:
            # Processando a fila 1
            for i in range(num_servidores1):
                if servidores1[i] == 0 and fila1:
                    servidores1[i] = fila1.pop(0)  # Cliente começa a ser atendido
                if servidores1[i] > 0:
                    servidores1[i] -= 1
                    if servidores1[i] == 0:
                        SAIDA1()  # Transfere para a fila 2

            # Processando a fila 2
            for i in range(num_servidores2):
                if servidores2[i] == 0 and fila2:
                    servidores2[i] = fila2.pop(0)  # Cliente começa a ser atendido na fila 2
                if servidores2[i] > 0:
                    servidores2[i] -= 1
                    if servidores2[i] == 0:
                        SAIDA2()

        times1[len(fila1)] += 1
        times2[len(fila2)] += 1
        tempo_global += 1
        count -= 1
        time.sleep(0.01)
    
    print("Fila 1")
    for i in range(K1 + 1):
        print(f"Fila 1 - {i}: {times1[i]} ({times1[i] / tempo_global * 100:.2f}%)")
    print("Fila 2")
    for i in range(K2 + 1):
        print(f"Fila 2 - {i}: {times2[i]} ({times2[i] / tempo_global * 100:.2f}%)")

    print(f"Clientes perdidos fila 1: {clientes_perdidos1}")
    print(f"Clientes perdidos fila 2: {clientes_perdidos2}")
    print(f"Tempo total da simulação: {tempo_global}")


if __name__ == "__main__":
    inicializar_simulacao(sys.argv)
    simulador()
