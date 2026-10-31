from random import choice, randint


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position):
        """Инициализирует базовые атрибуты объекта."""
        self.position = position
        # Цвет по умолчанию не задан, ожидается в дочерних классах
        self.body_color = None

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта.

        Должен быть переопределен в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс яблока, наследуется от GameObject."""

    def __init__(self, cell_size=20, screen_width=640, screen_height=480):
        """Инициализирует яблоко, задает цвет и случайную позицию."""
        self.cell_size = cell_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Красный цвет
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        # Вычисляем количество ячеек по горизонтали и вертикали
        max_x = (self.screen_width // self.cell_size) - 1
        max_y = (self.screen_height // self.cell_size) - 1

        # Генерируем случайные координаты в ячейках и переводим в пиксели
        x = randint(0, max_x) * self.cell_size
        y = randint(0, max_y) * self.cell_size
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (self.cell_size, self.cell_size))
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки, наследуется от GameObject."""

    def __init__(self, cell_size=20, screen_width=640, screen_height=480):
        """Инициализирует начальное состояние змейки."""
        self.cell_size = cell_size
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Зеленый цвет
        self.body_color = (0, 255, 0)

        # Начальная позиция - центр экрана
        start_x = (screen_width // 2) // cell_size * cell_size
        start_y = (screen_height // 2) // cell_size * cell_size
        self.positions = [(start_x, start_y)]
        self.length = 1
        self.direction = (cell_size, 0)  # Движение вправо
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки, добавляя новую голову и удаляя хвост."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        # Вычисляем новые координаты головы
        new_head_x = head_x + dir_x
        new_head_y = head_y + dir_y

        # Телепортация через стены (выход за границы)
        if new_head_x < 0:
            new_head_x = self.screen_width - self.cell_size
        elif new_head_x >= self.screen_width:
            new_head_x = 0

        if new_head_y < 0:
            new_head_y = self.screen_height - self.cell_size
        elif new_head_y >= self.screen_height:
            new_head_y = 0

        new_head = (new_head_x, new_head_y)

        # Добавляем новую голову в начало списка
        self.positions.insert(0, new_head)

        # Если длина не увеличилась, удаляем последний элемент (хвост)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране, затирая след."""
        # Затираем след (последний сегмент)
        if len(self.positions) > 1:
            # Берем предпоследний элемент, так как последний уже может быть
            # новой головой.
            # Но проще затереть тот, который был удален.
            # В данной реализации move() удаляет хвост, поэтому нам нужно
            # затирать позицию, которой больше нет в списке.
            # Для простоты затираем весь экран перед отрисовкой (см. main),
            # либо храним предыдущую позицию хвоста.
            pass

        # Отрисовываем все сегменты
        for position in self.positions:
            rect = pygame.Rect(position, (self.cell_size, self.cell_size))
            pygame.draw.rect(surface, self.body_color, rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        start_x = (
            (self.screen_width // 2) // self.cell_size * self.cell_size
        )
        start_y = (
            (self.screen_height // 2) // self.cell_size * self.cell_size
        )
        self.positions = [(start_x, start_y)]
        self.length = 1
        self.direction = (self.cell_size, 0)
        self.next_direction = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_UP
                and snake.direction != (0, snake.cell_size)
            ):
                snake.next_direction = (0, -snake.cell_size)
            elif (
                event.key == pygame.K_DOWN
                and snake.direction != (0, -snake.cell_size)
            ):
                snake.next_direction = (0, snake.cell_size)
            elif (
                event.key == pygame.K_LEFT
                and snake.direction != (snake.cell_size, 0)
            ):
                snake.next_direction = (-snake.cell_size, 0)
            elif (
                event.key == pygame.K_RIGHT
                and snake.direction != (-snake.cell_size, 0)
            ):
                snake.next_direction = (snake.cell_size, 0)


def main():
    """Основной игровой цикл."""
    pygame.init()
    screen_width = 640
    screen_height = 480
    cell_size = 20

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Изгиб Питона')
    clock = pygame.time.Clock()

    snake = Snake(cell_size, screen_width, screen_height)
    apple = Apple(cell_size, screen_width, screen_height)

    while True:
        # Обработка событий
        handle_keys(snake)

        # Обновление направления
        snake.update_direction()

        # Движение змейки
        snake.move()

        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка столкновения с собой
        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()

        # Отрисовка
        screen.fill((0, 0, 0))  # Черный фон
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    main()
