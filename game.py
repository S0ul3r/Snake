import pygame
import random
import sys
from pygame.locals import *
from locals import *
import time

EMPTY = 'E'
FOOD = 'F'
SNAKE = 'S'
WALL = 'W'

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

RUNNING = 0
WIN = 1
LOSE = 2

STATES = [RUNNING, WIN, LOSE]

dierctions = [UP, RIGHT, DOWN, LEFT]

class Cell:
    def __init__(self, x  = 0, y = 0, typ = 'E'):
        self.x = x
        self.y = y
        self.typ = typ
    def __str__(self):
        return "[%s]" % (self.typ)


class Board:
    def __init__(self, x = BOARDWIDTH, y = BOARDHEIGHT):
        self.width = BOARDWIDTH
        self.height = BOARDHEIGHT
        self.board = []
        for i in range(y):
            row = []
            for j in range(x):
                if(i == 0 or j == 0 or i == BOARDHEIGHT -1 or j == BOARDWIDTH - 1):
                    row.append(Cell(i, j, WALL))
                else:
                    row.append(Cell(i, j, EMPTY))
            self.board.append(row)
        
        
    def __str__(self):
        s = ""
        for i in self.board:
            row = ""
            for j in i:
                row += str(j)
            row += "\n"
            s += row
        return s 

    
class Snake:
    def __init__(self, x, y):
        self.snakeBody = []
        self.snakeBody.append(Cell(x, y - 1, SNAKE))
        self.snakeBody.append(Cell(x, y, SNAKE))
    
    def move(self, cell):
        self.snakeBody.append(cell)
        if(cell.typ != FOOD):
            del self.snakeBody[0]
        if(cell.typ == WALL or cell.typ == SNAKE):
            return LOSE
        cell.typ = SNAKE   
        return RUNNING
    
class Game:
    def __init__(self, x = BOARDWIDTH, y = BOARDHEIGHT):
        self.width = x
        self.height = y
        self.board = Board(x, y)
        self.snake = Snake(int(y/2), int(x/2))
        self.vis_board = []
        self.state = RUNNING
        for i in range(self.height):
            row = []    
            for j in range(self.width):
                row.append(Cell(i, j, self.board.board[i][j].typ))
            self.vis_board.append(row)
        for i in self.snake.snakeBody:
            self.vis_board[i.x][i.y].typ = i.typ

        self.direction = RIGHT
        self.changed = False

    def update_vis(self):
        for i in range(self.height):
            for j in  range(self.width):
                self.vis_board[i][j].typ = self.board.board[i][j].typ
        
        for i in range(len(self.snake.snakeBody)):
            self.vis_board[self.snake.snakeBody[i].x][self.snake.snakeBody[i].y].typ =self.snake.snakeBody[i].typ

    def addFood(self):
        puste = []
        for i in range(self.height):
            for j in range(self.width):
                if(self.vis_board[i][j].typ == EMPTY):
                    puste.append((i,j))
        if(len(puste)>0):
            x, y = random.choice(puste)
            self.board.board[x][y].typ = FOOD
            self.vis_board[x][y].typ = FOOD
    
    def display(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.vis_board[i][j], end="")
            print()
        
    def changeDirection(self, button):
        if button == K_LEFT:
            if self.direction == UP or self.direction == DOWN:
                self.changed = True
                self.direction = LEFT 
        if button == K_RIGHT:
            if self.direction == UP or self.direction == DOWN:
                self.changed = True
                self.direction = RIGHT
        if button == K_UP:
            if self.direction == LEFT or self.direction == RIGHT:
                self.changed = True
                self.direction = UP
        if button == K_DOWN:
            if self.direction == LEFT or self.direction == RIGHT:
                self.changed = True
                self.direction = DOWN
    
    def handleEvent(self):
        for event in pygame.event.get():
            if event.type ==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and self.changed == False:
                self.changeDirection(event.key)


    def nextCell(self, c):
        x, y = c.x, c.y
        if self.direction == UP:
            x -= 1
        elif self.direction == RIGHT:
            y += 1
        elif self.direction == DOWN:
            x += 1
        elif self.direction == LEFT:
            y -= 1
        return x, y

    def update(self):
        head = self.snake.snakeBody[-1]
        x, y = self.nextCell(head)
        newCell = Cell(self.vis_board[x][y].x, self.vis_board[x][y].y, self.vis_board[x][y].typ)
        print(self.vis_board[x][y].typ)
        if newCell.typ == FOOD:
            self.addFood()
        self.state = self.snake.move(newCell)
        
        for i in self.snake.snakeBody:
            self.board.board[i.x][i.y].typ = EMPTY
        
        self.update_vis()
    
    def play(self):
        self.addFood()
        self.display()
        time.sleep(1)
        clock = pygame.time.Clock()

        while self.state == RUNNING:
            clock.tick(MOVESPERSEC)
            self.update()
            self.display()