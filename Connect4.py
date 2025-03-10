import pygame,numpy

def main(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Connect 4')
    grid = [[] for _ in range(7)]


    def jeton(turn, col, grid):
        if turn % 2:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        if len(grid[col]) < 6:
            grid[col].append('r' if color == (255, 0, 0) else 'y')
            pygame.draw.circle(screen,color,((col + 1) * width // 8, (7 - len(grid[col])) * (height // 7)), height // 15)
            turn += 1
        return grid, turn


    def maxcons(L):
        i = 0
        r, y= [], []
        count = 1
        while i < len(L) - 1:
            if L[i] == L[i + 1]:
                count += 1
            else:
                if L[i] == 'r':
                    r.append(count)
                elif L[i] == 'y':
                    y.append(count)
                count = 1
            if i == len(L) - 2:
                if L[i] == 'r':
                    r.append(count)
                elif L[i] == 'y':
                    y.append(count)
            i += 1
        return r, y


    def winverif(gridverif, run = True):
        r, y = [], []
        for i in range(7):
            for _ in range(6 - len(gridverif[i])):
                gridverif[i] += [0]
            r += maxcons(gridverif[i])[0]
            y += maxcons(gridverif[i])[1]
        for i in range(6):
            L = []
            for j in range(7):
                L += [gridverif[j][i]]
            r += maxcons(L)[0]
            y += maxcons(L)[1]
        a = numpy.array(gridverif)
        diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0] + 1, a.shape[1])]
        diags.extend(a.diagonal(i) for i in range(a.shape[1] - 1, -a.shape[0],-1))
        L = [n.tolist() for n in diags]
        for i in L:
            r += maxcons(i)[0]
            y += maxcons(i)[1]
        if r != [] and max(r) == 4:
            run = False
            print('red win')
        elif y != [] and max(y) == 4:
            run = False
            print('yellow win')
        return run


    pygame.draw.rect(screen, (69, 69, 69), pygame.Rect(0, 0, width, height))
    for i in range(1, 7):
        for j in range(1, 8):
            pygame.draw.circle(screen, (0, 0, 0), (j * (width // 8), i * (height // 7)), height // 15)

    run = True
    turn = 0
    while run:
        for event in pygame.event.get():
            run = not event.type == pygame.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = event.pos
                if mousePos[0] > width // 16 and mousePos[0] < width - width // 16:
                    col = (mousePos[0] - width // 16) // (width // 8)
                    grid, turn = jeton(turn, col, grid)
                    grid2 = [grid[i].copy() for i in range(7)]
                    run = winverif(grid2)

        pygame.display.update()
    pygame.quit()
