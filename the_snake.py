"""Модуль для генерации случайных позиций объектов."""
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - Pacific Blue:
BOARD_BACKGROUND_COLOR = (46, 71, 85)

# Цвет границы ячейки = цвет фона + примерно на 1/4 тона
BORDER_COLOR = tuple(item + 12 for item in BOARD_BACKGROUND_COLOR)

# Цвет яблока
APPLE_COLOR = (165, 40, 44)

# Цвет змейки
SNAKE_COLOR = (31, 32, 32)

# Цвет камня
STONE_COLOR = (249, 246, 239)

# Цвет яда
POISON_COLOR = (0, 128, 0)

# Скорость движения змейки:
SPEED = 12

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Список занятых позиций
# Нужен, чтобы избежать накладывания генерируемых объектов друг на друга
occupied_positions = []

# Классы игры.


class GameObject:
    """Класс, описывающий игровое поле и его объекты"""

    def __init__(self, position=None, body_color=None):
        if position is None:
            position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Определение отрисовки объкта"""


class Apple(GameObject):
    """Класс, отвечающий за яблоко на игровом поле"""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Позиция яблока"""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            # Если новой позиции нет в списке занятых позиций
            if self.position not in occupied_positions:
                occupied_positions.append(self.position)
                break

    def draw(self):
        """Отрисовывает яблоко"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    """Класс отвечает за камень, сбрасывающий игру в начальное состояние"""

    def __init__(self):
        super().__init__(body_color=STONE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Позиция канмя"""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            # Если новой позиции нет в списке занятых позиций
            if self.position not in occupied_positions:
                occupied_positions.append(self.position)
                break

    def draw(self):
        """Отрисовать камень"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Posion(GameObject):
    """Класс отвечает за яд, уменьшающий змейку на одно значение"""

    def __init__(self):
        super().__init__(body_color=POISON_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Позиция яда"""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            # Если новой позиции нет в списке занятых позиций
            if self.position not in occupied_positions:
                occupied_positions.append(self.position)
                break

    def draw(self):
        """Отрисовать яд"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, отвечающий за механику змейки на игровом поле"""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы"""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод отвечает за обновление позиции змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        # Получаем позицию головы змейки
        new_head = (
            self.positions[0][0] + self.direction[0] * GRID_SIZE,
            self.positions[0][1] + self.direction[1] * GRID_SIZE
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
        """Отрисовывает змейку и затирает след"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        if self.length:
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        # Если не съела яблоко - удаляем последний элемент из хвоста
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сброс игры в начальное состояние"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        occupied_positions.clear()


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def draw_grid():
    """Отрисовывает сетку на игровом поле"""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):  # Вертикальные линии
        pygame.draw.line(screen, BORDER_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):  # Горизонтальные линии
        pygame.draw.line(screen, BORDER_COLOR, (0, y), (SCREEN_WIDTH, y))


def draw_world(snake, apple, stones, poisons):
    """Отрисовка объектов игрового мира"""
    screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана
    draw_grid()  # Отрисовать сетку
    snake.draw()  # Отрисовать змейку
    apple.draw()  # Отрисовать яблоко

    for stone in stones:  # Отрисовать камни
        stone.draw()

    for poison in poisons:  # Отрисовать яды
        poison.draw()

    # Обновить игровое поле
    pygame.display.update()


def main():
    """Обновление состояний объектов и логика игры"""
    # Инициализация PyGame:
    pygame.init()

    # Создание объектов
    apple = Apple()
    snake = Snake()
    # Создаем 1 камень и 1 яд на игровом поле
    stones = [Stone()]
    poisons = [Posion()]

    while True:
        clock.tick(SPEED)

        handle_keys(snake)  # Обработка события клавиш
        snake.move()

        # Если змейка съела яблоко...
        if snake.get_head_position() == apple.position:
            # Удаляем позицию яблока из списка занятых позиций
            if apple.position in occupied_positions:
                occupied_positions.remove(apple.position)
            snake.length += 1
            apple.randomize_position()
            # Добавляем 1 камень и 1 яд на поле
            poisons.append(Posion())
            stones.append(Stone())

        # Проверка на столкновение с собой
        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            # Сбрасываем/пересоздаём камни и яды
            stones = [Stone()]
            poisons = [Posion()]
            apple.randomize_position()

        # Cтолкновение с камнем
        for stone in stones:
            if snake.get_head_position() == stone.position:
                snake.reset()
                stones = [Stone()]
                poisons = [Posion()]

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
                    stones = [Stone()]
                    poisons = [Posion()]

        draw_world(snake, apple, stones, poisons)
        # Ведём счёт
        pygame.display.set_caption(f'Счёт: {str(snake.length)}')


if __name__ == '__main__':
    main()
