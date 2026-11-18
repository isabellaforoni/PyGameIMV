"""
sprites.py — Classes dos objetos que aparecem no jogo.

Cada classe estende pygame.sprite.Sprite (como Meteor e Ship no handout) e
precisa ter os atributos `image` (o desenho) e `rect` (a posição). O método
`update` é chamado uma vez por frame para mover e animar o objeto.

Classes:
    Jogador   — personagem controlado pelo jogador (pula e abaixa).
    Obstaculo — árvores, arbusto e bengala de doce que vêm na direção do jogador.
    Presente  — presentes que somam pontos quando coletados.
    PapaiNoel — aparece no fim da corrida; encostar nele = vitória.
    Floco     — floco de neve que cai o tempo todo.
"""
import math  # para a função seno (balanço do floco de neve)
import random  # para sortear tamanhos, posições e obstáculos
import pygame  # biblioteca de jogos
from config import (LARGURA, ALTURA, CHAO_Y, JOGADOR_X, GRAVIDADE, FORCA_PULO,
                    QUEDA_RAPIDA, BRANCO)  # constantes usadas aqui

# Dicionário com as informações de cada tipo de obstáculo.
# 'tipo' diz se é BAIXO (precisa pular) ou ALTO (precisa abaixar).
# 'altura_do_chao' é quantos pixels acima do chão fica a parte de baixo do obstáculo.
TIPOS_OBSTACULO = {
    'arbusto': {'tipo': 'baixo', 'altura_do_chao': 0},  # arbusto pequeno no chão
    'arvore': {'tipo': 'baixo', 'altura_do_chao': 0},  # árvore normal no chão
    'arvore_luzes': {'tipo': 'baixo', 'altura_do_chao': 0},  # árvore com luzes no chão
    'bengala': {'tipo': 'alto', 'altura_do_chao': 64},  # bengala de doce flutuando no alto
}

# Lista com os nomes dos obstáculos; random.choice sorteia um deles.
# 'bengala' aparece duas vezes para ser sorteada com mais frequência.
SORTEIO_OBSTACULOS = ['arbusto', 'arvore', 'arvore_luzes', 'bengala', 'bengala']

# Quantos pixels o personagem "sobe" em cada quadro da corrida (efeito de quicar).
QUIQUE = [0, 3, 5, 3]


class Jogador(pygame.sprite.Sprite):
    """
    Personagem controlado pelo jogador.

    Ele fica sempre na mesma posição x; só se move para cima (pulo) e para
    baixo (gravidade). Também pode se abaixar para passar embaixo da bengala.
    """

    def __init__(self, assets, chave_personagem):
        """
        Cria o jogador.

        Parâmetros:
            assets (dict): dicionário de recursos do jogo.
            chave_personagem (str): 'rena', 'gnomo' ou 'gingerbread'.
        """
        pygame.sprite.Sprite.__init__(self)  # inicializa a classe mãe (obrigatório, como no handout)
        imagens = assets['personagens'][chave_personagem]  # dicionário com as imagens desse personagem
        self.quadros_correndo = imagens['correndo']  # lista de quadros da corrida em pé
        self.quadros_abaixado = imagens['abaixado']  # lista de quadros da corrida abaixado
        self.imagem_pulando = imagens['pulando']  # imagem usada enquanto está no ar
        self.som_pulo = assets['som_pulo']  # som tocado ao pular
        self.quadro = 0  # índice do quadro atual da animação
        self.image = self.quadros_correndo[0]  # imagem inicial
        self.rect = self.image.get_rect()  # retângulo da imagem (posição e tamanho)
        self.rect.centerx = JOGADOR_X  # posição horizontal fixa
        self.rect.bottom = CHAO_Y  # pés no chão
        self.mask = pygame.mask.from_surface(self.image)  # máscara: só os pixels visíveis contam na colisão
        self.velocidade_y = 0  # velocidade vertical (positiva = descendo)
        self.y_pes = CHAO_Y  # altura dos pés (guardada à parte para o efeito de quicar não atrapalhar)
        self.no_chao = True  # True quando está pisando no chão
        self.abaixado = False  # True enquanto o botão de abaixar estiver apertado
        self.ultima_troca = pygame.time.get_ticks()  # instante (ms) da última troca de quadro
        self.tempo_por_quadro = 90  # milissegundos que cada quadro fica na tela

    def pular(self):
        """Começa um pulo, mas só se o jogador estiver no chão (não existe pulo duplo)."""
        if self.no_chao and not self.abaixado:  # só pula se estiver no chão e em pé
            self.velocidade_y = FORCA_PULO  # velocidade para cima
            self.no_chao = False  # agora está no ar
            self.som_pulo.play()  # toca o som do pulo

    def abaixar(self, apertado):
        """
        Liga ou desliga o "abaixar".

        Parâmetros:
            apertado (bool): True quando o botão/tecla foi apertado, False quando foi solto.
        """
        self.abaixado = apertado  # guarda o novo estado

    def update(self):
        """Aplica a gravidade, mantém o jogador no chão e troca o quadro da animação."""
        # ----- Física (gravidade) -----
        self.velocidade_y += GRAVIDADE  # a gravidade aumenta a velocidade para baixo a cada frame
        if self.abaixado and not self.no_chao:  # se apertou "abaixar" no ar...
            self.velocidade_y += QUEDA_RAPIDA  # ...cai mais rápido (igual ao jogo do dinossauro)
        self.y_pes += self.velocidade_y  # move os pés de acordo com a velocidade
        if self.y_pes >= CHAO_Y:  # se passou do chão...
            self.y_pes = CHAO_Y  # ...volta para cima do chão
            self.velocidade_y = 0  # para de cair
            self.no_chao = True  # está no chão de novo

        # ----- Animação (mesma lógica da Explosion do handout) -----
        agora = pygame.time.get_ticks()  # instante atual em milissegundos
        if agora - self.ultima_troca > self.tempo_por_quadro:  # já passou o tempo de trocar?
            self.ultima_troca = agora  # marca o instante da troca
            self.quadro = (self.quadro + 1) % len(self.quadros_correndo)  # próximo quadro (volta ao 0 no fim)

        # ----- Escolhe a imagem certa para a situação -----
        if not self.no_chao:  # no ar
            self.image = self.imagem_pulando  # imagem inclinada do pulo
            quique = 0  # no ar não quica
        elif self.abaixado:  # no chão e abaixado
            self.image = self.quadros_abaixado[self.quadro]  # quadro da corrida abaixado
            quique = 0  # abaixado não quica (para passar embaixo da bengala com folga)
        else:  # no chão e em pé
            self.image = self.quadros_correndo[self.quadro]  # quadro da corrida normal
            quique = QUIQUE[self.quadro]  # pixels de "pulinho" desse quadro

        self.rect = self.image.get_rect()  # recria o retângulo (o tamanho muda ao abaixar)
        self.rect.centerx = JOGADOR_X  # mantém a posição horizontal
        self.rect.bottom = round(self.y_pes) - quique  # posiciona os pés
        self.mask = pygame.mask.from_surface(self.image)  # atualiza a máscara de colisão


class Obstaculo(pygame.sprite.Sprite):
    """Obstáculo que anda da direita para a esquerda (árvores, arbusto ou bengala)."""

    def __init__(self, assets, nome, x):
        """
        Cria um obstáculo.

        Parâmetros:
            assets (dict): recursos do jogo.
            nome (str): chave de TIPOS_OBSTACULO ('arbusto', 'arvore', 'arvore_luzes' ou 'bengala').
            x (float): posição horizontal inicial (lado esquerdo).
        """
        pygame.sprite.Sprite.__init__(self)  # inicializa a classe mãe
        info = TIPOS_OBSTACULO[nome]  # dicionário com as informações desse tipo
        self.nome = nome  # guarda o nome (útil para testes e depuração)
        self.tipo = info['tipo']  # 'baixo' ou 'alto'
        self.image = assets[nome]  # imagem do obstáculo (a chave do assets tem o mesmo nome)
        self.rect = self.image.get_rect()  # retângulo da imagem
        self.x = float(x)  # posição x com casas decimais (a velocidade não é inteira)
        self.rect.left = round(self.x)  # posiciona na horizontal
        self.rect.bottom = CHAO_Y - info['altura_do_chao']  # posiciona na vertical
        self.mask = pygame.mask.from_surface(self.image)  # máscara para colisão precisa

    def update(self, velocidade):
        """
        Move o obstáculo para a esquerda e o apaga quando sai da tela.

        Parâmetros:
            velocidade (float): quantos pixels o cenário anda neste frame.
        """
        self.x -= velocidade  # anda para a esquerda
        self.rect.left = round(self.x)  # atualiza o retângulo
        if self.rect.right < 0:  # saiu totalmente pela esquerda?
            self.kill()  # remove de todos os grupos (como as balas do handout)


class Presente(pygame.sprite.Sprite):
    """Presente que gira e dá um ponto quando o jogador encosta nele."""

    def __init__(self, assets, x, no_ar):
        """
        Cria um presente.

        Parâmetros:
            assets (dict): recursos do jogo.
            x (float): posição horizontal do centro.
            no_ar (bool): True = flutuando (precisa pular), False = no chão.
        """
        pygame.sprite.Sprite.__init__(self)  # inicializa a classe mãe
        self.quadros = assets['presente_anim']  # lista de quadros da animação
        self.quadro = 0  # quadro atual
        self.image = self.quadros[0]  # primeira imagem
        self.rect = self.image.get_rect()  # retângulo
        self.x = float(x)  # centro x com casas decimais
        if no_ar:  # se for um presente flutuando...
            self.base = CHAO_Y - 125  # ...fica na altura de um pulo
        else:  # se for no chão...
            self.base = CHAO_Y - 6  # ...fica quase encostando no chão
        self.rect.midbottom = (round(self.x), self.base)  # posiciona
        self.ultima_troca = pygame.time.get_ticks()  # instante da última troca de quadro

    def update(self, velocidade):
        """
        Move o presente com o cenário e troca o quadro da animação de giro.

        Parâmetros:
            velocidade (float): quantos pixels o cenário anda neste frame.
        """
        self.x -= velocidade  # anda junto com o chão
        agora = pygame.time.get_ticks()  # instante atual
        if agora - self.ultima_troca > 80:  # troca de quadro a cada 80 ms
            self.ultima_troca = agora  # marca a troca
            self.quadro = (self.quadro + 1) % len(self.quadros)  # avança e volta ao início no fim
            self.image = self.quadros[self.quadro]  # nova imagem
        self.rect = self.image.get_rect()  # o tamanho muda a cada quadro (efeito de giro)
        self.rect.midbottom = (round(self.x), self.base)  # reposiciona pelo centro de baixo
        if self.rect.right < 0:  # saiu da tela?
            self.kill()  # apaga


class PapaiNoel(pygame.sprite.Sprite):
    """Papai Noel: aparece no final da corrida. Encostar nele vence o jogo."""

    def __init__(self, assets):
        """
        Cria o Papai Noel logo depois da borda direita da tela.

        Parâmetros:
            assets (dict): recursos do jogo.
        """
        pygame.sprite.Sprite.__init__(self)  # inicializa a classe mãe
        self.quadros = assets['papai_noel']  # animação dele balançando
        self.quadro = 0  # quadro atual
        self.image = self.quadros[0]  # primeira imagem
        self.rect = self.image.get_rect()  # retângulo
        self.x = float(LARGURA + 40)  # começa fora da tela, à direita
        self.rect.midbottom = (round(self.x), CHAO_Y)  # em pé no chão
        self.ultima_troca = pygame.time.get_ticks()  # instante da última troca de quadro

    def update(self, velocidade):
        """
        Move o Papai Noel com o cenário e anima o aceno.

        Parâmetros:
            velocidade (float): quantos pixels o cenário anda neste frame.
        """
        self.x -= velocidade  # vem na direção do jogador
        agora = pygame.time.get_ticks()  # instante atual
        if agora - self.ultima_troca > 150:  # troca de quadro a cada 150 ms
            self.ultima_troca = agora  # marca a troca
            self.quadro = (self.quadro + 1) % len(self.quadros)  # próximo quadro
            self.image = self.quadros[self.quadro]  # nova imagem
        self.rect = self.image.get_rect()  # atualiza o retângulo
        self.rect.midbottom = (round(self.x), CHAO_Y)  # mantém no chão


class Floco(pygame.sprite.Sprite):
    """Floco de neve que cai balançando e volta para o topo quando sai da tela."""

    def __init__(self):
        """Cria um floco com tamanho, posição e velocidade sorteados."""
        pygame.sprite.Sprite.__init__(self)  # inicializa a classe mãe
        raio = random.randint(1, 4)  # raio do floco em pixels
        self.image = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)  # superfície transparente
        transparencia = random.randint(140, 240)  # quanto o floco é visível (0 a 255)
        pygame.draw.circle(self.image, BRANCO + (transparencia,), (raio, raio), raio)  # desenha a bolinha
        self.rect = self.image.get_rect()  # retângulo
        self.x = random.uniform(0, LARGURA)  # posição horizontal sorteada
        self.y = random.uniform(-ALTURA, ALTURA)  # posição vertical sorteada (alguns começam acima da tela)
        self.velocidade = random.uniform(0.6, 1.8) + raio * 0.2  # flocos maiores caem mais rápido
        self.fase = random.uniform(0, 2 * math.pi)  # ponto de partida do balanço

    def update(self):
        """Faz o floco cair e balançar; se sair por baixo, volta para o topo."""
        self.y += self.velocidade  # cai
        self.fase += 0.03  # avança o balanço
        self.x += math.sin(self.fase) * 0.5  # balança para os lados usando seno
        if self.y > ALTURA:  # saiu por baixo?
            self.y = -10  # volta para cima
            self.x = random.uniform(0, LARGURA)  # em uma nova posição horizontal
        self.rect.center = (round(self.x), round(self.y))  # atualiza o retângulo


def criar_neve(quantidade):
    """
    Cria um grupo com vários flocos de neve.

    Parâmetros:
        quantidade (int): quantos flocos criar.

    Retorna:
        pygame.sprite.Group: grupo com todos os flocos.
    """
    neve = pygame.sprite.Group()  # grupo vazio
    for _ in range(quantidade):  # repete 'quantidade' vezes
        neve.add(Floco())  # cria um floco e coloca no grupo
    return neve  # devolve o grupo
