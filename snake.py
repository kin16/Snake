import sys
import pygame


def set_direction(stroke):
    if stroke == 'up':
        return 0, 1
    elif stroke == 'down':
        return 0, -1
    elif stroke == 'left':
        return -1, 0
    elif stroke == 'right':
        return 1, 0
    else:
        return None


def terminate():
    pygame.quit()
    sys.exit()


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 40
        self.top = 40
        self.cell_size = 20

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # отрисовка
    def render(self):
        pass


class Snake:
    def __init__(self, snake):
        self.snake = snake
        self.head = snake[0]

    def chod(self):
        if self.isAlive():
            del self.snake[-1]

    def isAlive(self):
        if len(self.snake) != 0:
            global running
            running = False
            return False
        else:
            return True


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Змейка')
    size = WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode(size)

    board = Board(10, 10)
    running = True
    direction = set_direction('right')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = set_direction('left')
                if event.key == pygame.K_RIGHT:
                    direction = set_direction('right')
                if event.key == pygame.K_UP:
                    direction = set_direction('up')
                if event.key == pygame.K_DOWN:
                    direction = set_direction('down')

        screen.fill((0, 0, 0))
        board.render()
        pygame.display.flip()
