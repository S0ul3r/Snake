from game import *

class Gui:
    def __init__(self, x = BOARDWIDTH, y = BOARDHEIGHT):
        pygame.init()
        self.game = Game(x, y)
        self.win = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
        pygame.display.set_caption("Snake")

    def display(self):
        for i in range(self.game.height):
            for j in range(self.game.width):
                c = BGCOLOR
                if self.game.vis_board[i][j].typ == WALL:
                    c = WALLCOLOR
                elif self.game.vis_board[i][j].typ == FOOD:
                    c= FOODCOLOR
                elif self.game.vis_board[i][j].typ == EMPTY:
                    c = BGCOLOR
                elif self.game.vis_board[i][j].typ == SNAKE:
                    c = SNAKECOLOR
                pygame.draw.rect(self.win, c, 
                (j * FIELDSIZE, i * FIELDSIZE, FIELDSIZE, FIELDSIZE))
                pygame.draw.rect(self.win, FRAMECOLOR, 
                (j * FIELDSIZE, i * FIELDSIZE, FIELDSIZE, FIELDSIZE), 1)
        pygame.display.update()
    
    def play(self):
        self.game.addFood()
        self.display()
        time.sleep(1)
        clock = pygame.time.Clock()
        while self.game.state == RUNNING:
            self.game.changed = False
            self.game.handleEvent()
            self.game.update()
            self.display()
            clock.tick(MOVESPERSEC)
