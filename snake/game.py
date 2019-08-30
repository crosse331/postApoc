import random as rnd
apple_pos = (14,14)

class Snake:

    def __init__(self, screen_size=(32,32)):
        self.SCREEN_SIZE = screen_size
        self.position = (int(self.SCREEN_SIZE[0]/2), int(self.SCREEN_SIZE[1]/2))
        self.moving_vector = (0,1)
        self.body = [self.position]
        #self.listener = keyboard.Listener(on_press=self.on_press)
        #self.listener.start()
        self.grow = False
        self.hunger = 500
        self.live = 0

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
        global apple_pos
        game_over = False
        self.hunger -= 1
        self.live += 1
        if self.hunger <= 0:
            game_over = True
            return game_over
        self.body.insert(0, (self.body[0][0] + self.moving_vector[0], self.body[0][1] + self.moving_vector[1]))
        if self.body[0][0] < 0 or self.body[0][0] > self.SCREEN_SIZE[0]-1 or self.body[0][1] < 0 or self.body[0][1] > self.SCREEN_SIZE[1]-1:
            game_over = True
        for c in self.body[1:-1]:
            if c == self.body[0]:
                game_over = True

        if apple_pos != self.body[0]:
            del self.body[-1]
        else:
            apple_pos = (rnd.randint(1,self.SCREEN_SIZE[0]-1), rnd.randint(1,self.SCREEN_SIZE[1]-1))
            self.hunger = 500
        return game_over

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
                if tmp[0] < 0 or tmp[0] > self.SCREEN_SIZE[0] - 1 or tmp[1] < 0 or tmp[1] > self.SCREEN_SIZE[1] - 1:
                    break
            if success:
                result.append(distance)
            else:
                result.append(0)

        #Borders and self body distance
        for v in vectors:
            tmp = self.body[0]
            distance = 0
            success = False
            while True:
                distance+=1
                tmp = (tmp[0] + v[0], tmp[1] + v[1])
                for b in self.body:
                    if b[0] == tmp[0] and b[1] == tmp[1]:
                        success = True
                        break
                if tmp[0] < 0 or tmp[0] > self.SCREEN_SIZE[0] - 1 or tmp[1] < 0 or tmp[1] > self.SCREEN_SIZE[1] - 1:
                    break
                if success:
                    break
            result.append(distance)

        return result

    def get_score(self):
        global apple_pos
        score = (len(self.body) - 1) ** 2 * 10 + self.live # - math.sqrt((self.body[0][0] - apple_pos[0]) ** 2 + (self.body[0][1] - apple_pos[1]) ** 2)
        if self.hunger == 0:
            score -= 400
        return score