import tdl
import random as rnd

SCREEN_SIZE = (10,20)
field = [[0 for __ in range(SCREEN_SIZE[0])] for _ in range(SCREEN_SIZE[1])]
LIMIT_FPS = 30
score = 0
speed = 30

game_over = False

tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
console = tdl.init(SCREEN_SIZE[0] + 10, SCREEN_SIZE[1] + 10, title="Tetris", fullscreen=False)
tdl.set_fps(LIMIT_FPS)

def_figures = [
    [[1,1],[1,1]],
    [[1,1,1],[1,0,0]],
    [[1,1,1],[0,0,1]],
    [[1,1,1,1]],
    [[1,1,0],[0,1,1]],
    [[0,1,1],[1,1,0]],
    [[0,1,0],[1,1,1]]
]

next_fig = def_figures[6]
cur_pos = (5,5)
cur_fig = None

def init():
    global score, field, cur_fig
    score = 0
    for i in range(len(field)):
        for j in range(len(field[i])):
            field[i][j] = 0
    cur_fig = None
    get_next()

def get_next():
    global next_fig, cur_fig, cur_pos, field, score, game_over

    for i in range(len(field[0])):
        if field[0][i] != 0:
            game_over = True
            return

    if cur_fig is not None:
        for i in range(len(cur_fig)):
            for j in range(len(cur_fig[i])):
                if cur_fig[i][j] == 1:
                    field[cur_pos[1] + i][cur_pos[0] + j] = 1
    cur_fig = next_fig
    cur_pos = (5,0)
    next_fig = def_figures[rnd.randint(0, len(def_figures)-1)]

    score += 10
    free = []
    for i in range(len(field)):
        sum = 0
        for j in range(len(field[i])):
            sum += field[i][j]
        if sum == len(field[i]):
            score += 100
            free.append(i)
    for i in range(len(field)):
        if i in free:
            for j in range(i,0,-1):
                for k in range(len(field[0])):
                    field[j][k] = field[j-1][k]

def rotate():
    global cur_fig, cur_pos

    tmp = [[0 for __ in range(len(cur_fig))] for _ in range(len(cur_fig[0]))]

    for i in range(len(tmp)):
        for j in range(len(tmp[0])):
            tmp[i][j] = cur_fig[j][len(cur_fig[0])-1-i]
    if cur_pos[0] + len(tmp[0]) > SCREEN_SIZE[0] or cur_pos[0] + len(tmp[0]) < 0:
        return
    cur_fig = tmp

def try_to_move():
    global cur_fig, cur_pos, field
    if cur_pos[1] + len(cur_fig) == SCREEN_SIZE[1]:
        get_next()
        return True
    for i in range(len(cur_fig)):
        for j in range(len(cur_fig[i])):
            if cur_fig[i][j] == 1 and field[cur_pos[1] + 1 + i][cur_pos[0] + j] == 1:
                get_next()
                return True
    cur_pos = (cur_pos[0], cur_pos[1] + 1)
    return False

def try_to_move_horz(pos):
    global cur_fig, field

    for i in range(pos[1], pos[1] + len(cur_fig), 1):
        for j in range(pos[0], pos[0] + len(cur_fig[0]), 1):
            if field[i][j] != 0:
                return False
    return True

def fall():
    res = False
    while not res:
        res = try_to_move()

tmp_time = 0
get_next()
_exit = False
while not tdl.event.is_window_closed():
    if _exit:
        break

    if not game_over:
        console.clear()
        console.draw_str(0,SCREEN_SIZE[1] + 1,"Score:" + str(score))
        for i in range(SCREEN_SIZE[0]):
            console.draw_char(i, SCREEN_SIZE[1], '-')
        for i in range(SCREEN_SIZE[1]):
            console.draw_char(SCREEN_SIZE[0], i, '|')

        console.draw_str(SCREEN_SIZE[0] + 3, 4, "Next:")
        for i in range(len(next_fig)):
            for j in range(len(next_fig[i])):
                if next_fig[i][j] == 1:
                    console.draw_char(SCREEN_SIZE[0] + 3 + j,6 + i,'1', fg=(255,255,255))

        for i in range(SCREEN_SIZE[1]):
            for j in range(SCREEN_SIZE[0]):
                if field[i][j] != 0:
                    console.draw_char(j, i, '1', fg=(255, 255, 255))
                else:
                    console.draw_char(j, i, str(j), fg=(30, 30, 30))

        for i in range(len(cur_fig)):
            for j in range(len(cur_fig[i])):
                if cur_fig[i][j] == 1:
                    console.draw_char(cur_pos[0] + j,cur_pos[1] + i,'1', fg=(255,255,255))
        tmp_time += 1/speed
        if tmp_time > 1:
            try_to_move()
            tmp_time = 0
        user_input = None
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
        if user_input is not None:
            if user_input.key == 'UP':
                rotate()
            elif user_input.key == 'RIGHT' and cur_pos[0] + len(cur_fig[0]) < SCREEN_SIZE[0]:
                tmp_pos = (cur_pos[0] + 1, cur_pos[1])
                if try_to_move_horz(tmp_pos):
                    cur_pos = tmp_pos
            elif user_input.key == 'LEFT' and cur_pos[0] > 0:
                tmp_pos = (cur_pos[0] - 1, cur_pos[1])
                if try_to_move_horz(tmp_pos):
                    cur_pos = tmp_pos
            elif user_input.key == 'DOWN':
                fall()
            elif user_input.key == 'ESCAPE':
                _exit = True
                break
            elif user_input.key == 'BACKSPACE':
                game_over = True
    else:
        console.draw_str(int(SCREEN_SIZE[0] / 2), int(SCREEN_SIZE[1]/2), "Game over!")
        user_input = None
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
        if user_input is not None:
            if user_input.key == 'ENTER':
                init()
                game_over = False
            elif user_input.key == 'ESCAPE':
                _exit = True
                break

    tdl.flush()