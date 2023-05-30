import numpy as np


def simulador_1(lambda_=1, mi_=2, simulation_total_time=10000, deterministic=False):
    n = simul_time = number_of_arrivals = system_spent_time = clients_in_system = clients_in_line = last_event_time = 0
    line_queue, arrivals, wait_times = [], [], []
    number_of_departure = 0
    exponential = (
        lambda mi: 1/mi) if deterministic else (lambda mi: np.random.exponential(scale=1/mi))

    while simul_time < simulation_total_time:
        arrival_time = np.random.exponential(scale=1/lambda_)
        departure_time = exponential(mi_)
        last_event_time = simul_time

        if n == 0 or arrival_time < departure_time:
            simul_time += arrival_time
            number_of_arrivals += 1
            clients_in_system += (simul_time - last_event_time) * n
            clients_in_line += (simul_time - last_event_time) * len(line_queue)
            n += 1
            arrivals.append(simul_time)

            if n > 1:
                line_queue.append(simul_time)

        else:
            number_of_departure += 1
            simul_time += departure_time
            clients_in_system += (simul_time - last_event_time) * n
            clients_in_line += (simul_time - last_event_time) * len(line_queue)

            if len(line_queue) > 0:
                wait_times.append(simul_time - line_queue.pop(0))

            n -= 1
            system_spent_time += simul_time - arrivals.pop(0)

    avg_waiting_time = sum(wait_times) / number_of_arrivals
    avg_system_time = system_spent_time / number_of_arrivals
    avg_clients_in_system = clients_in_system / simul_time
    avg_clients_in_line = clients_in_line / simul_time
    avg_number_of_departure = number_of_departure/simul_time
    avg_number_of_arrivals = number_of_arrivals/simul_time
    decimal = 2

    results = {
        'avg_clients_in_system': round(avg_clients_in_system, decimal),
        'avg_clients_in_line': round(avg_clients_in_line, decimal),
        'avg_system_time': round(avg_system_time, decimal),
        'avg_waiting_time': round(avg_waiting_time, decimal),
        'people_in_line': n,
        'simul_time': round(simul_time, decimal),
        'number_of_arrivals': round(number_of_arrivals, decimal),
        'wait_times': wait_times,
        'avg_number_of_arrivals': avg_number_of_arrivals,
        'avg_number_of_departure': avg_number_of_departure,

    }

    return results


def simulador_2(lambda_=1, mi_=2, simulation_total_time=10000, deterministic=False):
    n, number_of_arrivals, waiting_line_time, system_spent_time, clients_in_system, clients_in_line, last_event_time = [
        0]*7
    number_of_departure = 0
    queue, line_queue, arrivals, queue_evolution, event = [], [], [], [], [0, ""]
    queue.append([np.random.exponential(scale=1/lambda_), "Chegada"])

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

        else:
            number_of_departure += 1
            if len(line_queue) > 0:
                waiting_line_time += event[0] - line_queue.pop(0)
            n -= 1
            system_spent_time += (event[0] - arrivals.pop(0))

            if n > 0:
                queue.append([event[0] + exponential(mi_), "Saída"])

        queue.sort()
        queue_evolution.append(len(line_queue))

    avg_waiting_time = waiting_line_time / number_of_arrivals
    avg_system_time = system_spent_time / number_of_arrivals
    avg_clients_in_system = clients_in_system / event[0]
    avg_clients_in_line = clients_in_line / event[0]
    avg_number_of_departure = number_of_departure/event[0]
    avg_number_of_arrivals = number_of_arrivals/event[0]

    decimal = 2
    results = {
        'avg_clients_in_system': round(avg_clients_in_system, decimal),
        'avg_clients_in_line': round(avg_clients_in_line, decimal),
        'avg_system_time': round(avg_system_time, decimal),
        'avg_waiting_time': round(avg_waiting_time, decimal),
        'people_in_line': n,
        'simul_time': event[0],
        'number_of_arrivals': round(number_of_arrivals, decimal),
        'queue_evolution': queue_evolution,
        'avg_number_of_arrivals': avg_number_of_arrivals,
        'avg_number_of_departure': avg_number_of_departure
    }

    return results


def rodadas_simulacao(lambda_=1, mi_=2, simulation_total_time=10000, sample_size=1, deterministic=False, simulador=None):
    results = {}
    keys = ['avg_clients_in_system', 'avg_clients_in_line',
            'avg_system_time', 'avg_waiting_time', 'avg_number_of_departure']
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
