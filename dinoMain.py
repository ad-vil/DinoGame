# first real project :)
import os
import sys
import pygame

width = 650
height = 200

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Dino')


class Dino:

    def __init__(self):
        self.width = 44
        self.height = 44

        self.x = 10
        self.y = 120

        self.textureNum = 0  # to update dino between 0,1,2
        self.dy = 2.8
        self.gravity = 1.2

        self.onGround = True  # for on ground vs jumping
        self.jumping = False
        self.falling = False
        self.jumpStop = 20  # where to stop the jump
        self.fallStop = self.y

        self.setTexture()
        self.show()

    def update(self, loops):
        # jumping
        if self.jumping:
            self.y -= self.dy
            if self.y <= self.jumpStop:
                self.fall()  # not to fall but to update values of booleans

        # falling
        elif self.falling:
            self.y += self.gravity * self.dy
            if self.y >= self.fallStop:
                self.stop()

        # walking
        elif self.onGround and loops % 11 == 0:  # only receiving update every 11 ticks instead of every single tick
            self.textureNum = (self.textureNum + 1) % 3
            self.setTexture()


    def show(self):
        screen.blit(self.texture, (self.x, self.y))

    def setTexture(self):
        path = os.path.join(f'assets/images/dino{self.textureNum}.png')  # setting path for d0
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    # not to make him actually go thru the jump, but only changing bool values
    # {
    def jump(self):
        self.jumping = True
        self.onGround = False

    def fall(self):
        self.jumping = False
        self.falling = True

    def stop(self):
        self.falling = False
        self.onGround = True
    # }


class BG:

    def __init__(self, x):
        self.width = width
        self.height = height

        self.x = x
        self.y = 0  # never changes

        self.setTexture()  # adding background texture
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
    def setTexture(self):
        path = os.path.join('assets/images/bg.png')  # setting background
        self.texture = pygame.image.load(path)  # loading the bg at the path given above
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))  # scaling bg
        # width and height we gave earlier


class Game:

    def __init__(self):
        self.bg = [BG(x=0), BG(x=width)]
        self.dino = Dino()
        self.speed = 2  # set speed for bg movement


def main():
    game = Game()
    dino = game.dino  # gonna be typing dino a lot

    clock = pygame.time.Clock()

    loops = 0

    # main loop
    while True:

        loops += 1

        # -- BACKGROUND --
        for bg in game.bg:
            bg.update(-game.speed)
            bg.show()  # applies to both backgrounds

        # -- DINO --
        dino.update(loops)
        dino.show()

        # -- EVENTS --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if dino.onGround:
                        dino.jump()

        # setting same speeds for every computer, no matter the speed of computer
        clock.tick(144)

        pygame.display.update()


main()
