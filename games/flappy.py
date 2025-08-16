import random
import sys
import pygame

WIDTH, HEIGHT = 400, 600
BIRD_COLOR = (255, 255, 0)
PIPE_COLOR = (0, 255, 0)
BACKGROUND = (0, 0, 0)


def run():
    """Run a minimal Flappy Bird clone controllable via keyboard or joystick."""
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    # Initialise joysticks
    pygame.joystick.init()
    for i in range(pygame.joystick.get_count()):
        pygame.joystick.Joystick(i).init()

    bird = pygame.Rect(50, HEIGHT // 2, 30, 30)
    velocity = 0
    gravity = 0.5
    jump = -8

    pipes = []
    pipe_gap = 150
    pipe_speed = 3
    spawn_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                velocity = jump
            elif event.type == pygame.JOYBUTTONDOWN:
                velocity = jump

        spawn_timer += 1
        if spawn_timer > 90:
            spawn_timer = 0
            center = random.randrange(100, HEIGHT - 100)
            top = pygame.Rect(WIDTH, 0, 50, center - pipe_gap // 2)
            bottom = pygame.Rect(WIDTH, center + pipe_gap // 2, 50, HEIGHT - (center + pipe_gap // 2))
            pipes.append((top, bottom))

        velocity += gravity
        bird.y += int(velocity)

        for top, bottom in pipes:
            top.x -= pipe_speed
            bottom.x -= pipe_speed
        pipes = [p for p in pipes if p[0].right > 0]

        for top, bottom in pipes:
            if bird.colliderect(top) or bird.colliderect(bottom):
                running = False
        if bird.top < 0 or bird.bottom > HEIGHT:
            running = False

        screen.fill(BACKGROUND)
        pygame.draw.rect(screen, BIRD_COLOR, bird)
        for top, bottom in pipes:
            pygame.draw.rect(screen, PIPE_COLOR, top)
            pygame.draw.rect(screen, PIPE_COLOR, bottom)
        pygame.display.flip()

        clock.tick(60)

    game_over(screen, clock)


def game_over(screen, clock):
    """Display a game over screen waiting for user input."""
    font = pygame.font.SysFont(None, 48)
    msg = font.render("Game Over - Press Enter or Button", True, (255, 255, 255))
    rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    waiting = False
            elif event.type == pygame.JOYBUTTONDOWN:
                waiting = False

        screen.fill((0, 0, 0))
        screen.blit(msg, rect)
        pygame.display.flip()
        clock.tick(15)

