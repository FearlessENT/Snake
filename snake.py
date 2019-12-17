print("running")
import pygame
import os
import random
import math




WIN_WIDTH = 400
WIN_HEIGHT = 400

snake_img = pygame.image.load(os.path.join("square.png"))
snake_img = pygame.transform.scale(snake_img, (10, 10))

apple_img = pygame.image.load(os.path.join("red.png"))
apple_img = pygame.transform.scale(apple_img, (10, 10))

bg_img = pygame.image.load(os.path.join("bg_img.png"))
bg_img = pygame.transform.scale(bg_img, (WIN_WIDTH, WIN_HEIGHT))

SPEED = 10


class Snake:

    """class for the snake"""

    speed = SPEED

    sizex = SPEED
    sizey = SPEED

    snake_img = pygame.transform.scale(snake_img, (sizex, sizey))


    def __init__(self, window):

        self.img = snake_img

        self.current_dir = "right"
        self.length = 3
        self.segments = []
        self.window = window

        self.current_dir = "right"

        self.snake_x_coords = []
        self.snake_y_coords = []

        start_coordsx = WIN_WIDTH / 2
        start_coordsy = WIN_HEIGHT / 2

        x = 0
        while x < self.length:
            start_coordsx = start_coordsx - self.speed
            self.snake_x_coords.append(start_coordsx)
            self.snake_y_coords.append(start_coordsy)
            x += 1

        self.last_coordx = self.snake_x_coords[-1]
        self.last_coordy = self.snake_y_coords[-1]


    def move_up(self):
        self.update_snake()
        self.snake_y_coords[0] = self.snake_y_coords[0] - self.speed
        self.current_dir = "up"


    def move_down(self):
        self.update_snake()
        self.snake_y_coords[0] = self.snake_y_coords[0] + self.speed
        self.current_dir = "down"


    def move_left(self):
        self.update_snake()
        self.snake_x_coords[0] = self.snake_x_coords[0] - self.speed
        self.current_dir = "left"


    def move_right(self):
        self.update_snake()
        self.snake_x_coords[0] = self.snake_x_coords[0] + self.speed
        self.current_dir = "right"



    def update_snake(self):
        referencex = self.snake_x_coords.copy()
        referencey = self.snake_y_coords.copy()

        self.last_coordx = self.snake_x_coords[-1]
        self.last_coordy = self.snake_y_coords[-1]

        z = 1
        while z < len(self.snake_x_coords):
            ref_pos = z - 1
            new_coord = referencex[ref_pos]
            self.snake_x_coords[z] = new_coord
            new_coord = referencey[ref_pos]
            self.snake_y_coords[z] = new_coord
            z += 1

        for i in range(0, len(self.snake_x_coords)):
            currentx = self.snake_x_coords[i]
            currenty = self.snake_y_coords[i]





    def collision(self, apple_cors):

        temp_list_x = self.snake_x_coords.copy()
        temp_list_y = self.snake_y_coords.copy()
        temp_list_x.pop(0)
        temp_list_y.pop(0)

        x1 = self.snake_x_coords[0]
        y1 = self.snake_y_coords[0]

        ob_x1 = temp_list_x[1]
        ob_y1 = temp_list_y[1]

        z = 0
        while z < len(temp_list_x):

            if (x1 == temp_list_x[z]) and (y1 == temp_list_y[z]):
                print("collision")
                return "collision_snake"

            z += 1

        if (x1 == apple_cors[0]) and (y1 == apple_cors[1]):
            print("hit apple")
            return "collision_apple"


        if (x1 == -10) or (y1 == -10) or (x1 > (WIN_WIDTH - 10)) or (y1 > WIN_HEIGHT - 10):
            print("hit edge")
            return "collision_edge"

        return False


    def grow(self):
        self.snake_x_coords.append(self.last_coordx)
        self.snake_y_coords.append(self.last_coordy)
        self.length = self.length + 1


    def draw(self, window):

        for i in range(len(self.snake_x_coords)):
            rect = self.img
            topleft = (self.snake_x_coords[i], self.snake_y_coords[i])
            new_rect = self.img.get_rect(topleft = topleft)
            window.blit(rect, new_rect.topleft)










class Apple:

    """base class for the apple"""

    sizex = SPEED
    sizey = SPEED

    def __init__(self, window, x, y):

        self.x = x
        self.y = y
        self.img = pygame.transform.scale(apple_img, (self.sizex, self.sizey))
        self.coords = [self.x, self.y]


    def relocate(self):

        new_x = random.randint(20, WIN_WIDTH - 20)
        new_x = math.ceil(new_x / 10.0) * 10
        new_y = random.randint(20, WIN_HEIGHT - 20)
        new_y = math.ceil(new_y / 10.0) * 10
        self.x = new_x
        self.y = new_y
        self.coords = [self.x, self.y]


    def draw(self, window):
        rect = self.img
        topleft = (self.x, self.y)
        new_rect = self.img.get_rect(topleft = topleft)
        window.blit(rect, new_rect.topleft)







def draw_window(window, snake, apple):

    window.blit(bg_img, (0,0))
    snake.draw(window)
    apple.draw(window)

    pygame.display.update()


def main():


    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    snake = Snake(window)
    snake.draw(window)

    apple = Apple(window, 150, 150)

    draw_window(window, snake, apple)

    fps = 20

    running = True
    while running:

        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keypress = pygame.key.get_pressed()

        if keypress[pygame.K_UP]:
            snake.move_up()
        elif keypress[pygame.K_DOWN]:
            snake.move_down()
        elif keypress[pygame.K_LEFT]:
            snake.move_left()
        elif keypress[pygame.K_RIGHT]:
            snake.move_right()

        else:
            if snake.current_dir == "right":
                snake.move_right()
            elif snake.current_dir == "left":
                snake.move_left()
            elif snake.current_dir == "up":
                snake.move_up()
            elif snake.current_dir == "down":
                snake.move_down()

        collision = snake.collision(apple.coords)

        if collision == "collision_snake":
            running = False
            print("Score: ", snake.length)

        elif collision == "collision_apple":
            apple.relocate()
            snake.grow()
            pass

        elif collision == "collision_edge":
            running = False
            print("Score: ", snake.length)

        draw_window(window, snake, apple)

    pygame.quit()
    quit()










main()
