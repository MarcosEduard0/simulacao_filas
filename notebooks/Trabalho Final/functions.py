import numpy as np
import math
from collections import Counter


def simulador(lambda_=1, mi_=2, tempo_total_simulacao=10000, deterministico=False):
    n = tempo_simulacao = num_chegadas = tempo_ocupado_servidor = 0
    clientes_fila, chegadas, freq_clientes, tempo_clientes_fila, tempo_clientes_sistema, tempo_espera_sistema = [], [], [], [], [], []

    exponential = (lambda mi: 1 / mi) if deterministico else (
        lambda mi: np.random.exponential(scale=1 / mi))

    while tempo_simulacao < tempo_total_simulacao:
        tempo_chegada = np.random.exponential(scale=1 / lambda_)
        tempo_saida = exponential(mi_)
        last_event_time = tempo_simulacao

        if n == 0 or tempo_chegada < tempo_saida:
            if n == 0:
                freq_clientes.append(len(clientes_fila))

            tempo_simulacao += tempo_chegada
            num_chegadas += 1
            tempo_clientes_sistema.append(
                (tempo_simulacao - last_event_time) * n)
            tempo_clientes_fila.append(
                (tempo_simulacao - last_event_time) * len(clientes_fila))
            chegadas.append(tempo_simulacao)
            n += 1

            if n > 1:
                clientes_fila.append(tempo_simulacao)
                tempo_ocupado_servidor += tempo_chegada
                freq_clientes.append(len(clientes_fila))

        else:
            tempo_simulacao += tempo_saida
            tempo_clientes_sistema.append(
                (tempo_simulacao - last_event_time) * n)
            tempo_clientes_fila.append(
                (tempo_simulacao - last_event_time) * len(clientes_fila))

            if len(clientes_fila):
                clientes_fila.pop(0)

            tempo_espera_sistema.append(tempo_simulacao - chegadas.pop(0))
            tempo_ocupado_servidor += tempo_saida
            n -= 1

    soma_tempo_clientes_fila = sum(tempo_clientes_fila)
    soma_tempo_clientes_sistema = sum(tempo_clientes_sistema)

    Wq = soma_tempo_clientes_fila / num_chegadas
    W = soma_tempo_clientes_sistema / num_chegadas
    L = soma_tempo_clientes_sistema / tempo_simulacao
    Lq = soma_tempo_clientes_fila / tempo_simulacao
    rho = tempo_ocupado_servidor / tempo_simulacao
    pi = Counter(freq_clientes)

    for valor, freq in pi.items():
        pi[valor] = round(freq / num_chegadas, 6)

    results = {
        'Total de Clientes': num_chegadas,
        'Clientes Restantes': n,
        'Tempo Total': tempo_simulacao,
        'Tempo Espera Sistema': tempo_espera_sistema,
        'Wq': Wq,
        'W': W,
        'L': L,
        'Lq': Lq,
        'rho': rho,
        'pi': pi,
    }

    return results


def get_z_score(confidence_level):
    if confidence_level == 0.9:
        return 1.645
    elif confidence_level == 0.95:
        return 1.96
    elif confidence_level == 0.99:
        return 2.58


def geo(p, k):
    return (1 - p) * p ** k


def valor_analitico(lambda_, mu_):
    W = 1/(mu_-lambda_)
    Wq = W - (1/mu_)
    L = lambda_*W
    Lq = lambda_*Wq
    Rho = lambda_/mu_

    return [L, Lq, W, W, Rho]


def intervalo_confianca(data, conf_level, sample_size):
    x_barra = np.mean(data)
    z = get_z_score(conf_level)
    s = np.std(data, ddof=1)
    limite_inferior = x_barra - z*s/math.sqrt(sample_size)
    limite_superior = x_barra + z*s/math.sqrt(sample_size)

    return (limite_inferior, limite_superior)


def simulator_confidence_interval(lambda_, mi_, sample_size, conf_level, tempo_total_simulacao=1000, deterministico=False):
    Wq_data = []
    W_data = []
    L_data = []
    Lq_data = []
    rho_data = []
    pi = {}

    results = [simulador(lambda_, mi_, tempo_total_simulacao)
               for _ in range(sample_size)]

    for sample in results:
        Wq_data.append(sample['Wq'])
        W_data.append(sample['W'])
        L_data.append(sample['L'])
        Lq_data.append(sample['Lq'])
        rho_data.append(sample['rho'])
        for k, value in sample['pi'].items():
            if k not in pi:
                pi[k] = []
            pi[k].append(value)

    conf_level = 0.95

    Wq_ic = intervalo_confianca(Wq_data, conf_level, sample_size)
    W_ic = intervalo_confianca(W_data, conf_level, sample_size)
    L_ic = intervalo_confianca(L_data, conf_level, sample_size)
    Lq_ic = intervalo_confianca(Lq_data, conf_level, sample_size)
    rho_ic = intervalo_confianca(rho_data, conf_level, sample_size)

    pi_ic = {i: [] for i in range(len(pi)+1)}
    for k in pi.keys():
        pi_ic[k] = intervalo_confianca(pi[k], conf_level, sample_size)

    return {'Wq': {'IC': Wq_ic, 'Amostras': Wq_data},
            'W': {'IC': W_ic, 'Amostras': W_data},
            'L': {'IC': L_ic, 'Amostras': L_data},
            'Lq': {'IC': Lq_ic, 'Amostras': Lq_data},
            'rho': {'IC': rho_ic, 'Amostras': rho_data},
            'pi': {'IC': pi_ic, 'Amostras': pi}
            }


def remove_outliers(data):
    q1 = np.quantile(data, 0.25)
    q3 = np.quantile(data, 0.75)
    iqr = q3 - q1

    upper_bound = q3 + (1.5 * iqr)
    lower_bound = q1 - (1.5 * iqr)

    data_without_outliers = [x for x in data if (
        x >= lower_bound) and (x <= upper_bound)]

    outlier_percentage = (
        len(data) - len(data_without_outliers)) / len(data) * 100

    print(f"Porcentagem de outliers removidos: {outlier_percentage} %")

    return data_without_outliers
