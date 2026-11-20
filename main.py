"""
main.py — Arquivo principal: é este que você executa para jogar.

    python main.py

Ele segue a estrutura básica de um jogo do handout (Inicialização → Loop
principal → Finalização) e usa uma MÁQUINA DE ESTADOS: a variável `estado`
diz qual tela está ativa. Cada tela é uma função que roda o seu próprio loop
e, quando termina, devolve o próximo estado.
"""
import pygame  # biblioteca de jogos
from config import LARGURA, ALTURA, TITULO, INICIO, JOGANDO, MORREU, VENCEU, SAIR  # constantes
from recursos import carregar_assets  # carrega imagens, sons e fontes
from recorde import ler_recorde  # lê o recorde salvo
from tela_inicial import tela_inicial  # tela de início
from tela_jogo import tela_jogo  # tela da corrida
from tela_final import tela_final  # telas YOU DIED! e YOU WIN!


def main():
    """Inicializa o PyGame, roda a máquina de estados e finaliza o jogo."""
    # ===== Inicialização =====
    pygame.init()  # inicia o PyGame
    pygame.mixer.init()  # inicia o módulo de som
    janela = pygame.display.set_mode((LARGURA, ALTURA))  # cria a janela
    pygame.display.set_caption(TITULO)  # título da janela
    assets = carregar_assets()  # carrega tudo (precisa vir depois do set_mode)

    # Dicionário com as informações que passam de uma tela para outra
    dados = {
        'personagem': 'rena',  # personagem escolhido (começa com a rena)
        'musica': True,  # música ligada?
        'presentes': 0,  # presentes coletados na partida atual
        'recorde': ler_recorde(),  # recorde salvo no arquivo
    }

    pygame.mixer.music.load(assets['musica'])  # carrega a música de Natal
    pygame.mixer.music.set_volume(0.45)  # volume (de 0 a 1)
    pygame.mixer.music.play(loops=-1)  # toca em loop infinito (-1)

    # ===== Loop principal: máquina de estados =====
    estado = INICIO  # o jogo começa na tela inicial
    while estado != SAIR:  # repete até alguém pedir para sair
        if estado == INICIO:  # tela inicial
            estado = tela_inicial(janela, assets, dados)
        elif estado == JOGANDO:  # corrida
            estado = tela_jogo(janela, assets, dados)
        elif estado == MORREU or estado == VENCEU:  # telas finais
            estado = tela_final(janela, assets, dados, estado)

    # ===== Finalização =====
    pygame.quit()  # fecha a janela e libera os recursos


if __name__ == '__main__':  # só roda se este arquivo for executado diretamente
    main()  # começa o jogo