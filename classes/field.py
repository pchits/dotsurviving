from random import randint
from classes.animal import Animal
import numpy as np
import math
import csv

class Field:

    def __init__(self, size):
        self.size = size
    
    def play(self):
        history = []
        self.animal = Animal(self.size)
        history.append([self.animal.position])
        # 
        for step in range(15):
            res = self.animal.make_turn()
            if res == 'continue':
                history.append([self.animal.position])
            else:
                break
        return {'history': history, 'report': res}

    def learn(self):
        self.animal = Animal(self.size)
        # self.prey = Animal(self.size)
        self.animal.generate_test_data()

    def go_train(self):
        self.animal = Animal(self.size)
        # self.prey = Animal(self.size)
        self.animal.train()

