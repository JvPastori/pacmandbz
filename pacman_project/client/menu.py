import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Caminho para o arquivo de som (Certifique-se que é o seu arquivo .wav)
CAMINHO_SOM_CLIQUE = 'client/assets/click.wav' 

som_clique = None
try:
    # Carrega o som
    som_clique = pygame.mixer.Sound(CAMINHO_SOM_CLIQUE)
except pygame.error as e:
    print(f"Erro ao carregar o som: {CAMINHO_SOM_CLIQUE}. {e}")
    print("O som de clique não estará disponível.")


# --- CONFIGURAÇÕES DA TELA ---
LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("MEU JOGO")

# --- DEFINIÇÃO DE CORES ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# CORES TEMA DRAGON BALL Z
LARANJA_DBZ = (255, 128, 0)        # Cor padrão dos botões
LARANJA_HOVER = (255, 165, 0)      # Laranja para o hover
AMARELO_SSJ = (255, 255, 0)        # Cor de destaque (Super Saiyan)

# CORES POP-UPS
COR_FUNDO_JANELA = (30, 40, 30)    # Fundo da janela pop-up
COR_BORDA_JANELA = (255, 215, 0)   # Borda/Título (Ouro)
COR_TEXTO_PADRAO = (200, 200, 200) # Cor padrão do texto

# Variáveis de estado para os pop-ups
mostrar_sobre = False 
mostrar_ajuda = False 

# --- CARREGAMENTO DE ASSETS ---

# Função para carregar e redimensionar imagens
def carregar_e_redimensionar(caminho, largura_desejada):
    try:
        imagem = pygame.image.load(caminho).convert_alpha()
        largura_original = imagem.get_width()
        altura_original = imagem.get_height()
        nova_altura = int((largura_desejada / largura_original) * altura_original)
        return pygame.transform.scale(imagem, (largura_desejada, nova_altura))
    except pygame.error as e:
        print(f"Erro ao carregar imagem: {caminho}. {e}")
        return None

# Imagem de fundo
imagem_fundo = None
try:
    imagem_fundo = pygame.image.load('client/assets/fundo.png')
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))
except pygame.error:
    print("Aviso: Imagem de fundo não encontrada. Usando tela preta.")

# Logo
logo_pacballz = None 
try:
    logo_pacballz = pygame.image.load('client/assets/logo.png').convert_alpha() 
    logo_pacballz = pygame.transform.scale(logo_pacballz, (500, 250)) 
except pygame.error as e:
    print(f"Erro ao carregar a logo: logo.png. Usando texto alternativo.")
    logo_pacballz = None

# Tamanhos dos Personagens
TAMANHO_GOKU = 180 
TAMANHO_VEGETA = 150 
TAMANHO_FREEZA = 195 
TAMANHO_CELL = 180 
TAMANHO_MAJINBOO = 185 

# Carregamento de Personagens
imagem_goku = carregar_e_redimensionar('client/assets/gokuzz.png', TAMANHO_GOKU)
imagem_veg = carregar_e_redimensionar('client/assets/veg.png', TAMANHO_VEGETA)
imagem_freeza = carregar_e_redimensionar('client/assets/freeza.png', TAMANHO_FREEZA)
imagem_cell = carregar_e_redimensionar('client/assets/cell.png', TAMANHO_CELL)
imagem_majinboo = carregar_e_redimensionar('client/assets/majinboo.png', TAMANHO_MAJINBOO)


# --- FONTES ---
CAMINHO_FONTE = 'client/assets/fonte.ttf'

try:
    # Carrega a fonte customizada
    fonte_grande = pygame.font.Font(CAMINHO_FONTE, 50)
    fonte_media = pygame.font.Font(CAMINHO_FONTE, 30)
    fonte_pequena = pygame.font.Font(CAMINHO_FONTE, 16)
except FileNotFoundError:
    # Fallback: Fonte padrão do Pygame
    print("Aviso: Fonte customizada não encontrada. Usando fonte padrão.")
    fonte_grande = pygame.font.Font(None, 80)
    fonte_media = pygame.font.Font(None, 50)
    fonte_pequena = pygame.font.Font(None, 36)


# --- FUNÇÕES DE DESENHO ---

def desenhar_texto(texto, fonte, cor, x, y):
    """Desenha texto centralizado na tela."""
    superficie = fonte.render(texto, True, cor)
    retangulo = superficie.get_rect(center=(x, y))
    TELA.blit(superficie, retangulo)

def desenhar_janela_popup(titulo_texto, cor_fundo, cor_borda, x, y, largura, altura, textos):
    """Desenha a janela de pop-up (SOBRE/AJUDA)."""
    # Overlay escuro
    overlay = pygame.Surface((LARGURA, ALTURA))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(150) 
    TELA.blit(overlay, (0, 0))
    
    # Janela principal
    pygame.draw.rect(TELA, cor_fundo, (x, y, largura, altura), 0, border_radius=20)
    pygame.draw.rect(TELA, cor_borda, (x, y, largura, altura), 8, border_radius=20)
    
    # Título
    titulo = fonte_media.render(titulo_texto, True, cor_borda)
    TELA.blit(titulo, (x + 30, y + 25))
    
    # Aviso de ESC
    aviso_esc = fonte_pequena.render("Pressione ESC para fechar", True, (100, 100, 100))
    TELA.blit(aviso_esc, (x + largura - 335, y + altura - 40))
    
    # Textos
    comandos_destaque = ["•", "↑", "↓", "←", "→", "W", "A", "S", "D", "ESC"]
    
    for i, linha in enumerate(textos):
        cor = COR_TEXTO_PADRAO
        
        # Destaca comandos com o AMARELO_SSJ
        deve_ser_amarela = any(item in linha for item in comandos_destaque)
        
        if deve_ser_amarela:
             cor = AMARELO_SSJ
        
        txt = fonte_pequena.render(linha, True, cor)
        TELA.blit(txt, (x + 30, y + 80 + i * 28))


# --- FUNÇÃO PARA TOCAR O SOM ---
def tocar_som_clique():
    """Toca o som de clique se ele foi carregado."""
    if som_clique:
        som_clique.play()


# --- LOOP PRINCIPAL DO MENU ---

def menu_principal():
    global mostrar_sobre 
    global mostrar_ajuda 
    
    clock = pygame.time.Clock()
    RAIO_BOTAO = 15

    # Posições da janela pop-up (centralizada)
    largura_janela, altura_janela = 600, 420 
    x_janela = (LARGURA - largura_janela) // 2 
    y_janela = (ALTURA - altura_janela) // 2 
    
    while True:
        # Retângulos dos botões
        botao_jogar = pygame.Rect(LARGURA//2 - 120, 260, 240, 60)
        botao_ajuda = pygame.Rect(LARGURA//2 - 120, 340, 240, 60)
        botao_sobre = pygame.Rect(LARGURA//2 - 120, 420, 240, 60)
        botao_sair = pygame.Rect(LARGURA//2 - 120, 500, 240, 60)
        
        # Lógica de Hover
        pos_mouse = pygame.mouse.get_pos()
        pop_aberto = mostrar_sobre or mostrar_ajuda
        
        cor_jogar = LARANJA_HOVER if botao_jogar.collidepoint(pos_mouse) and not pop_aberto else LARANJA_DBZ
        cor_ajuda = LARANJA_HOVER if botao_ajuda.collidepoint(pos_mouse) and not pop_aberto else LARANJA_DBZ
        cor_sobre = LARANJA_HOVER if botao_sobre.collidepoint(pos_mouse) and not pop_aberto else LARANJA_DBZ
        cor_sair = LARANJA_HOVER if botao_sair.collidepoint(pos_mouse) and not pop_aberto else LARANJA_DBZ
        
        # --- Tratamento de Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if not pop_aberto:
                    if botao_jogar.collidepoint(evento.pos):
                        tocar_som_clique()  # Som ao iniciar
                        print("🎮 JOGO INICIADO!")
                    elif botao_ajuda.collidepoint(evento.pos): 
                        tocar_som_clique()  # Som ao abrir Ajuda
                        mostrar_ajuda = True 
                    elif botao_sobre.collidepoint(evento.pos):
                        tocar_som_clique()  # Som ao abrir Sobre
                        mostrar_sobre = True
                    elif botao_sair.collidepoint(evento.pos):
                        tocar_som_clique()  # Som ao sair
                        pygame.quit()
                        sys.exit()
            
            # --- CORREÇÃO: Removendo som do ESC ---
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE and pop_aberto:
                    # tocar_som_clique() <-- REMOVIDO para que ESC não faça barulho
                    mostrar_sobre = False
                    mostrar_ajuda = False 
        
        # --- Desenho da Tela ---
        if imagem_fundo:
            TELA.blit(imagem_fundo, (0, 0))
        else:
            TELA.fill(PRETO)
            
        # Posição da logo
        if logo_pacballz:
            logo_x = (LARGURA - logo_pacballz.get_width()) // 2
            TELA.blit(logo_pacballz, (logo_x, -30))
        else:
            desenhar_texto("PAC BALL Z", fonte_grande, AMARELO_SSJ, LARGURA//2, 130)
        
        # Desenho dos Personagens (Posições ajustadas)
        if imagem_goku:
            TELA.blit(imagem_goku, (200, 100)) # Goku
        if imagem_veg:
            TELA.blit(imagem_veg, (280, 125)) # Vegeta
        if imagem_freeza:
            TELA.blit(imagem_freeza, (310, 155)) # Freeza
        if imagem_majinboo:
            TELA.blit(imagem_majinboo, (375, 160)) # Majin Boo
        if imagem_cell:
            TELA.blit(imagem_cell, (420, 165)) # Cell

        # Desenha os Botões
        pygame.draw.rect(TELA, cor_jogar, botao_jogar, border_radius=RAIO_BOTAO)
        pygame.draw.rect(TELA, cor_ajuda, botao_ajuda, border_radius=RAIO_BOTAO) 
        pygame.draw.rect(TELA, cor_sobre, botao_sobre, border_radius=RAIO_BOTAO) 
        pygame.draw.rect(TELA, cor_sair, botao_sair, border_radius=RAIO_BOTAO)

        # Desenha o Texto dos Botões
        desenhar_texto("INICIAR", fonte_media, BRANCO, LARGURA//2, 290)
        desenhar_texto("AJUDA", fonte_media, BRANCO, LARGURA//2, 370)
        desenhar_texto("SOBRE", fonte_media, BRANCO, LARGURA//2, 450)
        desenhar_texto("SAIR", fonte_media, BRANCO, LARGURA//2, 530)
        
        # Desenha os Pop-ups
        if mostrar_sobre:
            textos_sobre = [
                "Desenvolvido por:",
                "• Gabriel Ricetto",
                "• Joao Vitor Pastori",
                "• Victor Querino",
                "",
                "Materia de Redes",
                "3º ano - Ciencia da Computacao",
                "Universidade Estadual do Parana"
            ]
            desenhar_janela_popup("SOBRE", COR_FUNDO_JANELA, COR_BORDA_JANELA, x_janela, y_janela, largura_janela, altura_janela, textos_sobre)

        if mostrar_ajuda:
            textos_ajuda = [
                "COMANDOS DO JOGO:",
                "",
                "MOVIMENTACAO:",
                "",
                "W  - Mover para Cima",
                "S  - Mover para Baixo",
                "A  - Mover para Esquerda",
                "D  - Mover para Direita",
                "",
                "SAIR DO MENU:",
                "ESC",
            ]
            desenhar_janela_popup("AJUDA", COR_FUNDO_JANELA, COR_BORDA_JANELA, x_janela, y_janela, largura_janela, altura_janela, textos_ajuda)
        
        # Atualiza a tela
        pygame.display.flip()
        clock.tick(60)

# Inicia o menu
if __name__ == "__main__":
    menu_principal()
