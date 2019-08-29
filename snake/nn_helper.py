import math


def simple(x):
    if x < 0:
        return 0
    else:
        return 1

def sign(x):
    if x > 0:
        return 1
    else:
        return -1

def sigmoid(x):
    return 1/(1 + math.exp(-x))

def half_line(x):
    if x > 0:
        return x
    else:
        return 0

def line(x):
    return x

def rad_baz(x):
    return math.exp(math.pow(-x,2))

def half_line_norm(x):
    if x <= 0:
        return 0
    elif x > 1:
        return 1
    return x

def line_norm(x):
    if x <= -1:
        return -1
    elif x > 1:
        return 1
    return x

def hyp_tan(x):
    return (math.exp(x) - math.exp(-x))/(math.exp(x) + math.exp(-x))

def triangle(x):
    if math.fabs(x) <=1:
        return 1-math.fabs(x)
    return 0