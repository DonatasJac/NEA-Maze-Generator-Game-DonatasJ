import random
import pygame
import sys
import math
import time
import os


Difficulty = 'Easy'
GRID_SIZE = int(input("Grid Size: "))
BraidSeverity = float(input("Enter the braid severity (0 all dead ends removed, 1 none removed)"))

BLOCK_AMOUNT = (GRID_SIZE) ** 2


class Block:
    def __init__(self):
        self.Row = -1
        self.Column = -1
        self.North = 1
        self.South = 1
        self.West = 1
        self.East = 1
        self.Visited = 0
        self.Distance = 0


Grid = [['' for Column in range(GRID_SIZE)] for Row in range(GRID_SIZE)]
LOB = [Block() for block in range(BLOCK_AMOUNT)]


def BinaryTree(GRID_SIZE, LOB):
    Index = -1
    for Row in range(GRID_SIZE):
        for Column in range(GRID_SIZE):
            Index += 1
            LOB[Index].Row = Row
            LOB[Index].Column = Column
            Decider = random.randint(0, 1)  # 0 is north, 1 is east
            if Row == 0:
                Decider = 1
            elif Column == GRID_SIZE - 1:
                Decider = 0
            if Row == 0 and Column == GRID_SIZE - 1:
                continue
            if Decider == 0:
                if LOB[Index - GRID_SIZE].South == 0:
                    Decider = 1
                else:
                    LOB[Index].North = 0
                    LOB[Index - GRID_SIZE].South = 0
            if Decider == 1:
                if LOB[Index + 1].West == 0:
                    if Row != 0:
                        LOB[Index].North = 0
                        LOB[Index - GRID_SIZE].South = 0
                else:
                    LOB[Index].East = 0
                    LOB[Index + 1].West = 0
    return LOB


def Sidewinder(GRID_SIZE, LOB):
    Index = -1
    Run = []
    for Row in range(GRID_SIZE):
        for Column in range(GRID_SIZE):
            Index += 1
            Run.append(Index)
            LOB[Index].Row = Row
            LOB[Index].Column = Column
            Decider = random.randint(0, 1)  # 0 is north, 1 is east
            if Row == 0:
                Decider = 1
            if Column == GRID_SIZE - 1:
                Decider = 0
            if Decider == 2:
                continue
            if Decider == 1:
                LOB[Index].East = 0
                LOB[Index + 1].West = 0
                Adjacent = Index + 1
                if Adjacent not in Run:
                    Run.append(Adjacent)
            if Decider == 0:
                Decider2 = random.randint(0, len(Run) - 1)
                Index1 = Run[Decider2]
                LOB[Index1].North = 0
                LOB[Index1 - GRID_SIZE].South = 0
                Run = []
    for Block in range(GRID_SIZE):
        LOB[Block].North = 1
        LOB[Block + (BLOCK_AMOUNT - GRID_SIZE)].South = 1
    return LOB


def AldousBroder(GRID_SIZE, LOB):
    for block in LOB:
        block.Visited = 0
    UnvisitedCount = GRID_SIZE ** 2
    if GRID_SIZE % 2 == 0:
        Index = ((GRID_SIZE ** 2) // 2) + (GRID_SIZE // 2)
        CurrentRow = GRID_SIZE // 2
        CurrentColumn = GRID_SIZE // 2
    elif GRID_SIZE % 2 != 0:
        Index = (GRID_SIZE ** 2) // 2
        CurrentRow = GRID_SIZE // 2
        CurrentColumn = GRID_SIZE // 2
    while UnvisitedCount != 0:
        Decider = random.randint(0, 3)
        LOB[Index].Row = CurrentRow
        LOB[Index].Column = CurrentColumn
        if LOB[Index].Visited == 0:
            LOB[Index].Visited = 1
            UnvisitedCount = UnvisitedCount - 1

        if CurrentRow == 0:  # 0 is north, 1 is east, 2 is south, 3 is west
            if CurrentColumn == 0:
                Decider = random.randint(1, 2)
            elif CurrentColumn == GRID_SIZE - 1:
                Decider = random.randint(2, 3)
            else:
                Decider = random.randint(1, 3)
        elif CurrentRow == GRID_SIZE - 1:
            if CurrentColumn == 0:
                Decider = random.randint(0, 1)
            elif CurrentColumn == GRID_SIZE - 1:
                while Decider in [1, 2]:
                    Decider = random.randint(0, 3)
            else:
                while Decider == 2:
                    Decider = random.randint(0, 3)
        elif CurrentRow != 0 and CurrentRow != GRID_SIZE - 1 and CurrentColumn == 0:
            Decider = random.randint(0, 2)
        elif CurrentRow != 0 and CurrentRow != GRID_SIZE - 1 and CurrentColumn == GRID_SIZE - 1:
            while Decider == 1:
                Decider = random.randint(0, 3)

        if Decider == 0:
            AdjacentIndex = Index - GRID_SIZE
            NewRow = CurrentRow - 1
            if LOB[AdjacentIndex].Visited == 0:
                LOB[Index].North = 0
                LOB[AdjacentIndex].South = 0
            CurrentRow = NewRow
        elif Decider == 1:
            AdjacentIndex = Index + 1
            NewColumn = CurrentColumn + 1
            if LOB[AdjacentIndex].Visited == 0:
                LOB[Index].East = 0
                LOB[AdjacentIndex].West = 0
            CurrentColumn = NewColumn
        elif Decider == 2:
            AdjacentIndex = Index + GRID_SIZE
            NewRow = CurrentRow + 1
            if LOB[AdjacentIndex].Visited == 0:
                LOB[Index].South = 0
                LOB[AdjacentIndex].North = 0
            CurrentRow = NewRow
        elif Decider == 3:
            AdjacentIndex = Index - 1
            NewColumn = CurrentColumn - 1
            if LOB[AdjacentIndex].Visited == 0:
                LOB[Index].West = 0
                LOB[AdjacentIndex].East = 0
            CurrentColumn = NewColumn
        Index = AdjacentIndex
    return LOB


def Braid(GRID_SIZE, LOB, Severity):
    Decider = 1 / Severity

    for Index in range(0, BLOCK_AMOUNT):
        ends = []
        if (Index + 1) % Decider == 0:
            continue
        if LOB[Index].North == 1:
            ends.append('N')
        if LOB[Index].East == 1:
            ends.append('E')
        if LOB[Index].South == 1:
            ends.append('S')
        if LOB[Index].West == 1:
            ends.append('W')

        if LOB[Index].Row == 0:
            ends.remove('N')
        if LOB[Index].Row == GRID_SIZE - 1:
            ends.remove('S')
        if LOB[Index].Column == 0:
            ends.remove('W')
        if LOB[Index].Column == GRID_SIZE - 1:
            ends.remove('E')

        if len(ends) == 3:
            choice = random.choice(ends)
        else:
            continue

        if choice == 'N':
            LOB[Index].North = 0
            LOB[Index - GRID_SIZE].South = 0
        elif choice == 'E':
            LOB[Index].East = 0
            LOB[Index + 1].West = 0
        elif choice == 'S':
            LOB[Index].South = 0
            LOB[Index + GRID_SIZE].North = 0
        elif choice == 'W':
            LOB[Index].West = 0
            LOB[Index - 1].East = 0
    return LOB


def Djikstra(LOB, GRID_SIZE, sRow, sColumn, tRow, tColumn):
    for block in LOB:
        block.Visited = 0
        block.Distance = 0
    VisitedCount = 1
    step = 1
    Index = (sRow * GRID_SIZE) + sColumn
    Frontier = []
    Frontier.append(Index)
    LOB[Index].Distance = 0
    LOB[Index].Visited = 1
    while VisitedCount < GRID_SIZE ** 2:
        Add = []
        for Index in Frontier:
            if LOB[Index].North == 0:
                Add.append(Index - GRID_SIZE)
            if LOB[Index].East == 0:
                Add.append(Index + 1)
            if LOB[Index].South == 0:
                Add.append(Index + GRID_SIZE)
            if LOB[Index].West == 0:
                Add.append(Index - 1)

        Frontier = []
        for Block in Add:
            if LOB[Block].Visited == 0:
                Frontier.append(Block)
                LOB[Block].Visited = 1
                LOB[Block].Distance = step
                VisitedCount += 1
        step += 1
    Index = (tRow * GRID_SIZE) + tColumn
    return LOB[Index].Distance


if Difficulty == 'Easy':
    LOB = BinaryTree(GRID_SIZE, LOB)

elif Difficulty == 'Medium':
    LOB = Sidewinder(GRID_SIZE, LOB)

elif Difficulty == 'Hard':
    LOB = AldousBroder(GRID_SIZE, LOB)

Index = -1
for Row in range(GRID_SIZE):
    Rows1, Rows2, Rows3, Rows4 = '', '', '', ''
    for Column in range(GRID_SIZE):
        Index += 1
        if Column == 0:
            Rows1 = '#'
            Rows2 = '#'
            Rows3 = '#'
            Rows4 = '#'
        if LOB[Index].East == 1:  # 6 spaces before #
            Rows2 = Rows2 + '      #'
            if len(str(LOB[Index].Distance)) == 1:
                Rows3 = Rows3 + str(LOB[Index].Distance) + '     #'
            else:
                Rows3 = Rows3 + str(LOB[Index].Distance) + '    #'
            Rows4 = Rows4 + '      #'
        elif LOB[Index].East == 0:
            Rows2 = Rows2 + '       '
            if len(str(LOB[Index].Distance)) == 1:
                Rows3 = Rows3 + str(LOB[Index].Distance) + '      '
            else:
                Rows3 = Rows3 + str(LOB[Index].Distance) + '     '
            Rows4 = Rows4 + '       '
        if LOB[Index].North == 1:
            Rows1 = Rows1 + '#######'
        elif LOB[Index].North == 0:
            Rows1 = Rows1 + '      #'
    print(Rows1)
    print(Rows2)
    print(Rows3)
    print(Rows4)
    if Row == GRID_SIZE - 1:
        print('#' * ((GRID_SIZE * 7) + 1))
# PYGAME ------------------------------------------------


pygame.init()
pygame.font.init()

print(pygame.font.get_fonts())

def ClearMaze(Walls):
    removed = []
    for i in Walls:
        removed.append(i)
    for i in removed:
        Walls.remove(i)
    return Walls

def LoadMaze(c, hStart, vStart, LOB):
    for i in range(0, BLOCK_AMOUNT):
        if LOB[i].North == 1:
            Wall1 = Wall(c + 1, 1, hStart, vStart)
        if LOB[i].West == 1:
            Wall2 = Wall(1, c, hStart, vStart)
        if i >= (BLOCK_AMOUNT - GRID_SIZE):
            Wall3 = Wall(c + 1, 1, hStart, vStart + c)
        hStart += c
        if (i + 1) % GRID_SIZE == 0:
            Wall4 = Wall(1, c, hStart, vStart)
            hStart = 0
            vStart += c

LOS = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([c / 3, c / 3])
        self.rect = self.image.get_rect()
        self.xSpeed = 0
        self.ySpeed = 0
        pygame.sprite.Sprite.__init__(self, LOS)

    def RecordMove(self, xChange, yChange):
        self.xSpeed += xChange
        self.ySpeed += yChange

    def UpdatePos(self, Walls, Treasure, Collision, sPath, score):

        self.rect.x += self.xSpeed

        CollisionList = pygame.sprite.spritecollide(self, Walls, False)
        for wall in CollisionList:
            if self.xSpeed > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right

        self.rect.y += self.ySpeed

        CollisionList = pygame.sprite.spritecollide(self, Walls, False)
        for wall in CollisionList:
            if self.ySpeed > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom

        CollisionList = pygame.sprite.spritecollide(self, Treasure, False)
        if len(CollisionList) > 0 or Collision == True:
            treasure = TreasureL
            if len(CollisionList) > 0:
                score += 1
            Collision = True
            TreasureRowOld = treasure.Row
            TreasureColumnOld = treasure.Column
            treasure.UpdatePos()
            TreasureRowNew = treasure.Row
            TreasureColumnNew = treasure.Column
            LOW = ClearMaze(Walls)
            LOB = [Block() for block in range(BLOCK_AMOUNT)]

            if score < 2:
                LOB = BinaryTree(GRID_SIZE, LOB)

            if score >=2 and score < 4:
                LOB = Sidewinder(GRID_SIZE, LOB)

            elif score >= 4:
                LOB = AldousBroder(GRID_SIZE, LOB)

            LOB = Braid(GRID_SIZE, LOB, BraidSeverity)
            LoadMaze(c, hStart, vStart, LOB)
            sPath = Djikstra(LOB, GRID_SIZE, TreasureRowOld, TreasureColumnOld, TreasureRowNew, TreasureColumnNew)

        return score, Collision, sPath
LOT = pygame.sprite.Group()
class Treasure(pygame.sprite.Sprite):
    def __init__(self):
        Image = pygame.image.load("treasure.png")
        Image.set_colorkey((255, 255, 255))
        Image.convert_alpha()
        self.Row = random.randint(0, GRID_SIZE - 1)
        self.Column = random.randint(0, GRID_SIZE - 1)
        self.image = pygame.transform.scale(Image, (c // 2, c // 2))
        self.rect = self.image.get_rect()
        self.rect.x = (self.Column * c) + c // 4
        self.rect.y = (self.Row * c) + c // 4
        pygame.sprite.Sprite.__init__(self, LOT)

    def UpdatePos(self):
        self.Row = random.randint(0, GRID_SIZE-1)
        self.Column = random.randint(0, GRID_SIZE-1)
        self.rect.x = (self.Column * c) + c // 4
        self.rect.y = (self.Row * c) + c // 4

LOW = pygame.sprite.Group()
class Wall(pygame.sprite.Sprite):
    def __init__(self, width, height, xVertice, yVertice):
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 0))
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.x = xVertice
        self.rect.y = yVertice
        pygame.sprite.Sprite.__init__(self, LOW)


# c is used to to calculate distances - ensures scale of different objects is always the same.
hStart = 0
vStart = 0
c = 50

LOB = Braid(GRID_SIZE, LOB, BraidSeverity)
LoadMaze(c, hStart, vStart, LOB)

fps = 60
frame = 0
clock = pygame.time.Clock()
Width, Height = GRID_SIZE * c, GRID_SIZE * c
display = pygame.display.set_mode((Width, Height))
Speed = c / 15

PlayerL = Player()
TreasureL = Treasure()
PlayerL.rect.x = (GRID_SIZE * c / 2) + 1
PlayerL.rect.y = (GRID_SIZE * c / 2) + 1

Row, Column = GRID_SIZE // 2, GRID_SIZE // 2
sPath = Djikstra(LOB, GRID_SIZE, Row, Column, TreasureL.Row, TreasureL.Column)
TimeFrames = (sPath * c) / Speed
TimeSeconds = TimeFrames / fps
Ease = 5
TargetFrame = (frame + TimeFrames) + Ease*fps
SecondsRemaining = str(math.floor((TargetFrame - frame) / fps))
CollisionFrame = 0
CollisionCheck = False
Score = Completed = 0
Lives = 3

Running = True
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        # Game Logic

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PlayerL.RecordMove(0, -Speed)
            elif event.key == pygame.K_RIGHT:
                PlayerL.RecordMove(Speed, 0)
            elif event.key == pygame.K_DOWN:
                PlayerL.RecordMove(0, Speed)
            elif event.key == pygame.K_LEFT:
                PlayerL.RecordMove(-Speed, 0)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                PlayerL.RecordMove(0, Speed)
            elif event.key == pygame.K_RIGHT:
                PlayerL.RecordMove(-Speed, 0)
            elif event.key == pygame.K_DOWN:
                PlayerL.RecordMove(0, -Speed)
            elif event.key == pygame.K_LEFT:
                PlayerL.RecordMove(Speed, 0)

    Score, CollisionCheck, sPath = PlayerL.UpdatePos(LOW, LOT, CollisionCheck, sPath, Score)
    if CollisionCheck == True:
        Completed += 1
        if Completed % 2 == 0 and Completed != 0:
            Lives += 1
        CollisionFrame = frame
        TimeFrames = (sPath * c) / Speed
        TimeSeconds = TimeFrames % fps
        TargetFrame = (frame + TimeFrames) + Ease*fps
        if Ease > 1:
            Ease = Ease - 0.5
        print(Ease)
        CollisionCheck = False
    if (frame - CollisionFrame) % fps == 0:
        SecondsRemaining = str(math.floor((TargetFrame - frame) / fps))
    if TargetFrame == frame:
        Lives -= 1
        Score -= 1
        if Lives == 0:
            Running = False
        CollisionCheck = True
        Score, CollisionCheck, sPath = PlayerL.UpdatePos(LOW, LOT, CollisionCheck, sPath, Score)
        CollisionFrame = frame
        TimeFrames = (sPath * c) / Speed
        TimeSeconds = TimeFrames % fps
        TargetFrame = (frame + TimeFrames) + Ease*fps
        if Ease < 3:
            Ease = Ease + 0.5
        CollisionCheck = False
        print(Ease)
    LOS.update()
    # Drawing
    display.fill((255, 255, 255))

    #Double digit time needs to be displayed with different dimensions to remain centred on screen
    if len(SecondsRemaining) >= 2:
        TFont = pygame.font.SysFont('calibri', (c * GRID_SIZE))
    else:
        TFont = pygame.font.SysFont('calibri', (c*GRID_SIZE)+(2*c))
    timer = TFont.render(SecondsRemaining, False, (0,0,0))
    timer.set_alpha(20)
    LFont = pygame.font.SysFont('calibri', (c*2))
    LivesCounter = LFont.render(str(Lives), False, (255,0,0))
    LivesCounter.set_alpha(40)
    if len(SecondsRemaining) >= 2:
        display.blit(timer, ((0, 0)))
    else:
        display.blit(timer, ((c*GRID_SIZE/4, 0)))
    display.blit(LivesCounter, (0, 0))
    LOW.draw(display)
    LOT.draw(display)
    LOS.draw(display)
    frame += 1
    pygame.display.flip()
    clock.tick(fps)

    # python "EAL.py"
