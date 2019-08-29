import math
import random as rnd

import nn_helper

functions = [nn_helper.simple,
             nn_helper.sign,
             nn_helper.sigmoid,
             nn_helper.half_line,
             nn_helper.line,
             nn_helper.rad_baz,
             nn_helper.half_line_norm,
             nn_helper.line_norm,
             nn_helper.hyp_tan,
             nn_helper.triangle]


class Neuron:

    def __init__(self, def_weight):
        self.sum = 0
        self.next = []
        self.weights = []
        self.prev = []
        self.act_func = functions[0]
        self.was_activated = False
        self.def_weight = def_weight

    def activation_function(x):
        return 1/(1+math.e**-x)

    def add_next_neuron(self, neuron):
        self.next.append(neuron)
        neuron.prev.append(self)
        self.weights.append(self.def_weight)

    def add(self, signal):
        self.sum += signal

    def activate(self):
        #self.sum = Neuron.activation_function(self.sum)
        self.sum = self.act_func(self.sum)
        for i in range(len(self.next)):
            self.next[i].add(self.sum * self.weights[i])

    def check_prevs(self):
        for p in self.prev:
            if not p.was_activated:
                return False
        return True


class NeuralNetwork:
    def __init__(self, sizes, def_weight):
        self.neurons = []
        self.in_layer = []
        self.out_layer = []
        for _ in range(sizes[0]):
            self.neurons.append(Neuron(def_weight))
            self.in_layer.append(self.neurons[len(self.neurons) - 1])

        for _ in range(sizes[1]):
            self.neurons.append(Neuron(def_weight))
            self.out_layer.append(self.neurons[len(self.neurons) - 1])
            self.in_layer[rnd.randint(0,len(self.in_layer))].add_next_neuron(self.out_layer[len(self.out_layer) - 1])

    def input(self, inputs):
        to_work = []
        for n in self.neurons:
            to_work.append(n)
        inp_index = 0
        while len(to_work) > 0:
            cur = to_work[0]
            del to_work[0]
            if not cur.check_prevs():
                to_work.append(cur)
                continue
            if inp_index < len(inputs):
                cur.add(inputs[inp_index])
                inp_index+=1
            cur.activate()

        result = []
        for n in self.out_layer:
            result.append(n.sum)
        return result

    def copy(self):
        size = []
        size.append(len(self.in_layer))
        size.append(len(self.out_layer))
        
