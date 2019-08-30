import objects, logic, items


class Screen:
    def __init__(self, pos):
        self.position = pos


class RoomController(Screen):
    def __init__(self, pos, size):
        Screen.__init__(self, pos)
        self.size = size
        self.objects = []
        #self.player = None
        self.key_pressed = False

    def try_to_move(self, pos):
        if pos.x < 0 or pos.x > self.size.x - 1 or pos.y < 0 or pos.y > self.size.y - 1:
            return False

        for o in self.objects:
            if o.position == pos and o.physical:
                return False

        return True

    def try_to_interact(self, owner, pos):
        for o in self.objects:
            if o.position == pos:
                o.interact(owner)

    def try_to_search(self, pos):
        result = []
        for o in self.objects:
            if o.position == pos and not o.physical:
                result.append(o)
        return result

    def take_from_floor(self, taker, obj):
        if obj in self.objects:
            if taker.add_item(obj):
                self.objects.remove(obj)

    def add_object(self, obj):
        #if isinstance(obj, objects.Player):
        #    self.player = obj
        #    return
        if obj not in self.objects:
            self.objects.append(obj)

        self.objects.sort(key=logic.sort_by_physical)

    def draw(self, console):
        for x in range(self.position.x - 1, self.position.x + self.size.x + 1):
            console.draw_char(x, self.position.y - 1, 178, (128, 128, 128))
            console.draw_char(x, self.position.y + self.size.y, 178, (128, 128, 128))

        for y in range(self.position.y - 1, self.position.y + self.size.y + 1):
            console.draw_char(self.position.x - 1, y, 178, (128, 128, 128))
            console.draw_char(self.position.x + self.size.x, y, 178, (128, 128, 128))

        for o in self.objects:
            #if not isinstance(o, objects.Player):
            o.draw(console)
        #self.player.draw(console)

    def update_event(self, event):
        object_to_update = self.objects.copy()
        for o in object_to_update:
            o.update_event(event)



class Equipment:
    def __init__(self, stats):
        self.head = None
        self.body = None
        self.weapon = None
        self.pants = None
        self.boots = None

        self.stats = stats

    def get_eq_items(self):
        return [self.head,self.body,self.weapon, self.pants, self.boots]

    def is_equipped(self, item):
        if self.head == item or self.body == item or self.weapon == item or self.pants == item or self.boots == item:
            return True
        else:
            return False

    def try_to_equip(self, item):
        if isinstance(item, items.Head):
            self.head = item
        if isinstance(item, items.Body):
            self.body = item
        if isinstance(item, items.Weapon):
            self.weapon = item
        if isinstance(item, items.Pants):
            self.pants = item
        if isinstance(item, items.Boots):
            self.boots = item

        self.stats.resum_stats(self.get_eq_items())

    def try_to_unequip(self, item):
        if self.head == item:
            self.head = None
        if self.body == item:
            self.body = None
        if self.weapon == item:
            self.weapon = None
        if self.pants == item:
            self.pants = None
        if self.boots == item:
            self.boots = None

        self.stats.resum_stats(self.get_eq_items())




class Inventory:
    def __init__(self, capacity, controller, stats):
        self.capacity = capacity
        self.items = []
        self.equipment = Equipment(stats)
        self.controller = controller

    def add_item(self, item):
        if len(self.items) == self.capacity:
            return False
        self.items.append(item)
        return True

    def try_to_equip(self, pos):
        self.equipment.try_to_equip(self.items[pos])

    def ask_to_drop(self, pos):
        if pos >= len(self.items) or pos < 0:
            return
        self.controller.drop_item(self.items[pos])
        self.equipment.try_to_unequip(self.items[pos])
        self.items.remove(self.items[pos])


class InventoryController:
    def __init__(self, inv):
        self.cursor = 0
        self.inventory = inv

    def update_event(self, event):
        if event.key == "UP":
            self.move_cursor(logic.Vector(0, -1))
        if event.key == "DOWN":
            self.move_cursor(logic.Vector(0, 1))
        if event.key == "LEFT":
            self.move_cursor(logic.Vector(-1, 0))
        if event.key == "RIGHT":
            self.move_cursor(logic.Vector(1, 0))
        if event.keychar == 'e':
            self.inventory.try_to_equip(self.cursor)
        if event.keychar == 'd':
            self.inventory.ask_to_drop(self.cursor)
            self.cursor -=1
            if self.cursor < 0:
                self.cursor = 0


    def draw(self, console, is_selected):
        # 20 6
        count = 0
        for item in self.inventory.items:
            back = (0, 0, 0)
            if self.inventory.equipment.is_equipped(item):
                back = (150, 150, 0)
            if self.cursor == count and is_selected:
                back = (200,200,200)
            console.draw_char(20 + count % 10, 6 + count // 10, item.char, fg=item.get_color(), bg = back)
            count += 1
        for i in range(count, self.inventory.capacity):
            console.draw_char(20 + i % 10, 6 + i // 10, 224)

        # 20 10
        if is_selected and len(self.inventory.items) > 0:
            console.draw_str(3,20,self.inventory.items[self.cursor].get_name(),
                             fg=self.inventory.items[self.cursor].get_color())
            desc = self.inventory.items[self.cursor].get_description()
            for i in range(len(desc)):
                console.draw_str(3,22+i,desc[i])

    def move_cursor(self, vector):
        pos = self.cursor + vector.x + vector.y * 10
        if pos >= len(self.inventory.items) or pos < 0:
            return
        self.cursor = pos


class CreatureStats:
    def __init__(self, hp):
        self.hp = logic.Stat(hp)
        self.defence = 0
        self.damage = 0

    def take_damage_from(self, source):
        total = source.damage - self.defence
        if total < 1:
            total = 1
        self.hp -= total

    def resum_stats(self, equipment):
        self.defence = 0
        self.damage = 0
        for eq in equipment:
            if eq is not None:
                self.damage += eq.damage
                self.defence += eq.defence
