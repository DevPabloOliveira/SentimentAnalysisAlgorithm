# -*- coding: utf-8 -*-
import yaml
import nltk

nltk.download('punkt')

# Classe para representar um nó da árvore AVL
class Node:
    def __init__(self, palavra, sentimento):
        self.palavra = palavra
        self.sentimento = sentimento
        self.esquerda = None
        self.direita = None
        self.altura = 1

# Classe para representar a árvore AVL
class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    # Função auxiliar para obter a altura de um nó
    def get_altura(self, node):
        if node is None:
            return 0
        return node.altura

    # Função auxiliar para obter o fator de balanceamento de um nó
    def get_balancear(self, node):
        if node is None:
            return 0
        return self.get_altura(node.esquerda) - self.get_altura(node.direita)

    # Função auxiliar para realizar a rotação simples à esquerda
    def rotacionar_esquerda(self, node):
        filho_direito = node.direita
        node.direita = filho_direito.esquerda
        filho_direito.esquerda = node

        node.altura = max(self.get_altura(node.esquerda), self.get_altura(node.direita)) + 1
        filho_direito.altura = max(self.get_altura(filho_direito.esquerda), self.get_altura(filho_direito.direita)) + 1

        return filho_direito

    # Função auxiliar para realizar a rotação simples à direita
    def rotacionar_direita(self, node):
        filho_esquerdo = node.esquerda
        node.esquerda = filho_esquerdo.direita
        filho_esquerdo.direita = node

        node.altura = max(self.get_altura(node.esquerda), self.get_altura(node.direita)) + 1
        filho_esquerdo.altura = max(self.get_altura(filho_esquerdo.esquerda), self.get_altura(filho_esquerdo.direita)) + 1

        return filho_esquerdo

    # Função auxiliar para inserir uma palavra na árvore AVL
    def get_auxiliar_inserir_palavra(self, node, palavra, sentimento):
        if node is None:
            return Node(palavra, sentimento)
        if palavra < node.palavra:
            node.esquerda = self.get_auxiliar_inserir_palavra(node.esquerda, palavra, sentimento)
        else:
            node.direita = self.get_auxiliar_inserir_palavra(node.direita, palavra, sentimento)

        node.altura = max(self.get_altura(node.esquerda), self.get_altura(node.direita)) + 1
        balancear = self.get_balancear(node)

        # Realizar rotações caso necessário para manter o balanceamento
        if balancear > 1 and palavra < node.esquerda.palavra:
            return self.rotacionar_direita(node)
        if balancear < -1 and palavra > node.direita.palavra:
            return self.rotacionar_esquerda(node)
        if balancear > 1 and palavra > node.esquerda.palavra:
            node.esquerda = self.rotacionar_esquerda(node.esquerda)
            return self.rotacionar_direita(node)
        if balancear < -1 and palavra < node.direita.palavra:
            node.direita = self.rotacionar_direita(node.direita)
            return self.rotacionar_esquerda(node)

        return node

    # Função para inserir uma palavra na árvore AVL
    def inserir_palavra_na_arvore(self, palavra, sentimento):
        self.raiz = self.get_auxiliar_inserir_palavra(self.raiz, palavra, sentimento)

    # Função auxiliar para pesquisar uma palavra na árvore AVL
    def get_auxiliar_buscar_palavra(self, node, palavra):
        if node is None or node.palavra == palavra:
            return node
        if palavra < node.palavra:
            return self.get_auxiliar_buscar_palavra(node.esquerda, palavra)
        return self.get_auxiliar_buscar_palavra(node.direita, palavra)

    # Função para pesquisar uma palavra na árvore AVL
    def buscar_palavra_na_arvore(self, palavra):
        return self.get_auxiliar_buscar_palavra(self.raiz, palavra)


# Função para carregar um dicionário YAML contendo as palavras-chave e seus sentimentos
def carregar_dicionario(file_name):
    with open(file_name, 'r') as file:
        dicionario = yaml.safe_load(file)

    resultado = {}
    for k, v in dicionario.items():
        key = k.lower()
        if isinstance(v, list):
            resultado[key] = [x.lower() for x in v]
        else:
            resultado[key] = str(v).lower()

    return resultado


# Função para calcular o escore de sentimento de um texto
def calcular_score_sentimento(text, avl_tree, dicionario):
    words = nltk.word_tokenize(text)
    score_sentimento = 0
    count_positivas = 0
    count_negativas = 0
    count_ameacas = 0

    for palavra in words:
        palavra = palavra.lower()
        node = avl_tree.buscar_palavra_na_arvore(palavra)

        if node is not None and palavra in dicionario:
            score_sentimento += node.sentimento
            if node.sentimento > 0:
                count_positivas += 1
            elif node.sentimento < 0:
                count_negativas += 1
            elif node.sentimento < -1:
                count_ameacas += 1

    return score_sentimento, count_positivas, count_negativas, count_ameacas


# Carregar os dicionários YAML contendo as palavras-chave e sentimentos
positivo_dict = carregar_dicionario('Dics/positivo.yml')
negativo_dict = carregar_dicionario('Dics/negativo.yml')
ameaca_dict = carregar_dicionario('Dics/ameaca.yml')

# Atualizar os valores dos dicionários com os novos sentimentos
negativo_dict = {k: -1 for k in negativo_dict}
positivo_dict = {k: 1 for k in positivo_dict}
ameaca_dict = {k: -2 for k in ameaca_dict}

# Construir as árvores AVL correspondentes aos dicionários
positivo_arvore = ArvoreAVL()
negativo_arvore = ArvoreAVL()
ameaca_arvore = ArvoreAVL()

for palavra, sentimento in positivo_dict.items():
    positivo_arvore.inserir_palavra_na_arvore(palavra.lower(), sentimento)

for palavra, sentimento in negativo_dict.items():
    negativo_arvore.inserir_palavra_na_arvore(palavra.lower(), sentimento)

for palavra, sentimento in ameaca_dict.items():
    ameaca_arvore.inserir_palavra_na_arvore(palavra.lower(), sentimento)

# Texto a ser analisado
with open('ListaPalavas.txt', 'r', encoding='utf-8') as file:
    text = file.read()

print(f"Texto lido do arquivo: {text}")


# Calcular o escore de sentimento geral e contar as palavras positivas, negativas e ameaças
score_sentimento_positivo, count_positivas, _, count_ameacas = calcular_score_sentimento(text, positivo_arvore, positivo_dict)
score_sentimento_negativo, _, count_negativas, _, = calcular_score_sentimento(text, negativo_arvore, negativo_dict)
score_sentimento_ameaca, _, count_ameacas, _, = calcular_score_sentimento(text, ameaca_arvore, ameaca_dict)

# Inferir o sentimento predominante
if abs(score_sentimento_positivo) > abs(score_sentimento_negativo) and abs(score_sentimento_positivo) > abs(score_sentimento_ameaca):
    sentimento = "positivo"  # Positivo
elif abs(score_sentimento_negativo) > abs(score_sentimento_positivo) and abs(score_sentimento_negativo) > abs(score_sentimento_ameaca):
    sentimento = "negativo"  # Negativo
elif abs(score_sentimento_ameaca) > abs(score_sentimento_positivo) and abs(score_sentimento_ameaca) > abs(score_sentimento_negativo):
    sentimento = "ameaça"  # Ameaça
else:
    sentimento = "neutro"  # Neutro


print("\n")
print(f"Sentimento predominante do texto: {sentimento}")

print(f"Número de palavras positivas: {count_positivas}")
print(f"Número de palavras negativas: {count_negativas}")
print(f"Número de palavras ameaças: {count_ameacas}")

print('concluído')