# Análise de Sentimento com Árvore AVL

Este é um projeto simples que utiliza uma árvore AVL para realizar a análise de sentimentos em um texto. O código está escrito em Python e inclui a implementação da árvore AVL, bem como funções para carregar dicionários YAML de palavras-chave e calcular o escore de sentimento de um texto.

## Pré-requisitos

Certifique-se de ter o Python instalado em seu ambiente. Além disso, execute o seguinte comando para baixar as dependências necessárias:

        pip install nltk pyyaml

## Como Usar

1. Clone o repositório para o seu ambiente local:

        git clone https://github.com/DevPabloOliveira/SentimentAnalysisAlgorithm
        cd SentimentAnalysisAlgorithm

3. Execute o código Python:
   
        python SentimentAnalysisAlgorithm.py

Certifique-se de ter um arquivo de texto chamado `ListaPalavras.txt` no mesmo diretório. Você pode fazer alterações na estrutura tando dos dicionários quanto da lista de palavras a ser analisada.

## Estrutura do Projeto

        SentimentAnalysisAlgorithm.py: Contém o código principal.
        Dics/: Diretório contendo os dicionários YAML de palavras-chave e sentimentos.
        ListaPalavras.txt: Arquivo de texto a ser analisado.

## Notas Importantes

O projeto usa a biblioteca NLTK para tokenização de palavras. Certifique-se de ter as dependências instaladas usando `nltk.download('punkt')`.
Os dicionários YAML fornecem as palavras-chave e seus respectivos sentimentos, contribuindo para o escore geral de sentimento.

## Resultados da Análise

O código imprimirá o texto lido do arquivo, o sentimento predominante do texto (positivo, negativo, ameaça ou neutro), e o número de palavras positivas, negativas e ameaças encontradas.


        Sentimento predominante do texto: [sentimento]
        Número de palavras positivas: [count_positivas]
        Número de palavras negativas: [count_negativas]
        Número de palavras ameaças: [count_ameacas]
        concluído

Visualise os resultados ao final da execução `[sentimento]`, `[count_positivas]`, `[count_negativas]` e `[count_ameacas]`.
