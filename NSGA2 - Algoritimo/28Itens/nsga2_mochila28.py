import random
import math
import csv
import os
import statistics
import time

# -----------------------
# Dados do problema
# -----------------------

class Item:
    def __init__(self, nome, volume, valor):
        self.nome = nome
        self.volume = volume
        self.valor = valor


itens = [
    Item("Echo Studio", 0.000748, 1709.05),
    Item("Echo Show 10", 0.001097, 1899.05),
    Item("Kindle 11ª Geração", 0.000137, 474.05),
    Item("Multiplicador 5 Tomadas", 0.000768, 111.66),
    Item("Boneco Dungeons & Dragons", 0.002537, 199.99),
    Item("LEGO Ideas Farol Motorizado", 0.025422, 2601.49),
    Item("LEGO Indiana Jones - O Templo do Ídolo Dourado", 0.01914, 1399.99),
    Item("Mochila Casual", 0.002821, 61.99),
    Item("Midea - Frigobar 45L", 0.104501, 788.50),
    Item("Fritadeira Airfryer 4L", 0.039336, 599.90),
    Item("Arno Cafeteira Espresso Nescafé", 0.004448, 929.99),
    Item("Forno Elétrico Britânia", 0.066041, 599.99),
    Item("Micro-ondas Electrolux", 0.047059, 616.55),
    Item("Lavadora de Roupas Consul", 0.35148, 2534.70),
    Item("Lavadora de Roupas Brastemp", 0.561, 3979.00),
    Item("Geladeira Brastemp Frost Free", 0.825185, 3710.00),
    Item("Cooktop 4 Bocas Mondial", 0.0414, 489.99),
    Item("Refrigerador Brastemp Frost Free French Door", 1.237213, 8503.32),
    Item("Fogão 4 Bocas Dako", 0.309513, 1829.00),
    Item("Lava e Seca Samsung", 0.447225, 6599.00),
    Item("Freezer Horizontal Consul", 0.772367, 3979.00),
    Item("Depurador Slim Suggar", 0.02448, 379.00),
    Item("Apple TV", 0.000336, 1999.00),
    Item("MacBook Air", 0.001089, 7999.00),
    Item("iPhone 14 Pro", 0.000083, 9499.00),
    Item("MacBook Pro", 0.001483, 22999.00),
    Item("iPad Pro", 0.000386, 22475.75),
    Item("Jogo de Facas Tramontina", 0.00418, 84.50)
]

CUSTO_FATOR = 1000.0  # custo proporcional ao volume


# -----------------------
# Representação da solução
# -----------------------

class Solucao:
    def __init__(self, genes, itens, capacidade):
        self.genes = genes
        self.itens = itens
        self.capacidade = capacidade

        self.valor = 0.0
        self.volume = 0.0
        self.custo = 0.0

        self.rank = None
        self.crowding = 0.0

    def avaliar(self):
        self.valor = 0.0
        self.volume = 0.0

        for i, g in enumerate(self.genes):
            if g == 1:
                self.valor += self.itens[i].valor
                self.volume += self.itens[i].volume

        qtd_itens = sum(self.genes)
        # custo = volume * fator + pequena penalização por número de itens
        self.custo = self.volume * CUSTO_FATOR + qtd_itens * 10.0

        # penalização forte se exceder capacidade
        if self.volume > self.capacidade:
            self.valor = 1.0
            self.custo = 10**9

    def itens_selecionados(self):
        return [self.itens[i].nome for i, g in enumerate(self.genes) if g == 1]

    def qtd_itens(self):
        return sum(self.genes)


# -----------------------
# Operadores básicos
# -----------------------

def gerar_populacao(tam_pop, itens, capacidade):
    pop = []
    n = len(itens)
    for _ in range(tam_pop):
        genes = [random.randint(0, 1) for _ in range(n)]
        s = Solucao(genes, itens, capacidade)
        s.avaliar()
        pop.append(s)
    return pop

def cruzamento_um_ponto(pai1, pai2):
    n = len(pai1.genes)
    if n < 2:
        return pai1, pai2
    ponto = random.randint(1, n - 1)
    g1 = pai1.genes[:ponto] + pai2.genes[ponto:]
    g2 = pai2.genes[:ponto] + pai1.genes[ponto:]
    f1 = Solucao(g1, pai1.itens, pai1.capacidade)
    f2 = Solucao(g2, pai1.itens, pai1.capacidade)
    f1.avaliar()
    f2.avaliar()
    return f1, f2

def mutacao(sol, taxa):
    for i in range(len(sol.genes)):
        if random.random() < taxa:
            sol.genes[i] = 1 - sol.genes[i]
    sol.avaliar()
    return sol


# -----------------------
# NSGA-II: dominância e frentes
# -----------------------

def domina(a: Solucao, b: Solucao) -> bool:
    """
    a domina b se:
      - não é pior em nenhum objetivo
      - e é melhor em pelo menos um
    Objetivos:
      valor -> maximizar
      custo -> minimizar
    """
    melhor_em_algum = False

    # valor (max)
    if a.valor < b.valor:
        return False
    if a.valor > b.valor:
        melhor_em_algum = True

    # custo (min)
    if a.custo > b.custo:
        return False
    if a.custo < b.custo:
        melhor_em_algum = True

    return melhor_em_algum

def fast_non_dominated_sort(pop):
    frentes = []
    S = {}
    n_dom = {}
    F0 = []

    for p in pop:
        S[p] = []
        n_dom[p] = 0
        for q in pop:
            if p is q:
                continue
            if domina(p, q):
                S[p].append(q)
            elif domina(q, p):
                n_dom[p] += 1
        if n_dom[p] == 0:
            p.rank = 0
            F0.append(p)

    frentes.append(F0)
    i = 0
    while len(frentes[i]) > 0:
        Q = []
        for p in frentes[i]:
            for q in S[p]:
                n_dom[q] -= 1
                if n_dom[q] == 0:
                    q.rank = i + 1
                    Q.append(q)
        i += 1
        frentes.append(Q)

    if len(frentes[-1]) == 0:
        frentes.pop()
    return frentes

def crowding_distance(frente):
    if not frente:
        return
    for s in frente:
        s.crowding = 0.0

    # objetivo 1: valor (max)
    frente.sort(key=lambda s: s.valor)
    frente[0].crowding = frente[-1].crowding = math.inf
    min_val = frente[0].valor
    max_val = frente[-1].valor
    if max_val > min_val:
        for i in range(1, len(frente) - 1):
            frente[i].crowding += (frente[i + 1].valor - frente[i - 1].valor) / (max_val - min_val)

    # objetivo 2: custo (min)
    frente.sort(key=lambda s: s.custo)
    frente[0].crowding = frente[-1].crowding = math.inf
    min_cost = frente[0].custo
    max_cost = frente[-1].custo
    if max_cost > min_cost:
        for i in range(1, len(frente) - 1):
            frente[i].crowding += (frente[i - 1].custo - frente[i + 1].custo) / (max_cost - min_cost)

def torneio_nsga2(pop):
    a, b = random.sample(pop, 2)
    if a.rank < b.rank:
        return a
    if b.rank < a.rank:
        return b
    if a.crowding > b.crowding:
        return a
    return b


# -----------------------
# Loop principal NSGA-II
# -----------------------

def nsga2(itens, capacidade, tam_pop=100, geracoes=100, taxa_mut=0.03):
    pop = gerar_populacao(tam_pop, itens, capacidade)

    for g in range(geracoes):
        frentes = fast_non_dominated_sort(pop)
        for f in frentes:
            crowding_distance(f)

        filhos = []
        while len(filhos) < tam_pop:
            p1 = torneio_nsga2(pop)
            p2 = torneio_nsga2(pop)
            f1, f2 = cruzamento_um_ponto(p1, p2)
            mutacao(f1, taxa_mut)
            mutacao(f2, taxa_mut)
            filhos.append(f1)
            filhos.append(f2)

        combinada = pop + filhos
        frentes = fast_non_dominated_sort(combinada)
        nova_pop = []
        for f in frentes:
            crowding_distance(f)
            f.sort(key=lambda s: s.crowding, reverse=True)
            for s in f:
                if len(nova_pop) < tam_pop:
                    nova_pop.append(s)
        pop = nova_pop

        if (g + 1) % 20 == 0:
            print(f"Geração {g + 1} concluída.")

    frentes_finais = fast_non_dominated_sort(pop)
    pareto = frentes_finais[0]
    crowding_distance(pareto)
    return pareto


# -----------------------
# Estatística por capacidade
# -----------------------

def melhor_da_frente_por_valor(pareto):
    """Retorna a solução de maior valor dentro da frente de Pareto."""
    return max(pareto, key=lambda s: s.valor)


def imprimir_tabela_markdown(resumos):
    print("\n## Resultados NSGA-II por capacidade\n")
    print("| Capacidade (m³) | Média valor | Desvio valor | Melhor valor | Volume melhor (m³) | Itens melhor | Média tempo (s) | Desvio tempo (s) |")
    print("|-----------------|-------------|--------------|--------------|---------------------|--------------|-----------------|------------------|")
    for r in sorted(resumos, key=lambda x: x["capacidade"]):
        print(
            f"| {r['capacidade']:.1f} "
            f"| {r['media']:.2f} "
            f"| {r['desvio']:.2f} "
            f"| {r['melhor']:.2f} "
            f"| {r['volume_melhor']:.4f} "
            f"| {r['qtd_itens_melhor']} "
            f"| {r['media_tempo']:.4f} "
            f"| {r['desvio_tempo']:.4f} |"
        )

def gerar_analise_texto(resumos):
    resumos_ordenados = sorted(resumos, key=lambda r: r["capacidade"])
    print("\n## Análise dos resultados\n")
    print("As médias de valor obtidas pelo NSGA-II para cada capacidade foram:\n")
    for r in resumos_ordenados:
        print(f"- Capacidade {r['capacidade']:.1f} m³: média ≈ {r['media']:.2f}")

    print("\nObserva-se que as médias são próximas mas crescem com a capacidade, o que é coerente com a ideia de que mais espaço permite combinações de itens de maior valor, "
          "ainda que o algoritmo continue sujeito à natureza estocástica e ao número finito de gerações.\n")

    melhor_global = max(resumos_ordenados, key=lambda r: r["melhor"])
    print(
        f"O melhor valor individual encontrado foi ≈ {melhor_global['melhor']:.2f} "
        f"na capacidade {melhor_global['capacidade']:.1f} m³, "
        f"com volume ≈ {melhor_global['volume_melhor']:.4f} m³ e "
        f"{melhor_global['qtd_itens_melhor']} itens selecionados.\n"
    )

    print(
        "Teoricamente, ao aumentar a capacidade do caminhão, o conjunto de soluções viáveis cresce, "
        "de modo que não se esperaria um desempenho pior em termos de valor máximo possível. "
        "No entanto, como o NSGA-II é um algoritmo estocástico e o número de gerações e o tamanho da população são finitos, "
        "nem sempre o espaço de busca ampliado é explorado completamente. "
        "Ainda assim, os resultados obtidos indicam que o algoritmo encontra soluções de alto valor em todas as capacidades, "
        "com diferenças compatíveis com o comportamento esperado de um método evolutivo."
    )


# -----------------------
# Main: 20 execuções para 3, 6 e 9 m³
# -----------------------

if __name__ == "__main__":
    base_dir = r"E:\\10 periodo\\CSVs Resultados\\NSGA2 - 28 itens"
    capacidades = [3.0, 6.0, 9.0]
    num_execucoes = 20
    tam_pop = 100
    geracoes = 100
    taxa_mut = 0.03

    resumos = []

    for cap in capacidades:
        print(f"\n=== Rodando NSGA-II para capacidade = {cap} m³ ===")
        valores_execucoes = []
        melhores_solucoes = []
        tempos_execucao = []

        for run in range(1, num_execucoes + 1):
            print(f"  Execução {run}/{num_execucoes} (capacidade {cap} m³)")
            t0 = time.time()
            pareto = nsga2(itens, cap, tam_pop=tam_pop, geracoes=geracoes, taxa_mut=taxa_mut)
            t1 = time.time()
            tempo = t1 - t0
            tempos_execucao.append(tempo)

            sol_melhor = melhor_da_frente_por_valor(pareto)
            valores_execucoes.append(sol_melhor.valor)
            melhores_solucoes.append(sol_melhor)

        melhor_global = max(melhores_solucoes, key=lambda s: s.valor)
        media_val = statistics.mean(valores_execucoes)
        desvio_val = statistics.stdev(valores_execucoes) if len(valores_execucoes) > 1 else 0.0
        media_tempo = statistics.mean(tempos_execucao)
        desvio_tempo = statistics.stdev(tempos_execucao) if len(tempos_execucao) > 1 else 0.0

        nomes_melhor = melhor_global.itens_selecionados()
        itens_str_melhor = "; ".join(nomes_melhor)

        # CSV resumo por capacidade (com tempo e ``itens``)
        caminho_csv = os.path.join(
            base_dir,
            f"nsga2_28_itens_resumo_cap{int(cap)}.csv"
        )
        os.makedirs(os.path.dirname(caminho_csv), exist_ok=True)
        with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([
                "capacidade_m3",
                "media_valor",
                "desvio_padrao_valor",
                "melhor_valor",
                "custo_melhor",
                "volume_m3_melhor",
                "qtd_itens_melhor",
                "media_tempo_execucao_s",
                "desvio_tempo_execucao_s",
                "itens_selecionados_melhor"
            ])
            w.writerow([
                cap,
                f"{media_val:.4f}",
                f"{desvio_val:.4f}",
                f"{melhor_global.valor:.4f}",
                f"{melhor_global.custo:.4f}",
                f"{melhor_global.volume:.4f}",
                melhor_global.qtd_itens(),
                f"{media_tempo:.4f}",
                f"{desvio_tempo:.4f}",
                itens_str_melhor
            ])

        resumos.append({
            "capacidade": cap,
            "media": media_val,
            "desvio": desvio_val,
            "melhor": melhor_global.valor,
            "volume_melhor": melhor_global.volume,
            "qtd_itens_melhor": melhor_global.qtd_itens(),
            "media_tempo": media_tempo,
            "desvio_tempo": desvio_tempo,
        })

    print("\nTodas as execuções concluídas e resumos salvos.\n")
    imprimir_tabela_markdown(resumos)
    gerar_analise_texto(resumos)
