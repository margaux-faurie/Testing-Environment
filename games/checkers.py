import sys
import pygame

WIDTH = HEIGHT = 480
ROWS = COLS = 8
SQUARE_SIZE = WIDTH // COLS

LIGHT = (222, 184, 135)
DARK = (139, 69, 19)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
HIGHLIGHT = (0, 255, 0)


def create_board():
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    for y in range(3):
        for x in range(COLS):
            if (x + y) % 2 == 1:
                board[y][x] = ["black", False]
    for y in range(ROWS - 3, ROWS):
        for x in range(COLS):
            if (x + y) % 2 == 1:
                board[y][x] = ["red", False]
    return board


def valid_moves(board, x, y):
    color, king = board[y][x]
    moves = {}
    directions = [(-1, -1), (1, -1)] if color == "red" else [(-1, 1), (1, 1)]
    if king:
        directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS:
            if board[ny][nx] is None:
                moves[(nx, ny)] = None
            elif board[ny][nx][0] != color:
                jx, jy = nx + dx, ny + dy
                if 0 <= jx < COLS and 0 <= jy < ROWS and board[jy][jx] is None:
                    moves[(jx, jy)] = (nx, ny)
    return moves


def has_pieces(board, color):
    for row in board:
        for piece in row:
            if piece and piece[0] == color:
                return True
    return False


def run():
    """Simple two-player checkers controllable via keyboard or joystick."""
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers")
    clock = pygame.time.Clock()

    pygame.joystick.init()
    for i in range(pygame.joystick.get_count()):
        pygame.joystick.Joystick(i).init()

    board = create_board()
    cursor = [0, 0]
    selected = None
    turn = "red"
    winner = ""

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    cursor[0] = max(0, cursor[0] - 1)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    cursor[0] = min(COLS - 1, cursor[0] + 1)
                elif event.key in (pygame.K_UP, pygame.K_w):
                    cursor[1] = max(0, cursor[1] - 1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    cursor[1] = min(ROWS - 1, cursor[1] + 1)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    selected, turn = handle_move(board, cursor, selected, turn)
            elif event.type == pygame.JOYHATMOTION:
                dx, dy = event.value
                if dx == -1:
                    cursor[0] = max(0, cursor[0] - 1)
                elif dx == 1:
                    cursor[0] = min(COLS - 1, cursor[0] + 1)
                if dy == -1:
                    cursor[1] = max(0, cursor[1] - 1)
                elif dy == 1:
                    cursor[1] = min(ROWS - 1, cursor[1] + 1)
            elif event.type == pygame.JOYBUTTONDOWN:
                selected, turn = handle_move(board, cursor, selected, turn)

        # Drawing
        for y in range(ROWS):
            for x in range(COLS):
                rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                color = LIGHT if (x + y) % 2 == 0 else DARK
                pygame.draw.rect(screen, color, rect)

                piece = board[y][x]
                if piece:
                    pcolor = RED if piece[0] == "red" else BLACK
                    pygame.draw.circle(screen, pcolor, rect.center, SQUARE_SIZE // 2 - 5)
                    if piece[1]:
                        pygame.draw.circle(screen, HIGHLIGHT, rect.center, SQUARE_SIZE // 2 - 20, 2)

        # highlight cursor
        cursor_rect = pygame.Rect(cursor[0] * SQUARE_SIZE, cursor[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, HIGHLIGHT, cursor_rect, 3)

        # highlight selected piece moves
        if selected:
            moves = valid_moves(board, selected[0], selected[1])
            for (mx, my) in moves:
                move_rect = pygame.Rect(mx * SQUARE_SIZE, my * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, HIGHLIGHT, move_rect, 3)

        # show turn
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"Turn: {turn.title()}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

        # check win
        if not has_pieces(board, "red"):
            running = False
            winner = "Black"
        elif not has_pieces(board, "black"):
            running = False
            winner = "Red"

    game_over(screen, clock, winner)


def handle_move(board, cursor, selected, turn):
    x, y = cursor
    if selected is None and board[y][x] and board[y][x][0] == turn:
        selected = (x, y)
    elif selected:
        moves = valid_moves(board, selected[0], selected[1])
        if (x, y) in moves:
            sx, sy = selected
            board[y][x] = board[sy][sx]
            board[sy][sx] = None
            if moves[(x, y)]:
                jx, jy = moves[(x, y)]
                board[jy][jx] = None
            if (turn == "red" and y == 0) or (turn == "black" and y == ROWS - 1):
                board[y][x][1] = True
            selected = None
            turn = "black" if turn == "red" else "red"
    return selected, turn


def game_over(screen, clock, winner):
    font_size = 48
    font = pygame.font.SysFont(None, font_size)
    msg = font.render(f"{winner} Wins - Press Enter or Button", True, (255, 255, 255))
    while msg.get_width() > WIDTH - 20 and font_size > 10:
        font_size -= 2
        font = pygame.font.SysFont(None, font_size)
        msg = font.render(f"{winner} Wins - Press Enter or Button", True, (255, 255, 255))
    rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                waiting = False
            elif event.type == pygame.JOYBUTTONDOWN:
                waiting = False

        screen.fill((0, 0, 0))
        screen.blit(msg, rect)
        pygame.display.flip()
        clock.tick(15)

