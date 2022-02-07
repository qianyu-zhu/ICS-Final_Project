# encoding:utf-8
import pygame
from pygame.locals import *
import sys
import math
import storn
from socket import *
import select
from tkinter import *

pygame.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#
x = []
y = []
for i in range(0, 15):
    x.append(28 + i * 40)
    y.append(28 + i * 40)


map_chess = {}




def is_empty(me, targert):
    global map_chess
    a = False
    if map_chess[str(me[0]) + '|' + str(me[1])]:
        a = True
    return a


# is there five in a line
def iswin(targert):
    x = []
    y = []
    for i in range(0, 15):
        x.append(28 + i * 40)
    for i in range(0, 15):
        y.append(28 + i * 40)
    for each in targert:
        (a, b) = each.location()

        # x-axis
        num_x = 0
        c = a - 40
        d = a + 40
        while c > 0:
            isbreak = True
            for i in targert:
                if i.location() == (c, b):
                    num_x += 1
                    isbreak = False
            if not isbreak:
                c -= 40
            else:
                break
        while d < 615:
            isbreak = True
            for i in targert:
                if i.location() == (d, b):
                    num_x += 1
                    isbreak = False
            if not isbreak:
                d += 40
            else:
                break
        num_x += 1

        # y-axis
        num_y = 0
        e = b - 40
        f = b + 40
        while e > 0:
            isbreak = True
            for i in targert:
                if i.location() == (a, e):
                    num_y += 1
                    isbreak = False
            if not isbreak:
                e -= 40
            else:
                break
        while f < 615:
            isbreak = True
            for i in targert:
                if i.location() == (a, f):
                    num_y += 1
                    isbreak = False
            if not isbreak:
                f += 40
            else:
                break
        num_y += 1

        # 斜线
        num_en = 0
        c1 = a - 40
        c2 = b - 40
        c3 = a + 40
        c4 = b + 40
        while c1 > 0 and c2 > 0:
            isbreak = True
            for i in targert:
                if i.location() == (c1, c2):
                    num_en += 1
                    isbreak = False
            if not isbreak:
                c1 -= 40
                c2 -= 40
            else:
                break
        while c3 < 615 and c4 < 615:
            isbreak = True
            for i in targert:
                isbreak = True
                if i.location() == (c3, c4):
                    num_en += 1
                    isbreak = False
            if not isbreak:
                c3 += 40
                c4 += 40
            else:
                break
        num_en += 1

        # 斜线
        num_wn = 0
        c5 = a + 40
        c6 = b - 40
        c7 = a - 40
        c8 = b + 40
        while c5 < 615 and c6 > 0:
            isbreak = True
            for i in targert:
                if i.location() == (c5, c6):
                    num_wn += 1
                    isbreak = False
            if not isbreak:
                c5 += 40
                c6 -= 40
            else:
                break
        while c7 > 0 and c8 < 615:
            isbreak = True
            for i in targert:
                isbreak = True
                if i.location() == (c7, c8):
                    num_wn += 1
                    isbreak = False
            if not isbreak:
                c7 -= 40
                c8 += 40
            else:
                break
        num_wn += 1
        if num_x >= 5 or num_y >= 5 or num_en >= 5 or num_wn >= 5:
            return True
    return False


# different situations
def point_value(pos, white_chesses, black_chesses, identify1, identify2):
    value = 0
    for i in range(1,9):
        # *1111_ 活四
        if get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 4, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 5, white_chesses, black_chesses) == 0:
            value += 40000
        # *11112 死四1
        if get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 4, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 5, white_chesses, black_chesses) == identify2:
            value += 30000
        # 1*111 死四2
        if get_point(pos, i, -1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == identify1:
            value += 30000
        # 11*11 死四3
        if get_point(pos, i, -2, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, -1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == identify1:
            value += 30000
        # *111_ 活三1
        if get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 4, white_chesses, black_chesses) == 0:
            value += 20000
        # *1_11_ 活三2
        if get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == 0 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 4, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 5, white_chesses, black_chesses) == 0:
            value += 20000
        # *1112 死三1
        if get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 4, white_chesses, black_chesses) == identify2:
            value += 15000
        # _1_112 死三2
        if get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == 0 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 4, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 5, white_chesses, black_chesses) == identify2:
            value += 15000
        # _11_12 死三3
        if get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == 0 and \
            get_point(pos, i, 4, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 5, white_chesses, black_chesses) == identify2:
            value += 15000
        # 1__11 死三4
        if get_point(pos, i, -1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 1, white_chesses, black_chesses) == 0 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == identify1:
            value += 15000
        # 1_1_1 死三5
        if get_point(pos, i, -1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == 0 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == identify1:
            value += 15000
        # 2_111_2 死三6
        if get_point(pos, i, -1, white_chesses, black_chesses) == identify2 and \
            get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 4, white_chesses, black_chesses) == 0 and \
            get_point(pos, i, 5, white_chesses, black_chesses) == identify2:
            value += 15000
        # __11__ 活二1
        if get_point(pos, i, -1, white_chesses, black_chesses) == 0 and \
            get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == 0 and \
            get_point(pos, i, 4, white_chesses, black_chesses) == 0:
            value += 1000
        # _1_1_ 活二2
        if get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == 0 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 4, white_chesses, black_chesses) == 0:
            value += 1000
        # *1__
        if get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == 0 and \
            get_point(pos, i, 3, white_chesses, black_chesses) == 0:
            value += 30
        # *1_
        if get_point(pos, i, 1, white_chesses, black_chesses) == identify1 and \
            get_point(pos, i, 2, white_chesses, black_chesses) == 0:
            value += 20
        # *1
        if get_point(pos, i, 1, white_chesses, black_chesses) == identify1:
            value += 10
    return value

# how the computer make the choice
def ai(white_chesses, black_chesses, chesses):
    value = max1 = max2 = 0
    pos1 = pos2 = ()

    for i in range(0,15):
        row = 28 + i * 40
        for j in range(0,15):
            col = 28 + j * 40
            pos = (row,col)
            if is_empty(pos, chesses):
                continue
            value = point_value(pos, white_chesses, black_chesses, 1, 2)
            if value > max1:
                max1 = value
                pos1 = (row,col)


    for i in range(0,15):
        for j in range(0,15):
            row = 28 + i * 40
            col = 28 + j * 40
            if is_empty((row,col), chesses):
                continue
            value = point_value((row,col), white_chesses, black_chesses, 2, 1)
            if value > max2:
                max2 = value
                pos2 = (row,col)
    if max1 > max2:
        return pos1
    else:
        return pos2


#1: white, 2: black, 3: no storn
def get_point(pos, src, offset, white_chesses, black_chesses):

    global map_chess
    directions = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
    x1,y1 = pos
    x1 = x1 + directions[src-1][0] * offset * 40
    y1 = y1 + directions[src-1][1] * offset * 40
    if x1 > 588 or y1 > 588 or x1 < 28 or y1 < 28:
        return 5
    else:
        return map_chess[str(x1) + '|' + str(y1)]


def init():
    global map_chess
    for i in x:
        for j in y:
            map_chess[str(i) + '|' + str(j)] = 0


def main():
    BUFSIZ = 2048
    tcpclisock = socket(AF_INET, SOCK_STREAM)

    bg_size = 615, 615

    # IP address
    def gui():
        top = Tk()
        top.title('IP')
        top.geometry('300x200')
        HOST = ''
        POST = 21578
        nonlocal tcpclisock

        def fun():
            nonlocal HOST
            nonlocal POST
            nonlocal tcpclisock
            HOST = E1.get()
            ADDR = (HOST, POST)
            try:
                tcpclisock.connect(ADDR)
                L2 = Label(top, text='', font='华文行楷')
                L2 = Label(top, text='已连接', font='华文行楷')
                L2.grid(row=2, column=1)
            except error:
                L2 = Label(top, text='连接失败', font='华文行楷')
                L2.grid(row=2, column=1)

        L1 = Label(top, text='    IP 地址:', font='宋体', padx=5, pady=30)
        L1.grid(row=1, column=0)
        E1 = Entry(top, font='华文行楷')
        E1.grid(row=1, column=1)
        B1 = Button(top, text='连接', font='宋体', padx=1, command=fun)
        B1.grid(row=2, column=0)

        mainloop()



    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption('Gobang Game')
    bg_image = pygame.image.load('image/backpicture.png').convert_alpha()  # 背景图片

    # music
    bg_sound = pygame.mixer.music.load('sound/justbeme.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    running = True

    clock = pygame.time.Clock()

    inputs = [tcpclisock]

    white_chesses = []
    black_chesses = []
    chesses = []

    is_play = True

    islink = False

    result = False

    black_win = False
    white_win = False

    is_people = False

    is_ai = False

    is_choise = False

    is_have_sound = True

    is_playagain = False

    is_recieve1 = False

    is_recieve2 = False

    # win or lose
    font1 = pygame.font.Font('font/different_fonts.TTF', 30)
    win_text = font1.render(u"You win!!!", True, WHITE)
    win_text_rect = win_text.get_rect()
    win_text_rect.left, win_text_rect.top = (bg_size[0] - win_text_rect.width) // 2, \
                                            (bg_size[1] - win_text_rect.height) // 2
    lose_text = font1.render(u"You lose~~~", True, WHITE)
    lose_text_rect = lose_text.get_rect()
    lose_text_rect.left, lose_text_rect.top = (bg_size[0] - lose_text_rect.width) // 2, \
                                              (bg_size[1] - lose_text_rect.height) // 2
    play_text = font1.render(u"Play Again", True, WHITE)
    play_text_rect = play_text.get_rect()
    menu_text = font1.render(u"Main menue", True, WHITE)
    menu_text_rect = menu_text.get_rect()

    # Main menue
    text1 = font1.render(u"Play with other players", True, WHITE)
    text1_rect = text1.get_rect()
    text1_rect.left, text1_rect.top = (bg_size[0] - text1_rect.width) // 2, \
                                      (bg_size[1] - text1_rect.height) // 2 - 100
    text2 = font1.render(u'Play with computer', True, WHITE)
    text2_rect = text2.get_rect()
    text2_rect.left, text2_rect.top = (bg_size[0] - text1_rect.width) // 2, \
                                      (bg_size[1] - text1_rect.height) // 2
    text3 = font1.render(u'Sound：  on', True, WHITE)
    text3_rect = text3.get_rect()
    text3_rect.left, text3_rect.top = (bg_size[0] - text3_rect.width) // 2, \
                                      (bg_size[1] - text3_rect.height) // 2 + 100
    text4 = font1.render(u'Sound：  off', True, WHITE)
    text4_rect = text4.get_rect()
    text4_rect.left, text4_rect.top = (bg_size[0] - text4_rect.width) // 2, \
                                      (bg_size[1] - text4_rect.height) // 2 + 100
    text5 = font1.render(u"You are just so so~~\n I don't want to play with you", True, WHITE)
    text5_rect = text5.get_rect()
    text5_rect.left, text5_rect.top = (bg_size[0] - text5_rect.width) // 2, \
                                      (bg_size[1] - text5_rect.height) // 2
    text6 = font1.render(u'Here is a challenge from another player', True, WHITE)
    text6_rect = text6.get_rect()
    text6_rect.left, text6_rect.top = (bg_size[0] - text6_rect.width) // 2, \
                                      (bg_size[1] - text6_rect.height) // 2
    text7 = font1.render(u'Accept         Reject and Return to the main menu', True, WHITE)
    text7_rect = text7.get_rect()
    text7_rect.left, text7_rect.top = (bg_size[0] - text7_rect.width) // 2, \
                                      (bg_size[1] - text7_rect.height) // 2 + 100


    # initialize
    init()

    while running:

        screen.blit(bg_image, (0, 0))

        if not is_choise:
            screen.blit(text1, text1_rect)
            screen.blit(text2, text2_rect)
            if not is_have_sound:
                screen.blit(text4, text4_rect)
            else:
                screen.blit(text3, text3_rect)

        # 棋盘
        if is_choise:
            if chesses:
                for i in chesses:
                    screen.blit(i.image, i.image_rect())

        for event in pygame.event.get():
            if event.type == QUIT:
                if is_people:
                    tcpclisock.close()
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:


                    if is_choise:
                        pos = pygame.mouse.get_pos()
                        # is it time to play
                        if is_play and not is_recieve1 and not result:
                            me = storn.Storn_White(pos)
                            if not is_empty(me.location(), chesses):
                                white_chesses.append(me)
                                chesses.append(me)
                                map_chess[str(me.location()[0]) + '|' + str(me.location()[1])] = 1
                                if is_people:
                                    tcpclisock.send(str(pos).encode('utf8'))
                                is_play = False
                            else:
                                del (me)
                    else:
                        pos = pygame.mouse.get_pos()
                        if text1_rect.left <= pos[0] <= text1_rect.left + 170 and \
                                text1_rect.top <= pos[1] <= text1_rect.top + 30:
                            is_choise = True
                            is_people = True
                            gui()
                        if text1_rect.left <= pos[0] <= text1_rect.left + 170 and \
                                text1_rect.top + 100 <= pos[1] <= text1_rect.top + 130:
                            is_choise = True
                            is_ai = True
                        if text1_rect.left <= pos[0] <= text1_rect.left + 160 and \
                                text1_rect.top + 200 <= pos[1] <= text1_rect.top + 230:
                            is_have_sound = not is_have_sound
                            if not is_have_sound:
                                pygame.mixer.stop()
                                pygame.mixer.music.stop()
                            else:
                                pygame.mixer.music.play()

                    # the invitation
                    if result:
                        if not is_recieve1 and not is_recieve2:
                            pos = pygame.mouse.get_pos()
                            if win_text_rect.left < pos[0] < win_text_rect.right - 50 and \
                                    win_text_rect.top < pos[1] < win_text_rect.top + 30:
                                if is_people:
                                    tcpclisock.send('again'.encode('utf8'))
                                if is_ai:
                                    is_playagain = True
                                    is_play = True
                                    result = False
                                    init()

                            if win_text_rect.left < pos[0] < win_text_rect.right and \
                                    win_text_rect.top + 50 < pos[1] < win_text_rect.top + 120:
                                is_people = False
                                if islink:
                                    islink = False
                                    tcpclisock.send('no'.encode('utf8'))
                                tcpclisock.close()
                                main()


                    if is_recieve2:
                        pos = pygame.mouse.get_pos()
                        if text5_rect.left + 150 < pos[0] < text5_rect.left + 250 and \
                            text5_rect.top + 70 < pos[1] < text5_rect.top + 190:
                            main()

                    if is_recieve1:
                        pos = pygame.mouse.get_pos()
                        if text7_rect.left < pos[0] < text7_rect.left + 150 and \
                                text7_rect.top < pos[1] < text7_rect.top + 120:
                            tcpclisock.send('yes'.encode('utf8'))
                            result = False
                            white_win = False
                            black_win = False
                            is_recieve1 = False
                            is_playagain = True
                            is_play = True
                        if text7_rect.left + 190 < pos[0] < text7_rect.left + 330 and \
                                text7_rect.top < pos[1] < text7_rect.top + 120:
                            tcpclisock.send('no'.encode('utf8'))
                            main()

        # computer's choice
        if is_ai and not is_play:
            me = storn.Storn_Black(ai(white_chesses, black_chesses, chesses))
            black_chesses.append(me)
            chesses.append(me)
            map_chess[str(me.location()[0]) + '|' + str(me.location()[1])] = 2
            is_play = True

        # make the choice
        if is_people:
            rs, ws, es = select.select(inputs, [], [], 0)
            for r in rs:
                if r is tcpclisock:
                    try:
                        data = r.recv(BUFSIZ)
                        islink = True
                        disconnected = not data
                        print(data.decode('utf8'))
                        if data.decode('utf8') == 'again':
                            is_recieve1 = True
                        if data.decode('utf8') == 'yes':
                            is_playagain = True
                            is_play = True
                        if data.decode('utf8') == 'no':
                            is_recieve2 = True
                            islink = False
                        if not is_play and not result:
                            me = storn.Storn_Black(eval(data))
                            black_chesses.append(me)
                            chesses.append(me)
                            is_play = True
                    except error:
                        disconnected = True
                        islink = False

        # win or lose
        if not result and iswin(black_chesses):
            result = True;
            black_win = True
        if not result and iswin(white_chesses):
            result = True
            white_win = True

        if black_win and result and not is_recieve1 and not is_recieve2:
            screen.blit(lose_text, (win_text_rect.left, win_text_rect.top - 80))
            screen.blit(play_text, win_text_rect)
            screen.blit(menu_text, (win_text_rect.left, win_text_rect.top + 80))

        if white_win and result and not is_recieve1 and not is_recieve2:
            screen.blit(win_text, (win_text_rect.left, win_text_rect.top - 80))
            screen.blit(play_text, win_text_rect)
            screen.blit(menu_text, (win_text_rect.left, win_text_rect.top + 80))

        if is_recieve1:
            screen.blit(text6, text6_rect)
            screen.blit(text7, text7_rect)

        if is_recieve2:
            screen.blit(text5, text5_rect)
            screen.blit(menu_text, (text5_rect.left + 150, text5_rect.top + 70))


        if is_playagain:
            white_chesses = []
            black_chesses = []
            chesses = []
            result = False
            black_win = False
            white_win = False
            is_playagain = False

        pygame.display.flip()

        clock.tick(60)


if __name__ == '__main__':
    main()
