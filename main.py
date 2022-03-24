import pygame
from math import cos, sin
from time import sleep

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

BACKGROUND_IMG = pygame.transform.smoothscale(pygame.image.load(
    "Assets/background.png"), (800, 450)).convert_alpha()
PLAYER1_IMG = pygame.transform.smoothscale(pygame.image.load(
    "Assets/player1.png"), (20, 120)).convert_alpha()
PLAYER2_IMG = pygame.transform.smoothscale(pygame.image.load(
    "Assets/player2.png"), (20, 120)).convert_alpha()
SCOREBAR_IMG = pygame.transform.smoothscale(pygame.image.load(
    "Assets/scorebar.png"), (350, 50)).convert_alpha()
SCOREBAR_FLIPPED = pygame.transform.flip(SCOREBAR_IMG, True, False)
BALL_IMG = pygame.image.load("Assets/ball.png").convert_alpha()

group = pygame.sprite.Group()
UP = "UP"
DOWN = "DOWN"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.Font(pygame.font.get_default_font(), 32)

class Player(pygame.sprite.Sprite):
    def __init__(self, name, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.IMAGE = image
        self.rect = self.IMAGE.get_rect()
        self.add(group)
        self.rect.x = x
        self.rect.y = y
        self.score = 0
    
    def update(self):
        WIN.blit(self.IMAGE, (self.rect.x, self.rect.y))

    def move(self, direction):
        if direction == UP:
            if self.rect.top - 5 > 50:
                self.rect.y -= 5
        elif direction == DOWN:
            if self.rect.bottom + 5 < 500:
                self.rect.y += 5
    
    def __str__(self):
        return self.name
    
    def __gt__(self, other):
        return self.score > other.score

class Ball(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x, y): 
        pygame.sprite.Sprite.__init__(self)
        self.IMAGE = image
        self.x = x
        self.y = y
        self.SPEED = 5
        self.angle = -0.7 #-45 degrees in rads
        self.add(group)
    
    def update(self):
        WIN.blit(self.IMAGE, (self.x, self.y))
    
    def move(self):
        self.x = self.x + (self.SPEED * cos(self.angle))
        self.y = self.y + (self.SPEED * sin(self.angle))
    
    def check_bounce(self, players):
        player1, player2 = players
        if self.y <= 50:
            self.angle = -self.angle
        elif self.y >= 470:
            self.angle = -self.angle
        if not self.x > player1.rect.right:
            if self.x <= player1.rect.right and self.y >= player1.rect.top and self.y + 15 <= player1.rect.bottom:
                self.angle -= 1.5 # 90 degrees in rads
        if not self.x + 30 <= player1.rect.left: 
            if self.x + 30 >= player2.rect.left and self.y >= player2.rect.top and self.y + 15 <= player2.rect.bottom:
                self.angle += 1.5 # 90 degrees in rads
    
    def check_point(self):
        if self.x + 30 >= 800:
            return 1
        elif self.x <= 0:
            return 2

def draw_win(win, players):
    WIN.fill(BLACK)
    win.blit(BACKGROUND_IMG, (0, 50))
    win.blit(SCOREBAR_IMG, (0, 0))
    win.blit(SCOREBAR_FLIPPED, (450, 0))
    group.update()
    PLAYER1_SCORE_TEXT = FONT.render(f"{players[0].score}", True, WHITE)
    PLAYER2_SCORE_TEXT = FONT.render(f"{players[1].score}", True, WHITE)
    win.blit(PLAYER1_SCORE_TEXT, (280, 10))
    win.blit(PLAYER2_SCORE_TEXT, (500, 10))

def main():
    clock = pygame.time.Clock()
    run = True
    frame_count = 0
    player1 = Player("Player 1", PLAYER1_IMG, 20, 200)
    player2 = Player("Player 2", PLAYER2_IMG, 760, 200)
    ball = Ball(BALL_IMG, 385, 250)
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_w:
            #         player1.move(UP)
            #     elif event.key == pygame.K_s:
            #         player1.move(DOWN)
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            player1.move(UP)
        if pressed[pygame.K_s]:
            player1.move(DOWN)
        if pressed[pygame.K_UP]:
            player2.move(UP)
        if pressed[pygame.K_DOWN]:
            player2.move(DOWN)

        ball.check_bounce((player1, player2))
        try:
            if ball.check_point() == 1:
                assert player1.score < 9
                player1.score += 1
                ball.x = 385
                ball.y = 280
                frame_count = 0
            elif ball.check_point() == 2:
                assert player2.score < 9
                player2.score += 1
                ball.x = 385
                ball.y = 280
                frame_count = 0
        except AssertionError:
            WIN_TEXT = FONT.render(f"Game Over, {max(player1, player2)} has won!", True, WHITE)
            WIN.blit(WIN_TEXT, (400 - (WIN_TEXT.get_width() / 2), (250 - WIN_TEXT.get_height() / 2)))
            pygame.display.flip()
            sleep(2)
            run = False
        if frame_count >= 120: ball.move()
        draw_win(WIN, (player1, player2))
        pygame.display.flip()
        frame_count += 1

if __name__ == "__main__":
    main()