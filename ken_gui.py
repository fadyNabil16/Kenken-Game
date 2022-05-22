from http.client import NON_AUTHORITATIVE_INFORMATION
import pygame
import sys
import time


BLACK = (220, 224, 223)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 650
WINDOW_WIDTH = 500


class FirstWidget:

    def __init__(self):
        self.flag =True
        self.size_btns_pos = []
        self.algo_btns_pos=  []
        self.selected_n = None
        self.selected_algo = None
        
    def draw(self):
        self.WH = 300
        
        self.algos=['BT','BT+FC','BT+AC']
        for x in range(3, 10):
            pos = [(((x-3)*60))+50, 30, 50, 30]
            self.draw_btn(f"{x} x {x}", pos)
            self.size_btns_pos.append((pos, x))
        for x in range (3):
            pos = [(((x)*110))+80, 80, 80, 30]
            self.draw_btn(f"{self.algos[x]}", pos)
            self.algo_btns_pos.append((pos, x))
        self.draw_btn("Start", [WINDOW_WIDTH/2-50,self.WH-100,65,40],(0,0,0))

    def draw_btn(self, btn_name, pos,colour=(150,150,150)):
        smallfont = pygame.font.SysFont('Corbel', 20)
        solve_btn = smallfont.render(btn_name, True, (255, 255, 255))
        pygame.draw.rect(SCREEN, colour, pos)
        SCREEN.blit(solve_btn, (pos[0]+pos[2]//4, pos[1]+pos[3]//4))

    def select_btn(self,x):
        selCLR= (0,0,0)
        other_btns= [pos for pos in self.size_btns_pos if pos[1] != x ]
        selected = self.size_btns_pos[x-3]

        self.draw_btn(f"{x} x {x}", selected[0],selCLR)
        for btn in other_btns:
            self.draw_btn(f"{btn[1]} x {btn[1]}", btn[0])
        self.selected_n = x
        print (self.selected_n) 
    def select_algo(self,x):
        selCLR= (0,0,0)
        other_btns= [pos for pos in self.algo_btns_pos if pos[1] != x ]
        selected = self.algo_btns_pos[x]
        self.draw_btn(f"{self.algos[x]}", selected[0],selCLR)
        for btn in other_btns:
            self.draw_btn(f"{self.algos[btn[1]]}", btn[0])
        self.selected_algo = self.algos[x]
        print(self.selected_algo)

    def start(self):
        if (self.selected_n !=None and self.selected_algo !=None):
                
            self.flag=False
            SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            SCREEN.fill(WHITE)
            print("Start")
            # if (self.selected_algo not None)
            # return n,algo

    def check_event(self, mouse):
        for pos, x in self.size_btns_pos:
            if pos[0] <= mouse[0] <= pos[0]+50 and pos[1] <= mouse[1] <= pos[1]+30:
                # SCREEN.fill(WHITE)
                self.select_btn(x)
                # self.flag=False
                return None,None
        for pos, x in self.algo_btns_pos:
            if pos[0] <= mouse[0] <= pos[0]+80 and pos[1] <= mouse[1] <= pos[1]+30:
                self.select_algo(x)
                return None,None
        if WINDOW_WIDTH/2-50 <= mouse[0] <= WINDOW_WIDTH/2+15 and self.WH-100 <= mouse[1] <= self.WH-60:
            self.start()
            return self.selected_n,self.selected_algo
        return None,None
        



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
bi = (0, 0, 0)


def draw_cages(n, cages):
    for cage in cages:
        draw_cage(n, cage[0], cage[1], cage[2])


def draw_cage(n, _points, op, target):

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

    # draw Cage Operation and target
    x, y = (points[0][1]-0.95)*blockSize, (points[0][0]-0.99)*blockSize
    text = f"{op}{target}"
    putText((x, y), text)
    # my_font = pygame.font.SysFont('Comic Sans MS', 20) ##
    # text_surface = my_font.render(f"{op}{target}", False, (0, 0, 0)) ##
    # SCREEN.blit(text_surface, (x,y)) ##


def putText(coord, text):
    my_font = pygame.font.SysFont('Comic Sans MS', 20)
    text_surface = my_font.render(f"{text}", False, (0, 0, 0))
    SCREEN.blit(text_surface, coord)
    return


def solve(n, solveddic):
    blockSize = WINDOW_WIDTH//n
    for cage in solveddic:
        # print(cage,"cage")
        for i, cell in enumerate(cage):
            # print(cell)
            x, y = (cell[1]-0.5)*blockSize, (cell[0]-0.65)*blockSize
            text = solveddic[cage][i]
            putText((x, y), text)


def draw_btn(btn_name, pos):
    smallfont = pygame.font.SysFont('Corbel', 35)
    solve_btn = smallfont.render(btn_name, True, (255, 255, 255))
    pygame.draw.rect(SCREEN, (0, 0, 0), pos)
    SCREEN.blit(solve_btn, (pos[0]+25, pos[1]+10))


def main():
    global SCREEN, CLOCK
    pygame.init()
    pygame.font.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, 300))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)
    # draw_btn("solve", [320, 525, 120, 50])
    widget = FirstWidget()
    widget.draw()
    n,algo = None,None
    
    # drawGrid(n)
    testcase = [(((1, 1),), '.', 1), (((2, 1), (2, 2)), '/', 3), (((3, 1), (4, 1), (5, 1), (5, 2)), '*', 180), (((5, 3), (6, 1), (6, 2), (6, 3)), '+', 13), (((1, 2), (1, 3)), '-', 2), (((3, 2), (3, 3)), '-', 2), (((4, 2), (4, 3)), '/', 2),
                (((2, 3), (2, 4)), '-', 1), (((2, 5), (3, 5), (1, 4), (1, 5)), '+', 11), (((4, 4), (5, 4), (5, 5), (3, 4)), '*', 72), (((6, 6), (6, 4), (6, 5)), '+', 9), (((4, 5), (4, 6), (2, 6), (3, 6)), '+', 19), (((1, 6),), '.', 4), (((5, 6),), '.', 2)]
    # draw_cages(n, testcase)
    assign = {((1, 1),): (1,), ((2, 1), (2, 2)): (2, 6), ((3, 1), (4, 1), (5, 1), (5, 2)): (3, 4, 5, 3), ((5, 3), (6, 1), (6, 2), (6, 3)): (1, 6, 2, 4), ((1, 2), (1, 3)): (5, 3), ((3, 2), (3, 3)): (4, 6), ((4, 2), (4, 3)): (1, 2), ((
        2, 3), (2, 4)): (5, 4), ((2, 5), (3, 5), (1, 4), (1, 5)): (1, 2, 2, 6), ((4, 4), (5, 4), (5, 5), (3, 4)): (3, 6, 4, 1), ((6, 6), (6, 4), (6, 5)): (1, 5, 3), ((4, 5), (4, 6), (2, 6), (3, 6)): (5, 6, 3, 5), ((1, 6),): (4,), ((5, 6),): (2,)}

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if widget.flag:
                    n,algo=widget.check_event(mouse)
                    # print(n,algo)
                    if (n !=None and algo !=None):
                        drawGrid(n)
                        draw_cages(n, testcase)
                        draw_btn("solve", [320, 525, 120, 50])
                if 320 <= mouse[0] <= 440 and 525 <= mouse[1] <= 575:
                    solve(n, assign)

        pygame.display.update()


main()
