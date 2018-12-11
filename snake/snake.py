from pynput import keyboard
import time
import random as rnd
import tdl

import nn as NeuralNetworks

SCREEN_SIZE = (32,32)
LIMIT_FPS = 60
game_over = False
apple_pos = (14,14)

class Snake:
    def __init__(self):
        self.position = (int(SCREEN_SIZE[0]/2), int(SCREEN_SIZE[1]/2))
        self.moving_vector = (0,1)
        self.body = [self.position]
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.grow = False
        self.hunger = 500

    def on_press(self, key):
        # keyboard.Key
        char = ''
        try:
            char = key.char
        except AttributeError:
            char = key
        if char == 'w' and self.moving_vector != (0,1):
            self.moving_vector = (0, -1)
        elif char == 's' and self.moving_vector != (0,-1):
            self.moving_vector = (0, 1)
        elif char == 'a' and self.moving_vector != (1,0):
            self.moving_vector = (-1, 0)
        elif char == 'd' and self.moving_vector != (-1,0):
            self.moving_vector = (1, 0)


    def draw(self, console):
        for t in self.body:
            console.draw_char(t[0], t[1], 45, bg=None, fg=(255, 255, 255))


    def logic(self):
        global game_over, apple_pos
        self.hunger -= 1
        if self.hunger <= 0:
            game_over = True
            return
        self.body.insert(0, (self.body[0][0] + self.moving_vector[0], self.body[0][1] + self.moving_vector[1]))
        if self.body[0][0] < 0 or self.body[0][0] > SCREEN_SIZE[0]-1 or self.body[0][1] < 0 or self.body[0][1] > SCREEN_SIZE[1]-1:
            game_over = True
        for c in self.body[1:-1]:
            if c == self.body[0]:
                game_over = True

        if apple_pos != self.body[0]:
            del self.body[-1]
        else:
            apple_pos = (rnd.randint(1,SCREEN_SIZE[0]-1), rnd.randint(1,SCREEN_SIZE[1]-1))
            self.hunger = 500

    def set_controlls(self, controlls):
        vectors = ['w','s','a','d']
        self.on_press(vectors[controlls.index(max(controlls))])

    def get_inputs(self):
        global apple_pos
        vectors = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        result = []
        #Apple distance
        for v in vectors:
            tmp = self.body[0]
            distance = 0
            success = False
            while True:
                distance += 1
                tmp = (tmp[0] + v[0], tmp[1] + v[1])
                if tmp[0] == apple_pos[0] and tmp[1] == apple_pos[1]:
                    success = True
                    break
                if tmp[0] < 0 or tmp[0] > 63 or tmp[1] < 0 or tmp[1] > 63:
                    break
            if success:
                result.append(distance)
            else:
                result.append(0)
        #Self body distance
        for v in vectors:
            tmp = self.body[0]
            distance = 0
            success = False
            while True:
                distance += 1
                tmp = (tmp[0] + v[0], tmp[1] + v[1])
                for b in self.body:
                    if b[0] == tmp[0] and b[1] == tmp[1]:
                        success = True
                if tmp[0] < 0 or tmp[0] > 63 or tmp[1] < 0 or tmp[1] > 63:
                    break
            if success:
                result.append(distance)
            else:
                result.append(0)
        #Borders distance
        for v in vectors:
            tmp = self.body[0]
            distance = 0
            while True:
                distance+=1
                tmp = (tmp[0] + v[0], tmp[1] + v[1])
                if tmp[0] < 0 or tmp[0] > 63 or tmp[1] < 0 or tmp[1] > 63:
                    break
            result.append(distance)

        return result



tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
console = tdl.init(SCREEN_SIZE[0], SCREEN_SIZE[1], title="Snake", fullscreen=False)
tdl.set_fps(LIMIT_FPS)
count = 0

while True:
    snake = Snake()
    best = None
    best_size = 0
    if best is None:
        network = NeuralNetworks.NeuralNetwork([24,16,4])
    else:
        network = best.copy()
        network.mutate()
    while not tdl.event.is_window_closed():
        if game_over:
            print("Game Over! " + str(count))
            count += 1
            print("Your score: " + str(len(snake.body) - 1))
            game_over = False
            if len(snake.body) > 1:
                if best_size < len(snake.body):
                    best = network
                    best_size = len(snake.body)
                    network.save()
            break
        console.clear()
        res = network.input(snake.get_inputs())
        snake.set_controlls(res)
        snake.logic()
        snake.draw(console)
        console.draw_char(apple_pos[0], apple_pos[1], '@', fg=(255,0,0))
        tdl.flush()
