class Stat:
    def __init__(self, amount):
        self.cur = amount
        self.max = amount

    def __add__(self, amount):
        self.cur = self.cur+amount
        if self.cur > self.max:
            self.cur = self.max
        if self.cur < 0:
            self.cur = 0
        return self

    def __sub__(self, other):
        self.__add__(-other)
        return self

    def get_percent(self):
        return self.cur/self.max


class Vector:
    x = 0
    y = 0

    def __init__(self, posX, posY):
        self.x = posX
        self.y = posY

    def __add__(self, other):
        tmp = Vector(self.x, self.y)
        tmp.x += other.x
        tmp.y += other.y

        return tmp

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __mul__(self, other):
        tmp = Vector(self.x, self.y)
        tmp.x *= other
        tmp.y *= other
        return tmp

    def copy_from(self, other):
        self.x = other.x
        self.y = other.y

def sort_by_physical(obj):
    return int((obj).physical)

def draw_rect(console, x, y, width, height):
    for x in range(x, x + width):
        console.draw_char(x, y, 196, (128, 128, 128))
        console.draw_char(x, y + height, 196, (128, 128, 128))

    for y in range(y, y + height):
        console.draw_char(x, y, 179, (128, 128, 128))
        console.draw_char(x + width, y, 179, (128, 128, 128))
