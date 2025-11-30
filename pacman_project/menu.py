import pygame
import sys
import jogo  # Importa o módulo do jogo

# Inicializa o Pygame e o Mixer (Som)
pygame.init()
pygame.mixer.init()

# --- CONFIGURAÇÕES DE ASSETS DE SOM ---
CAMINHO_SOM_CLIQUE = 'client/assets/click.wav' 
CAMINHO_MUSICA_MENU = 'client/assets/menu_dbz.mp3' # Nova música

som_clique = None
try:
    som_clique = pygame.mixer.Sound(CAMINHO_SOM_CLIQUE)
    som_clique.set_volume(0.5)
except:
    print("Som de clique não disponível.")

# Tenta carregar e tocar a música do menu (INICIALIZAÇÃO)
try:
    pygame.mixer.music.load(CAMINHO_MUSICA_MENU)
    pygame.mixer.music.set_volume(0.2) # Volume 20%
    pygame.mixer.music.play(-1) # -1 significa loop infinito
except Exception as e:
    print(f"Erro ao carregar música do menu: {e}")

# --- CONFIGURAÇÕES DA TELA ---
LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("DBZ Pac-Man: Menu Principal")

# --- CORES ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
LARANJA_DBZ = (255, 128, 0)
LARANJA_HOVER = (255, 165, 0)
AMARELO_SSJ = (255, 255, 0)
COR_FUNDO_JANELA = (30, 40, 30)
COR_BORDA_JANELA = (255, 215, 0)
COR_TEXTO_PADRAO = (200, 200, 200)

# Variáveis de controle
mostrar_sobre = False 
mostrar_ajuda = False 

# --- CARREGAMENTO DE ASSETS (IMAGENS) ---
def carregar_dupla_por_altura(nome_arquivo_base, altura_fixa):
    sprites = {'p': None, 'f': None}
    def carregar_unico(sufixo):
        try:
            caminho = f'client/assets/{nome_arquivo_base}{sufixo}.png'
            img = pygame.image.load(caminho).convert_alpha()
            fator_escala = altura_fixa / img.get_height()
            nova_largura = int(img.get_width() * fator_escala)
            return pygame.transform.scale(img, (nova_largura, altura_fixa))
        except: return None
    sprites['p'] = carregar_unico('p')
    sprites['f'] = carregar_unico('f')
    if not sprites['p'] and sprites['f']: sprites['p'] = sprites['f']
    if not sprites['f'] and sprites['p']: sprites['f'] = sprites['p']
    return sprites

try: imagem_fundo = pygame.transform.scale(pygame.image.load('client/assets/fundo.png'), (LARGURA, ALTURA))
except: imagem_fundo = None

try: logo_pacballz = pygame.transform.scale(pygame.image.load('client/assets/logo.png').convert_alpha(), (500, 250))
except: logo_pacballz = None

ALTURA_PADRAO = 90
Y_PADRAO = 190
PERSONAGENS = {
    'GOKU':     {'imgs': carregar_dupla_por_altura('goku', ALTURA_PADRAO),   'pos': (200, Y_PADRAO)},
    'VEGETA':   {'imgs': carregar_dupla_por_altura('vegeta', ALTURA_PADRAO), 'pos': (300, Y_PADRAO)},
    'FREEZA':   {'imgs': carregar_dupla_por_altura('freeza', ALTURA_PADRAO), 'pos': (400, Y_PADRAO)},
    'CELL':     {'imgs': carregar_dupla_por_altura('cell', ALTURA_PADRAO),   'pos': (500, Y_PADRAO)},
    'MAJINBOO': {'imgs': carregar_dupla_por_altura('boo', ALTURA_PADRAO),    'pos': (600, Y_PADRAO)}
}

# --- FONTES ---
try:
    fonte_grande = pygame.font.Font('client/assets/fonte.ttf', 50)
    fonte_media = pygame.font.Font('client/assets/fonte.ttf', 30)
    fonte_pequena = pygame.font.Font('client/assets/fonte.ttf', 16)
except:
    fonte_grande = pygame.font.Font(None, 80)
    fonte_media = pygame.font.Font(None, 50)
    fonte_pequena = pygame.font.Font(None, 36)

# --- FUNÇÕES AUXILIARES ---
def desenhar_texto(texto, fonte, cor, x, y):
    surf = fonte.render(texto, True, cor)
    rect = surf.get_rect(center=(x, y))
    TELA.blit(surf, rect)

def desenhar_popup(titulo, linhas):
    overlay = pygame.Surface((LARGURA, ALTURA))
    overlay.fill((0,0,0)); overlay.set_alpha(150)
    TELA.blit(overlay, (0,0))
    w, h = 600, 420
    x, y = (LARGURA - w)//2, (ALTURA - h)//2
    pygame.draw.rect(TELA, COR_FUNDO_JANELA, (x, y, w, h), 0, border_radius=20)
    pygame.draw.rect(TELA, COR_BORDA_JANELA, (x, y, w, h), 8, border_radius=20)
    TELA.blit(fonte_media.render(titulo, True, COR_BORDA_JANELA), (x+30, y+25))
    TELA.blit(fonte_pequena.render("Pressione ESC para fechar", True, (100,100,100)), (x+w-335, y+h-40))
    destaques = ["•", "↑", "↓", "←", "→", "W", "A", "S", "D", "ESC"]
    for i, txt in enumerate(linhas):
        cor = AMARELO_SSJ if any(d in txt for d in destaques) else COR_TEXTO_PADRAO
        TELA.blit(fonte_pequena.render(txt, True, cor), (x+30, y+80 + i*28))

def tocar_som():
    if som_clique: som_clique.play()

# --- LOOP PRINCIPAL ---
def menu_principal():
    global mostrar_sobre, mostrar_ajuda
    clock = pygame.time.Clock()
    timer_animacao = 0
    frame_atual = 'p'
    
    # Garante que a música toque se voltar de um game over inesperado
    if not pygame.mixer.music.get_busy():
        try:
            pygame.mixer.music.load(CAMINHO_MUSICA_MENU)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
        except: pass

    while True:
        dt = clock.tick(60)
        timer_animacao += dt
        if timer_animacao >= 500:
            timer_animacao = 0
            frame_atual = 'f' if frame_atual == 'p' else 'p'
            
        botoes = [
            {'rect': pygame.Rect(LARGURA//2-120, 290, 240, 50), 'texto': 'INICIAR', 'acao': 'jogar'},
            {'rect': pygame.Rect(LARGURA//2-120, 360, 240, 50), 'texto': 'AJUDA', 'acao': 'ajuda'},
            {'rect': pygame.Rect(LARGURA//2-120, 430, 240, 50), 'texto': 'SOBRE', 'acao': 'sobre'},
            {'rect': pygame.Rect(LARGURA//2-120, 500, 240, 50), 'texto': 'SAIR', 'acao': 'sair'}
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        pop_aberto = mostrar_sobre or mostrar_ajuda
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and pop_aberto:
                    mostrar_sobre = False; mostrar_ajuda = False
            if event.type == pygame.MOUSEBUTTONDOWN and not pop_aberto:
                for btn in botoes:
                    if btn['rect'].collidepoint(event.pos):
                        tocar_som()
                        if btn['acao'] == 'jogar':
                            print("INICIANDO JOGO...")
                            
                            # PARA A MÚSICA DO MENU ANTES DE ENTRAR NO JOGO
                            pygame.mixer.music.stop()
                            
                            try: jogo.main_jogo()
                            except Exception as e: print(f"Erro no jogo: {e}")
                            
                            # VOLTA A TOCAR MÚSICA DO MENU AO SAIR DO JOGO
                            pygame.display.set_mode((LARGURA, ALTURA))
                            pygame.display.set_caption("DBZ Pac-Man: Menu Principal")
                            try:
                                pygame.mixer.music.load(CAMINHO_MUSICA_MENU)
                                pygame.mixer.music.set_volume(0.2) # <--- CORREÇÃO AQUI
                                pygame.mixer.music.play(-1)
                            except: pass
                            
                        elif btn['acao'] == 'ajuda': mostrar_ajuda = True
                        elif btn['acao'] == 'sobre': mostrar_sobre = True
                        elif btn['acao'] == 'sair': pygame.quit(); sys.exit()

        # Desenho
        if imagem_fundo: TELA.blit(imagem_fundo, (0,0))
        else: TELA.fill(PRETO)
        if logo_pacballz: TELA.blit(logo_pacballz, ((LARGURA - 500)//2, -30))
        else: desenhar_texto("PAC BALL Z", fonte_grande, AMARELO_SSJ, LARGURA//2, 100)
        
        for nome, dados in PERSONAGENS.items():
            img = dados['imgs'].get(frame_atual) or dados['imgs'].get('p')
            if img:
                x_pos = dados['pos'][0] - (img.get_width() // 2)
                y_pos = dados['pos'][1]
                TELA.blit(img, (x_pos, y_pos))
        
        for btn in botoes:
            cor = LARANJA_HOVER if btn['rect'].collidepoint(mouse_pos) and not pop_aberto else LARANJA_DBZ
            pygame.draw.rect(TELA, cor, btn['rect'], border_radius=15)
            desenhar_texto(btn['texto'], fonte_media, BRANCO, btn['rect'].centerx, btn['rect'].centery)
            
        if mostrar_sobre:
            desenhar_popup("SOBRE", ["Desenvolvido por:", "• Gabriel Ricetto", "• Joao Vitor Pastori", "• Victor Querino", "", "Materia de Redes", "3º ano - Ciencia da Computacao", "UNESPAR"])
        if mostrar_ajuda:
            desenhar_popup("AJUDA", ["COMANDOS:", "", "W, A, S, D - Movimentacao", "ESC - Sair/Voltar"])
            
        pygame.display.flip()

if __name__ == "__main__":
    menu_principal()