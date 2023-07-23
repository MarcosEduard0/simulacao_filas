import numpy as np
from collections import Counter
import pandas as pd


def simulador_1(lambda_=1, mi_=2, tempo_total_simulacao=10000, deterministico=False):
    n = tempo_simulacao = num_chegadas = tempo_ocupado_servidor = 0
    clientes_fila, chegadas, freq_clientes, tempo_clientes_fila, tempo_clientes_sistema, tempo_espera_sistema = [], [], [], [], [], []

    exponential = (lambda mi: 1 / mi) if deterministico else (
        lambda mi: np.random.exponential(scale=1 / mi))

    trace = {'Numero de clientes na fila': [],
             'Evento': [],
             'Tempo': [],
             }
    while tempo_simulacao < tempo_total_simulacao:
        tempo_chegada = np.random.exponential(scale=1 / lambda_)
        tempo_saida = exponential(mi_)
        last_event_time = tempo_simulacao

        if n == 0 or tempo_chegada < tempo_saida:
            tempo_simulacao += tempo_chegada
            num_chegadas += 1
            tempo_clientes_sistema.append(
                (tempo_simulacao - last_event_time) * n)

            chegadas.append(tempo_simulacao)

            if n == 0:
                freq_clientes.append(len(clientes_fila))

            n += 1
            if n > 1:
                clientes_fila.append(tempo_simulacao)
                tempo_ocupado_servidor += tempo_chegada
                freq_clientes.append(len(clientes_fila))

            trace['Numero de clientes na fila'].append(n)
            trace['Evento'].append('Chegada')
            trace['Tempo'].append(tempo_simulacao)

        else:
            tempo_simulacao += tempo_saida
            tempo_clientes_sistema.append(
                (tempo_simulacao - last_event_time) * n)

            if len(clientes_fila):
                tempo_clientes_fila.append(
                    tempo_simulacao - clientes_fila.pop(0))

            tempo_espera_sistema.append(tempo_simulacao - chegadas.pop(0))
            tempo_ocupado_servidor += tempo_saida
            n -= 1

            trace['Numero de clientes na fila'].append(n)
            trace['Evento'].append('Saida')
            trace['Tempo'].append(tempo_simulacao)

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
        'trace': pd.DataFrame(trace)
    }

    return results


def simulador_2(lambda_=1, mi_=2, simulation_total_time=10000, deterministic=False):
    n, number_of_arrivals, waiting_line_time, system_spent_time, clients_in_system, clients_in_line, last_event_time = [
        0]*7
    tempo_ocupado_servidor = 0
    queue, line_queue, arrivals, queue_evolution, event = [], [], [], [], [0, ""]
    queue.append([np.random.exponential(scale=1/lambda_), "Chegada"])

    exponential = (
        lambda mi: 1/mi) if deterministic else (lambda mi: np.random.exponential(scale=1/mi))

    while event[0] < simulation_total_time:
        last_event_time, event = event[0], queue.pop(0)
        clients_in_system += (event[0]-last_event_time) * n
        clients_in_line += (event[0]-last_event_time) * len(line_queue)

        if event[1] == "Chegada":
            taxa = np.random.exponential(scale=1/lambda_)
            queue.append(
                [event[0] + taxa, "Chegada"])
            arrivals.append(event[0])
            number_of_arrivals += 1
            n += 1

            if n == 1:
                queue.append([event[0] + exponential(mi_), "Saída"])
            if n > 1:
                line_queue.append(event[0])
                tempo_ocupado_servidor += taxa

        else:
            if len(line_queue) > 0:
                waiting_line_time += event[0] - line_queue.pop(0)

            n -= 1
            system_spent_time += (event[0] - arrivals.pop(0))

            if n > 0:
                taxa = exponential(mi_)
                queue.append([event[0] + taxa, "Saída"])

        queue.sort()
        queue_evolution.append(len(line_queue))

    Wq = waiting_line_time / number_of_arrivals
    W = system_spent_time / number_of_arrivals
    L = clients_in_system / event[0]
    Lq = clients_in_line / event[0]
    rho = tempo_ocupado_servidor/event[0]

    decimal = 2
    results = {
        'L': round(L, decimal),
        'Lq': round(Lq, decimal),
        'W': round(W, decimal),
        'Wq': round(Wq, decimal),
        'rho': round(rho, decimal),
        'Clientes Restantes': n,
        'Tempo Total': event[0],
        'Total de Clientes': round(number_of_arrivals, decimal),
        'queue_evolution': queue_evolution
    }

    return results


def rodadas_simulacao(lambda_=1, mi_=2, simulation_total_time=10000, sample_size=1, deterministic=False, simulador=None):
    results = {}
    keys = ['L', 'Lq', 'W', 'Wq', 'rho']
    for key in keys:
        results[key] = []

    for _ in range(sample_size):
        sample = simulador(lambda_, mi_, simulation_total_time, deterministic)
        for key in keys:
            results[key].append(sample[key])

    means = {}
    for key in keys:
        means[key] = round(np.mean(results[key]), 2)

    return means
