# first real project :)
import os
import sys
import pygame

width = 650
height = 200

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Dino')


class BG:

    def __init__(self, x):
        self.width = width
        self.height = height
        self.x = x
        self.y = 0  # never changes
        self.set_texture()  # adding background texture
        self.show()  # showing background

    # coding inf bg
    def update(self, dx):
        self.x += dx
        # adding parralax infinite scrolling to repeat background
        if self.x <= -width:
            self.x = width  # restarting bg if it is not present

    # showing bg on screen
    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    # converting bg to actual bg
    def set_texture(self):
        path = os.path.join('assets/images/bg.png')  # setting background
        self.texture = pygame.image.load(path)  # loading the bg at the path given above
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))  # scaling bg
        # width and height we gave earlier


class Game:

    def __init__(self):
        self.bg = [BG(x=0), BG(x=width)]
        self.speed = 0.4  # set speed for bg movement


def main():
    game = Game()

    # main loop
    while True:

        for bg in game.bg:
            bg.update(-game.speed)
            bg.show()  # applies to both backgrounds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


main()
