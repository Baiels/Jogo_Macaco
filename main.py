import os
import random
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
window_width, window_height = screen_width - 800, screen_height - 150

timer = pygame.time.Clock()
fps = 60

pygame.display.set_caption('Jogo do macaco')
font = pygame.font.Font('freesansbold.ttf', 50)
font2 = pygame.font.Font('freesansbold.ttf', 30)

screen = pygame.display.set_mode([window_width, window_height])
section_width = window_width // 32
section_height = window_height // 32
slope = section_height // 8

barrel_spawn_time = 360
barrel_count = barrel_spawn_time / 2
barrel_time = 360
barrel_img = pygame.transform.scale(pygame.image.load('assets/images/barrels/barrel.png'),
                                    (section_width * 1.5, section_height * 2))
barrel_side = pygame.transform.scale(pygame.image.load('assets/images/barrels/barrel2.png'),
                                 (section_width * 2, section_height * 2.5))
dk = pygame.transform.scale(pygame.image.load('assets/images/dk/dk.png'),
                          (section_width * 5, section_height * 5))
peach1 = pygame.transform.scale(pygame.image.load('assets/images/peach/peach1.png'),
                                (2 * section_width, 3 * section_height))
standing = pygame.transform.scale(pygame.image.load('assets/images/mario/standing.png'),
                                  (2 * section_width, 2.5 * section_height))
jumping = pygame.transform.scale(pygame.image.load('assets/images/mario/jumping.png'),
                                 (2 * section_width, 2.5 * section_height))

start_y = window_height - 2 * section_height
row2_y = start_y - 4 * section_height
row3_y = row2_y - 7 * slope - 3 * section_height
row4_y = row3_y - 4 * section_height
row5_y = row4_y - 7 * slope - 3 * section_height
row6_y = row5_y - 4 * section_height
row6_top = row6_y - 4 * slope
row5_top = row5_y - 8 * slope
row4_top = row4_y - 8 * slope
row3_top = row3_y - 8 * slope
row2_top = row2_y - 8 * slope
row1_top = start_y - 5 * slope
active_level = 0
counter = 0
score = 0
high_score = 0
lives = 5
bonus = 6000
victory = False
reset_game = False
levels = [
    {'bridges': [(1, start_y, 15), (16, start_y - slope, 3),
                 (19, start_y - 2 * slope, 3), (22, start_y - 3 * slope, 3),
                 (25, start_y - 4 * slope, 3), (28, start_y - 5 * slope, 3),
                 (25, row2_y, 3), (22, row2_y - slope, 3),
                 (19, row2_y - 2 * slope, 3), (16, row2_y - 3 * slope, 3),
                 (13, row2_y - 4 * slope, 3), (10, row2_y - 5 * slope, 3),
                 (7, row2_y - 6 * slope, 3), (4, row2_y - 7 * slope, 3),
                 (2, row2_y - 8 * slope, 2), (4, row3_y, 3),
                 (7, row3_y - slope, 3), (10, row3_y - 2 * slope, 3),
                 (13, row3_y - 3 * slope, 3), (16, row3_y - 4 * slope, 3),
                 (19, row3_y - 5 * slope, 3), (22, row3_y - 6 * slope, 3),
                 (25, row3_y - 7 * slope, 3), (28, row3_y - 8 * slope, 2),
                 (25, row4_y, 3), (22, row4_y - slope, 3),
                 (19, row4_y - 2 * slope, 3), (16, row4_y - 3 * slope, 3),
                 (13, row4_y - 4 * slope, 3), (10, row4_y - 5 * slope, 3),
                 (7, row4_y - 6 * slope, 3), (4, row4_y - 7 * slope, 3),
                 (2, row4_y - 8 * slope, 2), (4, row5_y, 3),
                 (7, row5_y - slope, 3), (10, row5_y - 2 * slope, 3),
                 (13, row5_y - 3 * slope, 3), (16, row5_y - 4 * slope, 3),
                 (19, row5_y - 5 * slope, 3), (22, row5_y - 6 * slope, 3),
                 (25, row5_y - 7 * slope, 3), (28, row5_y - 8 * slope, 2),
                 (25, row6_y, 3), (22, row6_y - slope, 3),
                 (19, row6_y - 2 * slope, 3), (16, row6_y - 3 * slope, 3),
                 (2, row6_y - 4 * slope, 14), (13, row6_y - 4 * section_height, 6),
                 (10, row6_y - 3 * section_height, 3)],
     'ladders': [(12, row2_y + 6 * slope, 2), (12, row2_y + 26 * slope, 2),
                 (25, row2_y + 11 * slope, 4), (6, row3_y + 11 * slope, 3),
                 (14, row3_y + 8 * slope, 4), (10, row4_y + 6 * slope, 1),
                 (10, row4_y + 24 * slope, 2), (16, row4_y + 6 * slope, 5),
                 (25, row4_y + 9 * slope, 4), (6, row5_y + 11 * slope, 3),
                 (11, row5_y + 8 * slope, 4), (23, row5_y + 4 * slope, 1),
                 (23, row5_y + 24 * slope, 2), (25, row6_y + 9 * slope, 4),
                 (13, row6_y + 5 * slope, 2), (13, row6_y + 25 * slope, 2),
                 (18, row6_y - 27 * slope, 4), (12, row6_y - 17 * slope, 2),
                 (10, row6_y - 17 * slope, 2), (12, -5, 13), (10, -5, 13)],
     'target': (13, row6_y - 4 * section_height, 3)}]


class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.y_change = 0
        self.x_speed = 3
        self.x_change = 0
        self.landed = False
        self.pos = 0
        self.dir = 1
        self.count = 0
        self.climbing = False
        self.image = standing
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.rect.center = (x_pos, y_pos)
        self.over_barrel = False
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)

    def update(self):
        self.landed = False
        for i in range(len(plats)):
            if self.bottom.colliderect(plats[i]):
                self.landed = True
                if not self.climbing:
                    self.rect.centery = plats[i].top - self.rect.height / 2 + 1
        if not self.landed and not self.climbing:
            self.y_change += 0.25
        self.rect.move_ip(self.x_change * self.x_speed, self.y_change)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)
        if self.x_change != 0 or (self.climbing and self.y_change != 0):
            if self.count < 3:
                self.count += 1
            else:
                self.count = 0
                if self.pos == 0:
                    self.pos += 1
                else:
                    self.pos = 0
        else:
            self.pos = 0

    def draw(self):
        if not self.climbing and self.landed:
            if self.pos == 0:
                self.image = standing

        if not self.landed and not self.climbing:
            self.image = jumping


        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image
        self.calc_hitbox()

        screen.blit(self.image, self.rect.topleft)

    def calc_hitbox(self):
        self.hitbox = pygame.rect.Rect((self.rect[0] + 15, self.rect[1] + 5),
                                       (self.rect[2] - 30, self.rect[3] - 10))


class Barrel(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.y_change = 0
        self.x_change = 1
        self.pos = 0
        self.count = 0
        self.falling = False
        self.check_lad = False
        self.bottom = self.rect

    def update(self):
        if self.y_change < 8 and not self.falling:
            barrel.y_change += 2
        for i in range(len(plats)):
            if self.bottom.colliderect(plats[i]):
                self.y_change = 0
                self.falling = False

        if not self.falling:
            if row5_top >= self.rect.bottom or row3_top >= self.rect.bottom >= row4_top or row1_top > self.rect.bottom >= row2_top:
                self.x_change = 3
            else:
                self.x_change = -3
        else:
            self.x_change = 0
        self.rect.move_ip(self.x_change, self.y_change)
        if self.rect.top > screen_height:
            self.kill()
        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            if self.x_change > 0:
                if self.pos < 3:
                    self.pos += 1
                else:
                    self.pos = 0
            else:
                if self.pos > 0:
                    self.pos -= 1
                else:
                    self.pos = 3
        self.bottom = pygame.rect.Rect((self.rect[0], self.rect.bottom), (self.rect[2], 3))
        return False

    def check_fall(self):
        already_collided = False
        below = pygame.rect.Rect((self.rect[0], self.rect[1] + section_height), (self.rect[2], section_height))
        for lad in lads:
            if below.colliderect(lad) and not self.falling and not self.check_lad:
                self.check_lad = True
                already_collided = True
                if random.randint(0, 60) == 60:
                    self.falling = True
                    self.y_change = 4
        if not already_collided:
            self.check_lad = False

    def draw(self):
        screen.blit(pygame.transform.rotate(barrel_img, 90 * self.pos), self.rect.topleft)


class Bridge:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.top = self.draw()

    def draw(self):
        line_width = 7
        platform_color = (225, 51, 129)
        for i in range(self.length):
            bot_coord = self.y_pos + section_height
            left_coord = self.x_pos + (section_width * i)
            mid_coord = left_coord + (section_width * 0.5)
            right_coord = left_coord + section_width
            top_coord = self.y_pos
            pygame.draw.line(screen, platform_color, (left_coord, top_coord),
                             (right_coord, top_coord), line_width)
        top_line = pygame.rect.Rect((self.x_pos, self.y_pos), (self.length * section_width, 2))
        return top_line


class Ladder:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.body = self.draw()

    def draw(self):
        line_width = 3
        lad_color = 'light blue'
        lad_height = 0.6
        for i in range(self.length):
            top_coord = self.y_pos + lad_height * section_height * i
            bot_coord = top_coord + lad_height * section_height
            mid_coord = (lad_height / 2) * section_height + top_coord
            left_coord = self.x_pos
            right_coord = left_coord + section_width
            pygame.draw.line(screen, lad_color, (left_coord, top_coord), (left_coord, bot_coord), line_width)
            pygame.draw.line(screen, lad_color, (right_coord, top_coord), (right_coord, bot_coord), line_width)
            pygame.draw.line(screen, lad_color, (left_coord, mid_coord), (right_coord, mid_coord), line_width)
        body = pygame.rect.Rect((self.x_pos, self.y_pos - section_height),
                                (section_width, (lad_height * self.length * section_height + section_height)))
        return body


def draw_screen():
    platforms = []
    climbers = []
    ladder_objs = []
    bridge_objs = []

    ladders = levels[active_level]['ladders']
    bridges = levels[active_level]['bridges']

    for ladder in ladders:
        ladder_objs.append(Ladder(*ladder))
        if ladder[2] >= 3:
            climbers.append(ladder_objs[-1].body)
    for bridge in bridges:
        bridge_objs.append(Bridge(*bridge))
        platforms.append(bridge_objs[-1].top)

    return platforms, climbers


def draw_extras():
    screen.blit(peach1, (10 * section_width, row6_y - 6 * section_height))
    draw_kong()
    return

def draw_kong():
    phase_time = barrel_time // 4
    screen.blit(dk, (3.5 * section_width, row6_y - 5.5 * section_height))


def check_climb():
    can_climb = False
    climb_down = False
    under = pygame.rect.Rect((player.rect[0], player.rect[1] + 2 * section_height), (player.rect[2], player.rect[3]))
    for lad in lads:
        if player.hitbox.colliderect(lad) and not can_climb:
            can_climb = True
        if under.colliderect(lad):
            climb_down = True
    if (not can_climb and (not climb_down or player.y_change < 0)) or \
            (player.landed and can_climb and player.y_change > 0 and not climb_down):
        player.climbing = False
    return can_climb, climb_down


def barrel_collide(reset):
    global score
    under = pygame.rect.Rect((player.rect[0], player.rect[1] + 2 * section_height), (player.rect[2], player.rect[3]))
    for brl in barrels:
        if brl.rect.colliderect(player.hitbox):
            reset = True
        elif not player.landed and not player.over_barrel and under.colliderect(brl):
            player.over_barrel = True
            score += 100
    if player.landed:
        player.over_barrel = False

    return reset


def reset():
    global player, barrels, victory, lives, bonus
    global barrel_spawn_time, barrel_count
    pygame.time.delay(1000)
    for bar in barrels:
        bar.kill()
    lives -= 1
    bonus = 6000
    player.kill()
    player = Player(250, window_height - 130)
    first_fireball_trigger = False
    barrel_spawn_time = 360
    barrel_count = barrel_spawn_time / 2
    victory = False


def check_victory():
    target = levels[active_level]['target']
    target_rect = pygame.rect.Rect((target[0] * section_width, target[1]), (section_width * target[2], 1))
    return player.bottom.colliderect(target_rect)


barrels = pygame.sprite.Group()
player = Player(250, window_height - 130)

run = True
while run:
    screen.fill('black')
    timer.tick(fps)
    if counter < 60:
        counter += 1
    else:
        counter = 0
        if bonus > 0:
            bonus -= 100

    plats, lads = draw_screen()

    draw_extras()

    climb, down = check_climb()
    victory = check_victory()
    if barrel_count < barrel_spawn_time:
        barrel_count += 1
    else:
        barrel_count = random.randint(0, 120)
        barrel_time = barrel_spawn_time - barrel_count
        barrel = Barrel(270, 270)
        barrels.add(barrel)

    for barrel in barrels:
        barrel.draw()
        barrel.check_fall()
        barrel.update()

    player.update()
    player.draw()

    reset_game = barrel_collide(reset_game)
    if reset_game:
        if lives > 0:
            reset()
            reset_game = False
        else:
            run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not player.climbing:
                player.x_change = 1
                player.dir = 1
            if event.key == pygame.K_LEFT and not player.climbing:
                player.x_change = -1
                player.dir = -1
            if event.key == pygame.K_SPACE and player.landed:
                player.landed = False
                player.y_change = -6
            if event.key == pygame.K_UP:
                if climb:
                    player.y_change = -2
                    player.x_change = 0
                    player.climbing = True
            if event.key == pygame.K_DOWN:
                if down:
                    player.y_change = 2
                    player.x_change = 0
                    player.climbing = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.x_change = 0
            if event.key == pygame.K_LEFT:
                player.x_change = 0
            if event.key == pygame.K_UP:
                if climb:
                    player.y_change = 0
                if player.climbing and player.landed:
                    player.climbing = False
            if event.key == pygame.K_DOWN:
                if climb:
                    player.y_change = 0
                if player.climbing and player.landed:
                    player.climbing = False
    if victory:
        screen.blit(font.render('VICTORY!', True, 'white'), (window_width / 2, window_height / 2))
        reset_game = True
        lives += 1
        score += bonus
        if score > high_score:
            high_score = score
        score = 0
        player.climbing = False

    pygame.display.flip()
pygame.quit()
