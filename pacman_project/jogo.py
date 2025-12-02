import pygame
import sys
import random
import time
import math 
import copy 
import xmlrpc.client
import threading 

if not pygame.get_init(): pygame.init()
if not pygame.mixer.get_init(): pygame.mixer.init()
if not pygame.font.get_init(): pygame.font.init()

SERVER_URL = "http://localhost:8000"

def chamar_servidor_thread(func_nome, *args):
    # Executa a comunicação com o servidor em uma Thread separada
    def target():
        try:
            temp_proxy = xmlrpc.client.ServerProxy(SERVER_URL)
            getattr(temp_proxy, func_nome)(*args)
        except: pass 
    t = threading.Thread(target=target)
    t.daemon = True 
    t.start()

PRETO = (0, 0, 0); AMARELO = (255, 255, 0); BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0); CIANO = (0, 255, 255); ROSA = (255, 184, 255)
LARANJA_VILAO = (255, 184, 82); LARANJA_PELLET = (255, 180, 80)
BRANCO_MARMORE = (245, 245, 250); DOURADO_CUPULA = (218, 165, 32)
AZUL_CEU = (70, 130, 160); COR_FUNDO_JANELA = (30, 40, 30)

TAMANHO_BLOCO = 36; RAIO_PONTO = 5; RAIO_POWER_PONTO = 9 
MAPA_COLS = 26; MAPA_ROWS = 20
TELA_LARGURA = MAPA_COLS * TAMANHO_BLOCO; ALTURA_HUD = 40 
TELA_ALTURA = (MAPA_ROWS * TAMANHO_BLOCO) + ALTURA_HUD
TELA_TAMANHO = (TELA_LARGURA, TELA_ALTURA)
FPS = 60; POWER_MODE_DURATION = 8 * 60; RESPAWN_TIME_FRAMES = 5 * 60 

X_INICIAL = 0; Y_INICIAL = ALTURA_HUD 
FANTASMA_SPAWN_X = 12; FANTASMA_SPAWN_Y = 9 
PACMAN_SPAWN_X_GRID = 13; PACMAN_SPAWN_Y_GRID = 15  

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
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
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
MAPA_JOGO = []; CAMINHO_IMAGENS = 'client/assets/'; SPRITES = {} 

SOM_SOCO = None; SOM_SSJ = None; MUSICA_FUNDO = 'client/assets/fundo_jogaveldbz.mp3'

def carregar_sons():
    global SOM_SOCO, SOM_SSJ
    try:
        SOM_SOCO = pygame.mixer.Sound('client/assets/socodbz.mp3')
        SOM_SOCO.set_volume(0.4) 
    except: print("Erro ao carregar socodbz.mp3")
    try:
        #  Sound (efeito) para tocar junto com a música de fundo
        SOM_SSJ = pygame.mixer.Sound('client/assets/ssj.mp3')
        SOM_SSJ.set_volume(0.7) 
    except: print("Erro ao carregar ssj.mp3")

def tocar_musica_fundo():
    try:
        pygame.mixer.music.load(MUSICA_FUNDO)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        chamar_servidor_thread("log_evento", "🎵 AUDIO", "Música de fundo iniciada.")
    except: print(f"Erro ao tocar musica de fundo")

def carregar_sprites():
    global SPRITES
    config = {'GOKU': 'goku', 'GOKU_SSJ': 'ssj', 'FREEZA': 'freeza', 'CELL': 'cell', 'MAJIN_BOO': 'boo', 'VEGETA': 'vegeta'}
    for k, v in config.items():
        SPRITES[k] = {}
        try: SPRITES[k]['p'] = pygame.transform.scale(pygame.image.load(f"{CAMINHO_IMAGENS}{v}p.png").convert_alpha(), (TAMANHO_BLOCO, TAMANHO_BLOCO))
        except: SPRITES[k]['p'] = None
        try: SPRITES[k]['f'] = pygame.transform.scale(pygame.image.load(f"{CAMINHO_IMAGENS}{v}f.png").convert_alpha(), (TAMANHO_BLOCO, TAMANHO_BLOCO))
        except: SPRITES[k]['f'] = None
        
    SPRITES['ESFERAS'] = [] 
    TAMANHO_ESFERA = int(TAMANHO_BLOCO * 0.75) 
    for i in range(1, 5): 
        try:
            img_original = pygame.image.load(f"{CAMINHO_IMAGENS}esfera{i}.png").convert_alpha()
            img_pequena = pygame.transform.scale(img_original, (TAMANHO_ESFERA, TAMANHO_ESFERA))
            
            superficie_final = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
            x_centro = (TAMANHO_BLOCO - TAMANHO_ESFERA) // 2
            y_centro = (TAMANHO_BLOCO - TAMANHO_ESFERA) // 2
            superficie_final.blit(img_pequena, (x_centro, y_centro))
            
            SPRITES['ESFERAS'].append(superficie_final)
        except Exception as e: print(f"Erro esfera{i}: {e}"); SPRITES['ESFERAS'].append(None)

    try:
        TAMANHO_FEIJAO = int(TAMANHO_BLOCO * 0.35) 
        img_original = pygame.image.load(f"{CAMINHO_IMAGENS}feijao.png").convert_alpha()
        img_pequena = pygame.transform.scale(img_original, (TAMANHO_FEIJAO, TAMANHO_FEIJAO))
        
        superficie_final = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
        x_centro = (TAMANHO_BLOCO - TAMANHO_FEIJAO) // 2
        y_centro = (TAMANHO_BLOCO - TAMANHO_FEIJAO) // 2
        superficie_final.blit(img_pequena, (x_centro, y_centro))
        
        SPRITES['FEIJAO'] = superficie_final
    except Exception as e: print(f"Erro ao carregar feijao.png: {e}"); SPRITES['FEIJAO'] = None

try: FONTE_PONTUACAO = pygame.font.Font('client/assets/fonte.ttf', 36)
except: FONTE_PONTUACAO = pygame.font.Font(None, 36) 
try: FONTE_MENSAGEM = pygame.font.Font('client/assets/fonte.ttf', 70)
except: FONTE_MENSAGEM = pygame.font.Font(None, 70)
try: FONTE_PEQUENA = pygame.font.Font('client/assets/fonte.ttf', 20)
except: FONTE_PEQUENA = pygame.font.Font(None, 30)

class Parede(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(); self.image = pygame.Surface([TAMANHO_BLOCO, TAMANHO_BLOCO]); self.image.fill(BRANCO_MARMORE)
        pygame.draw.rect(self.image, DOURADO_CUPULA, (0, 0, TAMANHO_BLOCO, TAMANHO_BLOCO), 3)
        margem = 6; pygame.draw.rect(self.image, AZUL_CEU, (margem, margem, TAMANHO_BLOCO - margem*2, TAMANHO_BLOCO - margem*2), 1)
        pygame.draw.rect(self.image, BRANCO, (2, 2, 4, 4))
        self.rect = self.image.get_rect(); self.rect.x = X_INICIAL + x * TAMANHO_BLOCO; self.rect.y = Y_INICIAL + y * TAMANHO_BLOCO

class Ponto(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        if SPRITES.get('FEIJAO'): self.image = SPRITES['FEIJAO']
        else:
            self.image = pygame.Surface([TAMANHO_BLOCO, TAMANHO_BLOCO]); self.image.set_colorkey(PRETO)
            pygame.draw.circle(self.image, LARANJA_PELLET, (TAMANHO_BLOCO//2, TAMANHO_BLOCO//2), RAIO_PONTO) 
        self.rect = self.image.get_rect(); self.rect.x = X_INICIAL + x * TAMANHO_BLOCO; self.rect.y = Y_INICIAL + y * TAMANHO_BLOCO

class PontoPoder(pygame.sprite.Sprite):
    def __init__(self, x, y, imagem_esfera=None):
        super().__init__()
        if imagem_esfera: self.image = imagem_esfera
        else:
            self.image = pygame.Surface([TAMANHO_BLOCO, TAMANHO_BLOCO]); self.image.set_colorkey(PRETO)
            pygame.draw.circle(self.image, AMARELO, (TAMANHO_BLOCO//2, TAMANHO_BLOCO//2), RAIO_POWER_PONTO) 
        self.rect = self.image.get_rect(); self.rect.x = X_INICIAL + x * TAMANHO_BLOCO; self.rect.y = Y_INICIAL + y * TAMANHO_BLOCO

class PacMan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(); self.image = pygame.Surface([TAMANHO_BLOCO, TAMANHO_BLOCO]); self.image.fill(AMARELO)
        self.rect = self.image.get_rect(); self.rect.x = x; self.rect.y = y
        self.velocidade = 3; self.grid_passos = TAMANHO_BLOCO // self.velocidade; self.passos_restantes = 0
        self.mudar_x = 0; self.mudar_y = 0; self.proximo_mudar_x = 0; self.proximo_mudar_y = 0
        self.olhando_esquerda = False; self.transformado_ssj = False 

    def set_movimento(self, x, y):
        if x != 0 or y != 0: self.proximo_mudar_x = x; self.proximo_mudar_y = y
        
    def _pode_mudar(self, dx, dy, paredes):
        orig_x, orig_y = self.rect.x, self.rect.y
        self.rect.x += dx * TAMANHO_BLOCO; self.rect.y += dy * TAMANHO_BLOCO
        colisao = pygame.sprite.spritecollideany(self, paredes)
        self.rect.x, self.rect.y = orig_x, orig_y
        return not colisao
    
    def _atualizar_sprite(self):
        movendo = (self.mudar_x != 0 or self.mudar_y != 0); estado = 'f' if movendo else 'p'
        chave_sprite = 'GOKU_SSJ' if self.transformado_ssj else 'GOKU'
        img = SPRITES.get(chave_sprite, {}).get(estado) or SPRITES.get('GOKU', {}).get(estado)
        if img:
            if self.mudar_x < 0: self.olhando_esquerda = True
            elif self.mudar_x > 0: self.olhando_esquerda = False
            self.image = pygame.transform.flip(img, True, False) if self.olhando_esquerda else img.copy()
        else: self.image.fill(AMARELO)

    def update(self, paredes):
        if self.passos_restantes == 0:
            if self.proximo_mudar_x != 0 or self.proximo_mudar_y != 0:
                if self.proximo_mudar_x != 0: self.proximo_mudar_x = self.velocidade if self.proximo_mudar_x > 0 else -self.velocidade
                if self.proximo_mudar_y != 0: self.proximo_mudar_y = self.velocidade if self.proximo_mudar_y > 0 else -self.velocidade
                dx = self.proximo_mudar_x // self.velocidade; dy = self.proximo_mudar_y // self.velocidade
                if self._pode_mudar(dx, dy, paredes):
                    self.mudar_x, self.mudar_y = self.proximo_mudar_x, self.proximo_mudar_y
                    self.passos_restantes = self.grid_passos
                    self.proximo_mudar_x = 0; self.proximo_mudar_y = 0
                         
            if self.mudar_x != 0 or self.mudar_y != 0:
                dx = self.mudar_x // self.velocidade; dy = self.mudar_y // self.velocidade
                if self._pode_mudar(dx, dy, paredes): self.passos_restantes = self.grid_passos
                else: self.mudar_x = 0; self.mudar_y = 0

        if self.passos_restantes > 0:
            self.rect.x += self.mudar_x; self.rect.y += self.mudar_y; self.passos_restantes -= 1
        lim_esq = X_INICIAL; lim_dir = X_INICIAL + (len(MAPA_JOGO[0]) * TAMANHO_BLOCO)
        if self.rect.left >= lim_dir: self.rect.right = lim_esq + self.rect.width 
        elif self.rect.right <= lim_esq: self.rect.left = lim_dir - self.rect.width 
        self._atualizar_sprite()

class Fantasma(pygame.sprite.Sprite):
    def __init__(self, x_bloco, y_bloco, nome, cor_fallback):
        super().__init__()
        self.nome_vilao = nome; self.original_cor = cor_fallback; self.velocidade = 2; self.grid_velocidade = TAMANHO_BLOCO // self.velocidade
        self.frightened = False; self.eaten = False; self.respawn_timer = 0 
        self.image = pygame.Surface([TAMANHO_BLOCO, TAMANHO_BLOCO]).convert_alpha()
        self.rect = self.image.get_rect(); self.rect.x = X_INICIAL + x_bloco * TAMANHO_BLOCO; self.rect.y = Y_INICIAL + y_bloco * TAMANHO_BLOCO
        self.mudar_x = self.velocidade; self.mudar_y = 0; self.passos_restantes = self.grid_velocidade 
        self.direcoes = [(self.velocidade, 0), (-self.velocidade, 0), (0, self.velocidade), (0, -self.velocidade)]
        self.olhando_esquerda = False; self._atualizar_sprite()

    def _atualizar_sprite(self):
        self.image.fill((0,0,0,0)); movendo = (self.mudar_x != 0 or self.mudar_y != 0); estado = 'f' if movendo else 'p'
        img_base = SPRITES.get(self.nome_vilao, {}).get(estado)
        
        # invertendo o freeza
        virar_imagem = self.olhando_esquerda
        if self.nome_vilao == 'FREEZA': virar_imagem = not virar_imagem

        if img_base:
            if virar_imagem: img_final = pygame.transform.flip(img_base, True, False)
            else: img_final = img_base
            self.image.blit(img_final, (0, 0))
        else: pygame.draw.circle(self.image, self.original_cor, (TAMANHO_BLOCO//2, TAMANHO_BLOCO//2), TAMANHO_BLOCO//2)

        if self.eaten: self.image.set_alpha(80) 
        elif self.frightened: self.image.set_alpha(180) 
        else: self.image.set_alpha(255)

    def set_frightened(self, is_frightened):
        if self.frightened != is_frightened and not self.eaten: self.frightened = is_frightened; self._atualizar_sprite()

    def update(self, paredes, pacman=None, freeza_ref=None):
        if self.eaten:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0: self.eaten = False; self.frightened = False; self.respawn_timer = 0
            self._atualizar_sprite()
            if self.eaten: return

        if self.passos_restantes <= 0:
            dirs_validas = []; dir_reversa = (-self.mudar_x, -self.mudar_y); alvo_x, alvo_y = 0, 0
            
            # IA de cada vilão
            if pacman and not self.frightened:
                if self.nome_vilao == 'FREEZA': alvo_x, alvo_y = pacman.rect.x, pacman.rect.y # Segue o Goku diretamente
                
                elif self.nome_vilao == 'VEGETA': # Tenta interceptar o Goku 4 blocos à frente
                    dx = 1 if pacman.mudar_x > 0 else (-1 if pacman.mudar_x < 0 else 0); dy = 1 if pacman.mudar_y > 0 else (-1 if pacman.mudar_y < 0 else 0)
                    alvo_x = pacman.rect.x + (dx * 4 * TAMANHO_BLOCO); alvo_y = pacman.rect.y + (dy * 4 * TAMANHO_BLOCO)
                    
                elif self.nome_vilao == 'CELL' and freeza_ref: # Vetor complexo baseado no Freeza e no Goku
                    dx = 1 if pacman.mudar_x > 0 else (-1 if pacman.mudar_x < 0 else 0); dy = 1 if pacman.mudar_y > 0 else (-1 if pacman.mudar_y < 0 else 0)
                    px = pacman.rect.x + (dx * 2 * TAMANHO_BLOCO); py = pacman.rect.y + (dy * 2 * TAMANHO_BLOCO)
                    vx = px - freeza_ref.rect.x; vy = py - freeza_ref.rect.y; alvo_x = px + vx; alvo_y = py + vy
                    
                else: # Boo (Aleatório/Híbrido)
                    d = math.hypot(pacman.rect.centerx - self.rect.centerx, pacman.rect.centery - self.rect.centery)
                    if (d/TAMANHO_BLOCO) > 8: alvo_x, alvo_y = pacman.rect.x, pacman.rect.y
                    else: alvo_x, alvo_y = 0, TELA_ALTURA 
            else: alvo_x, alvo_y = random.randint(0, TELA_LARGURA), random.randint(0, TELA_ALTURA)

            melhor_dist = float('inf'); melhor_dir = None
            for dx, dy in self.direcoes:
                if (dx, dy) == dir_reversa and (self.mudar_x != 0 or self.mudar_y != 0): continue
                self.rect.x += dx * self.grid_velocidade; self.rect.y += dy * self.grid_velocidade
                if not pygame.sprite.spritecollideany(self, paredes):
                    d = (alvo_x - self.rect.x)**2 + (alvo_y - self.rect.y)**2
                    if d < melhor_dist: melhor_dist = d; melhor_dir = (dx, dy)
                    dirs_validas.append((dx, dy))
                self.rect.x -= dx * self.grid_velocidade; self.rect.y -= dy * self.grid_velocidade
            
            if self.frightened and dirs_validas: self.mudar_x, self.mudar_y = random.choice(dirs_validas)
            elif melhor_dir: self.mudar_x, self.mudar_y = melhor_dir
            elif dirs_validas: self.mudar_x, self.mudar_y = random.choice(dirs_validas)
            else: self.mudar_x *= -1; self.mudar_y *= -1
            self.passos_restantes = self.grid_velocidade
            
            if self.mudar_x < 0: self.olhando_esquerda = True
            elif self.mudar_x > 0: self.olhando_esquerda = False

        self.rect.x += self.mudar_x; self.rect.y += self.mudar_y; self.passos_restantes -= 1
        lim_esq = X_INICIAL; lim_dir = X_INICIAL + (len(MAPA_JOGO[0]) * TAMANHO_BLOCO)
        if self.rect.left >= lim_dir: self.rect.right = lim_esq + self.rect.width 
        elif self.rect.right <= lim_esq: self.rect.left = lim_dir - self.rect.width 
        self._atualizar_sprite()

def configurar_labirinto(mapa, todos, paredes, pontos, powers):
    contador_esferas = 0 
    for r, linha in enumerate(mapa):
        for c, bloco in enumerate(linha):
            if bloco == 1: p = Parede(c, r); paredes.add(p); todos.add(p)
            elif bloco == 0: p = Ponto(c, r); pontos.add(p); todos.add(p)
            elif bloco == 2: 
                # Alterna entre as 4 esferas disponíveis
                img_esfera = None
                if SPRITES.get('ESFERAS'): img_esfera = SPRITES['ESFERAS'][contador_esferas % 4]
                p = PontoPoder(c, r, img_esfera); powers.add(p); todos.add(p)
                contador_esferas += 1

def resetar_jogo_local(pacman, todos, paredes, pontos, fantasmas, powers, g_fantasmas):
    global MAPA_JOGO
    paredes.empty(); pontos.empty(); powers.empty(); g_fantasmas.empty(); todos.empty()
    MAPA_JOGO = copy.deepcopy(MAPA_JOGO_BASE)
    configurar_labirinto(MAPA_JOGO, todos, paredes, pontos, powers)
    pacman.rect.x = X_INICIAL + PACMAN_SPAWN_X_GRID * TAMANHO_BLOCO
    pacman.rect.y = Y_INICIAL + PACMAN_SPAWN_Y_GRID * TAMANHO_BLOCO
    pacman.mudar_x, pacman.mudar_y, pacman.proximo_mudar_x, pacman.proximo_mudar_y = 0, 0, 0, 0
    pacman.passos_restantes = 0; pacman.transformado_ssj = False 
    todos.add(pacman) 
    spawns = [(12, 7), (12, 9), (13, 9), (11, 9)]
    for i, f in enumerate(fantasmas):
        c, r = spawns[i]; f.rect.x = X_INICIAL + c * TAMANHO_BLOCO; f.rect.y = Y_INICIAL + r * TAMANHO_BLOCO
        f.mudar_x, f.mudar_y = f.velocidade, 0; f.passos_restantes = f.grid_velocidade
        f.set_frightened(False); f.eaten = False; f.respawn_timer = 0 
        todos.add(f); g_fantasmas.add(f)
    return "JOGANDO"

def main_jogo():
    tela = pygame.display.set_mode(TELA_TAMANHO); pygame.display.set_caption("DBZ Pac-Man: Versão Final")
    relogio = pygame.time.Clock()
    carregar_sprites(); carregar_sons()
    chamar_servidor_thread("resetar_jogo") 
    tocar_musica_fundo()

    jogo_ativo = True; power_mode_timer = 0 
    pontuacao_local = 0; vidas_local = 3; frame_count = 0 
    final_time_str = "00:00"
    
    todos = pygame.sprite.Group(); paredes = pygame.sprite.Group()
    pontos = pygame.sprite.Group(); g_fantasmas = pygame.sprite.Group(); powers = pygame.sprite.Group() 
    pacman = PacMan(0, 0) 
    fantasmas_fixos = [Fantasma(0,0, 'FREEZA', VERMELHO), Fantasma(0,0, 'CELL', CIANO), Fantasma(0,0, 'MAJIN_BOO', LARANJA_VILAO), Fantasma(0,0, 'VEGETA', ROSA)]
    status_jogo = resetar_jogo_local(pacman, todos, paredes, pontos, fantasmas_fixos, powers, g_fantasmas)

    while jogo_ativo:
        if status_jogo == "JOGANDO": frame_count += 1
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: jogo_ativo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: jogo_ativo = False 
                if status_jogo == "JOGANDO":
                    if evento.key in [pygame.K_LEFT, pygame.K_a]: pacman.set_movimento(-pacman.velocidade, 0)
                    elif evento.key in [pygame.K_RIGHT, pygame.K_d]: pacman.set_movimento(pacman.velocidade, 0)
                    elif evento.key in [pygame.K_UP, pygame.K_w]: pacman.set_movimento(0, -pacman.velocidade)
                    elif evento.key in [pygame.K_DOWN, pygame.K_s]: pacman.set_movimento(0, pacman.velocidade)

        if status_jogo == "JOGANDO":
            if power_mode_timer > 0: power_mode_timer -= 1
            else: 
                pacman.transformado_ssj = False
                for f in fantasmas_fixos: f.set_frightened(False)

            pacman.update(paredes)
            for f in fantasmas_fixos: f.update(paredes, pacman, freeza_ref=fantasmas_fixos[0])
            
            colisoes_fantasmas = pygame.sprite.spritecollide(pacman, g_fantasmas, False)
            for f in g_fantasmas:
                distancia = math.hypot(pacman.rect.centerx - f.rect.centerx, pacman.rect.centery - f.rect.centery)
                if distancia < TAMANHO_BLOCO * 0.7: 
                    if f not in colisoes_fantasmas: colisoes_fantasmas.append(f)

            if pygame.sprite.spritecollide(pacman, pontos, True):
                pontuacao_local += 10; chamar_servidor_thread("processar_colisao_item", "PONTO")
            
            if pygame.sprite.spritecollide(pacman, powers, True):
                pontuacao_local += 50; power_mode_timer = POWER_MODE_DURATION
                pacman.transformado_ssj = True
                
                if SOM_SSJ: SOM_SSJ.play()
                chamar_servidor_thread("log_evento", "AUDIO", "Som Transformacao SSJ tocando")
                chamar_servidor_thread("log_evento", "POWERUP", "Goku se transformou em Super Sayajin!")
                chamar_servidor_thread("log_evento", "ITEM", "Goku pegou uma Esfera do Dragão!")
                
                for f in fantasmas_fixos: f.set_frightened(True)
                chamar_servidor_thread("processar_colisao_item", "POWER")

            if colisoes_fantasmas:
                for f in colisoes_fantasmas:
                    if f.frightened and not f.eaten:
                        f.eaten = True; f.respawn_timer = RESPAWN_TIME_FRAMES; f._atualizar_sprite()
                        pontuacao_local += 200
                        if SOM_SOCO: SOM_SOCO.play()
                        
                        chamar_servidor_thread("log_evento", "COMBATE", f"Goku (SSJ) eliminou {f.nome_vilao}!")
                        chamar_servidor_thread("log_evento", "AUDIO", "Som de Soco tocando")
                        
                        spawn_col = random.randint(11, 14); spawn_row = random.randint(8, 9) 
                        f.rect.x = X_INICIAL + spawn_col * TAMANHO_BLOCO; f.rect.y = Y_INICIAL + spawn_row * TAMANHO_BLOCO
                        f.mudar_x, f.mudar_y = 0, 0; f.passos_restantes = 0
                    elif not f.frightened and not f.eaten:
                        vidas_local -= 1
                        chamar_servidor_thread("log_evento", "COMBATE", f"Goku colidiu com {f.nome_vilao} e perdeu uma vida.")
                        if vidas_local <= 0:
                            status_jogo = "PERDEU"; seg = frame_count // 60; final_time_str = f"{seg // 60:02d}:{seg % 60:02d}"
                            pygame.mixer.music.stop() 
                            chamar_servidor_thread("log_evento", "FIM DE JOGO", f"Pontuacao final: {pontuacao_local}")
                        else: status_jogo = "MORREU"
                        chamar_servidor_thread("processar_colisao_vilao")

            if frame_count % 60 == 0:
                def sync():
                    try: svr = xmlrpc.client.ServerProxy(SERVER_URL); st = svr.get_estado()
                    except: pass
                threading.Thread(target=sync, daemon=True).start()

        elif status_jogo == "MORREU":
            pygame.time.wait(1000) 
            status_jogo = resetar_jogo_local(pacman, todos, paredes, pontos, fantasmas_fixos, powers, g_fantasmas)
            if not pygame.mixer.music.get_busy(): tocar_musica_fundo()

        tela.fill(PRETO); todos.draw(tela)
        pygame.draw.rect(tela, PRETO, (0, 0, TELA_LARGURA, ALTURA_HUD))
        pygame.draw.line(tela, DOURADO_CUPULA, (0, ALTURA_HUD-2), (TELA_LARGURA, ALTURA_HUD-2), 2)
        
        placar = FONTE_PONTUACAO.render(f"KI: {pontuacao_local} | VIDAS: {vidas_local}", True, BRANCO)
        tela.blit(placar, (20, 10))
        if power_mode_timer > 0:
            aviso = FONTE_PONTUACAO.render(f"SUPER SAYAJIN: {power_mode_timer//60}", True, AMARELO)
            tela.blit(aviso, (TELA_LARGURA//2, 10))
        
        if status_jogo == "PERDEU":
            overlay = pygame.Surface(TELA_TAMANHO); overlay.set_alpha(200); overlay.fill(PRETO); tela.blit(overlay, (0, 0))
            w_j, h_j = 600, 400; x_j, y_j = (TELA_LARGURA - w_j) // 2, (TELA_ALTURA - h_j) // 2
            pygame.draw.rect(tela, COR_FUNDO_JANELA, (x_j, y_j, w_j, h_j), 0, border_radius=20)
            pygame.draw.rect(tela, DOURADO_CUPULA, (x_j, y_j, w_j, h_j), 4, border_radius=20)
            t_fim = FONTE_MENSAGEM.render("GAME OVER", True, VERMELHO)
            t_pts = FONTE_PONTUACAO.render(f"PONTUACAO FINAL: {pontuacao_local}", True, BRANCO)
            t_tmp = FONTE_PONTUACAO.render(f"TEMPO DE JOGO: {final_time_str}", True, BRANCO)
            t_sair = FONTE_PEQUENA.render("Pressione ESC para Sair", True, (200, 200, 200))
            tela.blit(t_fim, (x_j + (w_j - t_fim.get_width())//2, y_j + 50))
            tela.blit(t_pts, (x_j + (w_j - t_pts.get_width())//2, y_j + 160))
            tela.blit(t_tmp, (x_j + (w_j - t_tmp.get_width())//2, y_j + 220))
            tela.blit(t_sair, (x_j + (w_j - t_sair.get_width())//2, y_j + h_j - 50))

        pygame.display.flip(); relogio.tick(FPS)

if __name__ == '__main__':
    main_jogo()