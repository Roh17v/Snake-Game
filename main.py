import pygame 
from pygame.locals import *
import random

SIZE = 30

class Apple:
    def __init__(self,parent_surface):
        self.apple = pygame.image.load("resources/apple1.png").convert()
        self.parent_surface = parent_surface
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_surface.blit(self.apple,(self.x,self.y))


    def move(self):
        self.x = random.randint(0,24) * SIZE
        self.y = random.randint(0,14) * SIZE


class Snake:
    def __init__(self,parent_surface):
        self.length = 1
        self.parent_surface = parent_surface
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * self.length
        self.y = [SIZE] * self.length
        self.direction = "down"

    def increment_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_surface.fill((0,0,0))
        for i in range(self.length):
            self.parent_surface.blit(self.block,(self.x[i],self.y[i]))

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move(self):

        for i in range(self.length - 1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE 
        if self.direction == "right":
            self.x[0] += SIZE
    
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000,600))
        pygame.display.set_caption("Snake Game")
        self.surface.fill((0,0,0))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)


    def play(self):
        self.snake.move()
        self.apple.draw()    
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.apple.move() 
            self.snake.increment_length()

        for i in range(1,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                raise "Collision Occured"

    def is_collision(self, x1,y1,x2,y2):
        if x1 >= x2 and x1 <= x2 + SIZE - 5:
            if y1 >= y2 and y1 <= y2 + SIZE - 5:
                return True
            

    def show_game_over(self):
        self.surface.fill((0,0,0))
        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (250, 250))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (250, 300))
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(255,255,255))
        self.surface.blit(score,(880,10))
            

    def run(self):
        pause = False
        self.run = True
        clock = pygame.time.Clock()
        while self.run:
            pygame.time.delay(100)
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                    self.run = False

            if keys[pygame.K_RETURN]:
                pause = False

            if not pause:
                if keys[pygame.K_UP]:
                    self.snake.move_up()
                
                if keys[pygame.K_DOWN]:
                    self.snake.move_down()

                if keys[pygame.K_LEFT]:
                    self.snake.move_left()

                if keys[pygame.K_RIGHT]:
                    self.snake.move_right()

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
                

if __name__ =="__main__":
    game = Game()
    game.run()

pygame.quit()
    
