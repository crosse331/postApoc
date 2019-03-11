import tdl
import objects, logic, gameplay
import items as It
import random

SCREEN_SIZE = (32,32)
LIMIT_FPS = 30
exit_game = False

tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
console = tdl.init(SCREEN_SIZE[0], SCREEN_SIZE[1], title="Roguelike", fullscreen=False)
tdl.set_fps(LIMIT_FPS)

room = gameplay.RoomController(logic.Vector(3,3),logic.Vector(15,15))
player = objects.Player("@", (255,255,255), logic.Vector(8,8), room, 10)

en = objects.Enemy("E", (255,0,0), logic.Vector(1,1), room, 5)

for i in range(7):
    #it = It.Item("test" + str(i), 65 + i)
    it = It.get_random_item(i)
    objects.ItemObject(it, logic.Vector(random.randint(0,room.size.x-1), random.randint(0,room.size.y-1)), room)

while not tdl.event.is_window_closed():
    for event in tdl.event.get():
        if event.type == "KEYDOWN" and event.key == "ESCAPE":
            exit_game = True
        room.update_event(event)
    room.draw(console)
    #for i in range(300):
    #    console.draw_char(i % 30, 20 + i // 30, i)
    tdl.flush()
    console.clear()
    if exit_game:
        break
