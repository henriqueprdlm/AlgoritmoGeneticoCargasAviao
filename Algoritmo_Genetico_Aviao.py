import random
import numpy as np
import pandas as pd
from tabulate import tabulate

# Definição das constantes do problema
COMPARTIMENTOS = {
    'D': {'volume': 6800, 'peso': 10},  # dianteiro
    'C': {'volume': 8700, 'peso': 16},  # central
    'T': {'volume': 5300, 'peso': 8}    # traseiro
}

CARGAS = {
    'C1': {'volume': 480, 'peso': 18, 'lucro': 310},  # volume e lucro POR TONELADA
    'C2': {'volume': 650, 'peso': 15, 'lucro': 380},
    'C3': {'volume': 580, 'peso': 23, 'lucro': 350},
    'C4': {'volume': 390, 'peso': 12, 'lucro': 285}
}

# Parâmetros do algoritmo genético
TAMANHO_POPULACAO = 600
GERACOES = 2500
TAXA_MUTACAO = 0.1
TAXA_CROSSOVER = 0.8



def criar_individuo():
    """
    Cria um indivíduo representando a distribuição das cargas nos compartimentos.
    Retorna uma matriz 4x3:
        linhas = cargas (C1, C2, C3, C4)
        colunas = compartimentos (D, C, T)
        valores = toneladas daquela carga colocada no compartimento
    """

    # Criação da matriz 4x3 zerada
    individuo = np.zeros((4, 3))

    # Vetores para acompanhar quanto resta de cada compartimento
    pesos_restantes = [comp['peso'] for comp in COMPARTIMENTOS.values()]
    volumes_restantes = [comp['volume'] for comp in COMPARTIMENTOS.values()]

    # Ordem aleatória das cargas
    cargas_indices = list(range(len(CARGAS)))  # [0,1,2,3]
    random.shuffle(cargas_indices)

    # Iterar sobre cada carga na ordem sorteada
    for i in cargas_indices:
        carga = list(CARGAS.values())[i]

        # Quanto dessa carga ainda pode ser usado (peso máximo)
        peso_max_carga = carga['peso']

        # Quanto ainda cabe no avião em peso
        peso_max_aviao = min(pesos_restantes)

        # Peso aleatório até o mínimo dos dois (mas sempre maior que 1 kg)
        peso_total = np.random.uniform(0.001, max(0.001, min(peso_max_carga, peso_max_aviao)))

        # Distribui esse peso entre os compartimentos (através da distribuição aleatória de Dirichlet)
        distribuicao = np.random.dirichlet(np.ones(3)) * peso_total

        # Verifica volume e peso em cada compartimento
        for j in range(3):  # D, C, T
            peso_adicionado = min(distribuicao[j], pesos_restantes[j])
            volume_adicionado = peso_adicionado * carga['volume']

            # Se couber em volume também
            if volume_adicionado <= volumes_restantes[j]:
                individuo[i, j] = peso_adicionado
                pesos_restantes[j] -= peso_adicionado
                volumes_restantes[j] -= volume_adicionado


    return individuo



def avaliar_individuo(individuo):
    fitness = 0     # soma dos lucros das cargas alocadas
    penalidade = 0  #soma das penalidades de excesso de peso, excesso de volume e desbalanceamento
    
    # Lucro total
    for i, carga in enumerate(CARGAS.values()):   # percorre as cargas
        for j in range(3):                        # percorre cada compartimento
            fitness += individuo[i,j] * carga['lucro']  # fitness é a soma dos lucros (lucro é quantidade de carga alocada * lucro por tonelada da carga)
    
    # Penalidades
    # Verificar restrições de peso e volume -> se exceder zera o fitness, pois é inválido
    pesos_compartimentos = individuo.sum(axis=0)  # soma por coluna (soma de todos os pesos em cada compartimento)
    volumes_compartimentos = np.zeros(3)          # vetor que será usado para calcular volume total ocupado em cada compartimento
    
    for j in range(3):                                # percorre os compartimentos
        for i, carga in enumerate(CARGAS.values()):   # percorre as cargas
            volumes_compartimentos[j] += individuo[i,j] * carga['volume']  # soma dos volumes ocupados pela carga i em cada compartimento j
    
    for j, comp in enumerate(COMPARTIMENTOS.values()):
        if pesos_compartimentos[j] > comp['peso'] or volumes_compartimentos[j] > comp['volume']:
            return 0  # fitness zerado se alguma restrição violada
    
    # Penalidade por desbalanceamento
    peso_total = pesos_compartimentos.sum()   # soma de todos os pesos alocados
    volume_total = sum(comp['volume'] for comp in COMPARTIMENTOS.values())  # soma do volume máximo de todos os compartimentos
    for j, comp in enumerate(COMPARTIMENTOS.values()):
        peso_ideal = peso_total * (comp['volume'] / volume_total)     # quanto de peso deveria estar em cada compartimento para estar equilibrado
        fitness -= abs(pesos_compartimentos[j] - peso_ideal) * 50     # fator de penalidade: diferença absoluta entre peso real e peso ideal, multiplicada por 50

    return fitness 



def criar_populacao(TAMANHO_POPULACAO):
    populacao = []
    for _ in range(TAMANHO_POPULACAO):
        ind = criar_individuo()
        populacao.append(ind)
    return populacao    # população é uma lista de indivíduos (lista de matrizes 4x3)



def selecao_roleta(populacao, fitnesses):
    total_fitness = sum(fitnesses)
    
    if total_fitness == 0:
        # Se todos forem inválidos, escolhemos aleatoriamente
        return random.choice(populacao)
    
    # Probabilidade de seleção proporcional ao fitness (quanto maior fitness, maior chance de ser selecionado)
    probabilidade = [f / total_fitness for f in fitnesses]   # vetor de probabilidades da população
    index_selecionado = np.random.choice(len(populacao), p=probabilidade)  # escolhe um índice da população usando as probabilidades calculadas

    return populacao[index_selecionado]



def crossover(pai1, pai2, taxa_crossover=TAXA_CROSSOVER):
    filho1 = pai1.copy()
    filho2 = pai2.copy()
    
    if np.random.rand() < taxa_crossover:   # se o número aleatório (entre 0 e 1) for menor que a taxa de crossover, ele ocorre
        
        # Crossover uniforme: escolhe aleatoriamente valores de pai1 ou pai2
        for i in range(pai1.shape[0]):
            for j in range(pai1.shape[1]):
                if np.random.rand() < 0.5:    # para cada célula, com 50% de chance, troca os valores entre os pais
                    filho1[i,j] = pai2[i,j]
                    filho2[i,j] = pai1[i,j]
    
    # Se não ocorrer crossover, filhos são cópias exatas dos pais
    return filho1, filho2



def mutacao(individuo, taxa_mutacao=TAXA_MUTACAO):
    for i in range(individuo.shape[0]):
        for j in range(individuo.shape[1]):
            if np.random.rand() < taxa_mutacao:   # se o número aleatório (entre 0 e 1) for menor que a taxa de mutação, ela ocorre
                individuo[i,j] *= np.random.uniform(0.9, 1.1) # Mutação: altera o valor levemente (±10% do valor atual)
    return individuo



# Criar população inicial
populacao = criar_populacao(TAMANHO_POPULACAO)

# Guardar o melhor indivíduo encontrado
melhor_fitness_geral = 0
melhor_individuo_geral = None

# Loop de gerações
for geracao in range(GERACOES):
    nova_populacao = []   # Para armazenar os filhos gerados nesta geração

    # Avaliar fitnesses uma vez por geração
    fitnesses = [avaliar_individuo(ind) for ind in populacao]

    while len(nova_populacao) < TAMANHO_POPULACAO:
        
        # Selecionar dois pais
        pai1 = selecao_roleta(populacao, fitnesses)
        pai2 = selecao_roleta(populacao, fitnesses)

        # Crossover
        filho1, filho2 = crossover(pai1, pai2)

        # Mutação
        filho1 = mutacao(filho1)
        filho2 = mutacao(filho2)

        # Adicionar filhos à nova população
        nova_populacao.extend([filho1, filho2])

    # Garantir que a população tenha exatamente TAMANHO_POPULACAO
    populacao = nova_populacao[:TAMANHO_POPULACAO]

    # Avaliar população para acompanhar o melhor (calcula o fitness de todos e identifica o melhor indivíduo)
    fitnesses = [avaliar_individuo(ind) for ind in populacao]
    max_fitness = max(fitnesses)
    idx_melhor = fitnesses.index(max_fitness)

    if max_fitness > melhor_fitness_geral:
        melhor_fitness_geral = max_fitness
        melhor_individuo_geral = populacao[idx_melhor]

    # Mostrar progresso a cada 100 gerações
    if geracao % 100 == 0:
        print(f"Geração {geracao}: Melhor fitness = {melhor_fitness_geral:.2f}")


# Resultado final
import pandas as pd
from tabulate import tabulate
import numpy as np

# Criar DataFrame a partir do melhor indivíduo
cargas = list(CARGAS.keys())                    # ['C1','C2','C3','C4']
compartimentos = list(COMPARTIMENTOS.keys())    # ['D','C','T']

tabela_melhor = pd.DataFrame(melhor_individuo_geral, index=cargas, columns=compartimentos)

# alcular estatísticas do melhor indivíduo
pesos_compartimentos = melhor_individuo_geral.sum(axis=0)
volumes_compartimentos = np.zeros(3)
for j in range(3):  # para cada compartimento
    for i, carga in enumerate(CARGAS.values()):
        volumes_compartimentos[j] += melhor_individuo_geral[i,j] * carga['volume']

# Criar DataFrame resumido
resumo = pd.DataFrame({
    'peso (t)': [f"{pesos_compartimentos[j]:.2f} / {COMPARTIMENTOS[c]['peso']}" 
                 for j, c in enumerate(COMPARTIMENTOS.keys())],
    'volume (m³)': [f"{volumes_compartimentos[j]:.2f} / {COMPARTIMENTOS[c]['volume']}" 
                    for j, c in enumerate(COMPARTIMENTOS.keys())]
}, index=COMPARTIMENTOS.keys())

# Estatísticas gerais
peso_total_ocupado = pesos_compartimentos.sum()
peso_total_max = sum(comp['peso'] for comp in COMPARTIMENTOS.values())
volume_total_ocupado = volumes_compartimentos.sum()
volume_total_max = sum(comp['volume'] for comp in COMPARTIMENTOS.values())
lucro_total = sum(melhor_individuo_geral[i,j] * carga['lucro'] 
                  for i, carga in enumerate(CARGAS.values()) 
                  for j in range(3))

# Impressão final com tabulate
print("\n####################################################")
print("\nMelhor indivíduo encontrado: \n(toneladas de cada carga em cada compartimento)\n")
print(tabulate(tabela_melhor, headers='keys', tablefmt='fancy_grid'))

print("\n\nResumo do melhor indivíduo: \n(peso e volume por compartimento)\n")
print(tabulate(resumo, headers='keys', tablefmt='fancy_grid'))

print(f"\n\nPeso total ocupado: {peso_total_ocupado:.2f} t / {peso_total_max} t")
print(f"Volume total ocupado: {volume_total_ocupado:.2f} m³ / {volume_total_max} m³")
print(f"\nFitness final: {melhor_fitness_geral:.2f}")
print(f"Lucro total: R${lucro_total:.2f}")
print("\n####################################################")
