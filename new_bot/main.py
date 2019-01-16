import pywinauto
from pywinauto.application import Application
import pyautogui
import time
import pynput
import sys

free_space_counter = 0
is_finished = False
monsters = []
ignore = []
rect = (450,120,800,720)

def take_sreenshot():
    global rect
    image = pyautogui.screenshot(region=rect)
    for y in range(18):
        for x in range(20):
            colors = []
            for i in range(40):
                for j in range(40):
                    pixel = image.getpixel((x*40 + j, y * 40 + i))
                    if pixel not in colors:
                        colors.append(pixel)

            center = (rect[0] + x*40+20,rect[1] + y*40+20)
            if len(colors) > 20 and center not in ignore:
                monsters.append(center)

def click_at(pos):
    pyautogui.moveTo(pos[0], pos[1], 0.2)
    #time.sleep(1)
    pyautogui.click()

def check_monster_screen():
    if pyautogui.pixelMatchesColor(614,842, (249,241,234), 5):
        return  True
    return False

def check_wrong_screen():
    return pyautogui.pixelMatchesColor(839,900,(255,241,230), 5) and \
        pyautogui.pixelMatchesColor(866,900,(39,28,20), 5)

def check_stats():
    #if not pyautogui.pixelMatchesColor(900,900,(1,0,254), 10) \
    #        or not pyautogui.pixelMatchesColor(900,880,(156,10,10),10):
    pyautogui.mouseDown(1600,900)
    time.sleep(3)
    pyautogui.mouseUp()

def check_stats_battle():
    if not pyautogui.pixelMatchesColor(400, 575, (0, 0, 255), 10):
        item_pos = pyautogui.locateCenterOnScreen('ItemButton.png')
        if item_pos is not None:
            click_at(item_pos)
            pos = pyautogui.locateCenterOnScreen('LargeManaBottle.png')
            if pos is not None:
                click_at(pos)
                time.sleep(2)
            else:
                pos = pyautogui.locateCenterOnScreen('LargeElexir.png')
                if pos is not None:
                    click_at(pos)

            click_at(item_pos)



def monster_battle():
    global free_space_counter, is_finished
    free_space_counter = 0
    click_at((898, 841))
    time.sleep(2)
    if check_monster_screen():
        return
    while True:
        if is_finished:
            return
        check_stats_battle()
        if pyautogui.pixelMatchesColor(80,90,(99,33,0),tolerance=5):
            break
        if pyautogui.pixelMatchesColor(839,839,(48,37,37), tolerance=1):
            click_at((839,839))
        #275 830
        if pyautogui.pixelMatchesColor(275,830,(48,37,37), tolerance=10):
            click_at((200,860))
        else:
            click_at((500,860))
        time.sleep(3)

    time.sleep(1)
    check_stats()

def move_on_map():
    ignore.clear()
    click_at((650,20))
    #840,570
    click_at((840 + 100, 570))
    click_at((400,20))
    time.sleep(5)

def use_map_items():
    click_at((1600,900))
    time.sleep(3)
    torch_pos = pyautogui.locateCenterOnScreen('Torch.png')
    if torch_pos is not None:
        click_at(torch_pos)
        time.sleep(5)
    click_at((835, 899))

def on_release(key):
    global is_finished
    if key == pynput.keyboard.Key.esc:
        is_finished = True

def main():
    global free_space_counter, is_finished


    listener = pynput.keyboard.Listener(on_release=on_release)
    listener.start()

    while not is_finished:
        take_sreenshot()
        while len(monsters)>2:
            for m in monsters:
                if is_finished:
                    return
                #basic checks
                if check_wrong_screen():
                    click_at((835,899))
                    time.sleep(2)
                    continue
                #check_stats()

                pos_to_click = m
                click_at(pos_to_click)
                time.sleep(0.5)
                if check_monster_screen():
                    monster_battle()
                else:
                    ignore.append(m)

        move_on_map()

use_map_items()