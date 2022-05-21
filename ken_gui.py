import pygame
import sys


BLACK = (220, 224, 223)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600


def checkborders(point, points):
    left = not (tuple([point[0], point[1]-1])) in points
    right = not (tuple([point[0], point[1]+1])) in points
    top = not (tuple([point[0]-1, point[1]])) in points
    bot = not (tuple([point[0]+1, point[1]])) in points
    # print(point, [left, right, top, bot])
    return [left, right, top, bot]


blockSize = WINDOW_WIDTH//9


def drawGrid(n):
    

    blockSize = WINDOW_WIDTH//n
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
bi = (0,0,0)

def draw_cages(n,cages):
    for cage in cages:
        draw_cage(n,cage[0],cage[1],cage[2])
def draw_cage(n,_points,op,target):

    blockSize = WINDOW_WIDTH//n
    points = sorted(list(_points))
    # target = 6
    # op = '+'
    # Draw Cages Borders:
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
    
    
    #draw Cage Operation and target
    x,y=(points[0][1]-0.95)*blockSize,(points[0][0]-0.99)*blockSize
    text = f"{op}{target}"
    putText((x,y),text)
    # my_font = pygame.font.SysFont('Comic Sans MS', 20) ##
    # text_surface = my_font.render(f"{op}{target}", False, (0, 0, 0)) ##
    # SCREEN.blit(text_surface, (x,y)) ##

def putText(coord,text):
    my_font = pygame.font.SysFont('Comic Sans MS', 20) ##
    text_surface = my_font.render(f"{text}", False, (0, 0, 0)) ##
    SCREEN.blit(text_surface, coord) ##
    return

def solve(n,solveddic):
    blockSize = WINDOW_WIDTH//n
    for cage in solveddic:
        # print(cage,"cage")
        for i,cell in enumerate(cage):
            # print(cell)
            x,y = (cell[1]-0.5)*blockSize,(cell[0]-0.65)*blockSize
            text = solveddic[cage][i]
            putText((x,y),text)

def main():
    global SCREEN, CLOCK
    pygame.init()
    pygame.font.init() ##
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)
    n=6
    drawGrid(n)
    testcase = [(((1, 1),), '.', 1), (((2, 1), (2, 2)), '/', 3), (((3, 1), (4, 1), (5, 1), (5, 2)), '*', 180), (((5, 3), (6, 1), (6, 2), (6, 3)), '+', 13), (((1, 2), (1, 3)), '-', 2), (((3, 2), (3, 3)), '-', 2), (((4, 2), (4, 3)), '/', 2), (((2, 3), (2, 4)), '-', 1), (((2, 5), (3, 5), (1, 4), (1, 5)), '+', 11), (((4, 4), (5, 4), (5, 5), (3, 4)), '*', 72), (((6, 6), (6, 4), (6, 5)), '+', 9), (((4, 5), (4, 6), (2, 6), (3, 6)), '+', 19), (((1, 6),), '.', 4), (((5, 6),), '.', 2)]
    draw_cages(n,testcase)
    assign = {((1, 1),): (1,), ((2, 1), (2, 2)): (2, 6), ((3, 1), (4, 1), (5, 1), (5, 2)): (3, 4, 5, 3), ((5, 3), (6, 1), (6, 2), (6, 3)): (1, 6, 2, 4), ((1, 2), (1, 3)): (5, 3), ((3, 2), (3, 3)): (4, 6), ((4, 2), (4, 3)): (1, 2), ((2, 3), (2, 4)): (5, 4), ((2, 5), (3, 5), (1, 4), (1, 5)): (1, 2, 2, 6), ((4, 4), (5, 4), (5, 5), (3, 4)): (3, 6, 4, 1), ((6, 6), (6, 4), (6, 5)): (1, 5, 3), ((4, 5), (4, 6), (2, 6), (3, 6)): (5, 6, 3, 5), ((1, 6),): (4,), ((5, 6),): (2,)}
    solve(n,assign)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


main()
