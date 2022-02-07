import pygame as pg
import pygame.mixer
import sys
import random
import time

pg.init()
pg.font.init()
pg.mixer.init()
#pg.mixer.music.load("/Users/a123/Documents/ics/finalv/Dark_Tranquility.mp3")
#pick_sound = pg.mixer.Sound('/Users/a123/Documents/ics/finalv/Glass_and_Metal_Collision.wav')
clock = pg.time.Clock()
pg.mixer.pre_init(44100, 16, 2, 4096)

gameDisplay = pygame.display.set_mode((600, 500))
pg.mixer.music.set_volume(0.9)
pg.mixer.music.play(-1)

# pg.mixer.Sound('background_music.mp3').play()
game_window = pg.display.set_mode((600, 500))
pg.display.set_caption('pick up the ball !!')
window_color = (230, 230, 250)
ball_color = (165, 42, 42)
rect_color = (0, 0, 0)
score = 0
font = pg.font.Font(None, 60)  # （字体，大小）
font1 = pg.font.Font(None, 30)
# ball_x = random.randint(20, 580)
# ball_y = 20
# move_x = 3
# move_y = 3
# mouse_x = 0
# keymove_x = 7
# keymove_y = 7
# point = 1
# count = 0
name = 'your score:\n'


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def quitgame():
    pg.quit()
    # quit()


def myscore(point):
    global score
    score += point


def unpause():
    global pause
    pause = False


def paused():
    largeText = pg.font.SysFont("comicsans", 115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = (300, 250)
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pg.event.get():
            # print(event)
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            # gameDisplay.fill(white)
        # button((0,255,0), 50, 50, 100, 80,'Click Me!!')
        button("Continue", 100, 360, 140, 70, (255, 255, 255), (253, 245, 230), unpause)
        button("Quit", 360, 360, 140, 70, (255, 255, 255), (253, 245, 230), quitgame)
        pg.display.update()
        clock.tick(15)


def game_over():
    largeText = pg.font.SysFont("comicsans", 115)
    smallText = pg.font.SysFont('comicsansms', 40)
    TextSurf, TextRect = text_objects("Game Over", largeText)
    TextRect.center = (300, 250)
    gameDisplay.blit(TextSurf, TextRect)

    while over:
        for event in pg.event.get():
            # print(event)
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        button("Quit", 230, 360, 140, 70, (255, 255, 255), (253, 245, 230), quitgame)
        pg.display.update()
        clock.tick(15)


def button(msg, x, y, w, h, ic, ac, action=None):
    global pause
    global over
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:

        pg.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == unpause:
                action()
                return
            elif action == paused:
                pause = True
                paused()
            elif action == quitgame:
                quitgame()
    else:
        pg.draw.rect(gameDisplay, ic, (x, y, w, h))
    smallText = pg.font.SysFont('comicsansms', 40)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


run = True
pause = False
over = False


def game_loop():
    global pause
    global run
    global score
    global over
    ball_x = random.randint(20, 580)
    ball_y = 20
    move_x = 3
    move_y = 3
    mouse_x = 0
    keymove_x = 7
    keymove_y = 7
    point = 1
    count = 0

    while run:
        game_window.fill(window_color)
        for event in pg.event.get():
            pos = pg.mouse.get_pos()
            if event.type == pg.QUIT:
                run = False
                pg.quit()

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            if mouse_x >= keymove_x:
                mouse_x -= keymove_x
        if keys[pg.K_RIGHT]:
            if mouse_x <= 500 - keymove_x:
                mouse_x += keymove_x
        if keys[pg.K_p]:
            pause = True
            paused()

        button("pause!", 10, 20, 100, 50, (255, 255, 255), (255, 248, 220), paused)
        button("quit", 10, 100, 100, 50, (255, 255, 255), (255, 248, 220), quitgame)

        mousex, mousey = pg.mouse.get_pos()  # return the position of the mouse
        pg.draw.circle(game_window, ball_color, (ball_x, ball_y), 18)
        pg.draw.rect(game_window, rect_color, (mouse_x, 490, 100, 10))  # 定位在左上角
        my_text = font.render(str(score), True, (160, 82, 45))
        game_window.blit(my_text, (490, 50))  # 文字位置的横纵坐标
        my_text1 = font1.render(name, True, (160, 82, 45))
        game_window.blit(my_text1, (460, 20))
        ball_x += move_x
        ball_y += move_y
        if ball_x <= 20 or ball_x >= 580:
            move_x = -move_x
        if ball_y <= 20:
            move_y = -move_y
        elif mouse_x < ball_x < mouse_x + 100 and ball_y >= 470:
            pg.mixer.Sound.play(pick_sound)
            time.sleep(0.001)
            move_y = -move_y
            myscore(point)
            # score += point
            count += 1
            if count == 2:
                count = 0
                point += point
                if move_x > 0:
                    move_x += 1
                else:
                    move_x -= 1
                move_y -= 1
        elif ball_y >= 480 and (ball_x <= mouse_x or ball_x >= mouse_x + 100):
            over = True
            # game_over()
            return score
            break
        pg.display.update()  # keep update,不会一闪而过
        time.sleep(0.001)  # 每隔0.005s循环一次

# game_loop()
# print(game_loop())

