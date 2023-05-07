import random
import math

# Configuração da simulação
tempo_total = 1000
chegada_media = 5
atendimento_media = 4

# Inicialização das variáveis
tempo_atual = 0
fila = []
atendidos = []
prox_chegada = random.expovariate(1/chegada_media)
prox_atendimento = math.inf

# Simulação
while tempo_atual < tempo_total:
    if prox_chegada < prox_atendimento:
        tempo_atual = prox_chegada
        if len(fila) == 0:
            prox_atendimento = tempo_atual + \
                random.expovariate(1/atendimento_media)
        fila.append(tempo_atual)
        prox_chegada = tempo_atual + random.expovariate(1/chegada_media)
    else:
        tempo_atual = prox_atendimento
        atendidos.append(tempo_atual)
        if len(fila) == 0:
            prox_atendimento = math.inf
        else:
            prox_atendimento = tempo_atual + \
                random.expovariate(1/atendimento_media)
            fila.pop(0)

# Resultados
tempo_medio_fila = sum([atendimento - chegada for chegada,
                       atendimento in zip(fila, atendidos)]) / len(atendidos)
print("Tempo médio de fila:", tempo_medio_fila)
