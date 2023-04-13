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
        layers.append(0)
        self.layers = [[self.Neuron(layers[layer + 1]) for _ in range(layers[layer])] for layer in range(len(layers) - 1)]

    def __str__(self):
        out = ""
        for layer in self.layers:
            out += str([len(neuron.outputs) for neuron in layer]) + "\n"
        return out

    class Neuron:

        # Takes the length of the next layer to determine how many weights it needs
        def __init__(self, next_layer):
            self.bias = 0
            self.outputs = [1 for _ in range(next_layer)]

        # Takes a dictionary of values and corresponding weights
        def calculate(self, inputs):
            out = 0
            for value in inputs.keys:
                out += value * inputs[value]
            return l_relu(out + self.bias)
