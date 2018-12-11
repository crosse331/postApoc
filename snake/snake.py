from pynput import keyboard
import time
import random as rnd
import tdl

SCREEN_SIZE = (64,64)
LIMIT_FPS = 20
game_over = False
apple_pos = (1,1)

class Snake:
    def __init__(self):
        self.position = (int(SCREEN_SIZE[0]/2), int(SCREEN_SIZE[1]/2))
        self.moving_vector = (0,1)
        self.body = [self.position]
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.grow = False

    def on_press(self, key):
        # keyboard.Key
        if key.char == 'w' and self.moving_vector != (0,1):
            self.moving_vector = (0, -1)
        elif key.char == 's' and self.moving_vector != (0,-1):
            self.moving_vector = (0, 1)
        elif key.char == 'a' and self.moving_vector != (1,0):
            self.moving_vector = (-1, 0)
        elif key.char == 'd' and self.moving_vector != (-1,0):
            self.moving_vector = (1, 0)


    def draw(self, console):
        for t in self.body:
            console.draw_char(t[0], t[1], 45, bg=None, fg=(255, 255, 255))


    def logic(self):
        global game_over, apple_pos
        self.body.insert(0, (self.body[0][0] + self.moving_vector[0], self.body[0][1] + self.moving_vector[1]))
        if self.body[0][0] < 0 or self.body[0][0] > SCREEN_SIZE[0] or self.body[0][1] < 0 or self.body[0][1] > SCREEN_SIZE[1]:
            game_over = True
        for c in self.body[1:-1]:
            if c == self.body[0]:
                game_over = True

        if apple_pos != self.body[0]:
            del self.body[-1]
        else:
            apple_pos = (rnd.randint(1,SCREEN_SIZE[0]-1), rnd.randint(1,SCREEN_SIZE[1]-1))


tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
console = tdl.init(SCREEN_SIZE[0], SCREEN_SIZE[1], title="Snake", fullscreen=False)
tdl.set_fps(LIMIT_FPS)
snake = Snake()



while not tdl.event.is_window_closed():
    if game_over:
        print("Game Over!")
        print("Your score: " + str(len(snake.body) - 1))
        break
    console.clear()
    snake.logic()
    snake.draw(console)
    console.draw_char(apple_pos[0], apple_pos[1], '@', fg=(255,0,0))
    tdl.flush()