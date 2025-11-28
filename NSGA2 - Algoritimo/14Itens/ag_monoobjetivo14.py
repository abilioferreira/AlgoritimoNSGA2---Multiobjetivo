import random
import statistics

class Item:
    def __init__(self, nome, volume, valor):
        self.nome = nome
        self.volume = volume
        self.valor = valor

class Solucao:
    def __init__(self, genes, itens, capacidade):
        self.genes = genes
        self.itens = itens
        self.capacidade = capacidade
        self.valor = 0
        self.volume = 0
        self.valida = True

    def avaliar(self):
        self.valor = 0
        self.volume = 0
        for i, gene in enumerate(self.genes):
            if gene == 1:
                self.valor += self.itens[i].valor
                self.volume += self.itens[i].volume
        if self.volume > self.capacidade:
            self.valor = 1
            self.valida = False
        else:
            self.valida = True

    def __repr__(self):
        return f"Valor: {self.valor:.2f}, Volume: {self.volume:.4f}"

def gerar_populacao(itens, capacidade, tam_pop):
    pop = []
    n = len(itens)
    for _ in range(tam_pop):
        genes = [random.randint(0, 1) for _ in range(n)]
        s = Solucao(genes, itens, capacidade)
        s.avaliar()
        pop.append(s)
    return pop

def selecao_roleta(populacao):
    fitness_total = sum(s.valor for s in populacao)
    if fitness_total == 0:
        return random.choice(populacao)
    probabilidades = [s.valor / fitness_total for s in populacao]
    return random.choices(populacao, weights=probabilidades, k=1)[0]

def selecao_torneio(populacao, tamanho_torneio=2):
    torneio = random.sample(populacao, tamanho_torneio)
    return max(torneio, key=lambda x: x.valor)

def cruzamento_um_ponto(pai1, pai2):
    n = len(pai1.genes)
    ponto = random.randint(1, n - 1)
    filho1_genes = pai1.genes[:ponto] + pai2.genes[ponto:]
    filho2_genes = pai2.genes[:ponto] + pai1.genes[ponto:]
    filho1 = Solucao(filho1_genes, pai1.itens, pai1.capacidade)
    filho2 = Solucao(filho2_genes, pai1.itens, pai1.capacidade)
    filho1.avaliar()
    filho2.avaliar()
    return filho1, filho2

def mutacao(solucao, taxa_mutacao):
    for i in range(len(solucao.genes)):
        if random.random() < taxa_mutacao:
            solucao.genes[i] = 1 - solucao.genes[i]
    solucao.avaliar()

def ag_monoobjetivo(itens, capacidade, tam_pop, num_geracoes, taxa_mut, usar_torneio=True):
    populacao = gerar_populacao(itens, capacidade, tam_pop)
    for _ in range(num_geracoes):
        nova_populacao = []
        for _ in range(tam_pop):
            if usar_torneio:
                pai1 = selecao_torneio(populacao)
                pai2 = selecao_torneio(populacao)
            else:
                pai1 = selecao_roleta(populacao)
                pai2 = selecao_roleta(populacao)
            filho1, filho2 = cruzamento_um_ponto(pai1, pai2)
            mutacao(filho1, taxa_mut)
            mutacao(filho2, taxa_mut)
            nova_populacao.append(filho1)
            nova_populacao.append(filho2)
        populacao = sorted(nova_populacao, key=lambda x: x.valor, reverse=True)[:tam_pop]
    melhor = max(populacao, key=lambda x: x.valor)
    return melhor.valor

if __name__ == "__main__":
    itens = [
    Item("Echo Show 8", 0.0026989, 949.05),
    Item("A História da Terra-média - Box 2", 0.002893, 169.99),
    Item("Oster PrimaLatte II - Cafeteira Espresso", 0.030949, 1499.90),
    Item("Umidificador WAP Air Flow", 0.013445, 199.99),
    Item("Aquecedor WAP Air Heat", 0.006393, 138.90),
    Item("Torre WAP Air Silence 220", 0.0927, 479.90),
    Item("Ventilador Rajada Arno", 0.39984, 284.29),
    Item("Risqué Top Coat", 0.000071, 10.16),
    Item("Truss Hidratação Intensa", 0.000008, 379.00),
    Item("CD Dua Lipa - Future Nostalgia", 0.000201, 52.90),
    Item("Mop Plano 3 em 1", 0.057443, 100.73),
    Item("Kit Casa Conectada Positivo", 0.005, 499.99),
    Item("Mouse com fio USB Logitech", 0.001315, 44.90),
    Item("Difusor de Aromas", 0.004677, 139.90)
]
    capacidade = 3.0
    tam_pop = 100
    taxa_mutacao = 0.03
    num_execucoes = 20

    lista_geracoes = [50, 100, 150, 200, 300, 400, 500, 750, 1000]

    print("=" * 70)
    print("ALGORITMO GENÉTICO - COMPARAÇÃO ROLETA vs TORNEIO POR NÚMERO DE GERAÇÕES")
    print("=" * 70)
    print(f"População = {tam_pop}, Execuções por configuração = {num_execucoes}\n")

    for num_geracoes in lista_geracoes:
        resultados_roleta = []
        resultados_torneio = []

        for _ in range(num_execucoes):
            valor_roleta = ag_monoobjetivo(itens, capacidade, tam_pop, num_geracoes, taxa_mutacao, usar_torneio=False)
            valor_torneio = ag_monoobjetivo(itens, capacidade, tam_pop, num_geracoes, taxa_mutacao, usar_torneio=True)
            resultados_roleta.append(valor_roleta)
            resultados_torneio.append(valor_torneio)

        media_roleta = statistics.mean(resultados_roleta)
        desvio_roleta = statistics.stdev(resultados_roleta)
        melhor_roleta = max(resultados_roleta)
        pior_roleta = min(resultados_roleta)

        media_torneio = statistics.mean(resultados_torneio)
        desvio_torneio = statistics.stdev(resultados_torneio)
        melhor_torneio = max(resultados_torneio)
        pior_torneio = min(resultados_torneio)

        print(f"\n=== GERAÇÕES: {num_geracoes} ===")
        print(f"{'Método':<10} {'Média':<15} {'Desvio':<15} {'Melhor':<15} {'Pior':<15}")
        print("-" * 70)
        print(f"{'Roleta':<10} R$ {media_roleta:10.2f} R$ {desvio_roleta:10.2f} R$ {melhor_roleta:10.2f} R$ {pior_roleta:10.2f}")
        print(f"{'Torneio':<10} R$ {media_torneio:10.2f} R$ {desvio_torneio:10.2f} R$ {melhor_torneio:10.2f} R$ {pior_torneio:10.2f}")

        diff = (media_torneio - media_roleta) / media_roleta * 100
        print(f"Torneio foi {diff:+.2f}% melhor que Roleta em média para {num_geracoes} gerações.")
