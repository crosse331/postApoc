import math
import random as rnd

count_of_best = 0

class Neuron:
    def __init__(self):
        self.sum = 0
        self.next = []
        self.weights = []
        self.prev = []

    def activation_function(x):
        return 1/(1+math.e**-x)

    def add_next_neuron(self, neuron):
        self.next.append(neuron)
        self.weights.append(rnd.uniform(-1.1, 1.1))

    def add(self, signal):
        self.sum += signal

    def activate(self):
        self.sum = Neuron.activation_function(self.sum)
        for i in range(len(self.next)):
            self.next[i].add(self.sum * self.weights[i])


class Layer:
    def __init__(self, size, prev):
        self.neurons = [Neuron() for _ in range(size)]
        if prev is not None:
            prev.set_next(self)
        self.next_layer = None

    def set_next(self, layer):
        self.next_layer = layer
        for n in self.neurons:
            for n2 in layer.neurons:
                n.add_next_neuron(n2)
                #n2.prev.append(n)


    def input(self, inputs):
        if len(inputs) != len(self.neurons):
            print("Wrong count of inputs!")
            return
        for i in range(len(self.neurons)):
            self.neurons[i].sum = inputs[i]

        self.activate_layer()

    def activate_layer(self):
        if self.next_layer is None:
            #for n in self.neurons:
                #print(n.sum)
            return

        for n in self.neurons:
            n.activate()

        self.next_layer.activate_layer()


class NeuralNetwork:
    def __init__(self, sizes):
        self.layers = []
        for i in range(len(sizes)):
            if i > 0:
                self.layers.append(Layer(sizes[i], self.layers[i-1]))
            else:
                self.layers.append(Layer(sizes[i], None))

    def input(self, inputs):
        self.layers[0].input(inputs)

        result = []
        for n in self.layers[len(self.layers)-1].neurons:
            result.append(n.sum)

        return result

    def save(self):
        global count_of_best
        file = open(str(count_of_best) + '.nn', 'w+')
        count_of_best += 1
        for l in self.layers:
            for n in l.neurons:
                for w in n.weights:
                    file.write(str(w) + "\n")
                file.write("\n")
            file.write("\n")
        file.close()

    def mutate(self):
        for l in self.layers:
            for n in l.neurons:
                for w in n.weights:
                    w += rnd.uniform(-0.01, 0.01)

    def copy(self):
        size = []
        for l in self.layers:
            size.append(len(l.neurons))
            



#nn = NeuralNetwork([4,5,2])
#nn.input((-2,-1,0,1))