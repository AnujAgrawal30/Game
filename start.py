from game import *
from pygame.locals import *

def main():
    # Set Colors
    BGcolor = Yellowish
    TextColor = Purple
    rect_color = Red
    text_size = Display_size[1]/40

    while True: # Main Game Loop
        pygame.display.update()
        Surface.fill(BGcolor)
        """ The Rules of the game to be printed line by line """
        rect = getfont(caption, 'bahnschrift', 50, TextColor, Display_size[0]/2, Display_size[1]/10)
        rect = getfont("Rules", 'bahnschrift', 30, TextColor, Display_size[0]/2, rect.bottom + 20)
        rect = getfont('1. Control the bars by arrow keys or WASD keys', 'bahnschrift', text_size, TextColor, 50, rect.bottom + 50, alignment='topleft')
        rect = getfont('2. The bars highlighted by blue border are selected, press Spacebar to switch', 'bahnschrift', text_size, TextColor, rect.left, rect.bottom + text_size, alignment='topleft')
        rect = getfont('3. Move the bars to drop the green rocks out of the central region', 'bahnschrift', text_size, TextColor, rect.left, rect.bottom + text_size, alignment='topleft')
        rect = getfont('4. Each rock going into central region will cost one life', 'bahnschrift', text_size, TextColor, rect.left, rect.bottom + text_size, alignment='topleft')
        rect = getfont('5. Drop the blue diamonds into the central region to increase score', 'bahnschrift', text_size, TextColor, rect.left, rect.bottom + text_size, alignment='topleft')
        rect = getfont('6. Diamonds dropped out of the central region will cost points', 'bahnschrift', text_size, TextColor, rect.left, rect.bottom + text_size, alignment='topleft')
        rect = getfont('7. You lose if lives goes to 0 or if score is below 0', 'bahnschrift', text_size, TextColor, rect.left, rect.bottom + text_size, alignment='topleft')
        start_rect = getrect(150, 50, Display_size[0]/2, Display_size[1]*4/5, rect_color)
        getfont('Start', 'bahnschrift', 30, TextColor, Display_size[0]/2, Display_size[1]*4/5)

        for event in pygame.event.get():
            if event.type == QUIT:
                """ Quit Event """
                quitgame()
            elif event.type == MOUSEMOTION:
                if start_rect.collidepoint(event.pos):
                    rect_color = Green
                else:
                    rect_color = Red
            elif event.type == MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    rect_color = White
            elif event.type == MOUSEBUTTONUP:
                if start_rect.collidepoint(event.pos):
                    return "Go to level 1"
