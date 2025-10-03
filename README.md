# Algoritmo Genético para Distribuição de Carga em Avião

Este projeto implementa um **Algoritmo Genético** em Python para resolver o problema de **distribuição de carga em um avião** de forma a maximizar o lucro da empresa, respeitando restrições de peso, volume e equilíbrio do avião.

---

## Descrição do Problema

O problema consiste em distribuir quatro tipos de carga (C1, C2, C3 e C4) em três compartimentos do avião (Dianteiro, Central e Traseiro) de forma a maximizar o lucro. Cada compartimento possui limites de peso e volume, e cada carga possui peso, volume por tonelada e lucro por tonelada.

### Compartimentos:

| Compartimento | Volume (m³) | Peso (toneladas) |
|---------------|-------------|-----------------|
| Dianteiro (D) | 6800        | 10              |
| Central (C)   | 8700        | 16              |
| Traseiro (T)  | 5300        | 8               |

### Cargas:

| Carga | Volume (m³/ton) | Peso (toneladas) | Lucro (R$/ton) |
|-------|-----------------|-----------------|----------------|
| C1    | 480             | 18              | 310            |
| C2    | 650             | 15              | 380            |
| C3    | 580             | 23              | 350            |
| C4    | 390             | 12              | 285            |

### Restrições:

- Cada carga pode ser dividida entre dois ou mais compartimentos, desde que cada fração seja **≥ 1 kg**.
- O peso alocado em cada compartimento deve ser proporcional ao volume disponível para manter o equilíbrio do avião.
- Nenhum compartimento pode exceder seu limite de peso ou volume.

---

## Como Executar

### Link do Google Colab:

[https://colab.research.google.com/drive/1A9dn0ORcsN1bkAIGBe9YTje72Ib_ReB6?usp=sharing](https://colab.research.google.com/drive/1A9dn0ORcsN1bkAIGBe9YTje72Ib_ReB6?usp=sharing)

Obs.: demora mais para execução (uns 10 minutos)

### Por este repositório:

Obs.: demora menos para executar, dependendo da máquina (em testes deu uns 1min40s)

1. Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd <DIRETORIO_DO_REPOSITORIO>
```

2. Ative o ambiente virtual :
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Instale as dependências:
```bash
pip install numpy pandas tabulate
```

4. Execute o código:
```bash
python Algoritmo_Genetico_Aviao.py
```

5. O programa exibirá:
- Progresso do algoritmo a cada 100 gerações.
- A tabela com a distribuição de cada carga nos compartimentos.
- O fitness final (lucro total considerando penalidades).

6. Para sair do ambiente virtual:
```bash
deactivate
```

---

## Exemplo de Saída
```
Geração 0: Melhor fitness = 7640.54
[...]
Geração 2400: Melhor fitness = 11534.47

####################################################

Melhor indivíduo encontrado: 
(toneladas de cada carga em cada compartimento)

╒════╤═════════╤══════════╤══════════╕
│    │       D │        C │        T │
╞════╪═════════╪══════════╪══════════╡
│ C1 │ 0.43186 │ 2.72662  │ 2.72805  │
├────┼─────────┼──────────┼──────────┤
│ C2 │ 6.74185 │ 9.08315  │ 3.38595  │
├────┼─────────┼──────────┼──────────┤
│ C3 │ 2.62406 │ 0.922253 │ 1.58428  │
├────┼─────────┼──────────┼──────────┤
│ C4 │ 0.17466 │ 2.12401  │ 0.256278 │
╘════╧═════════╧══════════╧══════════╛


Resumo do melhor indivíduo: 
(peso e volume por compartimento)

╒════╤════════════╤════════════════╕
│    │ peso (t)   │ volume (m³)    │
╞════╪════════════╪════════════════╡
│ D  │ 9.97 / 10  │ 6179.57 / 6800 │
├────┼────────────┼────────────────┤
│ C  │ 14.86 / 16 │ 8576.10 / 8700 │
├────┼────────────┼────────────────┤
│ T  │ 7.95 / 8   │ 4529.16 / 5300 │
╘════╧════════════╧════════════════╛


Peso total ocupado: 32.78 t / 34 t
Volume total ocupado: 19284.83 m³ / 20800 m³

Fitness final: 11534.47
Lucro total: R$11648.86

####################################################
```