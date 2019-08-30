from pynput import keyboard
import time
import random as rnd
import tdl
import math

#import nn as NeuralNetworks
import wann
import game

SCREEN_SIZE = (32,32)
LIMIT_FPS = 240
game_over = False



def nn_sort_func(creature):
    return creature.score

tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)
console = tdl.init(SCREEN_SIZE[0], SCREEN_SIZE[1], title="Snake", fullscreen=False)
tdl.set_fps(LIMIT_FPS)

count = 0



#last_best =

#generation[0].mutate()

def learn():
    global game_over
    snake = game.Snake()
    generation = []
    generation_size = 120
    nn_sizes = [16, 4]
    for _ in range(int(generation_size/4)):
        generation.append(wann.NeuralNetwork(nn_sizes, -2))

    for i in range(int(generation_size/4)):
        cp = generation[i].copy()
        cp.set_def_weight(-1)
        generation.append(cp)
        cp = generation[i].copy()
        cp.set_def_weight(1)
        generation.append(cp)
        cp = generation[i].copy()
        cp.set_def_weight(2)
        generation.append(cp)

    best_score = 0
    equal_best = 0
    generation_number = 0
    while True:
        count = 0
        for creature in generation:
            while not tdl.event.is_window_closed():
                if game_over:
                    print("Game Over! Generation: {0}, Creature: {1}".format(generation_number, count))
                    print("Score: " + str(snake.get_score()))
                    creature.score = snake.get_score()
                    game_over = False
                    count+=1
                    snake = game.Snake()
                    break
                console.clear()
                res = creature.input(snake.get_inputs())
                snake.set_controlls(res)
                game_over = snake.logic()
                snake.draw(console)
                console.draw_char(game.apple_pos[0], game.apple_pos[1], '@', fg=(255,0,0))
                tdl.flush()

        generation_number += 1
        generation.sort(key=nn_sort_func,reverse=True)

        best = generation[0:10]
        generation.clear()
        for b in best:
            generation.append(b)
            b.set_def_weight(-2)

        for b in best:
            generation.append(b.copy())
            generation[len(generation) - 1].mutate()
            generation.append(b.copy())
            generation[len(generation) - 1].mutate()

        for i in range(int(generation_size / 4)):
            cp = generation[i].copy()
            cp.set_def_weight(-1)
            generation.append(cp)
            cp = generation[i].copy()
            cp.set_def_weight(1)
            generation.append(cp)
            cp = generation[i].copy()
            cp.set_def_weight(2)
            generation.append(cp)



def show_results(filename):
    global game_over
    snake = game.Snake()
    network = wann.NeuralNetwork(nn_sizes)
    network.load_from_file(filename)

    while not tdl.event.is_window_closed():
        if game_over:
            #print("Game Over! Generation: {0}, Creature: {1}".format(generation_number, count))
            print("Score: " + str(snake.get_score()))
            network.score = snake.get_score()
            game_over = False
            break
        console.clear()
        res = network.input(snake.get_inputs())
        snake.set_controlls(res)
        snake.logic()
        snake.draw(console)
        console.draw_char(game.apple_pos[0], game.apple_pos[1], '@', fg=(255,0,0))
        tdl.flush()

#show_results('2058.nn')
learn()