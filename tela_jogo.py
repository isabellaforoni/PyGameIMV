"""
tela_jogo.py — A corrida até o Papai Noel.

O jogador fica parado no lado esquerdo e o cenário (chão, obstáculos e
presentes) anda na direção dele. Dentro desta tela existe uma pequena
máquina de estados (variável `situacao`):

    'correndo' — jogo normal
    'pausado'  — menu de pausa aberto, nada se move
    'batendo'  — bateu em um obstáculo: pisca e depois vai para YOU DIED
    'chegou'   — encostou no Papai Noel: espera um pouco e vai para YOU WIN
"""
import random  # para sortear obstáculos e presentes
import pygame  # biblioteca de jogos
from config import (FPS, LARGURA, ALTURA, CHAO_Y, INICIO, MORREU, VENCEU, SAIR, BRANCO, AZUL_ESCURO,
                    AZUL_BOTAO, VERMELHO, VERMELHO_ESCURO, VERDE, DOURADO,
                    VELOCIDADE_INICIAL, VELOCIDADE_MAXIMA, ACELERACAO, DISTANCIA_TOTAL,
                    FRAMES_MIN_ENTRE_OBSTACULOS, FRAMES_MAX_ENTRE_OBSTACULOS, CHANCE_PRESENTE)  # constantes
from sprites import Jogador, Obstaculo, Presente, PapaiNoel, criar_neve, SORTEIO_OBSTACULOS  # objetos do jogo
from interface import Botao, desenhar_texto, desenhar_caixa  # ferramentas de tela

TEMPO_FINAL = 1300  # milissegundos de espera depois de bater ou de chegar no Papai Noel


def gerar_obstaculo(assets, obstaculos, presentes, velocidade):
    """
    Cria um obstáculo na borda direita e, às vezes, um presente no meio do espaço livre.

    Só existe UM obstáculo por vez em cada espaço, então nunca aparece um
    obstáculo baixo junto com um alto. O presente fica no meio do caminho
    entre este obstáculo e o próximo, longe dos dois.

    Parâmetros:
        assets (dict): recursos do jogo.
        obstaculos (pygame.sprite.Group): grupo onde o obstáculo será colocado.
        presentes (pygame.sprite.Group): grupo onde o presente será colocado.
        velocidade (float): velocidade atual do cenário.

    Retorna:
        float: distância (em pixels) até o próximo obstáculo.
    """
    nome = random.choice(SORTEIO_OBSTACULOS)  # sorteia o tipo de obstáculo
    obstaculo = Obstaculo(assets, nome, LARGURA + 20)  # cria logo depois da borda direita
    obstaculos.add(obstaculo)  # coloca no grupo
    frames = random.randint(FRAMES_MIN_ENTRE_OBSTACULOS, FRAMES_MAX_ENTRE_OBSTACULOS)  # sorteia o espaço
    espaco = velocidade * frames  # espaço em pixels (cresce junto com a velocidade)
    if random.random() < CHANCE_PRESENTE:  # sorteio: vai ter presente neste espaço?
        x_presente = obstaculo.rect.left + (espaco + obstaculo.rect.width) / 2  # meio do espaço livre
        no_ar = random.choice([True, False])  # sorteia se fica no ar ou no chão
        presentes.add(Presente(assets, x_presente, no_ar))  # cria e coloca no grupo
    return espaco  # devolve a distância até o próximo


def desenhar_fundo(janela, assets, deslocamento_montanhas, deslocamento_chao):
    """
    Desenha o céu parado, as montanhas andando devagar e o chão andando rápido.

    Cada camada é desenhada duas vezes, uma do lado da outra. Quando uma sai
    pela esquerda, a outra já está ocupando a tela: assim o cenário parece infinito.

    Parâmetros:
        janela (pygame.Surface): onde desenhar.
        assets (dict): recursos do jogo.
        deslocamento_montanhas (float): quanto as montanhas já andaram.
        deslocamento_chao (float): quanto o chão já andou.
    """
    janela.blit(assets['ceu'], (0, 0))  # céu com estrelas e lua (não se move)
    x = -(deslocamento_montanhas % LARGURA)  # o resto da divisão faz o valor "dar a volta"
    janela.blit(assets['montanhas'], (x, 0))  # primeira cópia das montanhas
    janela.blit(assets['montanhas'], (x + LARGURA, 0))  # segunda cópia logo à direita
    x = -(deslocamento_chao % LARGURA)  # mesma ideia para o chão
    janela.blit(assets['chao'], (x, CHAO_Y - 16))  # primeira cópia do chão
    janela.blit(assets['chao'], (x + LARGURA, CHAO_Y - 16))  # segunda cópia


def desenhar_hud(janela, assets, distancia, presentes, botao_menu, menu_aberto):
    """
    Desenha as informações por cima do jogo: progresso, presentes e botão de menu.

    Parâmetros:
        janela (pygame.Surface): onde desenhar.
        assets (dict): recursos do jogo.
        distancia (float): quanto o jogador já correu.
        presentes (int): quantos presentes já pegou.
        botao_menu (Botao): botão do menu (canto superior direito).
        menu_aberto (bool): True mostra o botão com um X.
    """
    # ----- Barra de progresso até o Papai Noel -----
    janela.blit(assets['fonte_pequena'].render('Até o Papai Noel', True, BRANCO), (20, 16))  # legenda
    contorno = pygame.Rect(20, 42, 190, 18)  # retângulo da barra
    desenhar_caixa(janela, AZUL_ESCURO, contorno)  # fundo da barra
    progresso = min(distancia / DISTANCIA_TOTAL, 1)  # fração percorrida (de 0 a 1)
    cheio = pygame.Rect(20, 42, max(18, round(190 * progresso)), 18)  # parte preenchida (no mínimo 18 px)
    desenhar_caixa(janela, DOURADO, cheio)  # preenchimento dourado
    pygame.draw.rect(janela, BRANCO, contorno, 2, border_radius=9)  # contorno branco
    noel = assets['papai_noel'][0]  # imagem do Papai Noel
    noel_pequeno = pygame.transform.smoothscale(noel, (noel.get_width() * 34 // noel.get_height(), 34))  # miniatura
    janela.blit(noel_pequeno, noel_pequeno.get_rect(midleft=(218, 50)))  # ao lado da barra

    # ----- Contador de presentes (centro) -----
    caixa = pygame.Rect(LARGURA // 2 - 85, 16, 170, 52)  # retângulo do contador
    desenhar_caixa(janela, AZUL_ESCURO, caixa, BRANCO)  # fundo com borda
    janela.blit(assets['presente'], assets['presente'].get_rect(midleft=(caixa.x + 30, caixa.centery)))  # ícone
    desenhar_texto(janela, f'× {presentes}', assets['fonte_placar'], BRANCO, (caixa.centerx + 22, caixa.centery))

    # ----- Botão de menu -----
    if menu_aberto:  # com o menu aberto o botão vira um X vermelho
        botao_menu.icone = assets['icone_fechar']
        botao_menu.cor = VERMELHO
    else:  # menu fechado: três risquinhos azuis
        botao_menu.icone = assets['icone_menu']
        botao_menu.cor = AZUL_BOTAO
    botao_menu.desenhar(janela)  # desenha o botão


def desenhar_pausa(janela, assets, botao_voltar, botao_sair):
    """
    Escurece a tela e mostra o menu de pausa com "Voltar para o jogo" e "Sair".

    Parâmetros:
        janela (pygame.Surface): onde desenhar.
        assets (dict): recursos do jogo.
        botao_voltar (Botao): botão verde de voltar.
        botao_sair (Botao): botão de sair.
    """
    escuro = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)  # superfície transparente do tamanho da tela
    escuro.fill((6, 12, 30, 160))  # azul bem escuro, meio transparente
    janela.blit(escuro, (0, 0))  # escurece tudo que já foi desenhado
    desenhar_texto(janela, 'Pausado', assets['fonte_pausado'], BRANCO, (LARGURA // 2, 250),
                   cor_sombra=AZUL_BOTAO)  # texto grande no meio
    painel = pygame.Rect(LARGURA - 270, 84, 250, 142)  # retângulo do painel (embaixo do botão de menu)
    desenhar_caixa(janela, BRANCO, painel)  # painel branco
    botao_voltar.desenhar(janela)  # botão "Voltar para o jogo"
    botao_sair.desenhar(janela)  # botão "Sair"


def tela_jogo(janela, assets, dados):
    """
    Roda uma partida até o jogador morrer, vencer, sair pelo menu ou fechar a janela.

    Parâmetros:
        janela (pygame.Surface): janela do jogo.
        assets (dict): recursos do jogo.
        dados (dict): dados compartilhados; aqui usamos 'personagem' e salvamos 'presentes'.

    Retorna:
        int: próximo estado (MORREU, VENCEU, INICIO ou SAIR).
    """
    relogio = pygame.time.Clock()  # relógio do FPS

    # ----- Objetos do jogo -----
    jogador = Jogador(assets, dados['personagem'])  # personagem escolhido na tela inicial
    obstaculos = pygame.sprite.Group()  # grupo dos obstáculos
    presentes = pygame.sprite.Group()  # grupo dos presentes
    final = pygame.sprite.Group()  # grupo do Papai Noel (vazio até o fim da corrida)
    neve = criar_neve(45)  # flocos de neve

    # ----- Botões -----
    botao_menu = Botao((LARGURA - 76, 16, 56, 56), AZUL_BOTAO)  # menu (o ícone é escolhido em desenhar_hud)
    botao_cima = Botao((LARGURA - 172, ALTURA - 86, 68, 68), AZUL_BOTAO, icone=assets['icone_cima'])  # pular
    botao_baixo = Botao((LARGURA - 90, ALTURA - 86, 68, 68), AZUL_BOTAO, icone=assets['icone_baixo'])  # abaixar
    botao_voltar = Botao((LARGURA - 256, 98, 222, 52), VERDE, texto='Voltar para o jogo', fonte=assets['fonte_menu'])
    botao_sair = Botao((LARGURA - 256, 160, 222, 52), VERMELHO, texto='Sair', fonte=assets['fonte_menu'])

    # ----- Variáveis da partida -----
    velocidade = VELOCIDADE_INICIAL  # velocidade atual do cenário
    distancia = 0  # quanto já correu (em pixels)
    ate_proximo_obstaculo = 600  # pixels até o primeiro obstáculo (um tempinho para se preparar)
    deslocamento_montanhas = 0  # quanto as montanhas já andaram
    deslocamento_chao = 0  # quanto o chão já andou
    dados['presentes'] = 0  # zera o contador de presentes
    situacao = 'correndo'  # estado atual dentro da partida
    instante_fim = 0  # quando bateu ou chegou (para esperar TEMPO_FINAL)
    abaixar_teclado = False  # seta para baixo do teclado apertada?
    abaixar_mouse = False  # botão de abaixar da tela apertado?

    while True:  # loop principal (sai com return)
        relogio.tick(FPS)  # limita o FPS

        # ===== Trata eventos =====
        for evento in pygame.event.get():  # percorre os eventos
            if evento.type == pygame.QUIT:  # fechou a janela
                return SAIR  # encerra

            if situacao == 'pausado':  # ----- eventos com o jogo pausado -----
                if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_ESCAPE, pygame.K_p):
                    situacao = 'correndo'  # ESC ou P voltam ao jogo
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # clique
                    if botao_voltar.contem(evento.pos) or botao_menu.contem(evento.pos):  # voltar ou X
                        assets['som_clique'].play()  # som de clique
                        situacao = 'correndo'  # volta a correr
                    elif botao_sair.contem(evento.pos):  # sair
                        assets['som_clique'].play()  # som de clique
                        return INICIO  # volta para a tela inicial

            elif situacao == 'correndo':  # ----- eventos com o jogo rodando -----
                if evento.type == pygame.KEYDOWN:  # apertou uma tecla
                    if evento.key in (pygame.K_UP, pygame.K_SPACE, pygame.K_w):  # seta para cima, espaço ou W
                        jogador.pular()  # pula
                    if evento.key in (pygame.K_DOWN, pygame.K_s):  # seta para baixo ou S
                        abaixar_teclado = True  # começou a abaixar
                    if evento.key in (pygame.K_ESCAPE, pygame.K_p):  # ESC ou P
                        situacao = 'pausado'  # pausa
                if evento.type == pygame.KEYUP and evento.key in (pygame.K_DOWN, pygame.K_s):  # soltou
                    abaixar_teclado = False  # parou de abaixar
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # clique
                    if botao_menu.contem(evento.pos):  # menu
                        assets['som_clique'].play()
                        situacao = 'pausado'  # pausa
                    elif botao_cima.contem(evento.pos):  # seta para cima
                        jogador.pular()  # pula
                    elif botao_baixo.contem(evento.pos):  # seta para baixo
                        abaixar_mouse = True  # fica abaixado enquanto segurar o clique
                if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:  # soltou o clique
                    abaixar_mouse = False  # levanta

        # ===== Atualiza o estado do jogo =====
        if situacao == 'correndo':
            jogador.abaixar(abaixar_teclado or abaixar_mouse)  # abaixado se teclado OU mouse estiver apertado
            velocidade = min(velocidade + ACELERACAO, VELOCIDADE_MAXIMA)  # acelera aos poucos
            distancia += velocidade  # soma a distância percorrida
            deslocamento_montanhas += velocidade * 0.15  # montanhas andam devagar (parecem longe)
            deslocamento_chao += velocidade  # chão anda junto com os obstáculos

            ate_proximo_obstaculo -= velocidade  # diminui a distância até o próximo obstáculo
            if ate_proximo_obstaculo <= 0:  # chegou a hora de criar algo novo?
                if distancia < DISTANCIA_TOTAL:  # ainda não chegou no fim da corrida
                    ate_proximo_obstaculo = gerar_obstaculo(assets, obstaculos, presentes, velocidade)
                elif len(final) == 0:  # chegou no fim e o Papai Noel ainda não apareceu
                    final.add(PapaiNoel(assets))  # o Papai Noel aparece!

            jogador.update()  # gravidade e animação do jogador
            obstaculos.update(velocidade)  # move os obstáculos (o Group passa a velocidade para cada um)
            presentes.update(velocidade)  # move os presentes
            final.update(velocidade)  # move o Papai Noel

            # ----- Verifica consequências (colisões) -----
            pegos = pygame.sprite.spritecollide(jogador, presentes, True, pygame.sprite.collide_rect)  # presentes
            for _ in pegos:  # para cada presente pego...
                dados['presentes'] += 1  # ...soma um ponto
                assets['som_presente'].play()  # ...e toca o som
            batidas = pygame.sprite.spritecollide(jogador, obstaculos, False, pygame.sprite.collide_mask)
            if len(batidas) > 0:  # encostou em algum obstáculo?
                assets['som_batida'].play()  # som da batida
                situacao = 'batendo'  # muda o estado
                instante_fim = pygame.time.get_ticks()  # guarda quando aconteceu
            elif pygame.sprite.spritecollide(jogador, final, False, pygame.sprite.collide_mask):  # Papai Noel!
                assets['som_vitoria'].play()  # som de vitória
                situacao = 'chegou'  # muda o estado
                instante_fim = pygame.time.get_ticks()  # guarda quando aconteceu

        elif situacao in ('batendo', 'chegou'):  # esperando para ir à tela final
            if pygame.time.get_ticks() - instante_fim > TEMPO_FINAL:  # já esperou o suficiente?
                if situacao == 'batendo':
                    return MORREU  # vai para YOU DIED!
                return VENCEU  # vai para YOU WIN!

        # ===== Gera saídas (desenha) =====
        desenhar_fundo(janela, assets, deslocamento_montanhas, deslocamento_chao)  # cenário
        obstaculos.draw(janela)  # obstáculos
        presentes.draw(janela)  # presentes
        final.draw(janela)  # Papai Noel (se já apareceu)
        piscando = situacao == 'batendo' and (pygame.time.get_ticks() // 120) % 2 == 0  # pisca a cada 120 ms
        if not piscando:  # quando não está no "apagado" da piscada...
            janela.blit(jogador.image, jogador.rect)  # ...desenha o jogador
        if situacao != 'pausado':  # a neve só se move quando o jogo não está pausado
            neve.update()
        neve.draw(janela)  # desenha os flocos

        desenhar_hud(janela, assets, distancia, dados['presentes'], botao_menu, situacao == 'pausado')  # placar
        botao_cima.desenhar(janela)  # seta para cima
        if jogador.abaixado:  # abaixado: botão de baixo fica vermelho
            botao_baixo.cor = VERMELHO
        else:  # normal: azul
            botao_baixo.cor = AZUL_BOTAO
        botao_baixo.desenhar(janela)  # seta para baixo
        if situacao == 'pausado':  # menu de pausa por cima de tudo
            desenhar_pausa(janela, assets, botao_voltar, botao_sair)
            botao_menu.desenhar(janela)  # redesenha o X por cima do escuro para continuar visível
        if situacao == 'chegou':  # mensagem rápida antes da tela de vitória
            desenhar_texto(janela, 'HOHOHO!', assets['fonte_pausado'], DOURADO, (LARGURA // 2, 200),
                           cor_sombra=VERMELHO_ESCURO)

        pygame.display.update()  # mostra o frame