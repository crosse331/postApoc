import math

import gamelib
import wann

game = gamelib.Game()
#test_nn = wann.NeuralNetwork([16,4])

#Test
#while True:
#    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n' + str(game))
#    input()
#    result = game.to_nn_input()
#    print(result)
#    result = test_nn.input(result)
#    print(result)
#    result = nn.Neuron.activation_function(result[0]) * 4
#    print(result)
#    game.step(int(result))

def nn_sort_func(creature):
    return creature.score

generation = []
generation_size = 120
nn_sizes = [16,4]
num_of_generation = 0

top_best = None
while True:
    game = gamelib.Game()

    #generation.clear()
    num_of_generation += 1
    for _ in range(int(generation_size / 4)):
        cur = wann.NeuralNetwork(nn_sizes, -2)
        generation.append(cur)
        cur = cur.copy()
        cur.set_def_weight(-1)
        generation.append(cur)
        cur = cur.copy()
        cur.set_def_weight(1)
        generation.append(cur)
        cur = cur.copy()
        cur.set_def_weight(2)
        generation.append(cur)

    for i in range(generation_size):
        while not game.is_game_over():
            tmp = generation[i].input(game.to_nn_input())
            #tmp = wann.Neuron.activation_function(tmp[0]) * 4
            max = -math.inf
            max_index = -1
            for i in range(len(tmp)):
                if tmp[i] > max:
                    max = tmp[i]
                    max_index = i
            game.step(max_index)
        #print("Gen: " + str(num_of_generation) + " Crea: " + str(i) + '\n' + str(game))
        generation[i].score = game.score
        game = gamelib.Game()
    generation.sort(key = nn_sort_func, reverse=True)
    best = generation[0:10]
    #best[0].save(num_of_generation)
    #if top_best is None or top_best.score < best[0].score:
    #    top_best = best[0]
    print(str(best[0].score))
    generation.clear()
    for b in best:
        generation.append(b)

    for i in range(len(best)):
        cur = best[i].copy()
        cur.mutate()
        generation.append(cur)
        cur = best[i].copy()
        cur.mutate()
        generation.append(cur)

    for i in range(int(generation_size / 4)):
        cur = generation[i].copy()
        cur.set_def_weight(-1)
        generation.append(cur)
        cur = generation[i].copy()
        cur.set_def_weight(1)
        generation.append(cur)
        cur = generation[i].copy()
        cur.set_def_weight(2)
        generation.append(cur)

