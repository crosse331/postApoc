import random

class Planet:
    def __init__(self, data):
        if data is not None:
            self.init_components(data[0],data[1])
        else:
            self.generate()

    def init_components(self,t,s):
        self.type = t
        # 0 - mercury
        # 1 - earth
        # 2 - jupiter
        # 3 - uran
        self.size = s
        # 0 - small
        # 1 - medium
        # 2 - big
        # 3 - huge

    def generate(self):
        self.init_components(random.randint(0,4), random.randint(0,4))

    def get_char_color(self):
        color = (0,0,0)
        if self.type == 0:
            color = (255, 0, 0)
        elif self.type == 1:
            color = (0, 255, 0)
        elif self.type == 2:
            color = (255, 200, 128)
        elif self.type == 3:
            color = (0,0,255)
        return color



class Spaceship:
    def __init__(self, t, s):
        self.type = t
        # 0 - civil
        # 1 - cargo
        # 2 - miner
        # 3 - fighter
        # 4 - cruiser
        # 5 - battleship
        # 6 - destroyer
        self.size = s
        # 0 - small
        # 1 - medium
        # 2 - big
        # 3 - huge


class SolarSystem:
    def __init__(self, data, sector, pos):
        self.planets = []
        self.sector = sector
        self.position = pos
        if data is None:
            self.generate()

    def generate(self):
        counts = [random.randint(1,2) for _ in range(4) ]
        type = 0
        for c in counts:
            for p in range(c):
                self.planets.append(Planet([type,1]))
            type+=1


class Viewer:
    def __init__(self, s):
        self.sector = s
        self.mousePos = (0,0)
        self.viewType = 0
        self.selectedSystem = 0
        # 0 - sector
        # 1 - system

    def draw(self, console):
        if self.sector is None:
            return
        if self.viewType == 0:
            for s in self.sector.stars:
                back = (0,0,0)
                if self.mousePos[0] == s.position[0] and self.mousePos[1] == s.position[1]:
                    back = (255,255,255)
                console.draw_char(s.position[0], s.position[1], ".", fg=(255,255,0), bg=back)
        elif self.viewType == 1:
            console.draw_char(4, console.height // 2, "O", fg=(255, 255, 0))
            count = 0
            for p in self.sector[self.selectedSystem].planets:
                back = (0,0,0)
                if self.mousePos == (7 + 3 * count, console.height // 2):
                    back = (255,255,255)
                console.draw_char(7 + 3 * count, console.height // 2, "o", fg=p.get_char_color(), bg=back)
                count += 1


    def update_event(self, ev):
        if ev.type == 'MOUSEDOWN':
            self.mousePos = ev.cell


class SpaceSector:
    size = (16,16)
    def __init__(self, data):
        self.stars = []
        if data is None:
            self.generate()

    def generate(self):
        count = 64
        for i in range (count):
            self.stars.append(SolarSystem(None, self, (random.randint(0,SpaceSector.size[0]-1),
                                                       random.randint(0,SpaceSector.size[1]-1))))

