from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, spr_w, spr_h):
        super().__init__()
        self.spr_w = spr_w
        self.spr_h = spr_h

        self.image = transform.scale(image.load(player_image), (spr_w, spr_h))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'

        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, color, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color = color
        self.width = wall_width
        self.height = wall_height

        self.image = Surface((self.width, self.height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('My little sister and the maze')
display.set_icon(image.load('hero.png'))
background = transform.scale(image.load('background.jpg'), (win_width, win_height))

player = Player('hero.png', 5, win_height - 80, 2, 75, 85)
monster = Enemy('enemy.png', win_width - 80, 280, 2, 55, 55)
final = GameSprite('goal.png', win_width - 120, win_height - 110, 20, 110, 110)

GREEN = (154, 205, 50)
RED = (180, 0, 0)
YELLOW = (255, 215, 0)

w1 = Wall(GREEN, 70, 20, 480, 10)
w2 = Wall(GREEN, 100, 480, 410, 10)
w3 = Wall(GREEN, 100, 150, 10, 330)
w4 = Wall(GREEN, 200, 20, 10, 330)
w5 = Wall(GREEN, 300, 150, 10, 330)
w6 = Wall(GREEN, 400, 20, 10, 330)
w7 = Wall(GREEN, 500, 350, 10, 140)
w8 = Wall(GREEN, 500, 150, 10, 90)

walls = sprite.Group()
walls.add(w1, w2, w3, w4, w5, w6, w7, w8)

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, YELLOW)
lose = font.render('YOU LOSE!', True, RED)

mixer.init()
portal = mixer.Sound('win.ogg')
kick = mixer.Sound('loss.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        monster.update()

        player.reset()
        monster.reset()
        final.reset()

        walls.draw(window)

        if sprite.collide_rect(player, monster) or sprite.spritecollide(player, walls, False):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200, 200))
            portal.play()

    display.update()
    clock.tick(FPS)
