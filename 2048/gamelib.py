import  random
import math

class Game:
    def __init__(self):
        self.clear_field()
        self.generate()
        self.score = 0
        self.dont_change_count = 0
        #print(self.field)

    #directions: 0 - left, 1 - up, 2 - right, 3 - down
    def step(self, direction):
        tmp_prev = str(self)
        if direction == 0:
            self.move_left()
        if direction == 1:
            self.move_up()
        if direction == 2:
            self.move_right()
        if direction == 3:
            self.move_down()
        if tmp_prev != str(self):
            self.generate()
        else:
            self.dont_change_count += 1

    def generate(self):
        empty = []
        for i in range(4):
            for j in range(4):
                if self.field[i][j] == 0:
                    empty.append((i,j))
        to_gen = empty[random.randint(0,len(empty)-1)]
        if random.randint(0,10) == 0:
            self.field[to_gen[0]][to_gen[1]] = 4
        else:
            self.field[to_gen[0]][to_gen[1]] = 2


    def move_left(self):
        for i in range(4):
            for j in range(3):
                for k in range(j + 1, 4):
                    if self.field[i][k] == self.field[i][j]:
                        self.field[i][j] *= 2
                        self.field[i][k] = 0
                        self.score += self.field[i][j]
                        break
                    if self.field[i][k] != self.field[i][j] and self.field[i][k] != 0:
                        break
        for _ in range(3):
            for i in range(4):
                for j in range(3, 0, -1):
                    if self.field[i][j] == 0:
                        continue
                    if self.field[i][j - 1] == 0:
                        self.field[i][j - 1] = self.field[i][j]
                        self.field[i][j] = 0

    def move_up(self):
        for j in range(4):
            for i in range(3):
                for k in range(i + 1, 4):
                    if self.field[k][j] == self.field[i][j]:
                        self.field[i][j] *=2
                        self.field[k][j] = 0
                        self.score += self.field[i][j]
                        break
                    if self.field[k][j] != self.field[i][j] and self.field[k][j] != 0:
                        break
        for _ in range(3):
            for j in range(4):
                for i in range(3,0,-1):
                    if self.field[i][j] == 0:
                        continue
                    if self.field[i - 1][j] == 0:
                        self.field[i-1][j] = self.field[i][j]
                        self.field[i][j] = 0

    def move_down(self):
        for j in range(4):
            for i in range(3,0,-1):
                for k in range(i - 1, -1,-1):
                    if self.field[k][j] == self.field[i][j]:
                        self.field[i][j] *=2
                        self.field[k][j] = 0
                        self.score += self.field[i][j]
                        break
                    if self.field[k][j] != self.field[i][j] and self.field[k][j] != 0:
                        break
        for _ in range(3):
            for j in range(4):
                for i in range(0,3,1):
                    if self.field[i][j] == 0:
                        continue
                    if self.field[i + 1][j] == 0:
                        self.field[i+1][j] = self.field[i][j]
                        self.field[i][j] = 0

    def move_right(self):
        for i in range(4):
            for j in range(3,0,-1):
                for k in range(j - 1, -1, -1):
                    if self.field[i][k] == self.field[i][j]:
                        self.field[i][j] *= 2
                        self.field[i][k] = 0
                        self.score += self.field[i][j]
                        break
                    if self.field[i][k] != self.field[i][j] and self.field[i][k] != 0:
                        break
        for _ in range(3):
            for i in range(4):
                for j in range(0, 3, 1):
                    if self.field[i][j] == 0:
                        continue
                    if self.field[i][j + 1] == 0:
                        self.field[i][j + 1] = self.field[i][j]
                        self.field[i][j] = 0

    def clear_field(self):
        self.field = [[0 for _ in range(4)] for __ in range(4)]

    def tests(self):
        self.clear_field()
        self.field = [[1,1,1,1],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        self.step(0)
        print(self.field)
        self.step(2)
        print(self.field)
        self.field = [[1,0,0,0],[1,1,0,0],[1,0,1,0],[1,0,0,1]]
        self.step(1)
        print(self.field)
        self.step(3)
        print(self.field)

    def is_game_over(self):
        if self.dont_change_count == 5:
            return True
        for i in range(4):
            for j in range(4):
                if self.field[i][j] == 0:
                    return False
                if i > 0 and self.field[i][j] == self.field[i-1][j]:
                    return False
                if i < 3 and self.field[i][j] == self.field[i+1][j]:
                    return False
                if j > 0 and self.field[i][j] == self.field[i][j-1]:
                    return False
                if j < 3 and self.field[i][j] == self.field[i][j+1]:
                    return False
        return True

    def to_nn_input(self):
        #print(self.field)
        result = []
        for i in range(4):
            for j in range(4):
                if self.field[i][j] != 0:
                    result.append(math.log2(self.field[i][j]))
                else:
                    result.append(0)
        min = 1000
        for i in result:
            if i < min and i != 0:
                min = i
        min -= 1
        for i in range(len(result)):
            if result[i] > 0:
                result[i] -= min
        #print.res
        return result

    def __str__(self):
        result = "Score: "+str(self.score) + '\n'
        for i in range(4):
            for j in range(4):
                result += str(self.field[i][j]) + " "
            result += '\n'
        return result