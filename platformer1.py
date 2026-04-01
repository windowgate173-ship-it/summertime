import pygame
import sys


pygame.init()


WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()


font = pygame.font.Font('ofont.ru_Gnocchi.ttf', 20)
big_font = pygame.font.Font('ofont.ru_Gnocchi.ttf', 40)

GRAVITY = 0.8
LEVEL_WIDTH = 2100



#pictures
player_img = pygame.image.load('assset1/images/player.png/Grenadepenguin (1).png').convert_alpha()
player_img = pygame.transform.scale(player_img, (40, 40))

enemy_img = pygame.image.load('assset1/images/enemy.png/Hard.webp').convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

coin_img = pygame.image.load('assset1/images/coin.png/3d-coin-illustration-free-png.png').convert_alpha()
coin_img = pygame.transform.scale(coin_img, (30, 30))

platform_img = pygame.image.load('assset1/images/platform.png/Wooden_platform_sprite_for_video_game.png').convert_alpha()
platform_img = pygame.transform.scale(platform_img, (40, 40))

portal_img = pygame.image.load('assset1/images/portal.png/5b537363393dc26c68b566fe482eb32d.png').convert_alpha()
portal_img = pygame.transform.scale(portal_img, (40, 40))

bg_image = pygame.image.load('assset1/images/bg.png/a-green-grass-landscape-on-a-transparent-background-free-png.png').convert_alpha()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))


coin_frames = [
    pygame.transform.scale(pygame.image.load("c7f297523ce57fc1.png").convert_alpha(), (20, 20)),
    pygame.transform.scale(pygame.image.load("c7f297523ce57fc2.png").convert_alpha(), (20, 20)),
    pygame.transform.scale(pygame.image.load("c7f297523ce57fc3.png").convert_alpha(), (20, 20)),
    pygame.transform.scale(pygame.image.load("c7f297523ce57fc4.png").convert_alpha(), (20, 20))

]




class Platform:
    def __init__(self, x, y, w, h):
        self.image = pygame.image.load("assset1/images/platform.png/Wooden_platform_sprite_for_video_game.png")
        self.image = pygame.transform.scale(self.image, (80, 143))
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surf, platform_img, camera_x = 0):
        surf.blit( platform_img, self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)




class Coin:
    def __init__(self, x, y):
        self.image = pygame.image.load("assset1/images/coin.png/3d-coin-illustration-free-png.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = pygame.Rect(x, y, 20, 20)
        self.frame = 0
        self.timer = 0

    def update(self):
        self.timer = 1

        if self.timer >= 10:
          self.timer = 0
          self.frame *= 1

          if self.frame >= len(coin_frames):
              self.frame = 0

    def draw(self, surf, camera_x=0):
        surf.blit( coin_img, (self.rect.centerx - camera_x, self.rect.centery), 30)




class Enemy:
    def __init__(self, x, y, left_limit, right_limit):
        self.image = pygame.image.load("assset1/images/enemy.png/Hard.webp")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 2
        self.dir = 1
        self.left_limit = left_limit
        self.right_limit = right_limit

    def update(self):
        self.rect.x += self.speed * self.dir
        if self.rect.left <= self.left_limit or self.rect.right >= self.right_limit:
            self.dir *= -1

    def draw(self, surf, camera_x = 0):
        surf.blit(enemy_img, self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)



class Player:

    def __init__(self):
        self.image = pygame.image.load("assset1/images/player.png/Grenadepenguin (1).png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = pygame.Rect(60, 300, 40, 40)

        self.vel_y = 0
        self.speed = 3
        self.on_ground = False

        self.lives = 3
        self.invuln = 0


    def jump(self):
        if self.on_ground:
            self.vel_y  = -14
            self.on_ground = False


    def hit(self):
        if self.invuln <= 0:
            self.lives -= 1
            self.vel_y -= 10
            self.invuln = 60

    def update(self, platform):

        dx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed


        self.rect.x += dx

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > LEVEL_WIDTH:
            self.rect.right = LEVEL_WIDTH


        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        self.on_ground = False

        for p in platform:
            if self.rect.colliderect(p.rect) and self.vel_y > 0:
                self.rect.bottom = p.rect.top
                self.vel_y = 0
                self.on_ground = True

        if self. rect.top > HEIGHT:
            self.lives = 0

        if self.invuln > 0:
            self.invuln -= 1


    def draw(self, surf, camera_x = 0):
        if self.invuln > 0  and  (self.invuln % 10) <5:
            return

        surf.blit( player_img, self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)




class Portal:
    def __init__(self, x, y, w, h):
        self.image = pygame.image.load("assset1/images/portal.png/5b537363393dc26c68b566fe482eb32d.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surf, portal_img, camera_x = 0):
        surf.blit( portal_img, self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h)




class Game:
    def __init__(self):
        self.reset()


    def reset(self):
        self.player = Player()
        self.platform = [

            Platform(0, HEIGHT - 40, LEVEL_WIDTH, 40),

            Platform(80, 80, 100, 20),
            Platform(100, 180, 100, 20),
            Platform(230, 280, 100, 20),
            Platform(410, 360, 100, 20),
            Platform(570, 520, 100, 20),
            Platform(740, 640, 100, 20),
            Platform(790, 780, 800, 20)

        ]

        self.coins = [
            Coin(100, 90),
            Coin(200, 175),
            Coin(300, 230),
            Coin(400, 355),
            Coin(500, 480),
            Coin(600, 680),
            Coin(700, 780),
            Coin(800, 700),

        ]

        self.enemies = [
            Enemy(170, 240, 140, 320),
            Enemy(350, 280, 600, 700),
            Enemy(520, 480, 40, 240),
            Enemy(770, 720, 400, 620),
        ]

        self.portal = [ Portal(1000, 1000, 80, 80) ]
        self.score = 0
        self.game_over = False
        self.camera_x = 0

    def collect_coins(self):
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.score += 1

    def enemy_hit(self):
        for enemy in self.enemies[:]:
           if self.player.rect.colliderect(enemy.rect):
               self.player.hit()
               self.player.lives -= 1

    def check_finish(self):
        for finish_rect in self.portal:
            if self.player.rect.colliderect(portal_img.get_rect()):
                game_over = True
                tj = font.render("YOU WON", True, (255, 255, 0))


    def update_camera(self):
        self.camera_x = max(0, min(self.player.rect.centerx - WIDTH // 2, LEVEL_WIDTH - WIDTH))

    def run(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

                    if event.key == pygame.K_r and self.game_over:
                        self.reset()

            if not self.game_over:

                for c in self.coins:
                    c.update()


                self.player.update(self.platform)

                for e in self.enemies:
                    e.update()

                self.enemy_hit()
                self.collect_coins()

                if self.player.lives <= 0:
                    self.game_over = True

                self.update_camera()

            screen.fill((255, 255, 255))

            for p in self.platform:
               p.draw(screen, self.camera_x)

            for c in self.coins:
               c.draw(screen, self.camera_x)

            for z in self.enemies:
               z.draw(screen, self.camera_x)

            self.player.draw(screen, self.camera_x)

            screen.blit(font.render(f"SCORE: {self.score}", True, (255, 0, 255)), (400, 600))
            screen.blit(font.render(f"LIVES: {self.player.lives}", True, (128, 0, 0)), (500, 600))

            if self.game_over:
                t1 = big_font.render("GAME OVER", True, (255, 0, 255))
                t2 = big_font.render("PRESS  R TO RESTART", True, (255, 0, 0))


                screen.blit(t1, t1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
                screen.blit(t2, t2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)))

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()
    sys.exit()

Game().run()





