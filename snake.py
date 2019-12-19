import pygame
import os
import random
import math

WIN_WIDTH = 400
WIN_HEIGHT = 400
SPEED = 20
FPS = 10

bg_img = pygame.image.load(os.path.join("bg_img.png"))
bg_img = pygame.transform.scale(bg_img, (WIN_WIDTH, WIN_HEIGHT))


class Snake:

    """class for the snake"""

    def __init__(self, window):

        self.sizex = SPEED
        self.sizey = SPEED
        self.speed = SPEED
        snake_img = pygame.image.load(os.path.join("square.png"))
        self.img = pygame.transform.scale(snake_img, (self.sizex, self.sizey))

        self.current_dir = "right"
        self.length = 3
        self.segments = []
        self.window = window

        self.current_dir = "right"

        self.snake_x_coords = []
        self.snake_y_coords = []

        start_coordsx = WIN_WIDTH / 2
        start_coordsx = math.ceil(start_coordsx / float(self.speed)) * self.speed
        start_coordsy = WIN_HEIGHT / 2
        start_coordsy = math.ceil(start_coordsx / float(self.speed)) * self.speed

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

        if (x1 == -self.speed) or (y1 == -self.speed) or (x1 > (WIN_WIDTH - self.speed)) or (y1 > WIN_HEIGHT - self.speed):
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

    def __init__(self, window):

        self.sizex = SPEED
        self.sizey = SPEED
        apple_img = pygame.image.load(os.path.join("red.png"))
        self.img = pygame.transform.scale(apple_img, (self.sizex, self.sizey))
        self.relocate()


    def relocate(self):

        baseline = self.sizex * 2
        rounder = self.sizex
        rounder2 = float(self.sizex)

        new_x = random.randint(baseline, WIN_WIDTH - baseline)
        new_x = math.ceil(new_x / rounder2) * rounder
        new_y = random.randint(baseline, WIN_HEIGHT - baseline)
        new_y = math.ceil(new_y / rounder2) * rounder
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

    apple = Apple(window)
    apple.relocate()

    draw_window(window, snake, apple)

    running = True
    while running:
        clock.tick(FPS)
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
