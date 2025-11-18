import pygame
import sys
import random
import time
import math 
import copy 

# --- SOLUÇÃO DE INICIALIZAÇÃO SEGURA ---
if not pygame.get_init():
    pygame.init()
    
# Garante que a fonte esteja inicializada
if not pygame.font.get_init():
    pygame.font.init()

# --- 1. CONFIGURAÇÕES GERAIS ---
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)       
BRANCO = (255, 255, 255)      

LARANJA_PAREDE = (200, 100, 0)      
LARANJA_PELLET = (255, 180, 80)     
VERDE_TIMER = (0, 255, 0)           

VERMELHO = (255, 0, 0)          
CIANO = (0, 255, 255)           
ROSA = (255, 184, 255)          
LARANJA_VILAO = (255, 184, 82)  

POWER_MODE_DURATION = 8 * 60    
RESPAWN_TIME_SECONDS = 5        
RESPAWN_TIME_FRAMES = RESPAWN_TIME_SECONDS * 60 

TELA_LARGURA = 800
TELA_ALTURA = 600
TELA_TAMANHO = (TELA_LARGURA, TELA_ALTURA)
FPS = 60

# --- CONFIGURAÇÕES DO LABIRINTO ---
TAMANHO_BLOCO = 30
RAIO_PONTO = 4      
RAIO_POWER_PONTO = 8 

# Variáveis globais de posição (calculadas em configurar_labirinto)
X_INICIAL = 0
Y_INICIAL = 0 
FANTASMA_SPAWN_X = 12 
FANTASMA_SPAWN_Y = 8 

PACMAN_SPAWN_X_GRID = 0  
PACMAN_SPAWN_Y_GRID = 9  

# Matriz do Labirinto
MAPA_JOGO_BASE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # LINHA 9 (TÚNEL)
    [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Variável para ser populada com o mapa no início de cada jogo
MAPA_JOGO = []

# --- CONFIGURAÇÃO DE SPRITES (Mantida a mesma) ---
CAMINHO_IMAGENS = 'client/assets/' 
TAMANHO_SPRITE = TAMANHO_BLOCO

IMAGEM_GOKU_BASE = None 
IMAGEM_GOKU_ROTACAO = None 
IMAGENS_VILOES = {} 
IMAGEM_VILAO_MEDO = None 

def carregar_sprites():
    global IMAGEM_GOKU_BASE, IMAGEM_GOKU_ROTACAO, IMAGENS_VILOES, IMAGEM_VILAO_MEDO
    
    try:
        goku_img = pygame.image.load(CAMINHO_IMAGENS + 'goku.png').convert_alpha()
        IMAGEM_GOKU_BASE = pygame.transform.scale(goku_img, (TAMANHO_SPRITE, TAMANHO_SPRITE))
        IMAGEM_GOKU_ROTACAO = IMAGEM_GOKU_BASE.copy()
    except:
        IMAGEM_GOKU_BASE = None

    nomes_vilões = {'FREEZA': 'freeza.png', 'CELL': 'sell.png', 'MAJIN_BOO': 'majin.png', 'VEGETA': 'vegeta.png'}
    for nome_vilao, nome_arquivo in nomes_vilões.items():
        try:
            vilao_img = pygame.image.load(CAMINHO_IMAGENS + nome_arquivo).convert_alpha()
            IMAGENS_VILOES[nome_vilao] = pygame.transform.scale(vilao_img, (TAMANHO_SPRITE, TAMANHO_SPRITE))
        except:
            IMAGENS_VILOES[nome_vilao] = None
    
# --- FONTES (Mantidas as mesmas) ---
FONTE_PONTUACAO = pygame.font.Font(None, 40) 
FONTE_MENSAGEM = pygame.font.Font(None, 80)
FONTE_INSTRUCAO = pygame.font.Font(None, 30)
FONTE_TIMER = pygame.font.Font(None, 24)


# --- FUNÇÕES AUXILIARES ---
def desenhar_texto(tela, texto, fonte, cor, x, y, centralizado=True):
    """Desenha texto na tela com opção de centralização."""
    superficie = fonte.render(texto, True, cor)
    retangulo = superficie.get_rect()
    if centralizado:
        retangulo.center = (x, y)
    else:
        retangulo.topleft = (x, y)
    tela.blit(superficie, retangulo)

def configurar_labirinto(mapa, todos_os_sprites, lista_paredes, lista_pontos, lista_power_pellets):
    
    total_pontos = 0 
    
    global X_INICIAL 
    global Y_INICIAL 
    num_linhas = len(mapa)
    
    # Centraliza o mapa na tela
    X_INICIAL = (TELA_LARGURA - (len(mapa[0]) * TAMANHO_BLOCO)) // 2 
    Y_INICIAL = (TELA_ALTURA - (num_linhas * TAMANHO_BLOCO)) // 2 
    
    for linha_idx, linha in enumerate(mapa):
        for coluna_idx, bloco in enumerate(linha):
            
            if bloco == 1:
                parede = Parede(coluna_idx, linha_idx)
                lista_paredes.add(parede)
                todos_os_sprites.add(parede)
                
            elif bloco == 0: 
                ponto = Ponto(coluna_idx, linha_idx)
                lista_pontos.add(ponto)
                
                # Deixando a lógica de desenhar o ponto em todo lugar por causa do debug anterior
                todos_os_sprites.add(ponto)
                total_pontos += 1
            
            elif bloco == 2:
                ponto_poder = PontoPoder(coluna_idx, linha_idx)
                lista_power_pellets.add(ponto_poder)
                todos_os_sprites.add(ponto_poder)
                total_pontos += 1
                
    return total_pontos
    
def resetar_jogo(pacman, todos_os_sprites, lista_paredes, lista_pontos, fantasmas_fixos, lista_power_pellets, lista_fantasmas):
    
    global MAPA_JOGO
    
    # Limpa grupos
    lista_paredes.empty()
    lista_pontos.empty()
    lista_power_pellets.empty()
    lista_fantasmas.empty() 

    for sprite in todos_os_sprites.copy():
        if isinstance(sprite, Parede) or isinstance(sprite, Ponto) or isinstance(sprite, PontoPoder):
            todos_os_sprites.remove(sprite)
            
    MAPA_JOGO = copy.deepcopy(MAPA_JOGO_BASE)
    
    # Garante que X_INICIAL e Y_INICIAL sejam definidos
    configurar_labirinto(MAPA_JOGO, todos_os_sprites, lista_paredes, lista_pontos, lista_power_pellets)
    
    # Reposicionar Pac-Man
    pacman.rect.x = X_INICIAL + PACMAN_SPAWN_X_GRID * TAMANHO_BLOCO
    pacman.rect.y = Y_INICIAL + PACMAN_SPAWN_Y_GRID * TAMANHO_BLOCO
    
    pacman.mudar_x, pacman.mudar_y, pacman.proximo_mudar_x, pacman.proximo_mudar_y = 0, 0, 0, 0
    pacman.passos_restantes = 0
    if pacman not in todos_os_sprites: todos_os_sprites.add(pacman) 

    # Reposicionar Fantasmas e resetar estado
    fantasmas_pos_originais = [
        (FANTASMA_SPAWN_X, FANTASMA_SPAWN_Y), # Freeza
        (13, 8),                              # Cell
        (11, 8),                              # Majin Boo
        (14, 8)                               # Vegeta
    ]
    
    for i, fantasma in enumerate(fantasmas_fixos):
        if i < len(fantasmas_pos_originais): 
            col, row = fantasmas_pos_originais[i] 
            fantasma.rect.x = X_INICIAL + col * TAMANHO_BLOCO
            fantasma.rect.y = Y_INICIAL + row * TAMANHO_BLOCO
            
            # Restaurando a velocidade para 2 (Movimento normal)
            fantasma.velocidade = 2 
            fantasma.grid_velocidade = TAMANHO_BLOCO // fantasma.velocidade
            
            fantasma.mudar_x, fantasma.mudar_y = fantasma.velocidade, 0 # Inicia movendo para a direita
            fantasma.passos_restantes = fantasma.grid_velocidade
            
            fantasma.set_frightened(False) 
            fantasma.eaten = False 
            fantasma.respawn_timer = 0 
            
            if fantasma not in todos_os_sprites: todos_os_sprites.add(fantasma)
            if fantasma not in lista_fantasmas: lista_fantasmas.add(fantasma)
        
    return "JOGANDO" 


# --- 2. CLASSES DO JOGO ---

class Parede(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TAMANHO_BLOCO, TAMANHO_BLOCO])
        self.image.fill(LARANJA_PAREDE) 
        self.rect = self.image.get_rect()
        self.rect.x = X_INICIAL + x * TAMANHO_BLOCO
        self.rect.y = Y_INICIAL + y * TAMANHO_BLOCO

class Ponto(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TAMANHO_BLOCO, TAMANHO_BLOCO])
        self.image.set_colorkey(PRETO)
        centro = TAMANHO_BLOCO // 2
        pygame.draw.circle(self.image, LARANJA_PELLET, (centro, centro), RAIO_PONTO) 
        self.rect = self.image.get_rect()
        self.rect.x = X_INICIAL + x * TAMANHO_BLOCO
        self.rect.y = Y_INICIAL + y * TAMANHO_BLOCO

class PontoPoder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([TAMANHO_BLOCO, TAMANHO_BLOCO])
        self.image.set_colorkey(PRETO)
        centro = TAMANHO_BLOCO // 2
        pygame.draw.circle(self.image, AMARELO, (centro, centro), RAIO_POWER_PONTO) 
        self.rect = self.image.get_rect()
        self.rect.x = X_INICIAL + x * TAMANHO_BLOCO
        self.rect.y = Y_INICIAL + y * TAMANHO_BLOCO


class PacMan(pygame.sprite.Sprite):
    def __init__(self, x, y, tamanho):
        super().__init__()
        self.tamanho = tamanho
        
        if IMAGEM_GOKU_BASE: self.image = IMAGEM_GOKU_BASE.copy() 
        else:
            self.image = pygame.Surface([tamanho, tamanho])
            self.image.set_colorkey(PRETO) 
            pygame.draw.circle(self.image, AMARELO, (tamanho // 2, tamanho // 2), tamanho // 2)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = 3 
        self.grid_passos = TAMANHO_BLOCO // self.velocidade 
        self.passos_restantes = 0
        self.mudar_x = 0
        self.mudar_y = 0
        self.proximo_mudar_x = 0 
        self.proximo_mudar_y = 0

    def set_movimento(self, x, y):
        if x != 0 or y != 0:
            self.proximo_mudar_x = x
            self.proximo_mudar_y = y
        
    def _pode_mudar(self, dx, dy, paredes):
        """Verifica se o PacMan pode se mover para o próximo bloco."""
        posicao_original_x = self.rect.x
        posicao_original_y = self.rect.y
        
        self.rect.x += dx * TAMANHO_BLOCO
        self.rect.y += dy * TAMANHO_BLOCO
        
        colisao = pygame.sprite.spritecollideany(self, paredes)
        
        self.rect.x = posicao_original_x
        self.rect.y = posicao_original_y
        
        return not colisao

    def update(self, paredes):
        
        if self.passos_restantes == 0:
            
            if self.proximo_mudar_x != 0 or self.proximo_mudar_y != 0:
                dx_proximo = self.proximo_mudar_x // self.velocidade
                dy_proximo = self.proximo_mudar_y // self.velocidade
                
                if self._pode_mudar(dx_proximo, dy_proximo, paredes):
                    self.mudar_x = self.proximo_mudar_x
                    self.mudar_y = self.proximo_mudar_y
                    self.passos_restantes = self.grid_passos
                    self.proximo_mudar_x = 0
                    self.proximo_mudar_y = 0
                    
                    if IMAGEM_GOKU_BASE:
                        if self.mudar_x != 0:
                            if self.mudar_x > 0: # Direita
                                self.image = IMAGEM_GOKU_BASE.copy()
                            else: # Esquerda
                                self.image = pygame.transform.flip(IMAGEM_GOKU_BASE, True, False)
                        
            if self.mudar_x != 0 or self.mudar_y != 0:
                dx_atual = self.mudar_x // self.velocidade
                dy_atual = self.mudar_y // self.velocidade
                
                if self._pode_mudar(dx_atual, dy_atual, paredes):
                    self.passos_restantes = self.grid_passos
                else:
                    self.mudar_x = 0
                    self.mudar_y = 0

        if self.passos_restantes > 0:
            self.rect.x += self.mudar_x
            self.rect.y += self.mudar_y
            self.passos_restantes -= 1

        # Lógica de túnel (warp)
        limite_esquerdo = X_INICIAL
        limite_direito = X_INICIAL + (len(MAPA_JOGO[0]) * TAMANHO_BLOCO)

        if self.rect.left >= limite_direito: 
            self.rect.right = limite_esquerdo + self.rect.width 
        elif self.rect.right <= limite_esquerdo: 
            self.rect.left = limite_direito - self.rect.width 


class Fantasma(pygame.sprite.Sprite):
    def __init__(self, x_bloco, y_bloco, nome, cor_fallback):
        super().__init__()
        self.tamanho = TAMANHO_BLOCO
        self.nome_vilao = nome 
        self.original_cor = cor_fallback 
        
        # 🛑 VELOCIDADE RESTAURADA PARA O MOVIMENTO NORMAL
        self.velocidade = 2 
        
        self.grid_velocidade = TAMANHO_BLOCO // self.velocidade
        self.frightened = False
        self.eaten = False 
        self.respawn_timer = 0 

        self.image = pygame.Surface([self.tamanho, self.tamanho]).convert_alpha()
        self.image.set_colorkey(PRETO)
        
        self._desenhar_fantasma(self.original_cor) 

        self.rect = self.image.get_rect()
        self.rect.x = X_INICIAL + x_bloco * TAMANHO_BLOCO
        self.rect.y = Y_INICIAL + y_bloco * TAMANHO_BLOCO

        self.mudar_x = self.velocidade
        self.mudar_y = 0
        self.passos_restantes = self.grid_velocidade 

        self.direcoes = [(self.velocidade, 0), (-self.velocidade, 0), (0, self.velocidade), (0, -self.velocidade)]

    def _desenhar_fantasma(self, cor_fallback):
        """
        Atualiza a sprite/cor. Ciano removido (Mantido como você solicitou).
        """
        self.image.fill(PRETO) 

        if self.eaten: 
            pass 
        else:
            if self.nome_vilao in IMAGENS_VILOES and IMAGENS_VILOES[self.nome_vilao]:
                self.image.blit(IMAGENS_VILOES[self.nome_vilao], (0, 0))
            else:
                cor_desenho = cor_fallback
                pygame.draw.circle(self.image, cor_desenho, (self.tamanho // 2, self.tamanho // 2), self.tamanho // 2)
                pygame.draw.rect(self.image, cor_desenho, [0, self.tamanho // 2, self.tamanho, self.tamanho // 2])


    def set_frightened(self, is_frightened):
        """Define o estado de vulnerabilidade."""
        if self.frightened and not is_frightened:
            if not self.eaten:
                 self.frightened = False
                 self._desenhar_fantasma(self.original_cor) 
        
        elif is_frightened:
            self.frightened = True
            self._desenhar_fantasma(self.original_cor) 


    def calcular_alvo(self, pacman_rect, pacman_dx, pacman_dy, fantasma_freeza, modo_jogo):
        
        px = (pacman_rect.x - X_INICIAL) // TAMANHO_BLOCO
        py = (pacman_rect.y - Y_INICIAL) // TAMANHO_BLOCO
        
        mapa_cols = len(MAPA_JOGO[0])
        mapa_rows = len(MAPA_JOGO)

        canto_cima_dir = (mapa_cols - 2, 1)  
        canto_baixo_dir = (mapa_cols - 2, mapa_rows - 2) 
        canto_cima_esq = (1, 1)
        canto_baixo_esq = (1, mapa_rows - 2)
        
        if self.nome_vilao == 'FREEZA':
            canto_scatter = canto_cima_dir
        elif self.nome_vilao == 'VEGETA':
            canto_scatter = canto_cima_esq
        elif self.nome_vilao == 'CELL':
            canto_scatter = canto_baixo_dir
        elif self.nome_vilao == 'MAJIN_BOO':
            canto_scatter = canto_baixo_esq

        # 1. Respawn
        if self.eaten:
            return (FANTASMA_SPAWN_X, FANTASMA_SPAWN_Y)

        # 2. Medo (Retorno ignorado, a lógica é aleatória no update)
        if self.frightened:
            return (0, 0) 

        # 3. SCATTER/CHASE
        if modo_jogo == "SCATTER":
             return canto_scatter
        
        elif modo_jogo == "CHASE":
            
            dir_x = pacman_dx // self.velocidade if pacman_dx != 0 else 0
            dir_y = pacman_dy // self.velocidade if pacman_dy != 0 else 0

            # Freeza
            if self.nome_vilao == 'FREEZA':
                return (px, py)
            
            # Vegeta
            elif self.nome_vilao == 'VEGETA':
                target_x = px + dir_x * 4
                target_y = py + dir_y * 4
                return (target_x, target_y)
            
            # Cell
            elif self.nome_vilao == 'CELL':
                if not fantasma_freeza: return canto_scatter
                
                fx = (fantasma_freeza.rect.x - X_INICIAL) // TAMANHO_BLOCO
                fy = (fantasma_freeza.rect.y - Y_INICIAL) // TAMANHO_BLOCO
                
                p1_x = px + dir_x * 2
                p1_y = py + dir_y * 2
                
                dx_fp1 = p1_x - fx
                dy_fp1 = p1_y - fy
                
                target_x = fx + 2 * dx_fp1
                target_y = fy + 2 * dy_fp1
                
                return (target_x, target_y)
            
            # Majin Boo
            elif self.nome_vilao == 'MAJIN_BOO':
                mx = (self.rect.x - X_INICIAL) // TAMANHO_BLOCO
                my = (self.rect.y - Y_INICIAL) // TAMANHO_BLOCO
                
                dist_x = px - mx
                dist_y = py - my
                distancia_bloco = math.sqrt(dist_x**2 + dist_y**2)
                
                if distancia_bloco < 8:
                    return canto_scatter 
                else:
                    return (px, py)
        
        return FANTASMA_SPAWN_X, FANTASMA_SPAWN_Y 

    def update(self, paredes, pacman=None, fantasma_freeza=None, modo_jogo="CHASE"):
        
        # 1. LÓGICA DE RESPAWN POR TIMER
        if self.eaten:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.eaten = False 
                self.frightened = False 
                self.respawn_timer = 0
                self._desenhar_fantasma(self.original_cor) 
            
        # 2. LÓGICA DE MOVIMENTO (BASEADA NO ESTADO)
        if self.passos_restantes <= 0:
            
            # A. MODO FRIGHTENED (FUGA ALEATÓRIA)
            if self.frightened and not self.eaten:
                
                direcoes_validas = []
                direcao_reversa = (-self.mudar_x, -self.mudar_y)
                
                for dx_teste, dy_teste in self.direcoes:
                    
                    if (dx_teste, dy_teste) == direcao_reversa and (self.mudar_x != 0 or self.mudar_y != 0):
                         continue 
                    
                    self.rect.x += dx_teste * self.grid_velocidade
                    self.rect.y += dy_teste * self.grid_velocidade
                    
                    if not pygame.sprite.spritecollideany(self, paredes):
                        direcoes_validas.append((dx_teste, dy_teste))
                    
                    self.rect.x -= dx_teste * self.grid_velocidade
                    self.rect.y -= dy_teste * self.grid_velocidade
                
                if direcoes_validas:
                    self.mudar_x, self.mudar_y = random.choice(direcoes_validas)
                else:
                    if self.mudar_x != 0 or self.mudar_y != 0:
                         self.mudar_x *= -1
                         self.mudar_y *= -1
                    
            # B. MODO CHASE/SCATTER/EATEN (BASEADO EM ALVO)
            else:
                
                if pacman:
                    alvo_x, alvo_y = self.calcular_alvo(pacman.rect, pacman.mudar_x, pacman.mudar_y, fantasma_freeza, modo_jogo)
                else:
                    alvo_x, alvo_y = FANTASMA_SPAWN_X, FANTASMA_SPAWN_Y
                
                melhor_caminho = None
                melhor_distancia = float('inf')
                direcao_reversa = (-self.mudar_x, -self.mudar_y)
                
                for dx_teste, dy_teste in self.direcoes:
                    
                    if (dx_teste, dy_teste) == direcao_reversa and not self.eaten and (self.mudar_x != 0 or self.mudar_y != 0):
                         continue 
                    
                    self.rect.x += dx_teste * self.grid_velocidade
                    self.rect.y += dy_teste * self.grid_velocidade
                    
                    if not pygame.sprite.spritecollideany(self, paredes):
                        
                        novo_bloco_x = (self.rect.x - X_INICIAL) // TAMANHO_BLOCO
                        novo_bloco_y = (self.rect.y - Y_INICIAL) // TAMANHO_BLOCO
                        
                        dist_quadrado = (alvo_x - novo_bloco_x)**2 + (alvo_y - novo_bloco_y)**2
                        
                        if dist_quadrado < melhor_distancia:
                            melhor_distancia = dist_quadrado
                            melhor_caminho = (dx_teste, dy_teste)
                    
                    self.rect.x -= dx_teste * self.grid_velocidade
                    self.rect.y -= dy_teste * self.grid_velocidade

                if melhor_caminho:
                    self.mudar_x, self.mudar_y = melhor_caminho
                else:
                    if self.mudar_x != 0 or self.mudar_y != 0:
                         self.mudar_x *= -1
                         self.mudar_y *= -1
            
            self.passos_restantes = self.grid_velocidade

        # 3. Aplica o movimento
        self.rect.x += self.mudar_x
        self.rect.y += self.mudar_y
        self.passos_restantes -= 1

        # Lógica de túnel (warp)
        limite_esquerdo = X_INICIAL
        limite_direito = X_INICIAL + (len(MAPA_JOGO[0]) * TAMANHO_BLOCO)

        if self.rect.left >= limite_direito:
            self.rect.right = limite_esquerdo + self.rect.width 
        elif self.rect.right <= limite_esquerdo:
            self.rect.left = limite_direito - self.rect.width 


# --- 3. FUNÇÃO PRINCIPAL DO JOGO ---

def main_jogo():
    
    tela = pygame.display.set_mode(TELA_TAMANHO)
    # Título do jogo de volta ao normal
    pygame.display.set_caption("DBZ Pac-Man: Goku vs Vilões!")
    relogio = pygame.time.Clock()
    
    carregar_sprites() 

    # --- VARIÁVEIS DE ESTADO ---
    jogo_ativo = True
    pontuacao = 0
    vidas = 3 
    power_mode_timer = 0 
    
    # CONTROLE DE MODO (CHASE/SCATTER)
    MODO_ATUAL = "SCATTER"
    MODO_TIMER = 0
    CICLOS_MODO = [7 * FPS, 20 * FPS, 7 * FPS, 20 * FPS, 5 * FPS, 20 * FPS, 5 * FPS, float('inf')]
    MODO_INDICE = 0
    MODO_MAX_TIME = CICLOS_MODO[MODO_INDICE]

    
    # --- INICIALIZAÇÃO DOS GRUPOS E ELEMENTOS ---
    todos_os_sprites = pygame.sprite.Group()
    lista_paredes = pygame.sprite.Group()
    lista_pontos = pygame.sprite.Group()
    lista_fantasmas = pygame.sprite.Group() 
    lista_power_pellets = pygame.sprite.Group() 
    
    # 1. Inicializa Pac-Man e Fantasmas
    pacman_tamanho = TAMANHO_BLOCO 
    pacman = PacMan(0, 0, pacman_tamanho) 

    # Instancia os Fantasmas
    fantasma1 = Fantasma(FANTASMA_SPAWN_X, FANTASMA_SPAWN_Y, 'FREEZA', VERMELHO) 
    fantasma2 = Fantasma(13, 8, 'CELL', CIANO) 
    fantasma3 = Fantasma(11, 8, 'MAJIN_BOO', LARANJA_VILAO) 
    fantasma4 = Fantasma(14, 8, 'VEGETA', ROSA)             
    
    fantasmas_fixos = [fantasma1, fantasma2, fantasma3, fantasma4]
    fantasma_freeza = fantasmas_fixos[0] 

    # Inicializa o Jogo (primeiro reset)
    status_jogo = resetar_jogo(pacman, todos_os_sprites, lista_paredes, lista_pontos, fantasmas_fixos, lista_power_pellets, lista_fantasmas)

    # --- LOOP PRINCIPAL DO JOGO ---
    
    while jogo_ativo:
        
        # A. TRATAMENTO DE EVENTOS (INPUTS DO USUÁRIO)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_ativo = False
                
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: jogo_ativo = False 
                    
                if status_jogo == "JOGANDO":
                    if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                        pacman.set_movimento(-pacman.velocidade, 0)
                    elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                        pacman.set_movimento(pacman.velocidade, 0)
                    elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                        pacman.set_movimento(0, -pacman.velocidade)
                    elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                        pacman.set_movimento(0, pacman.velocidade)


        # B. LÓGICA DO JOGO
        if status_jogo == "JOGANDO":
            
            # 1. Gerenciar o tempo do Power Mode
            if power_mode_timer > 0:
                power_mode_timer -= 1
                if power_mode_timer == 0:
                    for fantasma in fantasmas_fixos: 
                        fantasma.set_frightened(False) 

            # 2. Gerenciar a transição CHASE/SCATTER
            if power_mode_timer == 0 and MODO_INDICE < len(CICLOS_MODO):
                MODO_TIMER += 1
                if MODO_TIMER >= MODO_MAX_TIME:
                    MODO_INDICE += 1
                    if MODO_INDICE < len(CICLOS_MODO):
                        MODO_TIMER = 0
                        MODO_MAX_TIME = CICLOS_MODO[MODO_INDICE]
                        MODO_ATUAL = "SCATTER" if MODO_INDICE % 2 == 0 else "CHASE"
                        
            pacman.update(lista_paredes)
            
            for fantasma in fantasmas_fixos:
                fantasma.update(lista_paredes, pacman, fantasma_freeza, MODO_ATUAL)
            
            # Colisão com Pontos
            pontos_comidos = pygame.sprite.spritecollide(pacman, lista_pontos, True)
            if pontos_comidos: pontuacao += 10
                
            # Colisão com Power Pellets
            power_pellets_comidos = pygame.sprite.spritecollide(pacman, lista_power_pellets, True)
            if power_pellets_comidos:
                pontuacao += 50
                power_mode_timer = POWER_MODE_DURATION
                for fantasma in fantasmas_fixos: 
                    fantasma.set_frightened(True) 
                
            # 🏆 Verifica se Venceu
            if len(lista_pontos) == 0 and len(lista_power_pellets) == 0:
                status_jogo = "VENCEU"
                # Removendo o LOG de DEBUG, mas você pode recolocá-lo se precisar
                
            # Colisão com Fantasmas
            fantasmas_colididos = pygame.sprite.spritecollide(pacman, lista_fantasmas, False)

            if fantasmas_colididos:
                for fantasma_atingido in fantasmas_colididos:
                    
                    if fantasma_atingido.frightened and not fantasma_atingido.eaten: 
                        pontuacao += 200 
                        fantasma_atingido.eaten = True
                        fantasma_atingido.respawn_timer = RESPAWN_TIME_FRAMES
                        fantasma_atingido._desenhar_fantasma(fantasma_atingido.original_cor)
                        
                    elif not fantasma_atingido.frightened and not fantasma_atingido.eaten:
                        vidas -= 1
                        if vidas <= 0:
                            status_jogo = "PERDEU"
                        else:
                            status_jogo = "MORREU"
                        break 
                        
        elif status_jogo == "MORREU":
            pygame.time.wait(2000)
            power_mode_timer = 0
            
            MODO_INDICE = 0
            MODO_TIMER = 0
            MODO_ATUAL = "SCATTER"
            MODO_MAX_TIME = CICLOS_MODO[MODO_INDICE]
            
            status_jogo = resetar_jogo(pacman, todos_os_sprites, lista_paredes, lista_pontos, fantasmas_fixos, lista_power_pellets, lista_fantasmas)


        # C. DESENHO
        tela.fill(PRETO) 
        todos_os_sprites.draw(tela)
        
        # Desenhar timer de respawn
        for fantasma in fantasmas_fixos:
            if fantasma.eaten:
                tempo_restante_sec = math.ceil(fantasma.respawn_timer / FPS)
                timer_texto = f"{tempo_restante_sec}"
                x_centro = fantasma.rect.centerx
                y_centro = fantasma.rect.centery
                desenhar_texto(tela, timer_texto, FONTE_TIMER, VERDE_TIMER, x_centro, y_centro)


        # Desenhar TIMER PRINCIPAL e Pontuação/Vidas
        if power_mode_timer > 0:
            tempo_power_restante = math.ceil(power_mode_timer / FPS) 
            texto_timer = f"FÚRIA SUPER SAYAJIN: {tempo_power_restante}s"
            desenhar_texto(tela, texto_timer, FONTE_PONTUACAO, AMARELO, TELA_LARGURA // 2, 10 + FONTE_PONTUACAO.get_height() // 2)
        
        desenhar_texto(tela, f"PONTOS: {pontuacao} | VIDAS: {vidas}", FONTE_PONTUACAO, BRANCO, X_INICIAL + 10, 10, centralizado=False)
        
        if MODO_INDICE < len(CICLOS_MODO):
            desenhar_texto(tela, f"MODO: {MODO_ATUAL} (Ciclo {MODO_INDICE//2 + 1})", FONTE_INSTRUCAO, BRANCO, X_INICIAL + 10, TELA_ALTURA - 20, centralizado=False)
        else:
            desenhar_texto(tela, f"MODO: {MODO_ATUAL} (Infinito)", FONTE_INSTRUCAO, BRANCO, X_INICIAL + 10, TELA_ALTURA - 20, centralizado=False)


        # DESENHO DA MENSAGEM DE FIM DE JOGO
        if status_jogo == "VENCEU":
            desenhar_texto(tela, "VOCÊ VENCEU!", FONTE_MENSAGEM, AMARELO, TELA_LARGURA // 2, TELA_ALTURA // 2)
        elif status_jogo == "PERDEU":
            desenhar_texto(tela, "GAME OVER", FONTE_MENSAGEM, VERMELHO, TELA_LARGURA // 2, TELA_ALTURA // 2)
            
        # D. CONTROLE DE VELOCIDADE
        pygame.display.flip()
        relogio.tick(FPS)

if __name__ == '__main__':
    main_jogo()
    pygame.quit()
    sys.exit()