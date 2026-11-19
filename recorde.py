"""
recorde.py — Salva e lê o recorde em um arquivo de texto.

Usa o conteúdo "Armazenamento permanente em arquivos": o recorde continua
salvo mesmo depois de fechar o jogo. O arquivo recorde.txt tem uma linha
por informação, no formato chave=valor. Exemplo:

    presentes=27
    vitorias=3
"""
import os  # para verificar se o arquivo existe
from config import ARQUIVO_RECORDE  # caminho do arquivo


def ler_recorde():
    """
    Lê o arquivo de recorde e devolve um dicionário com os valores.

    Se o arquivo ainda não existe (primeira vez que o jogo roda), devolve zeros.

    Retorna:
        dict: {'presentes': int, 'vitorias': int}
    """
    recorde = {'presentes': 0, 'vitorias': 0}  # valores padrão
    if not os.path.exists(ARQUIVO_RECORDE):  # o arquivo ainda não foi criado?
        return recorde  # devolve os zeros
    with open(ARQUIVO_RECORDE, 'r', encoding='utf-8') as arquivo:  # abre para leitura ('r')
        conteudo = arquivo.read()  # lê o texto inteiro como uma string
    for linha in conteudo.split('\n'):  # separa o texto em linhas
        linha = linha.strip()  # tira espaços e quebras de linha das pontas
        if '=' in linha:  # só processa linhas no formato chave=valor
            partes = linha.split('=')  # 'presentes=27' vira ['presentes', '27']
            chave = partes[0]  # 'presentes'
            valor = partes[1]  # '27' (ainda é string)
            if chave in recorde and valor.isdigit():  # chave conhecida e valor numérico?
                recorde[chave] = int(valor)  # converte para inteiro e guarda
    return recorde  # devolve o dicionário


def salvar_recorde(recorde):
    """
    Escreve o dicionário de recorde no arquivo (substituindo o conteúdo antigo).

    Parâmetros:
        recorde (dict): {'presentes': int, 'vitorias': int}
    """
    linhas = []  # lista de linhas do arquivo
    for chave in recorde:  # percorre as chaves do dicionário
        linhas.append(f'{chave}={recorde[chave]}')  # monta 'chave=valor' com f-string
    with open(ARQUIVO_RECORDE, 'w', encoding='utf-8') as arquivo:  # abre para escrita ('w')
        arquivo.write('\n'.join(linhas) + '\n')  # junta as linhas com quebra de linha e escreve


def atualizar_recorde(dados, venceu):
    """
    Confere se a partida bateu o recorde e salva no arquivo.

    Parâmetros:
        dados (dict): dados do jogo (usa 'presentes' e 'recorde').
        venceu (bool): True se o jogador chegou no Papai Noel.

    Retorna:
        bool: True se foi um novo recorde de presentes.
    """
    recorde = dados['recorde']  # dicionário com o recorde atual
    novo_recorde = dados['presentes'] > recorde['presentes']  # pegou mais presentes que antes?
    if novo_recorde:  # se sim...
        recorde['presentes'] = dados['presentes']  # ...atualiza o valor
    if venceu:  # se venceu...
        recorde['vitorias'] += 1  # ...conta mais uma vitória
    salvar_recorde(recorde)  # grava no arquivo
    return novo_recorde  # avisa se foi recorde