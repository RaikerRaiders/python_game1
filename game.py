import pygame
import random2

pygame.init()
width = 1280
height = 554
disp = pygame.display.set_mode((width, height))
pygame.display.set_caption("Among Us Red Player vs Impostors!")

playerWalkRight = [pygame.image.load("player/player_pos_move1.png"),
                   pygame.image.load("player/player_pos_move2.png"),
                   pygame.image.load("player/player_pos_move3.png"),
                   pygame.image.load("player/player_pos_move4.png")]
playerWalkLeft = list(map(lambda x: pygame.transform.flip(x, True, False),
                          [playerWalkRight[0],
                           playerWalkRight[1],
                           playerWalkRight[2],
                           playerWalkRight[3]]))
enemyWalkRight = [pygame.image.load("enemy/enemy_pos_move1.png"),
                  pygame.image.load("enemy/enemy_pos_move2.png"),
                  pygame.image.load("enemy/enemy_pos_move3.png"),
                  pygame.image.load("enemy/enemy_pos_move4.png")]
enemyWalkLeft = list(map(lambda x: pygame.transform.flip(x, True, False),
                         [enemyWalkRight[0],
                          enemyWalkRight[1],
                          enemyWalkRight[2],
                          enemyWalkRight[3]]))

playerStandRight = pygame.image.load("player/player_pos_passive.png")
playerStandLeft = pygame.transform.flip(playerStandRight, True, False)
playerStand = playerStandLeft
enemyStand = pygame.image.load("enemy/enemy_pos_passive.png")
enemy_dead = pygame.image.load("enemy/enemy_pos_dead.png")
back = pygame.image.load("maps/back.png")
st_skill = pygame.image.load("maps/skill_1.png")
knifeLeftPos = pygame.image.load("player/player_weapon_knife.png")
knifeRightPos = pygame.transform.flip(knifeLeftPos, True, False)
knifeStand = knifeLeftPos

playerHealthBarEmpty = pygame.image.load("player/player_hpBarEmpty.png")
playerHealthBarFull = pygame.image.load("player/player_hpBarFull.png")
playerHealthBarWidth = 505
playerHealthBarHigh = 60

cloneCount = 0


class Player:
    def __init__(self):
        self.x = 1080
        self.y = 267
        self.width = 161
        self.high = 208
        self.speed = 18
        self.life = 100
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.isJump = False
        self.animCount = 0

    def spawnPlayer(self):
        global playerStand, knifeStand
        keys = pygame.key.get_pressed()

        if self.animCount + 1 >= 60:
            self.animCount = 0

        if self.right:
            disp.blit(playerWalkRight[self.animCount // 15], (self.x, self.y))
            self.animCount += 1
            playerStand = playerStandRight
            knifeStand = knifeRightPos
        elif self.left:
            disp.blit(playerWalkLeft[self.animCount // 15], (self.x, self.y))
            self.animCount += 1
            playerStand = playerStandLeft
            knifeStand = knifeLeftPos
        else:
            disp.blit(playerStand, (self.x, self.y))

        if keys[pygame.K_a] and self.x >= 10:
            self.x -= self.speed
            self.left = True
            self.right = False
        elif keys[pygame.K_d] and self.x <= 1270 - 166:
            self.x += self.speed
            self.right = True
            self.left = False
        else:
            self.right = False
            self.left = False
            self.animCount = 0

        if keys[pygame.K_v]:
            self.speed += 5
        elif keys[pygame.K_c]:
            self.speed -= 5

        if not self.isJump:
            if keys[pygame.K_SPACE]:
                self.isJump = True
        else:
            if self.jumpCount >= -10:
                if self.jumpCount < 0:
                    self.y += (self.jumpCount ** 2) / 2
                else:
                    self.y -= (self.jumpCount ** 2) / 2
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10


player = Player()


class Knife:
    def __init__(self):
        self.x = player.x
        self.y = player.y + 90
        self.speed = 29
        self.destination = 0.5

    def draw(self):
        global mousePosX

        self.x += self.speed * (int(self.destination) * 2 - 1)
        disp.blit([knifeLeftPos, knifeRightPos][int(self.destination)], (self.x, self.y))


knifes = []


class Bar:
    def __init__(self):
        self.barHigh = 20
        self.barWidth = 180
        self.barEmpty = pygame.image.load("enemy/enemy_hpBarEmpty.png")
        self.barFull = pygame.image.load("enemy/enemy_hpBarFull.png")




class Enemy:
    def __init__(self):
        self.x = random2.randrange(-161, 200)
        self.y = 267
        self.speed = random2.randint(10, 16)
        self.animCount = 0
        self.right = False
        self.left = False
        self.enemyLife = 30
        self.bar = None
        self.alive = True

    def spawn(self):
        if self.alive:
            if self.animCount + 1 >= 60:
                self.animCount = 0

            if self.right:
                disp.blit(enemyWalkRight[self.animCount // 15], (self.x, self.y))
                self.animCount += 1
            elif self.left:
                disp.blit(enemyWalkLeft[self.animCount // 15], (self.x, self.y))
                self.animCount += 1
            else:
                disp.blit(enemyStand, (self.x, self.y))

            if self.x < player.x:
                self.x += self.speed
                self.right = True
                self.left = False
            elif self.x > player.x:
                self.x -= self.speed
                self.right = False
                self.left = True
            else:
                self.right = False
                self.left = False
                self.animCount = 0
        else:
            disp.blit(enemy_dead, (self.x, self.y))

    def enemyDamage(self):
        global run
        global playerHealthBarWidth
        if abs(player.x - self.x) <= 40 and abs(player.y - self.y) <= 80:
            player.life -= 1
            playerHealthBarWidth -= 5
        if player.life == 0:
            run = False

    def collide(self):
        for knife in knifes:
            if abs(knife.x - self.x) <= 120 and knife.y >= self.y:
                return True

    def kill(self):
        if self.enemyLife <= 0 or self.bar.barWidth < 5:
            self.alive = False
        elif self.collide():
            self.enemyLife -= 1
            self.bar.barWidth = self.enemyLife * 6 * int(self.enemyLife > 0)
            create_particles((self.x, self.y))
            print(self.enemyLife, self.bar.barWidth)

    def show_hp(self):
        disp.blit(pygame.transform.scale(self.bar.barEmpty, (180, 20)), (self.x - 15, self.y - 15))
        disp.blit(pygame.transform.scale(self.bar.barFull, (self.bar.barWidth, self.bar.barHigh)),
                  (self.x - 15, self.y - 15))


enemies = []


def spawn_newEnemy():
    global cloneCount
    if cloneCount == 0:
        enemyf = Enemy()
        enemies.append(enemyf)
        enemyf.bar = Bar()
        enemyf.spawn()
        if enemyf.alive:
            enemyf.show_hp()
            enemyf.enemyDamage()
            enemyf.kill()
        cloneCount = 360
        print(enemyf.enemyLife, enemyf.bar.barWidth)
    else:
        for enemyg in enemies:
            enemyg.spawn()
            if enemyg.alive:
                enemyg.enemyDamage()
                enemyg.kill()
                enemyg.show_hp()
        cloneCount -= 1


screen_rect = (0, 0, width, height)


class Particle(pygame.sprite.Sprite):
    fire = [pygame.image.load("enemy/blood.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = random2.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 2

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random2.choice(numbers), random2.choice(numbers))


def drawWindow():
    disp.blit(back, (0, 0))
    disp.blit(st_skill, (20, 20))
    disp.blit(pygame.transform.scale(playerHealthBarEmpty, (505, 60)), (388, 30))
    disp.blit(pygame.transform.scale(playerHealthBarFull, (playerHealthBarWidth, playerHealthBarHigh)), (388, 30))
    player.spawnPlayer()
    for knife in knifes:
        knife.draw()

    spawn_newEnemy()

    pygame.display.update()


clock = pygame.time.Clock()
run = True

while run:
    clock.tick(60)
    for event in pygame.event.get():
        keysMouse = pygame.mouse.get_pressed()
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and keysMouse[0]:
            knife2 = Knife()
            knifes.append(knife2)
            if mousePosX > player.x:
                knife2.destination = True
            else:
                knife2.destination = False
    mousePosX = pygame.mouse.get_pos()[0]
    mousePosY = pygame.mouse.get_pos()[1]
    drawWindow()
pygame.quit()
