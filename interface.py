import pygame  # biblioteca de jogos
from config import BRANCO, AZUL_ESCURO  # cores


def desenhar_texto(janela, texto, fonte, cor, centro, cor_sombra=None):
    """
    Escreve um texto com o centro na posição pedida.

    Parâmetros:
        janela (pygame.Surface): onde desenhar.
        texto (str): o que escrever.
        fonte (pygame.font.Font): fonte a usar.
        cor (tuple): cor do texto.
        centro (tuple): (x, y) do centro do texto.
        cor_sombra (tuple ou None): cor da sombra; None = sem sombra.
    """
    
    imagem = fonte.render(texto, True, cor)  # cria a imagem do texto (como no jogo_v3.py do handout)
    janela.blit(imagem, imagem.get_rect(center=centro))  # desenha o texto centralizado


def desenhar_caixa(janela, cor, rect, cor_borda=None):
    """
    Desenha um retângulo com cantos arredondados e, se quiser, uma borda.

    Parâmetros:
        janela (pygame.Surface): onde desenhar.
        cor (tuple): cor de dentro.
        rect (pygame.Rect): posição e tamanho.
        cor_borda (tuple ou None): cor da borda; None = sem borda.
    """
    pygame.draw.rect(janela, cor, rect, border_radius=14)  # retângulo cheio com cantos arredondados
    if cor_borda is not None:  # se pediu borda...
        pygame.draw.rect(janela, cor_borda, rect, 3, border_radius=14)  # ...desenha só o contorno (3 pixels)

def desenhar_etiqueta(janela, texto, fonte, centro):
    """
    Escreve um texto branco dentro de uma caixinha azul escura (para ler bem em cima da neve).

    Parâmetros:
        janela (pygame.Surface): onde desenhar.
        texto (str): o que escrever.
        fonte (pygame.font.Font): fonte a usar.
        centro (tuple): (x, y) do centro.
    """
    imagem = fonte.render(texto, True, BRANCO)  # imagem do texto
    caixa = imagem.get_rect(center=centro).inflate(28, 12)  # retângulo 28 px mais largo e 12 px mais alto
    desenhar_caixa(janela, AZUL_ESCURO, caixa)  # fundo azul escuro
    janela.blit(imagem, imagem.get_rect(center=centro))  # texto por cima


def alternar_musica(dados):
    """
    Liga a música se estiver desligada e desliga se estiver ligada.

    Parâmetros:
        dados (dict): dados do jogo; a chave 'musica' guarda True ou False.
    """
    dados['musica'] = not dados['musica']  # inverte: True vira False e False vira True
    if dados['musica']:  # se agora está ligada...
        pygame.mixer.music.unpause()  # ...continua a música
    else:  # se agora está desligada...
        pygame.mixer.music.pause()  # ...pausa a música


class Botao:
    """
    Botão clicável com um ícone OU um texto no meio.

    Os cantos são arredondados pela metade da altura: se o botão for quadrado
    ele vira um círculo, se for comprido ele vira uma "pílula".
    """

    def __init__(self, rect, cor, icone=None, texto='', fonte=None):
        """
        Cria o botão.

        Parâmetros:
            rect (tuple): (x, y, largura, altura) do botão.
            cor (tuple): cor de fundo.
            icone (pygame.Surface ou None): imagem no meio do botão.
            texto (str): texto no meio do botão (usado quando não tem ícone).
            fonte (pygame.font.Font ou None): fonte do texto.
        """
        self.rect = pygame.Rect(rect)  # posição e tamanho
        self.cor = cor  # cor de fundo (pode ser trocada depois, ex.: botão vermelho quando apertado)
        self.icone = icone  # imagem do ícone
        self.texto = texto  # texto
        self.fonte = fonte  # fonte do texto

    def contem(self, posicao):
        """
        Diz se um ponto (por exemplo, onde o mouse clicou) está dentro do botão.

        Parâmetros:
            posicao (tuple): (x, y) do ponto.

        Retorna:
            bool: True se o ponto está dentro do botão.
        """
        return self.rect.collidepoint(posicao)  # o Rect do pygame já sabe fazer essa conta

    def desenhar(self, janela):
        """
        Desenha o botão: sombra, fundo, borda branca e o ícone ou o texto.

        Parâmetros:
            janela (pygame.Surface): onde desenhar.
        """
        raio = self.rect.height // 2  # arredondamento = metade da altura
        sombra = self.rect.move(0, 5)  # cópia do retângulo 5 pixels mais para baixo
        pygame.draw.rect(janela, AZUL_ESCURO, sombra, border_radius=raio)  # sombra (dá efeito 3D)
        pygame.draw.rect(janela, self.cor, self.rect, border_radius=raio)  # fundo colorido
        pygame.draw.rect(janela, BRANCO, self.rect, 3, border_radius=raio)  # borda branca de 3 pixels
        if self.icone is not None:  # se tem ícone...
            janela.blit(self.icone, self.icone.get_rect(center=self.rect.center))  # ...desenha no centro
        else:  # se não tem ícone...
            desenhar_texto(janela, self.texto, self.fonte, BRANCO, self.rect.center)  # ...escreve o texto no centro