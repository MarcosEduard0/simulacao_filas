import random                           # gerador de números aleatórios
import simpy                            # biblioteca de simulação

# tempo médio entre chegadas sucessivas de clientes
TEMPO_MEDIO_CHEGADAS = 0.5
TEMPO_MEDIO_ATENDIMENTO = 0.5           # tempo médio de atendimento no servidor


def geraChegadas(env):
    # função que cria chegadas de entidades no sistema
    contaChegada = 0
    while True:
        # aguardo um intervalo de tempo exponencialmente distribuído
        yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_CHEGADAS))
        contaChegada += 1
        print('%.1f Chegada do cliente %d. Cliente(s) na fila: %d.' %
              (env.now, contaChegada, len(servidorRes.queue)))

        # inicia o processo de atendimento
        env.process(atendimentoServidor(env, "cliente %d" %
                    contaChegada, servidorRes))


def atendimentoServidor(env, nome, servidorRes):
    # função que ocupa o servidor e realiza o atendimento
    # solicita o recurso servidorRes
    request = servidorRes.request()

    # aguarda em fila até a liberação do recurso e o ocupa
    yield request
    print('%.1f Servidor inicia o atendimento do %s' % (env.now, nome))

    # aguarda um tempo de atendimento exponencialmente distribuído
    yield env.timeout(random.expovariate(1.0/TEMPO_MEDIO_ATENDIMENTO))
    print('%.1f Servidor termina o atendimento do %s' % (env.now, nome))
    # o cliente foi atendido e saiu da fila, decrementa a variável fila
    # libera o recurso servidorRes
    yield servidorRes.release(request)


# semente do gerador de números aleatórios
random.seed(25)
env = simpy.Environment()                       # cria o environment do modelo
servidorRes = simpy.Resource(env, capacity=1)   # cria o recurso servidorRes
# incia processo de geração de chegadas
env.process(geraChegadas(env))

env.run(until=10)                                # executa o modelo por 5 min
