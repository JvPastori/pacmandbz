
import pygame
import requests

pygame.init()

# Configurações básicas
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Sprites (simplificados)
player = pygame.Rect(50, 50, 20, 20)
ghost = pygame.Rect(200, 200, 20, 20)
fruit = pygame.Rect(300, 300, 15, 15)

API_URL = "http://127.0.0.1:8000/event"

def send_event(event_type, details=None):
    """Envia um evento de colisão para o servidor"""
    data = {"type": event_type, "details": details or {}}
    response = requests.post(API_URL, json=data)
    print(response.json())

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: player.y -= 3
    if keys[pygame.K_DOWN]: player.y += 3
    if keys[pygame.K_LEFT]: player.x -= 3
    if keys[pygame.K_RIGHT]: player.x += 3

    # 🧠 Detectar colisões locais
    if player.colliderect(ghost):
        print("Colidiu com o fantasma!")
        send_event("collision_ghost")

    if player.colliderect(fruit):
        print("Comeu uma fruta!")
        send_event("eat_fruit")

    # Renderização
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 0), player)  # Player (amarelo)
    pygame.draw.rect(screen, (255, 0, 0), ghost)     # Fantasma (vermelho)
    pygame.draw.rect(screen, (0, 255, 0), fruit)     # Fruta (verde)
    pygame.display.flip()

    clock.tick(30)
