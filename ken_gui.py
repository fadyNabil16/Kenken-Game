import pygame
import sys


class Board:
    def __init__(self, window, n):
        self.tiles = [[Tile(5, window, i*60, j*60)
                       for j in range(n)] for i in range(n)]
        self.window = window

    def draw_board(self):
        '''Fills the board with Tiles and renders their values'''


class Tile:
    def __init__(self, value, window, x1, y1):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 60, 60)  # dimensions for the rectangle
        self.selected = False
        self.correct = False
        self.incorrect = False


BLACK = (220, 224, 223)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600


def checkborders(point, points):
    left = not (tuple([point[0], point[1]-1])) in points
    right = not (tuple([point[0], point[1]+1])) in points
    top = not (tuple([point[0]-1, point[1]])) in points
    bot = not (tuple([point[0]+1, point[1]])) in points
    print(point, [left, right, top, bot])
    return [left, right, top, bot]


blockSize = WINDOW_WIDTH//9


def drawGrid(n):
    # Set the size of the grid block
    for x in range(n):
        for y in range(n):
            rect = pygame.Rect(x*blockSize, y*blockSize, blockSize, blockSize)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
            # pygame.draw.line(SCREEN, (0, 0, 0), (50, 0), (50, blockSize), 4)
            # pygame.draw.line(SCREEN, (0, 0, 0),
            #                  (50, blockSize), (50, 2*blockSize), 4)

            # points = sorted(list(((2,1),(1,1),(3,1),(2,2))))
            # for point in points:
            # checkborders(point,points)
bi = (125, 210, 110)


def draw_cages(_points):
    points = sorted(list(_points))
    for point in points:
        x = checkborders(point, points)
        if x[0]:  # left (1,1) -> x = 0 *20 = 0 , y = 20  (0, 20)
            # (0 ,20)
            pygame.draw.line(SCREEN, bi, ((
                point[1]-1)*blockSize, (point[0] - 1)*blockSize), ((point[1]-1)*blockSize, (point[0])*blockSize), 3)
        if x[1]:  # r
            pygame.draw.line(SCREEN, bi, ((
                point[1])*blockSize, (point[0]-1)*blockSize), ((point[1])*blockSize, (point[0])*blockSize), 3)
        if x[2]:  # t
            pygame.draw.line(SCREEN, bi, ((
                point[1]-1)*blockSize, (point[0]-1)*blockSize), ((point[1])*blockSize, (point[0]-1)*blockSize), 3)
        if x[3]:  # t
            pygame.draw.line(SCREEN, bi, ((
                point[1]-1)*blockSize, (point[0])*blockSize), ((point[1])*blockSize, (point[0])*blockSize), 3)


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)
    drawGrid(9)
    draw_cages(((1, 1), (1, 2), (2, 2), (2, 3)))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


main()
