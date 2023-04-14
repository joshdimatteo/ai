def step(n):
    if n < 0:
        return 0
    return 1


def linear(n):
    return 4 * n


def relu(n):
    if n > 0:
        return n
    return 0


def l_relu(n):
    if n > 0:
        return n
    return 0.01 * n


def p_relu(a, n):
    if n > 0:
        return n
    return a * n


class Network:
    def __init__(self, *layers):
        layers = list(layers)

        # Creates layers. 2D Array of neurons. Each neuron is passed in the previous layer as a parameter.
        self.layers = [[self.Neuron(layers[i - 1]) for _ in range(layers[i])] for i in range(1, len(layers))]

    def __str__(self):
        out = ""
        for layer in self.layers:
            out += str([len(neuron.weights) for neuron in layer]) + "\n"
        return out

    def run(self, inputs):
        values = list(inputs)

        # Goes through each layer and in order passes the values to each neuron and records them.
        for layer in self.layers:
            new_values = []

            for neuron in layer:
                new_values.append(neuron.calculate(values))

            values = new_values

        return values

    class Neuron:

        # Takes the length of the previous layer to determine how many weights it needs
        def __init__(self, prev_layer):
            self.bias = 0
            self.weights = [1 for _ in range(prev_layer)]

        # Takes a list of values and applies input weights
        def calculate(self, inputs):
            out = 0
            for i in range(len(inputs)):
                out += inputs[i] * self.weights[i]
            return l_relu(out + self.bias)
