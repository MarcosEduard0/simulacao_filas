import numpy as np

num_samples = 40
mean_arrival_time = 1
mean_departure_time = 2

print("\nSimulando fila...")
print("\nTempo de chegada | Tipo de evento | Número de amostras\n")

n = 0
simul_time = 0

for i in range(num_samples):
    arrival_time = np.random.exponential(scale=mean_arrival_time)
    departure_time = np.random.exponential(scale=mean_departure_time)

    if n == 0:
        simul_time += arrival_time
        print(f"{simul_time:8.4f} \t\t{'Chegada':14} {n:2} => {n+1:2}")
        n += 1
    else:
        if arrival_time < departure_time:
            simul_time += arrival_time
            print(f"{simul_time:8.4f} \t\t{'Chegada':14} {n:2} => {n+1:2}")
            n += 1
        else:
            simul_time += departure_time
            print(f"{simul_time:8.4f} \t\t{'Saída':14} {n:2} => {n-1:2}")
            n -= 1

print(f"\nNúmero de amostras na fila ao final da simulação: {n}")
print(f"Tempo total da simulação: {simul_time:.4f}")
print(
    f"Tempo médio de espera na fila: {(simul_time/num_samples - mean_arrival_time):.4f}")
