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
    Item("God Of War Ragnarok PS4 - Standard Edition", 0.00077, 160),
    Item("Ventilador Mondial", 0.042017, 130),
    Item("Liquidificador Turbo Power Mondial", 0.01722, 99),
    Item("Lavadora de Alta Pressão WAP", 0.04394, 448),
    Item("Furadeira Parafusadeira WAP", 0.002819, 172),
    Item("Fonte MSI MAG", 0.001806, 588.22),
    Item("Monitor Gamer LG", 0.037278, 459.99),
    Item("Utensílios de Cozinha de Madeira", 0.00385, 384),
    Item("Estante Aparador", 0.608, 108.85),
    Item("3 Prateleiras", 0.012, 99.99),
    Item("Panela de Pressão 4,5 Polida", 0.012, 78.72),
    Item("Varal Dobrável", 0.00364, 50.9),
    Item("Módulo Automotivo Soundigital", 0.000776, 399.9),
    Item("Churrasqueira Elétrica Giratória de Inox", 0.152898, 2077.67),
    Item("Balcão Caixa Recepção Wallet", 0.264, 499.99),
    Item("Fogão Cooktop Chamalar", 0.046512, 614.92),
    Item("Multiprocessador Philco", 0.03159, 568.9),
    Item("Cortador Elétrico Mondial Spiralize", 0.01036, 308.9),
    Item("Passadeira de Roupas", 0.04446, 215),
    Item("Mala de Viagem Rose em ABS - P", 0.06591, 490),
    Item("Fritadeira Industrial Elétrica Cuba Profissional", 0.025461, 270.9),
    Item("Box - O Fantasma da Ópera", 0.001137, 79.9),
    Item("Bauleto 28L Smart Box Pro Tork", 0.048, 105.99),
    Item("Taça Prime Scotland Degustação Whisky", 0.00098, 120.9),
    Item("Copo Trainer 220ml MAM Rosa", 0.000936, 64.9),
    Item("Glencairn Copo de Uísque (15 cm) - Pacote Comercial", 0.007704, 103.9),
    Item("Lâmpada Inteligente 15W Smart", 0.00101, 57.49),
    Item("Câmera de Esgoto com Tela LED", 0.0168, 1503),
    Item("A História da Terra-média - Box 2", 0.003005, 289.9),
    Item("Escova de Dentes MAM Training Brush Azul", 0.000073, 27.46),
    Item("Mini Desembaraçador Aqua (Exclusivo Amazon)", 0.000713, 30.73),
    Item("Umidificador Difusor de Ar BanpinSH", 0.001604, 113.9),
    Item("Faqueiro Amazonas 48 Peças Tramontina", 0.002728, 469.9),
    Item("Controle Remoto Universal para Smart TVs", 0.000313, 19.9),
    Item("Balcão Cozinha Armário Gabinete para Pia", 0.6179, 434.9),
    Item("Nebzmart Portátil", 0.001954, 398.59),
    Item("Pruie Mini Carregador de Bateria Portátil", 0.000019, 55.99),
    Item("Shampoo Desamarelador Truss Blond 300ml", 0.000568, 89.9),
    Item("Mop Flat Chenile com Cabo Telescópico", 0.00712, 34.99),
    Item("Magic Mixies - Caldeirão Mágico Rosa", 0.020384, 732.97),
    Item("Barbeador Série Flex", 0.001861, 1089.79),
    Item("Barbeador Elétrico Seco Philips", 0.001888, 450),
    Item("Magic Mixies - Mixlings Twin Pack", 0.001803, 169.89),
    Item("Sérum Facial Vitamina C 10% Tracta", 0.000132, 69.99),
    Item("Jogo de Facas Tramontina Colorcut", 0.004292, 169.9),
    Item("Multiplicador 5 Tomadas Bivolt", 0.000768, 110.57),
    Item("BLACK+DECKER Ferro a Vapor", 0.004461, 120.05),
    Item("Headset Gamer HyperX Cloud II", 0.006218, 590),
    Item("Natura Essencial Único Deo Parfum Feminino 90ml", 0.000815, 156.81),
    Item("Phebo Sabonete Líquido 320ml", 0.000581, 19.9),
    Item("Jogo Rummikub Júnior", 0.005944, 69.99),
    Item("Lixeira para Banheiro 3L", 0.007225, 49.9),
    Item("Caixa Organizadora Empilhável Bambu", 0.003291, 89.9),
    Item("Arandela Carvalho", 0.014896, 129.9),
    Item("Gaveteiro Madeira Branco", 0.1364, 999.9),
    Item("Vela Aromatizada Jasmim Silvestre Branco", 0.000475, 99.9)
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
