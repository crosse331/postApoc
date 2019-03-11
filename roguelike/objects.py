import logic, gameplay, items

class Object:
    def __init__(self, c, color, pos, room, phy):
        self.position = pos
        self.char = c
        self.color = color
        self.room = room
        self.physical = phy

        self.room.add_object(self)

    def draw(self, console):
        screen_pos = self.get_screen_pos()
        console.draw_char(screen_pos.x, screen_pos.y, self.char, fg = self.color)

    def update_event(self, event):
        if event is None:
            return

    def get_screen_pos(self):
        return self.position + self.room.position

    def interact(self, obj):
        return


class ItemObject(Object):
    def __init__(self, item, pos, room):
        Object.__init__(self, item.char, item.get_color(), pos, room, False)
        self.item = item


class Creature(Object):
    def __init__(self, c, color, pos, room, hp):
        Object.__init__(self, c, color, pos, room, True)
        #self.hp = logic.Stat(hp)
        self.stats = gameplay.CreatureStats(hp)
        self.inventory = gameplay.Inventory(16, self, self.stats)
        self.creature_type = 1

    def try_to_search(self):
        result = self.room.try_to_search(self.position)
        for r in result:
            self.room.take_from_floor(self, r)

    def add_item(self, obj):
        if isinstance(obj,ItemObject):
            self.inventory.add_item(obj.item)
            return True
        return False

    def drop_item(self, item):
        ItemObject(item, self.position, self.room)

    def try_to_move(self, vector):
        if self.room.try_to_move(self.position + vector):
            self.position += vector
            return True
        else:
            self.room.try_to_interact(self, self.position + vector)
        return False

    def interact(self, source):
        if source.creature_type != self.creature_type:
            self.stats.take_damage_from(source.stats)


class Player(Creature):
    def __init__(self, c, color, pos, room, hp):
        Creature.__init__(self, c, color, pos, room, hp)
        self.input_type = 0
        self.invController = gameplay.InventoryController(self.inventory)
        self.init_items()
        self.creature_type = 0

    def init_items(self):
        weapon = items.get_item(0,1)
        armour = items.get_item(8,1)
        self.inventory.add_item(weapon)
        self.inventory.try_to_equip(0)
        self.inventory.add_item(armour)
        self.inventory.try_to_equip(1)

    def update_event(self, event):
        if event.type == "KEYDOWN":
            if event.key == "TAB":
                if self.input_type == 0:
                    self.input_type = 1
                else:
                    self.input_type = 0
            if self.input_type == 0:
                if event.key == "UP":
                    self.try_to_move(logic.Vector(0, -1))
                if event.key == "DOWN":
                    self.try_to_move(logic.Vector(0, 1))
                if event.key == "LEFT":
                    self.try_to_move(logic.Vector(-1, 0))
                if event.key == "RIGHT":
                    self.try_to_move(logic.Vector(1, 0))
                if event.keychar == "s":
                    self.try_to_search()
            elif self.input_type == 1:
                self.invController.update_event(event)

    def draw(self, console):
        Object.draw(self, console)
        #20 2
        console.draw_str(20,2,chr(178)*int(self.stats.hp.get_percent() * 10), fg=(255,0,0))

        self.invController.draw(console, self.input_type == 1)


class Enemy(Creature):
    def __init__(self, c, color, pos, room, hp):
        Creature.__init__(self,c,color,pos,room,hp)
        self.dir = logic.Vector(1,0)

    def update_event(self, event):
        Creature.update_event(self,event)
        if not self.try_to_move(self.dir):
            self.dir *= -1

