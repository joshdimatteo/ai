from time import sleep
import random
import os


class Eco:
    def __init__(self, width, height):

        # Creatures are represented with a 1. Food is represented with a 2. Blank is 0.
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.creatures = []

    def spawn(self):
        self.creatures.append(
            self.Creature(
                random.randint(0, len(self.board[0])),
                random.randint(0, len(self.board))
            )
        )

    def print(self):
        print('┏' + '━' * len(self.board[0]) * 2 + '┓')
        for row in range(len(self.board)):
            print('┃', end='')
            for column in range(len(self.board[row])):
                if self.board[row][column] == 0:
                    print(' ', end=' ')
                elif self.board[row][column] == 1:
                    print('█', end=' ')
            print('┃')
        print('┗' + '━' * len(self.board[0]) * 2 + '┛')

    def refresh_board(self):

        # Marks all the creature's locations
        self.board = [[0 for w in range(len(self.board[0]))] for h in range(len(self.board))]
        for creature in self.creatures:
            self.board[creature.location[1]][creature.location[0]] = 1

        # Randomly generates food (can't overlap with a creature)

    def refresh_creatures(self):
        for creature in self.creatures:

            # Gets the creature's position updated.
            creature.refresh()
            creature.bind(len(self.board[0]), len(self.board))

            # Checks if the creature is overlapping with food. Food gives random
            if self.board[creature.location[1]][creature.location[0]] == 2:
                creature.feed()

    def main(self):
        while True:
            print("[1] Run\n[2] Break")
            inp = input('\n[>] Enter your choice: ')

            if inp == "1":
                for n in range(int(input("[>] Enter frames to run: "))):
                    os.system('cls')
                    self.refresh_board()
                    self.print()
                    self.refresh_creatures()
                    sleep(0.1)
            elif inp == "2":
                break

    class Creature:
        def __init__(self, x, y):
            self.location = [x, y]
            self.energy = 10000  # Needs energy to move.

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


eco = Eco(25, 10)
eco.spawn()
eco.main()
