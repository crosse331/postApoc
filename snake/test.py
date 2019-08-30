import wann

nn = wann.NeuralNetwork((4,1), 1)
cp = nn.copy()
cp.mutate()
cp.mutate()
cp.mutate()

r = nn.input((0.5,0.1,-2,0.5))
r2 = cp.input((0.5,0.1,-2,0.5))
print(r)
print(r2)