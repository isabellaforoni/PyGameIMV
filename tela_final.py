"""
tela_final.py — Telas de fim de jogo: YOU DIED! (bateu) ou YOU WIN! (chegou no Papai Noel).
"""
import pygame  # biblioteca de jogos
from config import (FPS, LARGURA, JOGANDO, INICIO, SAIR, VENCEU, BRANCO, AZUL_ESCURO, AZUL_BOTAO,
                    VERMELHO, VERDE, DOURADO, DOURADO_ESCURO)  # constantes
from interface import Botao, desenhar_texto, desenhar_caixa, desenhar_etiqueta, alternar_musica  # ferramentas de tela
from sprites import criar_neve  # flocos de neve
from tela_inicial import desenhar_cenario  # mesmo cenário da tela inicial
from recorde import atualizar_recorde  # salva o recorde no arquivo

# Posições (x, y) das estrelas da tela de vitória
POSICOES_ESTRELAS = [(245, 88), (300, 150), (715, 96), (660, 160), (190, 190), (780, 200)]


def desenhar_vitoria_extra(janela, assets, dados, instante):
    """
    Enfeites só da vitória: o personagem escolhido ao lado do Papai Noel, presentes e estrelas piscando.

    Parâmetros:
        janela (pygame.Surface): onde desenhar.
        assets (dict): recursos do jogo.
        dados (dict): dados do jogo (personagem escolhido).
        instante (int): tempo atual em ms (para as estrelas piscarem).
    """
    personagem = assets['personagens'][dados['personagem']]['correndo'][0]  # imagem do personagem escolhido
    janela.blit(personagem, personagem.get_rect(midbottom=(285, 500)))  # ao lado do Papai Noel
    janela.blit(assets['presente'], assets['presente'].get_rect(midbottom=(52, 502)))  # presente no chão
    janela.blit(assets['presente'], assets['presente'].get_rect(midbottom=(352, 504)))  # outro presente
    for indice, posicao in enumerate(POSICOES_ESTRELAS):  # percorre as estrelas com o índice
        if (instante // 400 + indice) % 3 != 0:  # cada estrela fica apagada 1/3 do tempo, em momentos diferentes
            janela.blit(assets['estrela'], assets['estrela'].get_rect(center=posicao))  # desenha a estrela


def tela_final(janela, assets, dados, resultado):
    """
    Mostra a tela final até o jogador clicar para jogar de novo.

    Parâmetros:
        janela (pygame.Surface): janela do jogo.
        assets (dict): recursos do jogo.
        dados (dict): dados compartilhados (presentes da partida, recorde, música...).
        resultado (int): MORREU ou VENCEU.

    Retorna:
        int: próximo estado (JOGANDO para jogar de novo, INICIO com ESC, ou SAIR).
    """
    relogio = pygame.time.Clock()  # relógio do FPS
    neve = criar_neve(70)  # flocos de neve
    venceu = resultado == VENCEU  # True se chegou no Papai Noel
    novo_recorde = atualizar_recorde(dados, venceu)  # salva no arquivo e descobre se bateu o recorde

    if venceu:  # na vitória: botão verde, um pouco mais baixo (tem o "Congrats!" em cima)
        cor = VERDE
        y_botao = 300
    else:  # na derrota: botão vermelho
        cor = VERMELHO
        y_botao = 280
    botao_repetir = Botao((LARGURA // 2 - 46, y_botao, 92, 92), cor, icone=assets['icone_repetir_grande'])  # jogar de novo
    botao_musica = Botao((LARGURA - 80, 20, 56, 56), AZUL_BOTAO)  # botão de música

    while True:  # loop da tela
        relogio.tick(FPS)  # limita o FPS

        # ----- Trata eventos -----
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # fechou a janela
                return SAIR
            if evento.type == pygame.KEYDOWN:  # teclado
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):  # Enter ou espaço: jogar de novo
                    assets['som_clique'].play()
                    return JOGANDO
                if evento.key == pygame.K_ESCAPE:  # ESC: volta para a tela inicial (trocar personagem)
                    return INICIO
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # clique
                if botao_repetir.contem(evento.pos):  # seta de jogar de novo
                    assets['som_clique'].play()
                    return JOGANDO
                if botao_musica.contem(evento.pos):  # botão de música
                    alternar_musica(dados)

        # ----- Gera saídas -----
        desenhar_cenario(janela, assets)  # mesmo fundo da tela inicial
        if venceu:  # enfeites da vitória
            desenhar_vitoria_extra(janela, assets, dados, pygame.time.get_ticks())
        neve.update()  # move os flocos de neve
        neve.draw(janela)  # desenha os flocos

        if venceu:  # textos da vitória
            desenhar_texto(janela, 'YOU WON!', assets['fonte_titulo_gigante'], DOURADO, (LARGURA // 2, 112),
                           cor_sombra=DOURADO_ESCURO)
            desenhar_texto(janela, 'Congrats!', assets['fonte_hohoho'], BRANCO, (LARGURA // 2, 186),
                           cor_sombra=VERMELHO)
            y_caixa = 236  # posição do contador de presentes
        else:  # textos da derrota
            desenhar_texto(janela, 'YOU LOST!', assets['fonte_titulo_gigante'], BRANCO, (LARGURA // 2, 126),
                           cor_sombra=VERMELHO)
            y_caixa = 218

        caixa = pygame.Rect(LARGURA // 2 - 150, y_caixa, 300, 46)  # caixinha dos presentes coletados
        desenhar_caixa(janela, AZUL_ESCURO, caixa, BRANCO)  # fundo azul escuro com borda branca
        janela.blit(assets['presente_icone'], assets['presente_icone'].get_rect(midleft=(caixa.x + 18, caixa.centery)))
        desenhar_texto(janela, f'Presentes coletados: {dados["presentes"]}', assets['fonte_texto'], BRANCO,
                       (caixa.centerx + 18, caixa.centery))

        botao_repetir.desenhar(janela)  # seta de jogar de novo
        desenhar_etiqueta(janela, 'Jogar de novo', assets['fonte_texto'], (LARGURA // 2, botao_repetir.rect.bottom + 28))  # legenda do botão

        if novo_recorde:  # mensagem especial se bateu o recorde
            texto_recorde = 'Novo recorde de presentes!'
        else:  # senão mostra o recorde salvo
            texto_recorde = f'Recorde: {dados["recorde"]["presentes"]} presentes'
        desenhar_etiqueta(janela, texto_recorde, assets['fonte_pequena'], (LARGURA // 2, botao_repetir.rect.bottom + 66))
        desenhar_etiqueta(janela, 'ESC: trocar de personagem', assets['fonte_pequena'], (LARGURA // 2, 516))  # dica

        if dados['musica']:  # ícone da música
            botao_musica.icone = assets['icone_musica']
        else:
            botao_musica.icone = assets['icone_musica_off']
        botao_musica.desenhar(janela)

        pygame.display.update()  # mostra o frame