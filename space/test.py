import tdl
import objects

SCREEN_SIZE = (32,32)
LIMIT_FPS = 30

tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
console = tdl.init(SCREEN_SIZE[0], SCREEN_SIZE[1], title="Space", fullscreen=False)
tdl.set_fps(LIMIT_FPS)


s = objects.SpaceSector(None)
viewer = objects.Viewer(s)
while not tdl.event.is_window_closed():
    for event in tdl.event.get():
        viewer.update_event(event)
    viewer.draw(console)
    tdl.flush()