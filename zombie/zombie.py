import tdl

WINDOW_SIZE = 50


class Vector:
    x = 0
    y = 0

    def __init__(self):
        self.x = 0
        self.y = 0

    def __init__(self, posX, posY):
        self.x = posX
        self.y = posY

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def __eq__(self, other):

        return self.x == other.x and self.y == other.y


class GameObject:

    symbol = '?'
    color = (255, 255, 255)
    bg_color = (0, 0, 0)
    position = Vector(0, 0)

    def __init__(self):
        self.symbol = '?'
        self.position = Vector(0, 0)

    def logic(self):
        #self.symbol='?'
        a=0

    def move_to_dir(self, dir):
        newPos = self.position + dir
        if newPos.x < 0 or newPos.x > WINDOW_SIZE-1 or newPos.y < 0 or newPos.y > WINDOW_SIZE - 1:
            return
        else:
            self.position = newPos

    def draw(self, console):
        console.draw_char(self.position.x, self.position.y, self.symbol, bg=self.bg_color, fg=self.color)

class Player(GameObject):

    def __init__(self):
        self.symbol = "@"
        self.position = Vector(25,25)

    def input(self, user_input):

        if user_input.key == "UP":
            self.move_to_dir(Vector(0, -1))
        elif user_input.key == "DOWN":
            self.move_to_dir(Vector(0, 1))
        elif user_input.key == "RIGHT":
            self.move_to_dir(Vector(1, 0))
        elif user_input.key == "LEFT":
            self.move_to_dir(Vector(-1, 0))


class MainScreen:

    field = []
    objects = []

    def __init__(self):
        self.field = []
        for i in range(WINDOW_SIZE):
            for j in range(WINDOW_SIZE):
                self.field.append(' ')
        self.objects = []

    def logic(self):
        for obj in self.objects:
            obj.logic()

    def draw(self, console):

        self.field = [' ' for i in range(WINDOW_SIZE * WINDOW_SIZE)]

        for obj in self.objects:
            self.field[obj.position.y * WINDOW_SIZE + obj.position.x] = obj.symbol

        for i in range(len(self.field)):
            console.draw_char(int(i % WINDOW_SIZE), int(i / WINDOW_SIZE), self.field[i], bg=None, fg=(255, 255, 255))

    def add_game_object(self, obj):
        self.objects.append(obj)


def Main():

    screen = MainScreen()

    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50
    LIMIT_FPS = 20

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Zombie", fullscreen=False)

    tdl.setFPS(LIMIT_FPS)

    objects = []

    player = Player()
    objects.append(player)


    while not tdl.event.is_window_closed():

        console.clear()
        for obj in objects:
            obj.draw(console)
        tdl.flush()

        for obj in objects:
            obj.logic()

        keypress = False
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                keypress = True
        if not keypress:
            continue
        player.input(user_input)





Main()