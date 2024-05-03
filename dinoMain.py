# first real project :)
import os
import sys
import pygame
import random
import math

width = 650
height = 200

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Dino')


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
        # adding parallax infinite scrolling to repeat background
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


class Dino:

    def __init__(self):
        self.width = 44
        self.height = 44

        self.x = 10
        self.y = 120

        self.textureNum = 0  # to update dino between 0,1,2
        self.dy = 2.7
        self.gravity = 1

        self.onGround = True  # for on ground vs jumping
        self.jumping = False
        self.falling = False
        self.jumpStop = 20  # where to stop the jump
        self.fallStop = self.y

        self.setSound()
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

    def setSound(self):
        path = os.path.join(f'assets/sound effects/jump.wav')
        self.sound = pygame.mixer.Sound(path)

    # not to make him actually go through the jump, but only changing bool values
    # {
    def jump(self):
        self.sound.play()
        self.jumping = True
        self.onGround = False

    def fall(self):
        self.jumping = False
        self.falling = True

    def stop(self):
        self.falling = False
        self.onGround = True
    # }


class Cactus:

    def __init__(self, x):
        self.width = 34
        self.height = 44
        self.x = x
        self.y = 120
        self.setTexture()
        self.show()

    def update(self, dx):
        self.x += dx  # negative to create illusion of cactus moving to the left

    def show(self):
        screen.blit(self.texture, (self.x, self.y))  # blit

    def setTexture(self):
        path = os.path.join(f'assets/images/cactus.png')  # setting texture
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


class Collisions:

    def between(self, object1, object2):
        distance = math.sqrt((object1.x - object2.x) ** 2 + (object1.y - object2.y) ** 2)
        return distance < 35  # returning bool


class Score:
    def __init__(self, hs):
        self.hs = hs
        self.act = 0  # current score
        self.font = pygame.font.SysFont('monospace', 20)
        self.color = (0, 0, 0)
        self.setSound()
        self.show()

    def update(self, loops):
        self.act = loops // 20
        self.checkHighScore()
        self.checkSound()

    def show(self):
        self.label = self.font.render(f'HI {self.hs} {self.act}', 1, self.color)
        labelWidth = self.label.get_rect().width
        screen.blit(self.label, (width - labelWidth - 10, 10))

    def setSound(self):
        path = os.path.join(f'assets/sound effects/point.wav')
        self.sound = pygame.mixer.Sound(path)
        pygame.mixer.Sound.set_volume(self.sound, 0.05)

    def checkHighScore(self):
        if self.act >= self.hs:
            self.hs = self.act  # replacing hs with current score

    def checkSound(self):
        if self.act % 100 == 0 and self.act != 0:
            self.sound.play()


class Game:

    def __init__(self, hs=0):
        self.bg = [BG(x=0), BG(x=width)]
        self.dino = Dino()
        self.obstacles = []
        self.collisions = Collisions()
        self.score = Score(hs)
        self.speed = 2  # set speed for bg movement
        self.playing = False  # only starts after pressing space
        self.setSound()
        self.setLabels()

    def setLabels(self):
        bigFont = pygame.font.SysFont('monospace', 35, bold=True)
        smallFont = pygame.font.SysFont('monospace', 20)
        self.bigLabel = bigFont.render(f'G A M E  O V E R', 1, (0, 0, 0))
        self.smallLabel = smallFont.render(f'press R to restart', 1, (0, 0, 0))

    def setSound(self):
        path = os.path.join(f'assets/sound effects/die.wav')
        self.sound = pygame.mixer.Sound(path)

    def start(self):
        self.playing = True

    def over(self):
        self.sound.play()
        screen.blit(self.bigLabel, (width // 2 - self.bigLabel.get_width() // 2, height // 4))
        screen.blit(self.smallLabel, (
            width // 2 - self.smallLabel.get_width() // 2, height // 2 - 5))  # formatting the death screen text
        self.playing = False

    def toSpawn(self, loops):
        return loops % 100 == 0

    def spawnCactus(self):
        # list with cactus
        if len(self.obstacles) > 0:
            prevCactus = self.obstacles[-1]
            x = random.randint(prevCactus.x + self.dino.width + 84, width + prevCactus.x + self.dino.width + 84)
            # ensuring that the dino can fit btwn cactus

        # empty list
        else:
            x = random.randint(width + 100, 1000)

        # create new cactus
        cactus = Cactus(x)
        self.obstacles.append(cactus)

    def restart(self):
        self.__init__(hs=self.score.hs)  # resetting all init to default values


def main():
    # objects
    game = Game()
    dino = game.dino  # gonna be typing dino a lot

    # variables
    clock = pygame.time.Clock()
    loops = 0
    over = False

    # main loop
    while True:

        if game.playing:

            loops += 1

            # -- BACKGROUND --
            for bg in game.bg:
                bg.update(-game.speed)
                bg.show()  # applies to both backgrounds

            # -- DINO --
            dino.update(loops)
            dino.show()

            # -- CACTUS --
            if game.toSpawn(loops):
                game.spawnCactus()

            for cactus in game.obstacles:
                cactus.update(-game.speed)  # updating w/ same speed as background
                cactus.show()

                # -- COLLISIONS --
                if game.collisions.between(dino, cactus):
                    over = True  # collision = game end

            if over:
                game.over()

                # -- SCORE --
                game.score.update(loops)
                game.score.show()

        # -- EVENTS --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not over:
                        if dino.onGround:
                            dino.jump()

                        if not game.playing:
                            game.start()  # game starts when we press space

                if event.key == pygame.K_r:
                    game.restart()
                    dino = game.dino
                    loops = 0
                    over = False

        # setting same speeds for every computer, no matter the speed of computer
        clock.tick(144)

        pygame.display.update()


main()
