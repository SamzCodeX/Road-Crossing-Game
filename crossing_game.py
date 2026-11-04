from pygame import *

init()

width = 600
height = 500
window = display.set_mode((width,height))
display.set_caption('Road-Crossing Game')
clock = time.Clock()

green = (80,180,80)
road = (70,70,70)
white = (255,255,255)
yellow = (255,220,0)
red = (255,0,0)
black = (0,0,0)

class Player(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = transform.scale(image.load('rocket.png'),(45,45))
        self.rect = self.image.get_rect()
        self.rect.x = 280
        self.rect.y = 440
        self.speed = 5

    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < width - self.rect.width:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < height - self.rect.height:
            self.rect.y += self.speed


class Car(sprite.Sprite):
    def __init__(self,x,y,speed):
        super().__init__()
        self.image = transform.scale(image.load('ufo.png'),(70,45))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.base_speed = speed
        self.speed = speed

    def update(self):
        self.rect.x += self.speed

        if self.speed > 0 and self.rect.x > width:
            self.rect.x = -self.rect.width

        if self.speed < 0 and self.rect.x < -self.rect.width:
            self.rect.x = width


font.init()
game_font = font.SysFont('Arial',35)
small_font = font.SysFont('Arial',23)

try:
    fire_sound = mixer.Sound('fire.ogg')
    mixer.music.load('space.ogg')
    mixer.music.play(-1)
except:
    fire_sound = None

player = Player()

cars = sprite.Group()

car1 = Car(0,350,4)
car2 = Car(250,260,-5)
car3 = Car(450,170,3)

cars.add(car1,car2,car3)

score = 0
level = 1
target_score = 20
level_time = 30

start_time = time.get_ticks()

game = True
finish = False
result = ''

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False

            if finish and e.key == K_r:
                score = 0
                level = 1
                target_score = 20
                player.rect.x = 280
                player.rect.y = 440
                start_time = time.get_ticks()
                finish = False
                result = ''

                car1.speed = car1.base_speed
                car2.speed = car2.base_speed
                car3.speed = car3.base_speed

                mixer.music.play(-1)

    if not finish:

        window.fill(green)

        draw.rect(window,road,(0,130,600,280))

        for y in [220,310]:
            for x in range(0,600,80):
                draw.rect(window,yellow,(x,y,40,5))

        elapsed_time = (time.get_ticks() - start_time) // 1000
        remaining_time = max(0,level_time - elapsed_time)

        player.update()
        cars.update()

        if sprite.spritecollide(player,cars,False):
            if fire_sound:
                fire_sound.play()

            score = max(0,score - 5)
            player.rect.x = 280
            player.rect.y = 440

        if player.rect.y <= 0:
            score += 10
            player.rect.x = 280
            player.rect.y = 440

        if score >= target_score:

            if level == 5:
                finish = True
                result = 'WIN!'
                mixer.music.stop()

            else:
                level += 1
                target_score += 20
                start_time = time.get_ticks()

                car1.speed = car1.base_speed * level
                car2.speed = car2.base_speed * level
                car3.speed = car3.base_speed * level

                player.rect.x = 280
                player.rect.y = 440

        if remaining_time <= 0 and score < target_score:
            finish = True
            result = 'LOSE!'
            mixer.music.stop()

        cars.draw(window)
        window.blit(player.image,player.rect)

        score_text = small_font.render(
            'Score: ' + str(score),True,white)

        level_text = small_font.render(
            'Level: ' + str(level) + '/5',True,white)

        time_text = small_font.render(
            'Time: ' + str(remaining_time),True,white)

        target_text = small_font.render(
            'Target: ' + str(target_score),True,white)

        window.blit(score_text,(10,10))
        window.blit(level_text,(10,40))
        window.blit(time_text,(450,10))
        window.blit(target_text,(450,40))

    else:

        window.fill(black)

        result_text = game_font.render(result,True,
            (0,255,0) if result == 'WIN!' else red)

        score_text = small_font.render(
            'Final Score: ' + str(score),True,white)

        level_text = small_font.render(
            'Level Reached: ' + str(level),True,white)

        restart_text = small_font.render(
            'Press R to Restart',True,yellow)

        exit_text = small_font.render(
            'Press ESC to Exit',True,white)

        window.blit(result_text,(220,130))
        window.blit(score_text,(210,210))
        window.blit(level_text,(200,250))
        window.blit(restart_text,(190,320))
        window.blit(exit_text,(205,360))

    display.update()
    clock.tick(60)

mixer.music.stop()
quit()
