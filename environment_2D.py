from time import sleep
import random
import os


class Eco:
    def __init__(self, width, height):

        # All blank spaces are marked as 0. Anything else is food, and it has a value from 1 to 10.
        self.bounds = (width, height)
        self.creatures = []
        self.food = []

    def spawn(self):
        self.creatures.append(
            self.Creature(
                random.randint(0, self.bounds[0] - 1),
                random.randint(0, self.bounds[1] - 1),
                10000
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

    def main(self):
        while True:
            print("[1] Run\n[2] Break")
            inp = input('\n[>] Enter your choice: ')

            if inp == "1":
                for n in range(int(input("[>] Enter frames to run: "))):
                    os.system('cls')
                    self.print()
                    self.refresh_creatures()
                    sleep(0.01)
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
            self.move(random.randint(1, 4))

    class Food:
        def __init__(self, x, y, value):
            self.location = [x, y]
            self.value = value


eco = Eco(25, 10)
print(f'[+] Eco created. Bounds: ({eco.bounds[0]}, {eco.bounds[1]})')
eco.spawn()

print(f'[+] Creature added. Location: ({eco.creatures[0].location[0]}, {eco.creatures[0].location[1]})\n')
eco.main()
