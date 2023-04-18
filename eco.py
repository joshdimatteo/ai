from random import random, randint
from copy import deepcopy
from time import sleep
import os
import ai

# Inputs: Vision, Energy
# Outputs: Split, Direction


# x1 and y1 are the current coordinates and x2 and y2 are the bounds.
def bind(x1, y1, x2, y2):
    if y1 > y2 - 1:
        y1 -= y2
    if y1 < 0:
        y1 += y2
    if x1 > x2 - 1:
        x1 -= x2
    if x1 < 0:
        x1 += x2

    return x1, y1


class Eco:

    def __init__(self, width=10, height=10):
        self.bounds = (width, height)

        # All creatures and food
        self.creatures = []
        self.food = []

        # Values for se = spawn energy, fv = food value (range), vi = vision radius
        self.se = 10
        self.fv = (1, 9)
        self.vi = 4

        # Spawn rate and gen rate for creatures and food respectively
        self.sr = 0.05
        self.gr = 0.5

        # Entropy for AI training.
        self.entropy = 0.1

    # Gets info on a position. Creature = -1, Blank = 0, Food = Range
    def get(self, x, y):
        x, y = bind(x, y, self.bounds[0], self.bounds[1])

        # Checks for creatures
        for creature in self.creatures:
            if creature.location == [x, y]:
                return -1
        for food in self.food:
            if food.location == [x, y]:
                return food.value
        return 0

    # Spawns creature
    def spawn(self, amount=1):
        for _ in range(amount):
            self.creatures.append(
                Creature(
                    randint(0, self.bounds[0] - 1),
                    randint(0, self.bounds[1] - 1),
                    self
                )
            )

    # Generates food
    def generate(self, amount=1):
        for _ in range(amount):
            self.food.append(
                Food(
                    randint(0, self.bounds[0] - 1),
                    randint(0, self.bounds[1] - 1),
                    randint(self.fv[0], self.fv[1])
                )
            )

    def print(self):

        # Marks all the creature's locations
        board = [[' ' for _ in range(self.bounds[0])] for _ in range(self.bounds[1])]
        for creature in self.creatures:
            board[creature.location[1]][creature.location[0]] = '■'
        for food in self.food:
            board[food.location[1]][food.location[0]] = food.value

        print('┏' + '━' * (self.bounds[0] + 1) * 2 + '┓')
        for row in range(self.bounds[1]):
            print('┃ ', end='')
            for column in range(self.bounds[0]):
                print(board[row][column], end=' ')
            print(' ┃')
        print('┗' + '━' * (self.bounds[0] + 1) * 2 + '┛')

    def refresh_creatures(self):
        for creature in self.creatures:

            # Gets the creature's position updated.
            creature.refresh()
            creature.location = bind(creature.location[0], creature.location[1], self.bounds[0], self.bounds[1])

            # Checks if the creature is overlapping with food. If so, feed the creature and delete the food.
            for food in self.food:
                if food.location == creature.location:
                    creature.feed(food.value)
                    self.food.remove(food)

            # Checks the energy of the creature. If it's out, kill it.
            if creature.energy == 0:
                self.creatures.remove(creature)

    def main(self):
        while True:

            # Gets input
            print("[1] Run\n[2] Break")
            inp = input('\n[>] Enter your choice: ')

            # Runs simulation
            if inp == "1":
                for n in range(int(input("[>] Enter frames to run: "))):

                    # Prints board
                    os.system('cls')
                    self.print()

                    # Refreshes creatures
                    self.refresh_creatures()

                    # Adds food
                    if random() <= self.gr:
                        self.generate()

                    # Spawns creatures
                    if random() <= self.sr:
                        self.spawn()

                    # Splits creatures
                    for creature in self.creatures:
                        if random() <= self.rr:
                            creature.energy = int(creature.energy / 2)
                            self.creatures.append(deepcopy(creature))

                    sleep(0.1)
            elif inp == "2":
                break


class Creature:

    # Vision is the radius of its vision.
    def __init__(self, x: int, y: int, env: Eco):
        self.location = [x, y]
        self.energy = env.se  # Needs energy to move.

        # 2D array with coordinates for vision.
        self.vision = []
        self.env = env

        # For each row in vision.
        for i in range(env.vi * 2 + 1):

            # Adds a layer to vision and sets y value.
            self.vision.append([])
            y = -i + env.vi

            # Amount of columns is calculated from -|2(x - rad)| + 2(rad) + 1
            for j in range(-abs(2 * i - 2 * env.vi) + 2 * env.vi + 1):

                if (j + (abs(y) - env.vi), y) != (0, 0):
                    self.vision[i].append((j + (abs(y) - env.vi), y))

        # Vision inputs, 4 outputs for up, down, left, right. 1 for splitting.
        self.net = ai.Network(
            2 * env.vi * env.vi + 2 * env.vi,
            5
        )
        self.net.randomize(env.entropy)

    def feed(self, amount):
        self.energy += amount

    def refresh(self):

        # If there is any energy left
        if self.energy <= 0:
            return

        # Gets inputs for neural network.
        inputs = []

        for layer in self.vision:
            for value in layer:
                inputs.append(self.env.get(self.location[0] + value[0], self.location[1] + value[1]))

        # Gets outputs and finds the one with the highest value
        out = self.net.run(inputs)

        direction = 0
        for i in range(len(out)):
            if out[i] > out[direction]:
                direction = i
        direction += 1

        # This is super scuffed, but it's probably going to work. Moves the creature.
        if direction == 1:
            self.location[1] -= 1
        elif direction == 2:
            self.location[0] += 1
        elif direction == 3:
            self.location[1] += 1
        elif direction == 4:
            self.location[0] -= 1

        # Deletes energy
        self.energy -= 1

        # Decides whether to split
        if ai.step(out[4]) == 1:
            self.energy /= 2
            clone = deepcopy(self)
            clone.net.randomize(self.env.entropy)
            self.env.creatures.append(clone)


class Food:
    def __init__(self, x: int, y: int, value):
        self.location = [x, y]
        self.value = value


# eco = Eco(100, 10)
# eco.spawn()
# eco.main()
