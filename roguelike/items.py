import gameplay
import random

rarity_coefficients = [0.75,1,1.1,1.35,1.5,1.6,2]

class Item:
    def __init__(self, name, c):
        self.name = name
        self.char = c
        self.rarity = 0

    def get_color(self):
        if self.rarity == 0:#bad
            return (100,100,100)
        if self.rarity == 1:#common
            return (255,255,255)
        if self.rarity == 2:#uncommon
            return (0,255,0)
        if self.rarity == 3:#rare
            return (0,0,255)
        if self.rarity == 4:#rarest
            return (255,0,255)
        if self.rarity == 5:#legendary
            return (255,215,0)
        if self.rarity == 6:#mythic
            return (255,100,0)
        return (255,255,255)

        #RoomController.current.add_object(self)

    def get_copy(self):
        res = Item(self.name, self.char)
        res.rarity = self.rarity
        return res

    def get_name(self):
        if self.rarity == 0:
            return "Broken " + self.name
        if self.rarity == 1:
            return self.name
        if self.rarity == 2:
            return self.name
        if self.rarity == 3:
            return "Rare " + self.name
        if self.rarity == 4:
            return "Rarest " + self.name
        if self.rarity == 5:
            return "Legendary " + self.name
        if self.rarity == 6:
            return "Mythic " + self.name

    def set_rarity(self, r):
        self.rarity = r


class Equipment(Item):
    def __init__(self, name, c, dmg, df):
        Item.__init__(self, name, c)
        self.damage = dmg
        self.defence = df

    def get_copy(self):
        res = None
        if isinstance(self, Weapon):
            res = Weapon(self.name, self.char, self.damage)
        if isinstance(self, Head):
            res = Head(self.name, self.char, self.defence)
        if isinstance(self, Body):
            res = Body(self.name, self.char, self.defence)
        if isinstance(self, Pants):
            res = Pants(self.name, self.char, self.defence)
        if isinstance(self, Boots):
            res = Boots(self.name, self.char, self.defence)
        res.rarity = self.rarity
        return res

    def get_description(self):
        result = []
        if self.damage > 0:
            result.append("Damage: " + str(self.damage))
        if self.defence > 0:
            result.append("Defence: " + str(self.defence))

        return result

    def set_rarity(self, r):
        Item.set_rarity(self, r)
        self.damage *= rarity_coefficients[r]
        self.defence *= rarity_coefficients[r]


class Weapon(Equipment):
    def __init__(self, name, c, dmg):
        Equipment.__init__(self, name, c, dmg, 1)


class Head(Equipment):
    def __init__(self, name, c, df):
        Equipment.__init__(self, name, c, 0, df)


class Body(Equipment):
    def __init__(self, name, c, df):
        Equipment.__init__(self, name, c, 0,df)


class Pants(Equipment):
    def __init__(self, name, c, df):
        Equipment.__init__(self, name, c, 0, df)


class Boots(Equipment):
    def __init__(self, name, c, df):
        Equipment.__init__(self, name, c, 0, df)


ItemBase = [Weapon("Dagger", ',',1),
            Weapon("Sword", '!',2),
            Weapon("Curved Sword", '?', 3),
            Weapon("Long Sword", '|', 4),
            Weapon("Spike", '/', 3),
            Head("Leather Helmet", 'u', 1),
            Head("Iron Helmet", 'u',2),
            Head("Silver Helmet", 'u',3),
            Body("Leather Armour", 'W', 2),
            Body("Iron Armour", 'W', 4),
            Body("Silver Armour", 'W', 2),
            Pants("Leather Pants", 'H', 2),
            Pants("Iron Pants", 'H', 4),
            Pants("Silver Pants", 'H', 6),
            Boots("Leather Boots", 'J', 1),
            Boots("Iron Boots", 'J', 2),
            Boots("Silver Boots", 'J', 3)]

def get_item(id, rarity):
    item = ItemBase[id].get_copy()
    item.set_rarity(rarity)
    return item

def get_random_item(rarity):
    item = get_item(random.randint(0,len(ItemBase)-1), rarity)
    return item