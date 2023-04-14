from random import random, randint
from copy import deepcopy
from time import sleep
import os
import ai

# Inputs: Vision, Energy
# Outputs: Split, Direction


class Eco:
    def __init__(self, width=10, height=10):
        self.bounds = (width, height)

        # All creatures and food
        self.creatures = []
        self.food = []

        # Values for se = spawn energy, fv = food value (range)
        self.se = 10
        self.fv = (9, 9)

        # Spawn rate and gen rate for creatures and food respectively
        self.sr = 0.05
        self.gr = 0.5

        # Split rate and entropy for AI training.
        self.rr = 0.01
        self.entropy = 0.1

    # Spawns creature
    def spawn(self, amount=1):
        for _ in range(amount):
            self.creatures.append(
                self.Creature(
                    randint(0, self.bounds[0] - 1),
                    randint(0, self.bounds[1] - 1),
                    self.se
                )
            )

    # Generates food
    def generate(self, amount=1):
        for _ in range(amount):
            self.food.append(
                self.Food(
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
            creature.bind(self.bounds[0], self.bounds[1])

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
        def __init__(self, x: int, y: int, energy):
            self.location = [x, y]
            self.energy = energy  # Needs energy to move.

        def feed(self, amount):
            self.energy += amount

        def move(self, d):
            if self.energy > 0:
                if int(d) == 1:
                    self.location[1] -= 1
                elif int(d) == 2:
                    self.location[0] += 1
                elif int(d) == 3:
                    self.location[1] += 1
                elif int(d) == 4:
                    self.location[0] -= 1
                self.energy -= 1

        # If the creature is out of bounds, it keeps its position but puts the actual coordinates in bounds.
        def bind(self, width, height):
            if self.location[1] > height - 1:
                self.location[1] -= height
            if self.location[1] < 0:
                self.location[1] += height
            if self.location[0] > width - 1:
                self.location[0] -= width
            if self.location[0] < 0:
                self.location[0] += width

        def refresh(self):
            self.move(randint(1, 4))

    class Food:
        def __init__(self, x: int, y: int, value):
            self.location = [x, y]
            self.value = value


# eco = Eco(100, 10)
# eco.spawn()
# eco.main()

# net = ai.Network(2, 2, 10, 10, 5, 5, 4)
net = ai.Network(2, 2)
print(net)
print(net.run([1, 2]))
