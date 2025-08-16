import sys
import pygame

from games.snake import run as run_snake

WIDTH, HEIGHT = 640, 480
MENU_BG = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 255, 0)


def init_joysticks():
    """Initialise all connected joysticks."""
    pygame.joystick.init()
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
    return joysticks


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Hub")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    games = [("Snake", run_snake)]
    selected = 0

    joysticks = init_joysticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(games)
                elif event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(games)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    games[selected][1]()
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    joysticks = init_joysticks()
            elif event.type == pygame.JOYHATMOTION:
                if event.value[1] == -1:
                    selected = (selected + 1) % len(games)
                elif event.value[1] == 1:
                    selected = (selected - 1) % len(games)
            elif event.type == pygame.JOYBUTTONDOWN:
                games[selected][1]()
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
                joysticks = init_joysticks()

        screen.fill(MENU_BG)
        for idx, (name, _) in enumerate(games):
            color = HIGHLIGHT_COLOR if idx == selected else TEXT_COLOR
            text = font.render(name, True, color)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + idx * 60))
            screen.blit(text, rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
