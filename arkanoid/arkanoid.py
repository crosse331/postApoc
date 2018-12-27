import tdl
import random as rnd
import math

levels = [
    '0000000000000000000000' +
    '0000000000000000000000' +
    '2222222222222222222222' +
    '1111111111111111111111' +
    '1111111111111111111111' +
    '1111111111111111111111' +
    '1111111111111111111111' +
    '1111111111111111111111'
]

SCREEN_SIZE = (24,30)
field = [[0 for __ in range(SCREEN_SIZE[0])] for _ in range(SCREEN_SIZE[1])]
for i in range(SCREEN_SIZE[1]):
    for j in range(SCREEN_SIZE[0]):
        if i == 0 or i == SCREEN_SIZE[1]-1 or j == 0 or j == SCREEN_SIZE[0]-1:
            field[i][j] = '#'
LIMIT_FPS = 10
score = 0
speed = 30
cur_level = 0

game_over = False

player_pos = (9,26)
player_size = 3

class Ball:
    def __init__(self, pos):
        self.pos = pos
        self.vector = (0,-1)

    def move(self, field):
        while True:
            next_pos = (self.pos[0] + self.vector[0], self.pos[1] + self.vector[1])
            cell = field[int(next_pos[1])][int(next_pos[0])]
            if cell == 0:
                self.pos = next_pos
                return
            else:
                if len(str(cell)) > 1:
                    x = 0
                    if cell[1] == '0':
                        if player_size == 3:
                            x = -0.5
                        if player_size == 5:
                            x = -2
                    if cell[1] == '1' and player_size == 5:
                        x = -0.5
                    if cell[1] == '2' and player_size == 3 or cell[1] == '3':
                        x = 0.5
                    if cell[1] == '4':
                        x = 2
                    self.vector = self.get_vector((x,-1))
                    continue
                if math.fabs(self.pos[0] - next_pos[0]) < math.fabs(self.pos[1] - next_pos[1]):
                    self.vector = (self.vector[0], -self.vector[1])
                else:
                    self.vector = (-self.vector[0], self.vector[1])

    def get_vector(self, v):
        s = math.fabs(v[0])+math.fabs(v[1])
        return (v[0]/s, v[1]/s)

balls = [Ball((10,25))]

tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
console = tdl.init(SCREEN_SIZE[0] + 10, SCREEN_SIZE[1] + 10, title="Arkanoid", fullscreen=False)
tdl.set_fps(LIMIT_FPS)

def load_level():
    for i in range(1,SCREEN_SIZE[1]-1):
        for j in range(1, SCREEN_SIZE[0] - 1):
            if (j + i * 22 <= len(levels[cur_level])):
                field[i][j] = int(levels[cur_level][j-1 + (i-1) * 22])
            else:
                break

load_level()

while not tdl.event.is_window_closed():

    console.clear()
    for i in range(player_pos[0],player_pos[0] + player_size):
        field[player_pos[1]][i] = 0

    user_input = None
    for event in tdl.event.get():
        if event.type == 'KEYDOWN':
            user_input = event
    if user_input is not None:
        if user_input.key == 'LEFT' and player_pos[0] > 1:
            player_pos = (player_pos[0] - 1, player_pos[1])
        if user_input.key == 'RIGHT' and player_pos[0] + player_size < SCREEN_SIZE[0] - 1:
            player_pos = (player_pos[0] + 1, player_pos[1])

    for i in range(player_pos[0],player_pos[0] + player_size):
        field[player_pos[1]][i] = '_' + str(i-player_pos[0])
    for b in balls:
        b.move(field)
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == -1:
                console.draw_char(j,i,'#', (225,225,225))
            elif field[i][j] != 0:
                console.draw_char(j,i, str(field[i][j])[0], (255,255,255))
    for b in balls:
        console.draw_char(int(b.pos[0]),int(b.pos[1]), '@', (0,200,50))
    tdl.flush()