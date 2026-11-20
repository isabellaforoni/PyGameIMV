"""
recursos.py — Carrega todas as imagens, animações, sons e fontes do jogo.

Tudo fica guardado no dicionário `assets` (como no handout), por exemplo: assets['presente'].
"""
import os  # para montar o caminho de cada arquivo
import pygame  # biblioteca de jogos
from config import PASTA_IMG, PASTA_SND, PASTA_FONTES, ALTURA_JOGADOR, FATOR_ABAIXADO  # constantes

# Lista de dicionários com os personagens que o jogador pode escolher.
# 'chave' é o nome do arquivo de imagem; 'nome' é o texto mostrado na tela.
PERSONAGENS = [
    {'chave': 'rena', 'nome': 'Rena'},  # primeiro personagem
    {'chave': 'gnomo', 'nome': 'Gnomo'},  # segundo personagem
    {'chave': 'gingerbread', 'nome': 'Gingerbread'},  # terceiro personagem
]


def carregar_imagem(nome, altura):
    """Carrega uma imagem PNG e muda a altura dela, mantendo a proporção."""
    caminho = os.path.join(PASTA_IMG, nome + '.png')  # junta pasta + nome + '.png'
    imagem = pygame.image.load(caminho).convert_alpha()  # lê o arquivo; convert_alpha mantém o fundo transparente
    proporcao = imagem.get_width() / imagem.get_height()  # largura dividida pela altura original
    largura = round(altura * proporcao)  # nova largura que mantém a mesma proporção
    return pygame.transform.smoothscale(imagem, (largura, altura))  # devolve a imagem no novo tamanho


def criar_quadros_corrida(imagem, angulo=4):
    """Cria a animação de corrida: uma lista com a imagem inclinada para um lado e para o outro."""
    quadros = []  # lista vazia que vai receber os quadros
    for inclinacao in [0, angulo, 0, -angulo]:  # inclinação (em graus) de cada quadro
        quadros.append(pygame.transform.rotate(imagem, inclinacao))  # gira a imagem e guarda na lista
    return quadros  # devolve a lista pronta


def criar_quadros_presente(imagem):
    """Cria a animação do presente girando (a largura encolhe e volta)."""
    quadros = []  # lista dos quadros
    largura = imagem.get_width()  # largura original
    altura = imagem.get_height()  # altura original
    for fator in [1.0, 0.8, 0.5, 0.25, 0.5, 0.8]:  # quanto da largura cada quadro mantém
        nova_largura = max(1, round(largura * fator))  # calcula a largura (nunca menor que 1 pixel)
        quadros.append(pygame.transform.smoothscale(imagem, (nova_largura, altura)))  # guarda o quadro
    return quadros  # devolve a animação


def carregar_personagem(chave):
    """Carrega as imagens de um personagem (ícone, correndo, abaixado e pulando) em um dicionário."""
    em_pe = carregar_imagem(chave, ALTURA_JOGADOR)  # imagem em pé no tamanho do jogo
    largura_abaixado = round(em_pe.get_width() * 1.15)  # abaixado fica um pouco mais largo
    altura_abaixado = round(em_pe.get_height() * FATOR_ABAIXADO)  # e bem mais baixo
    abaixado = pygame.transform.smoothscale(em_pe, (largura_abaixado, altura_abaixado))  # "achata" a imagem
    return {
        'icone': carregar_imagem(chave, 70),  # versão pequena para o cartão da tela inicial
        'correndo': criar_quadros_corrida(em_pe),  # animação de corrida
        'abaixado': criar_quadros_corrida(abaixado, 1),  # abaixado inclina só 1 grau (para não encostar na bengala)
        'pulando': pygame.transform.rotate(em_pe, 8),  # um quadro inclinado para o pulo
    }


def carregar_fonte(arquivo, tamanho):
    """Carrega uma fonte da pasta de fontes (ou a fonte padrão, se o arquivo não existir)."""
    caminho = os.path.join(PASTA_FONTES, arquivo)  # caminho completo da fonte
    if os.path.exists(caminho):  # se o arquivo existe...
        return pygame.font.Font(caminho, tamanho)  # ...carrega a fonte natalina
    return pygame.font.SysFont(None, tamanho)  # senão, usa a fonte padrão (como no handout)


def carregar_assets():
    """Carrega todas as imagens, sons e fontes no dicionário assets (chamar depois de criar a janela)."""
    assets = {}  # dicionário vazio (mesma ideia do jogo_v14.py do handout)

    # ----- Fundos -----
    assets['fundo_inicio'] = carregar_imagem('fundo_inicio', 540)  # fundo das telas inicial e final
    assets['ceu'] = carregar_imagem('ceu', 540)  # céu com lua (fica parado)
    assets['montanhas'] = carregar_imagem('montanhas', 540)  # montanhas (andam devagar)
    assets['chao'] = carregar_imagem('chao', 118)  # chão de neve (anda junto com os obstáculos)

    # ----- Personagens jogáveis -----
    assets['personagens'] = {}  # dicionário dentro do dicionário: um item por personagem
    for personagem in PERSONAGENS:  # percorre a lista de personagens
        chave = personagem['chave']  # pega a chave ('rena', 'gnomo'...)
        assets['personagens'][chave] = carregar_personagem(chave)  # guarda as imagens dele

    # ----- Papai Noel e renas decorativas -----
    santa = carregar_imagem('papai_noel', 150)  # Papai Noel no tamanho do jogo
    assets['papai_noel'] = criar_quadros_corrida(santa)  # animação dele balançando (acenando)
    assets['papai_noel_grande'] = carregar_imagem('papai_noel', 200)  # versão grande para as telas
    rena = carregar_imagem('rena', 105)  # rena decorativa
    assets['rena_decoracao'] = pygame.transform.flip(rena, True, False)  # espelhada (olhando para a esquerda)
    assets['rena_decoracao_menor'] = pygame.transform.flip(carregar_imagem('rena', 96), True, False)  # segunda rena

    # ----- Obstáculos e presentes -----
    assets['arbusto'] = carregar_imagem('arbusto', 48)  # obstáculo baixo e pequeno
    assets['arvore'] = carregar_imagem('arvore', 105)  # obstáculo baixo médio
    assets['arvore_luzes'] = carregar_imagem('arvore_luzes', 125)  # obstáculo baixo grande
    assets['bengala'] = carregar_imagem('bengala', 40)  # obstáculo ALTO (precisa abaixar)
    presente = carregar_imagem('presente', 40)  # presente no tamanho do jogo
    assets['presente'] = presente  # imagem parada (usada no placar)
    assets['presente_anim'] = criar_quadros_presente(presente)  # animação girando
    assets['presente_icone'] = carregar_imagem('presente', 32)  # versão menor para os textos

    # ----- Ícones dos botões -----
    for nome in ['musica', 'musica_off', 'menu', 'fechar', 'cima', 'baixo']:
        assets['icone_' + nome] = carregar_imagem('icone_' + nome, 30)  # ex.: assets['icone_menu']
    assets['icone_repetir_grande'] = carregar_imagem('icone_repetir', 46)  # seta grande das telas finais
    assets['estrela'] = carregar_imagem('estrela', 34)  # estrela da tela de vitória

    # ----- Sons (efeitos curtos) -----
    assets['som_pulo'] = pygame.mixer.Sound(os.path.join(PASTA_SND, 'pulo.wav'))  # som do pulo
    assets['som_presente'] = pygame.mixer.Sound(os.path.join(PASTA_SND, 'presente.wav'))  # pegou presente
    assets['som_batida'] = pygame.mixer.Sound(os.path.join(PASTA_SND, 'batida.wav'))  # bateu no obstáculo
    assets['som_vitoria'] = pygame.mixer.Sound(os.path.join(PASTA_SND, 'vitoria.wav'))  # chegou no Noel
    assets['som_clique'] = pygame.mixer.Sound(os.path.join(PASTA_SND, 'clique.wav'))  # clique em botão
    assets['musica'] = os.path.join(PASTA_SND, 'jingle_bells.wav')  # música: só o caminho (tocada por mixer.music)

    # ----- Fontes -----
    natal = 'MountainsOfChristmas-Bold.ttf'  # fonte dos títulos
    texto = 'Fredoka-SemiBold.ttf'  # fonte dos textos e botões
    assets['fonte_titulo_gigante'] = carregar_fonte(natal, 104)  # YOU DIED! / YOU WIN!
    assets['fonte_titulo'] = carregar_fonte(natal, 54)  # título da tela inicial
    assets['fonte_hohoho'] = carregar_fonte(natal, 46)  # HOHOHO e Congrats!
    assets['fonte_pausado'] = carregar_fonte(natal, 76)  # texto "Pausado"
    assets['fonte_botao'] = carregar_fonte(texto, 34)  # texto do botão START
    assets['fonte_placar'] = carregar_fonte(texto, 28)  # contador de presentes
    assets['fonte_texto'] = carregar_fonte(texto, 20)  # textos normais
    assets['fonte_menu'] = carregar_fonte(texto, 19)  # botões do menu de pausa
    assets['fonte_pequena'] = carregar_fonte(texto, 15)  # legendas pequenas

    return assets  # devolve o dicionário completo
