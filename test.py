import pygame
import random
import sys
from enum import Enum
from typing import List, Tuple

# Инициализация PyGame
pygame.init()

# Константы игры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Цвета фигур
COLORS = [
    CYAN,     # I
    BLUE,     # J
    ORANGE,   # L
    YELLOW,   # O
    GREEN,    # S
    MAGENTA,  # T
    RED       # Z
]

# Фигуры Тетриса (форматы)
SHAPES = [
    # I
    [
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]]
    ],
    # J
    [
        [[1, 0, 0], [1, 1, 1]],
        [[1, 1], [1, 0], [1, 0]],
        [[1, 1, 1], [0, 0, 1]],
        [[0, 1], [0, 1], [1, 1]]
    ],
    # L
    [
        [[0, 0, 1], [1, 1, 1]],
        [[1, 0], [1, 0], [1, 1]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 1], [0, 1], [0, 1]]
    ],
    # O
    [
        [[1, 1], [1, 1]]
    ],
    # S
    [
        [[0, 1, 1], [1, 1, 0]],
        [[1, 0], [1, 1], [0, 1]]
    ],
    # T
    [
        [[0, 1, 0], [1, 1, 1]],
        [[1, 0], [1, 1], [1, 0]],
        [[1, 1, 1], [0, 1, 0]],
        [[0, 1], [1, 1], [0, 1]]
    ],
    # Z
    [
        [[1, 1, 0], [0, 1, 1]],
        [[0, 1], [1, 1], [1, 0]]
    ]
]

class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    DOWN = (0, 1)

class Tetromino:
    def __init__(self):
        self.type = random.randint(0, len(SHAPES) - 1)
        self.color = COLORS[self.type]
        self.rotation = 0
        self.shape = SHAPES[self.type][self.rotation]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
    
    def rotate(self):
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % len(SHAPES[self.type])
        self.shape = SHAPES[self.type][self.rotation]
        
        # Если после поворота фигура выходит за границы, отменяем поворот
        if self.x + len(self.shape[0]) > GRID_WIDTH:
            self.rotation = old_rotation
            self.shape = SHAPES[self.type][self.rotation]
    
    def move(self, direction: Direction) -> bool:
        dx, dy = direction.value
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Проверка на столкновение с границами
        if new_x < 0 or new_x + len(self.shape[0]) > GRID_WIDTH:
            return False
        if new_y + len(self.shape) > GRID_HEIGHT:
            return False
            
        self.x = new_x
        self.y = new_y
        return True
    
    def get_positions(self) -> List[Tuple[int, int]]:
        positions = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    positions.append((self.x + x, self.y + y))
        return positions

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Тетрис")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
        self.reset_game()
        
        # Таймеры
        self.fall_time = 0
        self.fall_speed = 500  # начальная скорость падения (мс)
        self.last_move_down_time = 0
        
    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = 500
        
    def draw_grid(self):
        # Рисуем сетку
        grid_left = (SCREEN_WIDTH - GRID_WIDTH * CELL_SIZE) // 2
        grid_top = 50
        
        # Фон сетки
        pygame.draw.rect(self.screen, BLACK, 
                        (grid_left - 2, grid_top - 2, 
                         GRID_WIDTH * CELL_SIZE + 4, GRID_HEIGHT * CELL_SIZE + 4))
        
        # Ячейки сетки
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(
                    grid_left + x * CELL_SIZE,
                    grid_top + y * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                
                # Рисуем заполненные ячейки
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x], rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect, 1)
        
        # Рисуем текущую фигуру
        for x, y in self.current_piece.get_positions():
            if 0 <= y < GRID_HEIGHT:
                rect = pygame.Rect(
                    grid_left + x * CELL_SIZE,
                    grid_top + y * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                pygame.draw.rect(self.screen, self.current_piece.color, rect)
                pygame.draw.rect(self.screen, WHITE, rect, 2)
    
    def draw_sidebar(self):
        sidebar_left = SCREEN_WIDTH - 200
        
        # Рисуем фон боковой панели
        pygame.draw.rect(self.screen, (50, 50, 50), 
                        (sidebar_left, 0, 200, SCREEN_HEIGHT))
        
        # Следующая фигура
        next_text = self.font.render("Следующая:", True, WHITE)
        self.screen.blit(next_text, (sidebar_left + 20, 50))
        
        # Рисуем следующую фигуру
        next_grid_left = sidebar_left + 50
        next_grid_top = 100
        
        for y, row in enumerate(self.next_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        next_grid_left + x * CELL_SIZE,
                        next_grid_top + y * CELL_SIZE,
                        CELL_SIZE, CELL_SIZE
                    )
                    pygame.draw.rect(self.screen, self.next_piece.color, rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
        
        # Статистика
        score_text = self.font.render(f"Очки: {self.score}", True, WHITE)
        level_text = self.font.render(f"Уровень: {self.level}", True, WHITE)
        lines_text = self.font.render(f"Линии: {self.lines_cleared}", True, WHITE)
        
        self.screen.blit(score_text, (sidebar_left + 20, 250))
        self.screen.blit(level_text, (sidebar_left + 20, 300))
        self.screen.blit(lines_text, (sidebar_left + 20, 350))
        
        # Управление
        controls_y = 450
        controls = [
            "Управление:",
            "← → : Движение",
            "↑ : Поворот",
            "↓ : Быстрее вниз",
            "Пробел : Сбросить",
            "P : Пауза"
        ]
        
        for i, text in enumerate(controls):
            control_text = self.small_font.render(text, True, WHITE)
            self.screen.blit(control_text, (sidebar_left + 20, controls_y + i * 30))
    
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("ИГРА ОКОНЧЕНА!", True, RED)
        score_text = self.font.render(f"Финальный счет: {self.score}", True, WHITE)
        restart_text = self.small_font.render("Нажмите ПРОБЕЛ для новой игры", True, WHITE)
        
        self.screen.blit(game_over_text, 
                        (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, 
                        (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, 
                        (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 + 50))
    
    def draw_title(self):
        title_font = pygame.font.SysFont(None, 48)
        title_text = title_font.render("ТЕТРИС", True, CYAN)
        self.screen.blit(title_text, 
                        (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
    
    def check_collision(self, piece: Tetromino, dx: int = 0, dy: int = 0) -> bool:
        for x, y in piece.get_positions():
            new_x = x + dx
            new_y = y + dy
            
            # Проверка границ
            if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                return True
                
            # Проверка столкновения с другими фигурами
            if new_y >= 0 and self.grid[new_y][new_x]:
                return True
                
        return False
    
    def merge_piece(self):
        for x, y in self.current_piece.get_positions():
            if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                self.grid[y][x] = self.current_piece.color
    
    def clear_lines(self) -> int:
        lines_to_clear = []
        
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_clear.append(y)
        
        for line in lines_to_clear:
            # Удаляем линию
            del self.grid[line]
            # Добавляем новую пустую линию вверху
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        return len(lines_to_clear)
    
    def update_score(self, lines_cleared: int):
        # Баллы за очищенные линии
        line_scores = {1: 100, 2: 300, 3: 500, 4: 800}
        self.score += line_scores.get(lines_cleared, 0) * self.level
        
        # Обновление уровня
        self.lines_cleared += lines_cleared
        self.level = self.lines_cleared // 10 + 1
        
        # Увеличение скорости
        self.fall_speed = max(50, 500 - (self.level - 1) * 50)
    
    def new_piece(self) -> bool:
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        
        # Проверка на конец игры
        if self.check_collision(self.current_piece):
            return False
        return True
    
    def hard_drop(self):
        while not self.check_collision(self.current_piece, 0, 1):
            self.current_piece.y += 1
        
        self.merge_piece()
        lines_cleared = self.clear_lines()
        if lines_cleared:
            self.update_score(lines_cleared)
        
        if not self.new_piece():
            self.game_over = True
    
    def handle_input(self):
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                else:
                    if event.key == pygame.K_LEFT:
                        if not self.check_collision(self.current_piece, -1, 0):
                            self.current_piece.move(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        if not self.check_collision(self.current_piece, 1, 0):
                            self.current_piece.move(Direction.RIGHT)
                    elif event.key == pygame.K_UP:
                        old_rotation = self.current_piece.rotation
                        self.current_piece.rotate()
                        if self.check_collision(self.current_piece):
                            self.current_piece.rotation = old_rotation
                            self.current_piece.shape = SHAPES[self.current_piece.type][old_rotation]
                    elif event.key == pygame.K_DOWN:
                        if not self.check_collision(self.current_piece, 0, 1):
                            self.current_piece.move(Direction.DOWN)
                            self.last_move_down_time = current_time
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()
                    elif event.key == pygame.K_p:
                        self.pause_game()
        
        # Непрерывное движение вниз при зажатой клавише
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            if current_time - self.last_move_down_time > 50:  # 50ms задержка
                if not self.check_collision(self.current_piece, 0, 1):
                    self.current_piece.move(Direction.DOWN)
                    self.last_move_down_time = current_time
    
    def pause_game(self):
        paused = True
        pause_text = self.font.render("ПАУЗА", True, YELLOW)
        continue_text = self.small_font.render("Нажмите P чтобы продолжить", True, WHITE)
        
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    paused = False
            
            # Рисуем затемнение
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            
            # Рисуем текст паузы
            self.screen.blit(pause_text, 
                           (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(continue_text, 
                           (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 + 20))
            
            pygame.display.flip()
            self.clock.tick(30)
    
    def update(self, delta_time: int):
        if self.game_over:
            return
            
        self.fall_time += delta_time
        
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            
            if not self.check_collision(self.current_piece, 0, 1):
                self.current_piece.move(Direction.DOWN)
            else:
                self.merge_piece()
                lines_cleared = self.clear_lines()
                if lines_cleared:
                    self.update_score(lines_cleared)
                
                if not self.new_piece():
                    self.game_over = True
    
    def draw(self):
        self.screen.fill((30, 30, 30))
        
        self.draw_title()
        self.draw_grid()
        self.draw_sidebar()
        
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        while True:
            delta_time = self.clock.tick(60)
            
            self.handle_input()
            self.update(delta_time)
            self.draw()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()