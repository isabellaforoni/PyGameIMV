"""
tela_inicial.py — Tela de início: título, botão START, música e escolha do personagem.
"""
import pygame  # biblioteca de jogos
from config import (FPS, LARGURA, JOGANDO, SAIR, BRANCO, AZUL_ESCURO, AZUL_BOTAO, VERMELHO,
                    DOURADO, DOURADO_ESCURO, CINZA_CLARO)  # constantes
from recursos import PERSONAGENS  # lista de personagens
from interface import Botao, desenhar_texto, desenhar_caixa, alternar_musica  # ferramentas de tela
from sprites import criar_neve  # flocos de neve

# Tamanho de cada cartão de personagem e espaço entre eles
LARGURA_CARTAO = 104  # largura do cartão
ALTURA_CARTAO = 118  # altura do cartão
ESPACO_CARTOES = 16  # espaço entre os cartões
Y_CARTOES = 302  # posição y dos cartões


def criar_cartoes():
    """
    Cria um retângulo para cada personagem, centralizados na tela.

    Retorna:
        list: lista de dicionários {'chave', 'nome', 'rect'}, um por personagem.
    """
    quantidade = len(PERSONAGENS)  # quantos personagens existem (3)
    largura_total = quantidade * LARGURA_CARTAO + (quantidade - 1) * ESPACO_CARTOES  # largura do conjunto
    x = (LARGURA - largura_total) // 2  # x do primeiro cartão (para o conjunto ficar no meio)
    cartoes = []  # lista de cartões
    for personagem in PERSONAGENS:  # percorre os personagens
        rect = pygame.Rect(x, Y_CARTOES, LARGURA_CARTAO, ALTURA_CARTAO)  # retângulo do cartão
        cartoes.append({'chave': personagem['chave'], 'nome': personagem['nome'], 'rect': rect})  # guarda
        x += LARGURA_CARTAO + ESPACO_CARTOES  # anda para o próximo cartão
    return cartoes  # devolve a lista


def desenhar_cenario(janela, assets):
    """
    Desenha o fundo de inverno com o Papai Noel e as duas renas (usado também nas telas finais).

    Parâmetros:
        janela (pygame.Surface): onde desenhar.
        assets (dict): recursos do jogo.
    """
    janela.blit(assets['fundo_inicio'], (0, 0))  # fundo: céu, lua, montanhas e árvores com neve
    santa = assets['papai_noel_grande']  # imagem do Papai Noel
    janela.blit(santa, santa.get_rect(midbottom=(150, 500)))  # Papai Noel à esquerda
    rena = assets['rena_decoracao']  # primeira rena
    janela.blit(rena, rena.get_rect(midbottom=(762, 500)))  # rena à direita
    rena2 = assets['rena_decoracao_menor']  # segunda rena (um pouco menor, mais longe)
    janela.blit(rena2, rena2.get_rect(midbottom=(868, 502)))  # rena mais à direita


def tela_inicial(janela, assets, dados):
    """
    Mostra a tela inicial até o jogador apertar START ou fechar a janela.

    Parâmetros:
        janela (pygame.Surface): janela do jogo.
        assets (dict): recursos do jogo.
        dados (dict): dados compartilhados (personagem escolhido, música ligada...).

    Retorna:
        int: próximo estado (JOGANDO ou SAIR).
    """
    relogio = pygame.time.Clock()  # relógio para controlar o FPS
    neve = criar_neve(70)  # flocos de neve desta tela
    botao_start = Botao((370, 166, 220, 72), VERMELHO, texto='START', fonte=assets['fonte_botao'])  # botão START
    botao_musica = Botao((LARGURA - 80, 20, 56, 56), AZUL_BOTAO)  # botão de música (o ícone é escolhido no loop)
    cartoes = criar_cartoes()  # cartões dos personagens

    while True:  # loop principal da tela (sai com return)
        relogio.tick(FPS)  # limita a velocidade do loop

        # ----- Trata eventos -----
        for evento in pygame.event.get():  # percorre os eventos que aconteceram
            if evento.type == pygame.QUIT:  # clicou no X da janela
                return SAIR  # encerra o jogo
            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):  # Enter/espaço
                assets['som_clique'].play()  # som de clique
                return JOGANDO  # começa o jogo
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # clique com o botão esquerdo
                if botao_start.contem(evento.pos):  # clicou no START?
                    assets['som_clique'].play()  # som de clique
                    return JOGANDO  # começa o jogo
                if botao_musica.contem(evento.pos):  # clicou no botão de música?
                    alternar_musica(dados)  # liga/desliga
                for cartao in cartoes:  # verifica cada cartão
                    if cartao['rect'].collidepoint(evento.pos):  # clicou neste cartão?
                        dados['personagem'] = cartao['chave']  # escolhe o personagem
                        assets['som_clique'].play()  # som de clique

        # ----- Gera saídas (desenha a tela) -----
        desenhar_cenario(janela, assets)  # fundo + Papai Noel + renas
        neve.update()  # move os flocos de neve
        neve.draw(janela)  # desenha os flocos

        desenhar_texto(janela, 'Você é capaz de chegar no Papai Noel?', assets['fonte_titulo'], BRANCO,
                       (LARGURA // 2, 72), cor_sombra=(179, 18, 43))  # título com sombra vermelha
        desenhar_texto(janela, 'HOHOHO', assets['fonte_hohoho'], DOURADO,
                       (LARGURA // 2, 128), cor_sombra=DOURADO_ESCURO)  # HOHOHO dourado

        botao_start.desenhar(janela)  # botão START
        if dados['musica']:  # escolhe o ícone conforme a música
            botao_musica.icone = assets['icone_musica']  # nota musical
        else:
            botao_musica.icone = assets['icone_musica_off']  # nota cortada
        botao_musica.desenhar(janela)  # desenha o botão de música

        desenhar_texto(janela, 'Escolha seu personagem', assets['fonte_texto'], CINZA_CLARO,
                       (LARGURA // 2, 284))  # legenda dos cartões
        for cartao in cartoes:  # desenha cada cartão
            escolhido = cartao['chave'] == dados['personagem']  # este é o personagem escolhido?
            if escolhido:  # cartão escolhido: fundo azul e borda dourada
                desenhar_caixa(janela, AZUL_BOTAO, cartao['rect'], DOURADO)
            else:  # cartão normal: fundo azul escuro e borda branca
                desenhar_caixa(janela, AZUL_ESCURO, cartao['rect'], BRANCO)
            icone = assets['personagens'][cartao['chave']]['icone']  # imagem pequena do personagem
            janela.blit(icone, icone.get_rect(center=(cartao['rect'].centerx, cartao['rect'].y + 48)))  # desenha
            desenhar_texto(janela, cartao['nome'], assets['fonte_pequena'], BRANCO,
                           (cartao['rect'].centerx, cartao['rect'].bottom - 16))  # nome embaixo

        pygame.display.update()  # mostra o novo frame
