import nn
import tdl
import random as rnd

LIMIT_FPS = 5
WORLD_SIZE=(64,64)


class Object:
    def __init__(self, pos):
        self.char = '0'
        self.color = (255, 255, 255)
        self.pos = pos
        World.current.objects.append(self)

    def logic(self):
        return 0

    def draw(self, console):
        console.draw_char(self.pos[0], self.pos[1], self.char, fg=self.color)


class Creature(Object):
    def __init__(self, pos):
        super(Creature, self).__init__(pos)
        self.neural_network = nn.NeuralNetwork([4,4,4])
        self.hunger = 1000
        self.life = 100
        self.char = '.'

    def logic(self):
        super(Creature, self).logic()
        vectors = [(1,0),(-1,0),(0,1),(0,-1)]
        outputs = self.neural_network.input([rnd.uniform(-2,2),rnd.uniform(-2,2),rnd.uniform(-2,2),rnd.uniform(-2,2)])
        self.move(vectors[outputs.index(max(outputs))])
        return 0

    def move(self, vector):
        global WORLD_SIZE
        self.pos = (self.pos[0] + vector[0], self.pos[1] + vector[1])
        if self.pos[0] < 0:
            self.pos = (self.pos[0] + WORLD_SIZE[0], self.pos[1])
        if self.pos[0] >= WORLD_SIZE[0]:
            self.pos = (self.pos[0] - WORLD_SIZE[0], self.pos[1])
        if self.pos[1] < 0:
            self.pos = (self.pos[0], self.pos[1] + WORLD_SIZE[1])
        if self.pos[1] >= WORLD_SIZE[1]:
            self.pos = (self.pos[0], self.pos[1] - WORLD_SIZE[1])


class Food(Object):
    def __init(self, pos):
        super(Food, self).__init__(pos)
        self.char = '@'


class World:
    current = None

    def __init__(self):
        World.current = self
        self.objects = []
        for _ in range(10):
            Creature((rnd.randrange(4, 60), rnd.randrange(4, 60)))

    def logic(self):
        for o in self.objects:
            o.logic()

    def draw(self, console):
        for o in self.objects:
            o.draw(console)


tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
console = tdl.init(WORLD_SIZE[0],WORLD_SIZE[1], title='World', fullscreen=False)
tdl.set_fps(LIMIT_FPS)

world = World()

while not tdl.event.is_window_closed():
    console.clear()
    world.logic()
    world.draw(console)
    tdl.flush()