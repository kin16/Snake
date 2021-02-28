import os
import sys
import pygame
import random

# предигровые настройки, фпс и название уровня
FPS = int(input('Введите FPS (скорость змейки, 3 - средняя): '))
filename = 'data/' + input('Введите название уровня (1-5): ') + '.txt'
pygame.display.set_caption('Перемещение героя')
with open(filename, 'r') as mapFile:
    level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    WIDTH, HEIGHT = max_width * 50, len(level_map) * 50


def close():  # выход из игры
    print("Игра окончена!!!")
    pygame.quit()
    sys.exit()


def load_level(filename):  # загрузка уровня через текстовой документ
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        WIDTH, HEIGHT = max_width * 50, len(level_map) * 50
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name):  # загрузка изображения
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def random_apple(level):
    le = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                le.append([x, y])
    return random.choice(le)


# спрайты и изображения
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
border_group = pygame.sprite.Group()
grass_group = pygame.sprite.Group()
snake_group = pygame.sprite.Group()
apple_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
apple_image = load_image('apple.png')
border_image = load_image('wall.png')
grass_image = load_image('grass.png')
head_image_right = load_image('head_right.png')
head_image_left = load_image('head_left.png')
head_image_up = load_image('head_up.png')
head_image_down = load_image('head_down.png')
body_image_right = load_image('body_right.png')
body_image_left = load_image('body_left.png')
body_image_up = load_image('body_up.png')
body_image_down = load_image('body_down.png')
tail_image_right = load_image('tail_right.png')
tail_image_left = load_image('tail_left.png')
tail_image_up = load_image('tail_up.png')
tail_image_down = load_image('tail_down.png')
player_image = load_image('body.png')
tile_width = tile_height = 50


class Border(pygame.sprite.Sprite):  # блоки, стены, недвижимые объекты
    def __init__(self, pos_x, pos_y):
        super().__init__(border_group, all_sprites)
        self.image = border_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Grass(pygame.sprite.Sprite):  # трава, пустое пространство
    def __init__(self, pos_x, pos_y):
        super().__init__(grass_group, all_sprites)
        self.image = grass_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Apple(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(apple_group, all_sprites)
        self.image = apple_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, x, y):
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)


class Head(pygame.sprite.Sprite):  # голова змеи
    def __init__(self, snake):
        super().__init__(snake_group, all_sprites)
        self.snake = snake
        self.head = snake[0]
        self.tail = snake[1]
        self.image = self.head_photo(self.head[2])
        self.rect = self.image.get_rect().move(
            self.head[0], self.head[1])
        self.direction = 1, 0

    def set_direction(self, stroke):  # выбор направления
        if stroke == 'up':
            self.direction = 0, 1
        elif stroke == 'down':
            self.direction = 0, -1
        elif stroke == 'left':
            self.direction = -1, 0
        elif stroke == 'right':
            self.direction = 1, 0

    def directions(self, coords):  # меняет координаты головы в зависимости от направления
        if self.direction[0] == 1:
            return coords[0] + 50, coords[1]
        elif self.direction[0] == -1:
            return coords[0] - 50, coords[1]
        elif self.direction[1] == 1:
            return coords[0], coords[1] - 50
        elif self.direction[1] == -1:
            return coords[0], coords[1] + 50

    def move(self):  # меняет координаты всех частей змеи (в том числе и головы)
        f = False
        if pygame.sprite.spritecollideany(self, border_group) and \
                pygame.sprite.spritecollideany(self, snake_group):
            close()
        elif pygame.sprite.spritecollideany(self, apple_group):
            Grass(self.head[0], self.head[1])
            f = True
            position = random_apple(load_level(filename))
            apple_group.update(position[0], position[1])

        copy = []
        for i in self.snake:
            copy.append(i)
        for i in range(len(self.snake)):
            if not i:
                copy[i] = (self.directions(self.snake[i])[0], self.directions(self.snake[i])[1], self.direction)
                self.head = copy[0]
            else:
                copy[i] = self.snake[i - 1]
        if self.head in copy[1:]:
            close()
        if f:
            copy.append(self.snake[-1])
        self.snake = copy
        self.tail = self.snake[-1]

    def head_photo(self, direction):
        if direction == (0, 1):
            return head_image_up
        if direction == (0, -1):
            return head_image_down
        if direction == (1, 0):
            return head_image_right
        if direction == (-1, 0):
            return head_image_left

    def render(self):  # визуальный рендер змеи
        self.image = self.head_photo(self.direction)
        self.rect = self.image.get_rect().move(
            self.head[0], self.head[1])
        for i in self.snake:
            if i != self.head and i != self.tail:
                Body(player_image.get_rect().move(
                    i[0], i[1]), i[2])
            elif i == self.tail:
                Tail(player_image.get_rect().move(
                    i[0], i[1]), i[2])


class Tail(pygame.sprite.Sprite):  # кусочки тела змеи
    def __init__(self, rect, direction):
        super().__init__(player_group, all_sprites)
        if direction == (0, 1):
            self.image = tail_image_up
        elif direction == (1, 0):
            self.image = tail_image_right
        elif direction == (0, -1):
            self.image = tail_image_down
        elif direction == (-1, 0):
            self.image = tail_image_left
        self.rect = rect


class Body(pygame.sprite.Sprite):  # кусочки тела змеи
    def __init__(self, rect, direction):
        super().__init__(player_group, all_sprites)
        if direction == (0, 1):
            self.image = body_image_up
        elif direction == (1, 0):
            self.image = body_image_right
        elif direction == (0, -1):
            self.image = body_image_down
        elif direction == (-1, 0):
            self.image = body_image_left
        self.rect = rect


def generate_level(level):  # генерация уровня через .txt
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Grass(x, y)
            elif level[y][x] == '#':
                Border(x, y)


if __name__ == '__main__':  # основная программа
    pygame.init()
    pygame.display.set_caption('Змейка')
    size = WIDTH, HEIGHT
    prev = 'left'  # чтобы змея не могла резко поворачиваться на 180 градусов и ломать программу
    screen = pygame.display.set_mode(size)
    generate_level(load_level(filename))
    pos = random_apple(load_level(filename))
    Apple(pos[0], pos[1])
    snake = Head([(150, 150, (0, 1)), (125, 150, (0, 1)), (100, 150, (0, 1))])
    running = True
    action_happened = False
    counter = 20 // FPS  # для стабильной работы поворотов и в целом самой игры я сделал такой подход к ФПС
    all_sprites.draw(screen)  # отрисовка спрайтов для начала игры
    snake_group.draw(screen)
    grass_group.draw(screen)
    border_group.draw(screen)
    apple_group.draw(screen)
    snake.set_direction('right')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not action_happened:
                if event.key == pygame.K_LEFT:
                    if prev != 'right':
                        action_happened = True
                        snake.set_direction('left')
                        prev = 'left'
                if event.key == pygame.K_RIGHT:
                    if prev != 'left':
                        action_happened = True
                        snake.set_direction('right')
                        prev = 'right'
                if event.key == pygame.K_UP:
                    if prev != 'down':
                        action_happened = True
                        snake.set_direction('up')
                        prev = 'up'
                if event.key == pygame.K_DOWN:
                    if prev != 'up':
                        action_happened = True
                        snake.set_direction('down')
                        prev = 'down'
        clock.tick(20)
        if counter == 20 // FPS:  # при каждом значении FPS что-то будет происходить
            action_happened = False
            counter = 0
            snake.move()
            snake.render()
            all_sprites.draw(screen)
            border_group.draw(screen)
            grass_group.draw(screen)
            snake_group.draw(screen)
            apple_group.draw(screen)
            player_group.draw(screen)
            pygame.display.flip()
            player_group.empty()
        counter += 1
    pygame.quit()
