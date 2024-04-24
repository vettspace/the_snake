"""Модуль для генерации случайных позиций объектов."""
from random import randint
from typing import List
import pygame as pg

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (46, 71, 85)

# Цвет границы ячейки = цвет фона + примерно на 1/4 тона
BORDER_COLOR = tuple(item + 12 for item in BOARD_BACKGROUND_COLOR)
APPLE_COLOR = (165, 40, 44)
SNAKE_COLOR = (31, 32, 32)
STONE_COLOR = (249, 246, 239)
POISON_COLOR = (0, 128, 0)
SPEED = 12


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()

# Список занятых позиций
# Нужен, чтобы избежать накладывания генерируемых объектов друг на друга
occupied_positions: List[int] = []

# Классы игры.


class GameObject:
    """Объект на игровом поле."""

    def __init__(self, position=None, body_color=None):
        """Инициализация объекта на игровом поле."""
        self.position = position or [
            ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на игровом поле."""
        raise NotImplementedError("Метод переопределяется в подклассе.")

    def draw_cell(self, position, body_color):
        """Отрисовывает одну клетку на игровом поле."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко на игровом поле."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию для яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_cell(self.position, self.body_color)


class Stone(GameObject):
    """Камень на игровом поле."""

    def __init__(self):
        super().__init__(body_color=STONE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию для камня."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовывает камень на игровом поле."""
        self.draw_cell(self.position, self.body_color)


class Poison(GameObject):
    """Яд на игровом поле."""""

    def __init__(self):
        super().__init__(body_color=POISON_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию для яда."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовывает яд на игровом поле."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Змейка на игровом поле."""

    def __init__(self):
        """Инициализирует змейку в начальной позиции."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        # Получаем новую позицию головы змейки
        new_head = (
            self.get_head_position()[0] + self.direction[0] * GRID_SIZE,
            self.get_head_position()[1] + self.direction[1] * GRID_SIZE
        )

        # Добавляем новую голову
        self.positions.insert(0, new_head)

        # Если змейка появилась с другой стороны
        head_width, head_height = self.positions[0]
        if head_width < 0:
            head_width = SCREEN_WIDTH - GRID_SIZE
        elif head_width >= SCREEN_WIDTH:
            head_width = 0
        if head_height < 0:
            head_height = SCREEN_HEIGHT - GRID_SIZE
        elif head_height >= SCREEN_HEIGHT:
            head_height = 0
        self.positions[0] = (head_width, head_height)

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color)

        # Отрисовка головы змейки
        if self.length:
            head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, head_rect)
            pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        # Если не съела яблоко - удаляем последний элемент из хвоста
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        occupied_positions.clear()


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления игровым объектом."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def draw_grid():
    """Отрисовывает сетку на игровом поле."""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):  # Вертикальные линии
        pg.draw.line(screen, BORDER_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):  # Горизонтальные линии
        pg.draw.line(screen, BORDER_COLOR, (0, y), (SCREEN_WIDTH, y))


def draw_world(snake, apple, stones, poisons):
    """Отрисовыввает объекты игрового мира."""
    screen.fill(BOARD_BACKGROUND_COLOR)
    draw_grid()
    snake.draw()
    apple.draw()

    for stone in stones:  # Отрисовать камни
        stone.draw()

    for poison in poisons:  # Отрисовать яды
        poison.draw()

    pg.display.update()


def get_uniq_position(game_thing):
    """Генерирует новую уникальную позицию объектов."""
    valid_position = False
    # Пока не будут найдены свободные значения координат
    while not valid_position:
        game_thing.randomize_position()
        if game_thing.position not in occupied_positions:
            valid_position = True
            occupied_positions.append(game_thing.position)


def create_thing():
    """Создает 1 камень и 1 яд на игровом поле."""
    new_stone = Stone()
    get_uniq_position(new_stone)
    new_poison = Poison()
    get_uniq_position(new_poison)
    return [new_stone], [new_poison]


def main():
    """Обновление состояний объектов и логика игры."""
    pg.init()
    apple = Apple()
    snake = Snake()
    stones, poisons = create_thing()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        # Если змейка съела яблоко...
        if snake.get_head_position() == apple.position:
            # Удаляем позицию яблока из списка занятых позиций
            if apple.position in occupied_positions:
                occupied_positions.remove(apple.position)
            snake.length += 1
            get_uniq_position(apple)
            # Добавляем камень и яд на поле
            new_stone, new_poison = create_thing()
            stones.append(new_stone[0])
            poisons.append(new_poison[0])

        # Проверка на столкновение с собой
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            # Сбрасываем/пересоздаём камни и яды
            stones, poisons = create_thing()
            get_uniq_position(apple)

        # Cтолкновение с камнем
        for stone in stones:
            if snake.get_head_position() == stone.position:
                snake.reset()
                stones, poisons = create_thing()

        # Cтолкновение с ядом
        for poison in poisons[:]:
            if snake.get_head_position() == poison.position:
                if snake.length > 1:  # Если длина больше 1 - удаляем блок
                    snake.positions.pop()
                    snake.length -= 1
                    # Удаления позиции яда из списков (так как съеден)
                    poisons.remove(poison)
                    occupied_positions.remove(poison.position)
                else:  # Если блоков не осталось - сброс игры
                    snake.reset()
                    stones, poisons = create_thing()

        draw_world(snake, apple, stones, poisons)
        # Ведём счёт
        pg.display.set_caption(f'Счёт: {str(snake.length)}')


if __name__ == '__main__':
    main()
