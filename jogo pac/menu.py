import pygame
import sys
import math

# ===================== INICIALIZAÇÃO =====================
pygame.init()
LARGURA, ALTURA = 1024, 768
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("GOKU PAC-MAN")
relogio = pygame.time.Clock()

# ===================== FONTES =====================
fonte_titulo = pygame.font.SysFont("Bangers", 140, bold=True)
fonte_botao = pygame.font.SysFont("Arial Black", 55, bold=True)

# ===================== CORES =====================
BRANCO = (255, 255, 255)
AMARELO = (255, 220, 0)
AMARELO_ESCURO = (200, 150, 0)
AZUL = (0, 150, 255)
AZUL_HOVER = (0, 200, 255)
VERMELHO = (255, 50, 50)
VERMELHO_HOVER = (255, 100, 100)
CINZA = (100, 100, 100)
CINZA_HOVER = (150, 150, 150)

# ===================== IMAGENS =====================
try:
    fundo = pygame.image.load("assets/fundo_menu.jpg").convert()
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
except:
    fundo = pygame.Surface((LARGURA, ALTURA))
    fundo.fill((135, 206, 235))  # céu azul

try:
    goku_img = pygame.image.load("assets/goku_esquerda.png").convert_alpha()
    goku_img = pygame.transform.scale(goku_img, (450, 650))
except:
    goku_img = None

# ===================== ANIMAÇÃO DO SOL =====================
sol_x = LARGURA
sol_y = 100
sol_vel = 2

# ===================== BOTÕES =====================
LARGURA_BOTAO = 380
ALTURA_BOTAO = 100
centro_x = LARGURA // 2 - LARGURA_BOTAO // 2
y_inicio = 450

botao_jogar = pygame.Rect(centro_x, y_inicio, LARGURA_BOTAO, ALTURA_BOTAO)
botao_ajuda = pygame.Rect(centro_x, y_inicio + 120, LARGURA_BOTAO, ALTURA_BOTAO)
botao_sair  = pygame.Rect(centro_x, y_inicio + 240, LARGURA_BOTAO, ALTURA_BOTAO)

# ===================== TEXTOS =====================
def texto_com_contorno(texto, fonte, cor, contorno, x, y):
    c = fonte.render(texto, True, contorno)
    tela.blit(c, (x-6, y-6)); tela.blit(c, (x+6, y-6))
    tela.blit(c, (x-6, y+6)); tela.blit(c, (x+6, y+6))
    t = fonte.render(texto, True, cor)
    tela.blit(t, (x, y))

texto_titulo = "GOKU PAC-MAN"
texto_jogar = "JOGAR"
texto_ajuda = "AJUDA"
texto_sair  = "SAIR"

# ===================== LOOP =====================
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if botao_jogar.collidepoint(mx, my):
                print("JOGO INICIADO!")
            elif botao_ajuda.collidepoint(mx, my):
                print("AJUDA!")
            elif botao_sair.collidepoint(mx, my):
                pygame.quit()
                sys.exit()

    # Hover
    mx, my = pygame.mouse.get_pos()
    cor_jogar = AZUL_HOVER if botao_jogar.collidepoint(mx, my) else AZUL
    cor_ajuda = CINZA_HOVER if botao_ajuda.collidepoint(mx, my) else CINZA
    cor_sair  = VERMELHO_HOVER if botao_sair.collidepoint(mx, my) else VERMELHO

    # ===================== DESENHAR =====================
    tela.blit(fundo, (0, 0))

    # Sol se movendo
    pygame.draw.circle(tela, (255, 200, 0), (sol_x, sol_y), 80)
    pygame.draw.circle(tela, (255, 220, 100), (sol_x, sol_y), 70)
    sol_x -= sol_vel
    if sol_x < -100:
        sol_x = LARGURA + 100

    # Goku com aura pulsante
    if goku_img:
        aura_tamanho = 480 + int(20 * math.sin(pygame.time.get_ticks() * 0.01))
        aura = pygame.Surface((aura_tamanho, aura_tamanho), pygame.SRCALPHA)
        pygame.draw.circle(aura, (0, 255, 255, 50), (aura_tamanho//2, aura_tamanho//2), aura_tamanho//2)
        tela.blit(aura, (LARGURA//2 - aura_tamanho//2, ALTURA//2 - aura_tamanho//2 + 50))
        tela.blit(goku_img, (LARGURA//2 - 225, ALTURA//2 - 300))

    # Título com brilho
    titulo_x = LARGURA // 2 - fonte_titulo.size(texto_titulo)[0] // 2
    texto_com_contorno(texto_titulo, fonte_titulo, AMARELO, (0,0,0), titulo_x, 80)

    # Botões com gradiente
    def botao_gradiente(botao, cor1, cor2):
        for i in range(botao.height):
            cor = (
                int(cor1[0] + (cor2[0] - cor1[0]) * i / botao.height),
                int(cor1[1] + (cor2[1] - cor1[1]) * i / botao.height),
                int(cor1[2] + (cor2[2] - cor1[2]) * i / botao.height)
            )
            pygame.draw.line(tela, cor, (botao.left, botao.top + i), (botao.right, botao.top + i))

    botao_gradiente(botao_jogar, AZUL, (0, 50, 150))
    botao_gradiente(botao_ajuda, CINZA, (50, 50, 50))
    botao_gradiente(botao_sair, VERMELHO, (150, 0, 0))

    # Textos nos botões
    def centralizar(texto, botao, cor=BRANCO):
        t = fonte_botao.render(texto, True, cor)
        x = botao.centerx - t.get_width() // 2
        y = botao.centery - t.get_height() // 2
        tela.blit(t, (x, y))

    centralizar(texto_jogar, botao_jogar)
    centralizar(texto_ajuda, botao_ajuda)
    centralizar(texto_sair,  botao_sair)

    # Bordas
    for b in [botao_jogar, botao_ajuda, botao_sair]:
        pygame.draw.rect(tela, BRANCO, b, 6, border_radius=30)

    pygame.display.flip()
    relogio.tick(60)