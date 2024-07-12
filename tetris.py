import pygame
import sys
import random

# Constants
FRAME_WIDTH = 700
FRAME_HEIGHT = 900
BLOCK_SIZE = 30
GAME_AREA_WIDTH = 500
GAME_AREA_HEIGHT = 900
INFO_AREA_WIDTH = FRAME_WIDTH - GAME_AREA_WIDTH

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Tetris")

# Screen and clock setup
game_display = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))
clock = pygame.time.Clock()

# Shapes and colors
SHAPES = [
    [[[0, 1], [1, 1], [2, 1], [3, 1]], [[2, 0], [2, 1], [2, 2], [2, 3]]],
    [[[1, 0], [1, 1], [1, 2], [2, 2]], [[0, 1], [1, 1], [2, 1], [0, 2]], [[1, 0], [2, 0], [2, 1], [2, 2]], [[2, 1], [0, 2], [1, 2], [2, 2]]],
    [[[1, 0], [2, 0], [0, 1], [1, 1]], [[0, 0], [0, 1], [1, 1], [1, 2]]],
    [[[1, 0], [0, 1], [1, 1], [2, 1]], [[1, 0], [1, 1], [2, 1], [1, 2]], [[0, 1], [1, 1], [2, 1], [1, 2]], [[1, 0], [0, 1], [1, 1], [1, 2]]],
    [[[1, 0], [2, 0], [1, 1], [2, 1]]]
]

COLORS = [
    pygame.Color(3, 65, 174),
    pygame.Color(114, 203, 59),
    pygame.Color(255, 213, 0),
    pygame.Color(255, 151, 28),
    pygame.Color(255, 50, 19)
]

# Shape class
class Shape:
    def __init__(self):
        self.shape_type = random.randint(0, len(SHAPES) - 1)
        self.rotation = 0
        self.shape = SHAPES[self.shape_type][self.rotation]
        self.color = COLORS[self.shape_type]
        self.position = [GAME_AREA_WIDTH // 2 // BLOCK_SIZE, 0]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(SHAPES[self.shape_type])
        self.shape = SHAPES[self.shape_type][self.rotation]

    def get_blocks(self):
        return [[self.position[0] + x, self.position[1] + y] for x, y in self.shape]

class Tetris:
    def __init__(self):
        self.field = [[0] * (GAME_AREA_WIDTH // BLOCK_SIZE) for _ in range(GAME_AREA_HEIGHT // BLOCK_SIZE)]
        self.current_shape = Shape()
        self.next_shape = Shape()
        self.score = 0
        self.high_score = 0
        self.game_over = False

    def check_collision(self, shape):
        for x, y in shape.get_blocks():
            if x < 0 or x >= GAME_AREA_WIDTH // BLOCK_SIZE or y >= GAME_AREA_HEIGHT // BLOCK_SIZE or self.field[y][x]:
                return True
        return False

    def lock_shape(self):
        for x, y in self.current_shape.get_blocks():
            self.field[y][x] = self.current_shape.color
        self.clear_lines()
        self.current_shape = self.next_shape
        self.next_shape = Shape()
        if self.check_collision(self.current_shape):
            self.game_over = True
            self.update_high_score()

    def clear_lines(self):
        new_field = [row for row in self.field if any(cell == 0 for cell in row)]
        lines_cleared = len(self.field) - len(new_field)
        self.score += lines_cleared * 100
        for _ in range(lines_cleared):
            new_field.insert(0, [0] * (GAME_AREA_WIDTH // BLOCK_SIZE))
        self.field = new_field

    def move_shape(self, dx, dy):
        self.current_shape.position[0] += dx
        self.current_shape.position[1] += dy
        if self.check_collision(self.current_shape):
            self.current_shape.position[0] -= dx
            self.current_shape.position[1] -= dy
            if dy:
                self.lock_shape()

    def rotate_shape(self):
        old_rotation = self.current_shape.rotation
        self.current_shape.rotate()
        if self.check_collision(self.current_shape):
            self.current_shape.rotation = old_rotation
            self.current_shape.shape = SHAPES[self.current_shape.shape_type][self.current_shape.rotation]

    def draw_field(self):
        game_display.fill(pygame.Color(0, 0, 0))
        for y, row in enumerate(self.field):
            for x, color in enumerate(row):
                if color:
                    pygame.draw.rect(game_display, color, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_shape(self):
        for x, y in self.current_shape.get_blocks():
            pygame.draw.rect(game_display, self.current_shape.color, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_next_shape(self):
        font = pygame.font.Font(None, 36)
        next_text = font.render("Next:", True, pygame.Color(255, 255, 255))
        game_display.blit(next_text, (GAME_AREA_WIDTH + 20, 200))
        for x, y in self.next_shape.get_blocks():
            pygame.draw.rect(game_display, self.next_shape.color, pygame.Rect((x + 10) * BLOCK_SIZE, (y + 10) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_grid(self):
        for i in range(GAME_AREA_HEIGHT // BLOCK_SIZE):
            pygame.draw.line(game_display, pygame.Color(20, 20, 20), (0, i * BLOCK_SIZE), (GAME_AREA_WIDTH, i * BLOCK_SIZE))
        for j in range(GAME_AREA_WIDTH // BLOCK_SIZE):
            pygame.draw.line(game_display, pygame.Color(20, 20, 20), (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, GAME_AREA_HEIGHT))

    def draw_info(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, pygame.Color(255, 255, 255))
        game_display.blit(score_text, (GAME_AREA_WIDTH + 20, 20))

        high_score_text = font.render(f"High Score: {self.high_score}", True, pygame.Color(255, 255, 255))
        game_display.blit(high_score_text, (GAME_AREA_WIDTH + 20, 60))

        if self.game_over:
            game_over_text = font.render("GAME OVER", True, pygame.Color(255, 0, 0))
            game_display.blit(game_over_text, (GAME_AREA_WIDTH + 20, 100))
            retry_text = font.render("Press R to Retry", True, pygame.Color(255, 255, 255))
            game_display.blit(retry_text, (GAME_AREA_WIDTH + 20, 140))
            home_text = font.render("Press Backspace for Home", True, pygame.Color(255, 255, 255))
            game_display.blit(home_text, (GAME_AREA_WIDTH + 20, 180))

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def update(self):
        if not self.game_over:
            self.move_shape(0, 1)
        self.draw_field()
        self.draw_shape()
        self.draw_next_shape()
        self.draw_grid()
        self.draw_info()
        pygame.display.update()

def quit_game():
    pygame.quit()
    sys.exit()

def draw_button(text, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_display, (170, 170, 170), (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(game_display, (100, 100, 100), (x, y, w, h))

    small_text = pygame.font.Font(None, 36)
    text_surf = small_text.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=((x + (w / 2)), (y + (h / 2))))
    game_display.blit(text_surf, text_rect)

def home_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        game_display.fill((0, 0, 0))

        font = pygame.font.Font(None, 72)
        title_text = font.render("TETRIS", True, (255, 255, 255))
        game_display.blit(title_text, (FRAME_WIDTH / 2 - title_text.get_width() / 2, 100))

        draw_button("Play", 250, 300, 200, 50, main_game)
        draw_button("High Score", 250, 400, 200, 50, display_high_score)
        draw_button("Quit", 250, 500, 200, 50, quit_game)

        pygame.display.update()
        clock.tick(15)

def display_high_score():
    viewing = True
    while viewing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    home_screen()

        game_display.fill((0, 0, 0))

        font = pygame.font.Font(None, 72)
        high_score_text = font.render(f"High Score: {tetris.high_score}", True, (255, 255, 255))
        game_display.blit(high_score_text, (FRAME_WIDTH / 2 - high_score_text.get_width() / 2, 300))

        pygame.display.update()
        clock.tick(15)

def main_game():
    global tetris
    tetris = Tetris()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    tetris.rotate_shape()
                elif event.key == pygame.K_LEFT:
                    tetris.move_shape(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    tetris.move_shape(1, 0)
                elif event.key == pygame.K_r and tetris.game_over:
                    tetris = Tetris()
                elif event.key == pygame.K_BACKSPACE:
                    home_screen()

        tetris.update()
        clock.tick(7)

if __name__ == "__main__":
    home_screen()