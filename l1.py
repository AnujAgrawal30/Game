from game import *
import pygame, random, math
from pygame.locals import *
# Its basically four screens in which the player will move simultaneously, avoiding obstacles and other stuff
#from new.game import getrect


def main():
    global star, diamond, speed, score, lives, toggle, heart, lose_game, high_score
    high_score = getlinesfrom('high_score.txt')
    star = pygame.image.load("star.png")
    heart = pygame.image.load('heart.png')
    diamond = pygame.image.load("diamond.png")
    initial_speed = 4
    lose_game = False
    speed = 2
    lives = 3
    heart_count = 1
    score = 0
    initial_freq = 0.2
    freq = 0.4
    counter = 0
    box_data = [[], [], [], [], [], [], [], []]
    gamestate = [True, True, True, True]
    toggle = True
    TextColor = Black
    while True:  # Main Game Loop
        if lose_game:
            while(True):
                pygame.display.update()
                center_rect = getrect(500, 400, Display_size[0]/2, Display_size[1]/2, Red)
                if score > int(high_score[0]):
                    getfont(str('New High Score: ' + str(score)), 'bahnchrift', 50, TextColor, center_rect.midtop[0], center_rect.top + 50)
                    writelinesto('high_score.txt', score)
                else:
                    getfont(str('Your Score: ' + str(score)), 'bahnchrift', 50, TextColor, center_rect.midtop[0], center_rect.top + 50)
                replay_rect = getrect(300, 50, center_rect.midtop[0], center_rect.top + 200, White)
                getfont('Replay', 'bahnchrift', 50, TextColor, replay_rect.center[0], replay_rect.center[1])
                quit_rect = getrect(300, 50, center_rect.midtop[0], center_rect.top + 300, White)
                getfont('Quit', 'bahnchrift', 50, TextColor, quit_rect.center[0], quit_rect.center[1])
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quitgame()
                    if event.type == MOUSEBUTTONDOWN:
                        if replay_rect.collidepoint(event.pos):
                            return "Go to level 1"
                        elif quit_rect.collidepoint(event.pos):
                            quitgame()
        drawSurface(gamestate, box_data)
        for event in pygame.event.get():
            if event.type == QUIT:
                quitgame()
            elif event.type == KEYDOWN:
                if (event.key == K_UP) | (event.key == K_w):
                    if toggle:
                        gamestate[0] = True
                    else:
                        gamestate[2] = False
                elif (event.key == K_DOWN) | (event.key == K_s):
                    if toggle:
                        gamestate[0] = False
                    else:
                        gamestate[2] = True
                elif (event.key == K_LEFT) | (event.key == K_a):
                    if toggle:
                        gamestate[1] = False
                    else:
                        gamestate[3] = True
                elif (event.key == K_RIGHT) | (event.key == K_d):
                    if toggle:
                        gamestate[1] = True
                    else:
                        gamestate[3] = False
                elif event.key == K_SPACE:
                    toggle = not toggle
        fpsClock.tick(FPS)
        counter += 1
        if counter > int(FPS/freq):
            i = random.randint(0, 7)
            j = random.randint(0, 1)
            if score/500 > heart_count:
                box_data[i].append([heart, 0])
                heart_count += 1
                i = 7-i
            if j == 0:
                box_data[i].append([star, 0])
            else:
                box_data[i].append([diamond, 0])
            counter = 0
        if score >= 0:
            speed = initial_speed*(math.log(score/1000 + 1) + 1)
            freq = initial_freq*(math.log(score/100 + 1) + 1)


def drawSurface(gamestate, box_data):
    # Set Colors
    global score, lives, lose_game, high_score
    bar_length = 420
    bar_width = 50
    BGcolor = Blue
    TextColor = Black
    button_color = Yellowish
    button_color2 = Red
    border_color = Green
    inner_boxcolor = Brown
    border = 5
    Surface.fill(BGcolor)
    getfont(caption, 'bahnchrift', 50, TextColor, Display_size[0]/4, Display_size[1]/12, italic=True)
    textbox = getfont(str("Score: " + str(score)), 'bahnchrift', 50, TextColor, Display_size[0]*3/4, Display_size[1]/12, italic=True)
    textbox = getfont(str("Lives: " + str(lives)), 'bahnchrift', 50, TextColor, textbox.bottomleft[0], textbox.bottomleft[1], alignment='topleft',  italic=True)
    getfont(str("High Score: " + str(int(high_score[0]))), 'bahnchrift', 50, TextColor, textbox.bottomleft[0], textbox.bottomleft[1], alignment='topleft',  italic=True)
    # Rectangular Objects
    center_rect = pygame.rect.Rect(0, 0, 3*bar_width, 3*bar_width)
    center_rect.center = (Display_size[0]/2, Display_size[1]/2)
    getrect(3*bar_width, bar_width, Display_size[0] / 2, Display_size[1] / 2, inner_boxcolor)
    getrect(bar_width, 3*bar_width, Display_size[0] / 2, Display_size[1] / 2, inner_boxcolor)
    getrect(bar_width, bar_width, Display_size[0] / 2, Display_size[1] / 2, Black, border=border)
    rect = pygame.rect.Rect(center_rect[0], center_rect[1], bar_length, bar_width)
    """If gamestat[i] means to check if the left(i = 0), right(i = 2), top(i = 1), or bottom(i = 3) is in its initial
    position or not."""
# Left Rectangle
    rect.midright = center_rect.midleft  # This rect Object will be used for all reference purposes
    if gamestate[0]:  # This means that the left boxes are in their initial positions (up position)
        pygame.draw.rect(Surface, button_color2, rect)  # drawing red box
        for obj in box_data[0]:  # for every sprite in box_data we blit it on the Surface
            Surface.blit(obj[0], (rect.topleft[0] + obj[1], rect.topleft[1]))
            obj[1] += speed
            if obj[1] > bar_length:  # If the sprite has reached its length, check for its status and then delete it
                if (obj[0] == star) & (rect.midright == center_rect.midleft):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if (rect.midright == center_rect.midleft):
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if(rect.midright == center_rect.midleft):
                        if lives < 5:
                            lives += 1
                del box_data[0][0]
        rect.bottom = rect.top
        pygame.draw.rect(Surface, button_color, rect)
        pygame.draw.line(Surface, Black, rect.bottomleft, rect.bottomright)
        for obj in box_data[1]:
            Surface.blit(obj[0], (rect.topleft[0] + obj[1], rect.topleft[1]))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midright == center_rect.midleft):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if (rect.midright == center_rect.midleft):
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if(rect.midright == center_rect.midleft):
                        if lives < 5:
                            lives += 1
                del box_data[1][0]
    else:
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[1]:
            Surface.blit(obj[0], (rect.topleft[0] + obj[1], rect.topleft[1]))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midright == center_rect.midleft):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if (rect.midright == center_rect.midleft):
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if(rect.midright == center_rect.midleft):
                        if lives < 5:
                            lives += 1
                del box_data[1][0]
        rect.top = rect.bottom
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[0]:
            Surface.blit(obj[0], (rect.topleft[0] + obj[1], rect.topleft[1]))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midright == center_rect.midleft):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if (rect.midright == center_rect.midleft):
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if(rect.midright == center_rect.midleft):
                        if lives < 5:
                            lives += 1
                del box_data[0][0]
        pygame.draw.line(Surface, Black, rect.topleft, rect.topright)
    # Drawing border if toggle = true
    if toggle:
        getrect(bar_length, 3*bar_width, center_rect.topleft[0], center_rect.topleft[1], Lightblue, border=border, alignment='topright')

# Right Rectangle
    rect.midleft = center_rect.midright
    if gamestate[2]:
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[4]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width - obj[1], rect.bottomright[1] - bar_width))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midleft == center_rect.midright):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if rect.midleft == center_rect.midright:
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if rect.midleft == center_rect.midright:
                        if lives < 5:
                            lives += 1
                del box_data[4][0]
        rect.top = rect.bottom
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[5]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width - obj[1], rect.bottomright[1] - bar_width))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midleft == center_rect.midright):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if (rect.midleft == center_rect.midright):
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if rect.midleft == center_rect.midright:
                        if lives < 5:
                            lives += 1
                del box_data[5][0]
    else:
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[5]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width - obj[1], rect.bottomright[1] - bar_width))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midleft == center_rect.midright):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if (rect.midleft == center_rect.midright):
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if rect.midleft == center_rect.midright:
                        if lives < 5:
                            lives += 1
                del box_data[5][0]
        rect.bottom = rect.top
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[4]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width - obj[1], rect.bottomright[1] - bar_width))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midleft == center_rect.midright):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if (rect.midleft == center_rect.midright):
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if rect.midleft == center_rect.midright:
                        if lives < 5:
                            lives += 1
                del box_data[4][0]
    # Drawing border if toggle = false
    if not toggle:
        getrect(bar_length, 3*bar_width, center_rect.topright[0], center_rect.topright[1], Lightblue, border=border, alignment='topleft')
    rect = pygame.rect.Rect(center_rect[0], center_rect[1], bar_width, bar_length)

# Top Rectangle
    rect.midbottom = center_rect.midtop
    if gamestate[1]:
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[2]:
            Surface.blit(obj[0], (rect.topleft[0], rect.topleft[1] + obj[1]))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midbottom == center_rect.midtop):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if rect.midbottom == center_rect.midtop:
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if rect.midbottom == center_rect.midtop:
                        if lives < 5:
                            lives += 1
                del box_data[2][0]
        rect.left = rect.right
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[3]:
            Surface.blit(obj[0], (rect.topleft[0], rect.topleft[1] + obj[1]))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midbottom == center_rect.midtop):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if rect.midbottom == center_rect.midtop:
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if rect.midbottom == center_rect.midtop:
                        if lives < 5:
                            lives += 1
                del box_data[3][0]
        pygame.draw.line(Surface, Black, rect.topleft, rect.bottomleft)
    else:
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[3]:
            Surface.blit(obj[0], (rect.topleft[0], rect.topleft[1] + obj[1]))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midbottom == center_rect.midtop):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if rect.midbottom == center_rect.midtop:
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if rect.midbottom == center_rect.midtop:
                        if lives < 5:
                            lives += 1
                del box_data[3][0]
        rect.right = rect.left
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[2]:
            Surface.blit(obj[0], (rect.topleft[0], rect.topleft[1] + obj[1]))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midbottom == center_rect.midtop):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if rect.midbottom == center_rect.midtop:
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if rect.midbottom == center_rect.midtop:
                        if lives < 5:
                            lives += 1
                del box_data[2][0]
        pygame.draw.line(Surface, Black, rect.topright, rect.bottomright)
    # Drawing border if toggle = true
    if toggle:
        getrect(3*bar_width, bar_length, center_rect.topleft[0], center_rect.topleft[1], Lightblue, border=border, alignment='bottomleft')

# Bottom Rectangle
    rect.midtop = center_rect.midbottom
    if gamestate[3]:
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[6]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width, rect.bottomright[1] - bar_width - obj[1]))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midtop == center_rect.midbottom):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if rect.midtop == center_rect.midbottom:
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if rect.midtop == center_rect.midbottom:
                        if lives < 5:
                            lives += 1
                del box_data[6][0]
        rect.right = rect.left
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[7]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width, rect.bottomright[1] - bar_width - obj[1]))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midtop == center_rect.midbottom):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if rect.midtop == center_rect.midbottom:
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if rect.midtop == center_rect.midbottom:
                        if lives < 5:
                            lives += 1
                del box_data[7][0]
        pygame.draw.line(Surface, Black, rect.topright, rect.bottomright)
    else:
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[7]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width, rect.bottomright[1] - bar_width - obj[1]))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midtop == center_rect.midbottom):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if rect.midtop == center_rect.midbottom:
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if rect.midtop == center_rect.midbottom:
                        if lives < 5:
                            lives += 1
                del box_data[7][0]
        rect.left = rect.right
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[6]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width, rect.bottomright[1] - bar_width - obj[1]))
            obj[1] += speed
            if obj[1] > bar_length:
                if (obj[0] == star) & (rect.midtop == center_rect.midbottom):
                    lives -= 1
                    if lives == 0:
                        lose_game = True
                elif obj[0] == diamond:
                    if rect.midtop == center_rect.midbottom:
                        score += 100
                    else:
                        score -= 100
                        if score < 0:
                            lose_game = True
                elif obj[0] == heart:
                    if rect.midtop == center_rect.midbottom:
                        if lives < 5:
                            lives += 1
                del box_data[6][0]
        pygame.draw.line(Surface, Black, rect.topleft, rect.bottomleft)
    # Drawing border if toggle = false
    if not toggle:
        getrect(3*bar_width, bar_length, center_rect.bottomleft[0], center_rect.bottomleft[1], Lightblue, border=border, alignment='topleft')

    getrect(3*bar_width, 3*bar_width, Display_size[0]/2, Display_size[1]/2, border_color, border=border)
    pygame.display.update()


if __name__ == '__main__':
    main()