import random
import sys
import pygame

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
BACKGROUND = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)


# Mapping of opposite directions to avoid reversal
OPPOSITES = {
    (1, 0): (-1, 0),
    (-1, 0): (1, 0),
    (0, 1): (0, -1),
    (0, -1): (0, 1),
}


def run():
    """Run a simple snake game controlled by keyboard or joystick."""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    # Initialise joysticks
    pygame.joystick.init()
    joysticks = []
    for i in range(pygame.joystick.get_count()):
        js = pygame.joystick.Joystick(i)
        js.init()
        joysticks.append(js)

    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    food = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))

    alive = True
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    new_dir = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    new_dir = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    new_dir = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    new_dir = (1, 0)
                else:
                    new_dir = direction
                if new_dir != OPPOSITES.get(direction):
                    direction = new_dir
            elif event.type == pygame.JOYHATMOTION:
                x, y = event.value
                if x == 1:
                    new_dir = (1, 0)
                elif x == -1:
                    new_dir = (-1, 0)
                elif y == 1:
                    new_dir = (0, 1)
                elif y == -1:
                    new_dir = (0, -1)
                else:
                    new_dir = direction
                if new_dir != OPPOSITES.get(direction):
                    direction = new_dir
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value > 0.5:
                        new_dir = (1, 0)
                    elif event.value < -0.5:
                        new_dir = (-1, 0)
                    else:
                        new_dir = direction
                elif event.axis == 1:
                    if event.value > 0.5:
                        new_dir = (0, 1)
                    elif event.value < -0.5:
                        new_dir = (0, -1)
                    else:
                        new_dir = direction
                else:
                    new_dir = direction
                if new_dir != OPPOSITES.get(direction):
                    direction = new_dir

        # Move snake
        head_x, head_y = snake[0]
        new_head = ((head_x + direction[0]) % GRID_WIDTH,
                    (head_y + direction[1]) % GRID_HEIGHT)

        if new_head in snake:
            alive = False
            break
        snake.insert(0, new_head)

        if new_head == food:
            while food in snake:
                food = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        else:
            snake.pop()

        # Draw
        screen.fill(BACKGROUND)
        for x, y in snake:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
        fx, fy = food
        food_rect = pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, FOOD_COLOR, food_rect)
        pygame.display.flip()

        clock.tick(10)

    game_over(screen, clock)


def game_over(screen, clock):
    """Display a game over screen waiting for user input."""
    font = pygame.font.SysFont(None, 48)
    msg = font.render("Game Over - Press Enter or Button", True, (255, 255, 255))
    rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

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

