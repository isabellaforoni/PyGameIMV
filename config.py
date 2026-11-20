
"""
Configurações gerais do jogo.
- CONSTANTES (valores que não mudam enquanto o jogo roda):

"""
import os  # biblioteca padrão do Python para montar caminhos de arquivos
# ===== Janela =====
LARGURA = 960  # largura da janela em pixels
ALTURA = 540  # altura da janela em pixels
TITULO = 'Você é capaz de chegar no Papai Noel?'  # texto da barra de título da janela
FPS = 60  # quantas vezes por segundo o loop principal roda (frames por segundo)

#Estados (máquina de estados, igual ao handout)
INICIO = 0  # estado da tela inicial
JOGANDO = 1  # estado da tela do jogo
MORREU = 2  # estado da tela final de derrota (YOU DIED!)
VENCEU = 3  # estado da tela final de vitória (YOU WIN!)
SAIR = 4  # estado que encerra o programa

#Cores (tuplas RGB: vermelho, verde, azul, de 0 a 255) 
BRANCO = (255, 255, 255)  # branco
AZUL_ESCURO = (11, 24, 56)  # azul da noite (usado em fundos de painéis)
AZUL_BOTAO = (35, 65, 122)  # azul dos botões redondos
VERMELHO = (210, 47, 60)  # vermelho natalino (botão START)
VERMELHO_ESCURO = (122, 16, 32)  # vermelho escuro (sombra do texto HOHOHO!)
VERDE = (47, 158, 90)  # verde natalino (botão de voltar ao jogo)
DOURADO = (255, 210, 63)  # dourado (seleção de personagem e YOU WIN)
DOURADO_ESCURO = (138, 90, 0)  # sombra do texto dourado
CINZA_CLARO = (230, 237, 251)  # texto secundário

#Chão e jogador 
CHAO_Y = 438  # coordenada y da linha do chão (lembrando: y cresce para baixo)
JOGADOR_X = 120  # posição x fixa do jogador (ele não anda; o cenário é que se move)
ALTURA_JOGADOR = 90  # altura em pixels do personagem em pé
FATOR_ABAIXADO = 0.55  # quando abaixa, a altura vira 55% da original

#Física do pulo 
GRAVIDADE = 0.9  # quanto a velocidade vertical aumenta a cada frame (puxa para baixo)
FORCA_PULO = -19  # velocidade vertical no início do pulo (negativa = para cima)
QUEDA_RAPIDA = 1.6  # gravidade extra quando aperta "abaixar" no ar (cai mais rápido)

#Velocidade do cenário 
VELOCIDADE_INICIAL = 7.0  # pixels por frame que o chão anda no começo
VELOCIDADE_MAXIMA = 12.5  # velocidade máxima que o chão pode atingir
ACELERACAO = 0.0015  # quanto a velocidade aumenta a cada frame (o jogo vai ficando difícil)
DISTANCIA_TOTAL = 60000  # distância (em pixels) até o Papai Noel aparecer
PRESENTES_NECESSARIOS = 15  # presentes mínimos para o Papai Noel aceitar a vitória

#Espaço entre obstáculos
# O espaço é medido em "frames de corrida": espaço = velocidade * frames.
# Assim, quanto mais rápido o jogo, maior o espaço 
FRAMES_MIN_ENTRE_OBSTACULOS = 55  # espaço mínimo entre dois obstáculos
FRAMES_MAX_ENTRE_OBSTACULOS = 90  # espaço máximo entre dois obstáculos
CHANCE_PRESENTE = 0.55  # probabilidade (0 a 1) de aparecer um presente entre dois obstáculos

#Pastas dos arquivos 
PASTA_JOGO = os.path.dirname(os.path.abspath(__file__))  # pasta onde este arquivo está
PASTA_IMG = os.path.join(PASTA_JOGO, 'assets', 'img')  # pasta das imagens
PASTA_SND = os.path.join(PASTA_JOGO, 'assets', 'snd')  # pasta dos sons
PASTA_FONTES = os.path.join(PASTA_JOGO, 'assets', 'fontes')  # pasta das fontes de texto
ARQUIVO_RECORDE = os.path.join(PASTA_JOGO, 'recorde.txt')  # arquivo onde o recorde é salvo

