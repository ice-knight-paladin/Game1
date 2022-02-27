import pygame
import os
import random

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Img", "Cube.png")),
           pygame.image.load(os.path.join("Img", "Cube.png"))]
JUMPING = pygame.image.load(os.path.join("Img", "Cube.png"))

THR = [pygame.image.load(os.path.join("Img/Thorns", "Thorns1.png")),
       pygame.image.load(os.path.join("Img/Thorns", "Thorns2.png")),
       pygame.image.load(os.path.join("Img/Thorns", "Thorns3.png"))]

BG = pygame.image.load(os.path.join("Img", "Track.png"))


class Cube:

    def __init__(self):
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.cube_run = True
        self.cube_jump = False

        self.step_index = 0
        self.jump_vel = 9
        self.image = self.run_img[0]
        self.cube_rect = self.image.get_rect()
        self.cube_rect.x = 80
        self.cube_rect.y = 310

    def update(self, userInput):
        if self.cube_run:
            self.run()
        if self.cube_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.cube_jump:
            self.cube_run = False
            self.cube_jump = True
        elif not self.cube_jump:
            self.cube_run = True
            self.cube_jump = False

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.cube_rect = self.image.get_rect()
        self.cube_rect.x = 80
        self.cube_rect.y = 310
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.cube_jump:
            self.cube_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - 9:
            self.cube_jump = False
            self.jump_vel = 9

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.cube_rect.x, self.cube_rect.y))


class Thorns:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            tr.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Thr(Thorns):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


def main():
    global game_speed, x_pos_bg, y_pos_bg, tr
    clock = pygame.time.Clock()
    player = Cube()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 400
    y_pos_bg = 400
    tr = []

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(tr) == 0:
            tr.append(Thr(THR))

        for i in tr:
            i.draw(SCREEN)
            i.update()
            if player.cube_rect.colliderect(i.rect):
                pygame.time.delay(1000)
                menu()

        background()
        clock.tick(30)
        pygame.display.update()


def menu():
    while True:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)
        text = font.render("Press any Key to Restart", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                main()


menu()
