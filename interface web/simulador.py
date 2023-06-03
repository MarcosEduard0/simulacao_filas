import numpy as np


def simulador_1(lambda_=1, mi_=2, simulation_total_time=1000, deterministic=False, initial_customers=1):
    n = initial_customers
    basic = 1 if initial_customers > 0 else 0
    simul_time = number_of_arrivals = system_spent_time = clients_in_system = clients_in_line = 0
    line_queue, wait_times, occupied_periods_basic, occupied_periods, occupied_periods_geral = [], [], [], [], []
    time_departures, time_arrivals = [], []
    occupied = True
    occupied_basic = True
    occupied_geral = True
    exponential = (lambda mi: 1 / mi) if deterministic else (
        lambda mi: np.random.exponential(scale=1 / mi))

    while simul_time < simulation_total_time:
        # Tempo de chegada exponencialmente distribuído
        arrival_time = np.random.exponential(scale=1 / lambda_)
        # Tempo de saída exponencialmente distribuído
        departure_time = exponential(mi_)
        # Tempo do último evento (chegada ou saída)
        last_event_time = simul_time

        if n == basic and occupied_basic:
            occupied_period_basic_start = simul_time  # Início do período ocupado
            occupied_basic = False

        if n == initial_customers and occupied:
            occupied_period_start = simul_time  # Início do período ocupado
            occupied = False

        if n == initial_customers and occupied_geral:
            occupied_period_geral_start = simul_time  # Início do período ocupado
            occupied_geral = False

        if n == 0:
            if not occupied:
                # Fim do período ocupado
                occupied_periods.append(simul_time - occupied_period_start)
                occupied = True
            if not occupied_basic:
                occupied_periods_basic.append(
                    simul_time - occupied_period_basic_start)
                occupied_basic = True

        if n == 1 and not occupied_geral:
            # Fim do período ocupado
            occupied_periods_geral.append(
                simul_time - occupied_period_geral_start)
            occupied_geral = True

        if n == 0 or arrival_time < departure_time:
            simul_time += arrival_time  # Incrementa o tempo total de simulação
            time_arrivals.append(simul_time)  # Registrar o tempo de chegada
            number_of_arrivals += 1  # Incrementar o número de chegadas
            # Atualizar o tempo total no sistema
            clients_in_system += (simul_time - last_event_time) * n
            # Atualizar o tempo total na fila
            clients_in_line += (simul_time - last_event_time) * len(line_queue)
            n += 1  # Incrementar o número de clientes no sistema

            if n > 1:
                # Adicionar o tempo de chegada à fila
                line_queue.append(simul_time)

        else:
            simul_time += departure_time  # Incrementa o tempo total de simulação
            time_departures.append(simul_time)  # Registrar o tempo de saída
            # Atualizar o tempo total no sistema
            clients_in_system += (simul_time - last_event_time) * n
            # Atualizar o tempo total na fila
            clients_in_line += (simul_time - last_event_time) * len(line_queue)

            if len(line_queue) > 0:
                # Calcular o tempo de espera do cliente que saiu da fila
                wait_times.append(simul_time - line_queue.pop(0))
            n -= 1  # Decrementar o número de clientes no sistema
            if len(time_arrivals) > 0:
                # Calcular o tempo total gasto no sistema
                system_spent_time += simul_time - time_arrivals.pop(0)

    # Calcular o tempo médio de espera
    Wq = sum(wait_times) / number_of_arrivals
    # Calcular o tempo médio no sistema
    W = system_spent_time / number_of_arrivals
    # Calcular a média de clientes no sistema
    L = clients_in_system / simul_time
    # Calcular a média de clientes na fila
    Lq = clients_in_line / simul_time
    # Calcular a média de partidas por unidade de tempo
    S = len(time_departures) / simul_time

    B = sum(occupied_periods_basic) / len(occupied_periods_basic) if len(
        occupied_periods_basic) > 0 else 0  # Calcular a duração média do período ocupado

    Bc = sum(occupied_periods) / len(occupied_periods) if len(
        occupied_periods) > 0 else 0  # Calcular a duração média do período ocupado

    Uc = sum(occupied_periods_geral) / len(occupied_periods_geral) if len(
        occupied_periods_geral) > 0 else 0  # Calcular a duração média do período ocupado

    results = {
        'Wq': Wq,
        'W': W,
        'L': L,
        'Lq': Lq,
        'S': S,
        'Bc': Bc,
        'Uc': Uc,
        'B': B
    }

    return results


def simulador_2(lambda_=1, mi_=2, simulation_total_time=1000, deterministic=False, initial_customers=1):
    basic = 1 if initial_customers > 0 else 0
    n, number_of_arrivals, waiting_line_time, system_spent_time, clients_in_system, clients_in_line, last_event_time = [
        0]*7
    number_of_departure = 0
    queue, line_queue, arrivals, queue_evolution, event = [], [], [], [], [0, ""]
    occupied_periods_basic, occupied_periods, occupied_periods_geral = [], [], []
    queue.append([np.random.exponential(scale=1/lambda_), "Chegada"])
    occupied_basic = True
    occupied = True
    occupied_geral = True

    exponential = (
        lambda mi: 1/mi) if deterministic else (lambda mi: np.random.exponential(scale=1/mi))

    while event[0] < simulation_total_time:
        last_event_time, event = event[0], queue.pop(0)
        clients_in_system += (event[0]-last_event_time) * n
        clients_in_line += (event[0]-last_event_time) * len(line_queue)

        if event[1] == "Chegada":
            queue.append(
                [event[0] + np.random.exponential(scale=1/lambda_), "Chegada"])
            arrivals.append(event[0])
            number_of_arrivals += 1
            n += 1

            if n == 1:
                queue.append([event[0] + exponential(mi_), "Saída"])
            if n > 1:
                line_queue.append(event[0])

            if n == basic and occupied_basic:
                # Início do período ocupado
                occupied_period_basic_start = event[0]
                occupied_basic = False

            if n == initial_customers and occupied:
                occupied_period_start = event[0]  # Início do período ocupado
                occupied = False

            if n == initial_customers and occupied_geral:
                # Início do período ocupado
                occupied_period_geral_start = event[0]
                occupied_geral = False

        else:
            number_of_departure += 1
            if len(line_queue) > 0:
                waiting_line_time += event[0] - line_queue.pop(0)
            n -= 1
            system_spent_time += (event[0] - arrivals.pop(0))

            if n > 0:
                queue.append([event[0] + exponential(mi_), "Saída"])

            if n == 0:
                if not occupied:
                    # Fim do período ocupado
                    occupied_periods.append(event[0] - occupied_period_start)
                    occupied = True
                if not occupied_basic:
                    occupied_periods_basic.append(
                        event[0] - occupied_period_basic_start)
                    occupied_basic = True
            if n == 1 and not occupied_geral:
                # Fim do período ocupado
                occupied_periods_geral.append(
                    event[0] - occupied_period_geral_start)
                occupied_geral = True
        queue.sort()
        queue_evolution.append(len(line_queue))

    Wq = waiting_line_time / number_of_arrivals
    W = system_spent_time / number_of_arrivals
    L = clients_in_system / event[0]
    Lq = clients_in_line / event[0]
    S = number_of_departure/event[0]
    avg_number_of_arrivals = number_of_arrivals/event[0]

    B = sum(occupied_periods_basic) / len(occupied_periods_basic) if len(
        occupied_periods_basic) > 0 else 0  # Calcular a duração média do período ocupado
    Bc = sum(occupied_periods) / len(occupied_periods) if len(
        occupied_periods) > 0 else 0  # Calcular a duração média do período ocupado

    Uc = sum(occupied_periods_geral) / len(occupied_periods_geral) if len(
        occupied_periods_geral) > 0 else 0  # Calcular a duração média do período ocupado

    decimal = 2
    results = {
        'L': round(L, decimal),
        'Lq': round(Lq, decimal),
        'W': round(W, decimal),
        'Wq': round(Wq, decimal),
        'S': S,
        'Bc': Bc,
        'Uc': Uc,
        'B': B
    }

    return results


def rodadas_simulacao(lambda_=1, mi_=2, simulation_total_time=10000, sample_size=1, deterministic=False, initial_customers=0, simulador=None):
    results = {}
    keys = ['L', 'Lq', 'W', 'Wq', 'S', 'B', 'Bc', 'Uc']
    for key in keys:
        results[key] = []

    for _ in range(sample_size):
        sample = simulador(lambda_, mi_, simulation_total_time,
                           deterministic, initial_customers)
        for key in keys:
            results[key].append(sample[key])

    means = {}
    for key in keys:
        means[key] = round(np.mean(results[key]), 2)

    return means
