# NSGA-II para Problema de Mochila Multiobjetivo

Este repositório contém a implementação, em Python, do algoritmo NSGA-II aplicada a uma versão multiobjetivo do problema de mochila/carremento de caminhão.

A formulação considera:

- Objetivo 1: maximizar o valor total dos itens selecionados.
- Objetivo 2: minimizar um custo logístico que combina volume ocupado e quantidade de itens.

Foram usados conjuntos de 28, 56 e 112 itens, com capacidades de 3, 6 e 9 m³.

---

## Estrutura do repositório

- `nsga2_mochila28.py`  
- `nsga2_mochila56.py`  
- `nsga2_mochila112.py`  
  Implementações do NSGA-II para instâncias com 56 e 112 itens (a versão de 28 segue a mesma lógica).

- `resultados/`  
  Resumos das execuções do NSGA-II em formato CSV:
  - `nsga2_28_itens_resumo_cap3.csv`, `cap6`, `cap9`
  - `nsga2_56_itens_resumo_cap3.csv`, `cap6`, `cap9`
  - `nsga2_112_itens_resumo_cap3.csv`, `cap6`, `cap9`

  Cada arquivo contém, por capacidade:
  - média do valor,
  - desvio padrão,
  - melhor valor encontrado,
  - custo da melhor solução,
  - volume e quantidade de itens da melhor solução,
  - tempo médio de execução.

- `apresentacao/main.tex`  
  Arquivo da apresentação em Beamer, usada na disciplina Tópicos Avançados em IA (UFRPE), comparando o NSGA-II com o AG monoobjetivo do Abner.

---

## Formulação do problema

- Cada indivíduo é um cromossomo binário, onde cada posição representa um item:
  - 1: item selecionado
  - 0: item não selecionado

- Objetivos:
  - Objetivo 1 (maximização): valor total da carga valor = soma dos valores dos itens selecionados
  - Objetivo 2 (minimização): custo logístico custo = 1000 × volume_total + 10 × quantidade_de_itens

- Restrição:
  - Se o volume total excede a capacidade do caminhão, a solução é penalizada (valor muito baixo e custo muito alto).

---

## Descrição da implementação

Principais componentes:

- Classe de indivíduo:
  - armazena cromossomo, valor, custo, volume e quantidade de itens;
  - possui método de avaliação que calcula os dois objetivos e aplica a penalização.

- NSGA-II:
  - população inicial aleatória;
  - seleção por torneio binário;
  - operadores de cruzamento e mutação binária;
  - ordenação por dominância de Pareto;
  - cálculo de crowding distance;
  - seleção dos sobreviventes com base em rank de dominância e diversidade.

Parâmetros típicos usados nos experimentos
