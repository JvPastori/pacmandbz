import pygame
from api_client import enviar_evento, obter_estado


pygame.init()


screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pacman Distribuído")

# Sprites (simplificados)
player = pygame.Rect(50, 50, 20, 20)
ghost = pygame.Rect(200, 200, 20, 20)
fruit = pygame.Rect(300, 300, 15, 15)

clock = pygame.time.Clock()

# Estado inicial
estado = obter_estado()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento do player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: player.y -= 3
    if keys[pygame.K_DOWN]: player.y += 3
    if keys[pygame.K_LEFT]: player.x -= 3
    if keys[pygame.K_RIGHT]: player.x += 3

    # Detecta colisões e envia eventos
    if player.colliderect(ghost):
        print("💀 Colidiu com fantasma!")
        estado = enviar_evento("collision_ghost")

    if player.colliderect(fruit):
        print("🍓 Comeu uma fruta!")
        estado = enviar_evento("eat_fruit")

    # Renderiza tudo
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 0), player)  # player
    pygame.draw.rect(screen, (255, 0, 0), ghost)     # fantasma
    pygame.draw.rect(screen, (0, 255, 0), fruit)     # fruta
    pygame.display.flip()

    clock.tick(30)
