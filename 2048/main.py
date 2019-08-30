import gamelib
import nn

game = gamelib.Game()
test_nn = nn.NeuralNetwork([16,32,16,1])

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
generation_size = 200
nn_sizes = [16,64,32, 16,1]
num_of_generation = 0

top_best = None
while True:
    game = gamelib.Game()

    #generation.clear()
    num_of_generation += 1
    for _ in range(generation_size):
        generation.append(nn.NeuralNetwork(nn_sizes))
    for i in range(generation_size):
        while not game.is_game_over():
            tmp = generation[i].input(game.to_nn_input())
            tmp = nn.Neuron.activation_function(tmp[0]) * 4
            game.step(int(tmp))
        #print("Gen: " + str(num_of_generation) + " Crea: " + str(i) + '\n' + str(game))
        generation[i].score = game.score
        game = gamelib.Game()
    generation.sort(key = nn_sort_func, reverse=True)
    best = generation[0:10]
    best[0].save(num_of_generation)
    if top_best is None or top_best.score < best[0].score:
        top_best = best[0]
    print(str(best[0].score))
    generation.clear()
    for b in best:
        generation.append(b)
    generation.append(top_best)

    for _ in range(generation_size):
        generation.append(best[0].copy())
        generation[len(generation) - 1].mutate()

