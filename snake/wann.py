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
        self.prev = []
        self.act_func = functions[2]
        self.was_activated = False
        self.def_weight = def_weight

    def add_next_neuron(self, neuron):
        if neuron in self.prev:
            return
        self.next.append(neuron)
        neuron.prev.append(self)

    def remove_next_neuron(self, neuron):
        self.next.remove(neuron)
        neuron.prev.remove(self)

    def add(self, signal):
        self.sum += signal

    def activate(self):
        #self.sum = Neuron.activation_function(self.sum)
        self.sum = self.act_func(self.sum)
        for i in range(len(self.next)):
            self.next[i].add(self.sum * self.def_weight)
        self.was_activated = True

    def check_prevs(self):
        for p in self.prev:
            if not p.was_activated and p not in self.next:
                return False
        return True

    def change_act_func(self):
        cur_index = functions.index(self.act_func)
        new_index = rnd.randint(0,len(functions)-1)
        while cur_index == new_index:
            new_index = rnd.randint(0, len(functions)-1)
        self.act_func = functions[new_index]


class NeuralNetwork:
    def __init__(self, sizes, def_weight):
        self.neurons = []
        self.in_layer = []
        self.out_layer = []
        self.def_weight = def_weight
        for _ in range(sizes[0]):
            self.neurons.append(Neuron(def_weight))
            self.in_layer.append(self.neurons[len(self.neurons) - 1])

        for _ in range(sizes[1]):
            new_out = Neuron(def_weight)
            self.neurons.append(new_out)
            self.out_layer.append(new_out)
            for n in self.in_layer:
                if rnd.randint(0,2) < 2:
                    n.add_next_neuron(new_out)
            if len(new_out.prev) == 0:
                self.in_layer[0].add_next_neuron(new_out)
            #self.in_layer[rnd.randint(0,len(self.in_layer))].add_next_neuron(self.out_layer[len(self.out_layer) - 1])

    def set_def_weight(self, def_weight):
        self.def_weight = def_weight
        for n in self.neurons:
            n.def_weight = def_weight

    def input(self, inputs):
        #print("start input")
        to_work = []
        for n in self.neurons:
            n.was_activated = False
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
        new_nn = NeuralNetwork(size, self.def_weight)
        new_nn.neurons.clear()
        new_nn.in_layer.clear()
        new_nn.out_layer.clear()
        for n in self.neurons:
            new_n = Neuron(self.def_weight)
            if n in self.in_layer:
                new_nn.in_layer.append(new_n)
            if n in self.out_layer:
                new_nn.out_layer.append(new_n)
            new_nn.neurons.append(new_n)

        for i in range(len(self.neurons)):
            for next_n in self.neurons[i].next:
                new_nn.neurons[i].add_next_neuron(new_nn.neurons[self.neurons.index(next_n)])

        return new_nn


    def mutate(self):
        #print("start mutate")
        #cp = self.copy()
        mutate_type = rnd.randint(0,2)
        if mutate_type == 0:
            #Incert neuron
            #print("-- start incert neuron")
            while True:
                #find neuron connection
                test_n = self.neurons[rnd.randint(0,len(self.neurons)-1)]
                if len(test_n.next) != 0:
                    index_to_gen = rnd.randint(0, len(test_n.next)-1)
                    new_n = Neuron(self.def_weight)
                    self.neurons.append(new_n)
                    test_n.add_next_neuron(new_n)
                    new_n.add_next_neuron(test_n.next[index_to_gen])
                    test_n.remove_next_neuron(test_n.next[index_to_gen])
                    break
        elif mutate_type == 1:
            #add new connection
            #print("-- start add new connection")
            if len(self.neurons) == 1:
                return
            first = self.neurons[rnd.randint(0,len(self.neurons)-1)]
            second = self.neurons[rnd.randint(0,len(self.neurons)-1)]
            anti_inf = 0
            while True:
                if first != second and\
                        second not in first.next and\
                        first not in second.next and\
                        first not in self.out_layer:
                    break
                second = self.neurons[rnd.randint(0, len(self.neurons)-1)]
                anti_inf +=1
                if anti_inf > 100:
                    return
            first.add_next_neuron(second)
        elif mutate_type == 2:
            #change activate function
            #print("-- start change act func")
            cur = self.neurons[rnd.randint(0, len(self.neurons)-1)]
            while cur in self.out_layer:
                cur = self.neurons[rnd.randint(0, len(self.neurons)-1)]
            cur.change_act_func()




