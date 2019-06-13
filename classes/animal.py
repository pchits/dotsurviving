from random import randint
import numpy as np
import math
import csv
from classes.brain import NeuralNetwork
from datetime import datetime

class Animal:

    def __init__(self, field_size):
        self.field_size = field_size
        self.position = self.generate_position()
        # 1-left 2-right 3-up 4-down
        self.face_direction = np.random.randint(1, 5)

    def generate_corner_position(self):
        # Generate corner position
        area = np.random.randint(1, 5)
        if area == 1:
            return [0, 0]
        elif area == 2:
            return [self.field_size - 1, 0]
        elif area == 3:
            return [0, self.field_size - 1]
        
        return [self.field_size - 1, self.field_size - 1]

    def generate_position(self):
        # Generate random position
        return [np.random.randint(0, self.field_size - 1), np.random.randint(0, self.field_size - 1)]

    def move(self, direction):

        movement = [0, 0]
        # generane movement vector based on direction and current orientation
        if self.face_direction == 1:
            if direction == -1:
                movement[1] = 1
                self.face_direction = 4
            elif direction == 0:
                movement[0] = -1
            elif direction == 1:
                movement[1] = -1
                self.face_direction = 3
            
        elif self.face_direction == 2:
            if direction == -1:
                self.face_direction = 3
                movement[1] = -1
            elif direction == 0:
                movement[0] = 1
            elif direction == 1:
                movement[1] = 1
                self.face_direction = 4
            
        elif self.face_direction == 3:
            if direction == -1:
                movement[0] = -1
                self.face_direction = 1
            elif direction == 0:
                movement[1] = -1
            elif direction == 1:
                movement[0] = 1
                self.face_direction = 2

        elif self.face_direction == 4:
            if direction == -1:
                movement[0] = 1
                self.face_direction = 2
            elif direction == 0:
                movement[1] = 1
            elif direction == 1:
                movement[0] = -1
                self.face_direction = 1

        new_pos_x = self.position[0] + movement[0]
        new_pos_y = self.position[1] + movement[1]

        self.position = [new_pos_x, new_pos_y]

    def collision_detector(self):
        if (self.position[0] == -1 or
            self.position[0] == (self.field_size) or
            self.position[1] == -1 or
            self.position[1] == (self.field_size)):
            return 1
        else:
            return 0
        
    def is_direction_blocked(self, direction):
        # check if direction is blocked
        # save current position and try to move at suggested direction
        current_position = self.position
        current_face_direction = self.face_direction
        self.move(direction)
        collision = self.collision_detector()
        # repare object position and orientation
        self.position = current_position
        self.face_direction = current_face_direction
        return collision

    def generate_action(self):
        # generate direction suggestion
        return np.random.randint(-1, 2)

    def generate_observation(self, direction):
        barrier_left = self.is_direction_blocked(-1)
        barrier_forward = self.is_direction_blocked(0)
        barrier_right = self.is_direction_blocked(1)
        
        return [direction, barrier_left, barrier_forward, barrier_right]

    def brain(self, input_layer):
        X = np.array([input_layer])
        y = np.array([[0]])
        nn = NeuralNetwork(X,y)
        nn.load()
        nn.feedforward()

        return nn.output

    def make_turn(self):
        wat = ''

        turns = [-1, 0, 1]
        
        prev_decision = 0
        best_observation = []
        for x in turns:
            observation = self.generate_observation(x)
            decision = self.brain(observation)
            
            if (decision[0] > prev_decision):
                best_observation = observation
        
        self.move(best_observation[0])
        
        collision = self.collision_detector()

        if collision == 1:
            wat = 'ubilsya ob stenu'
        else:
            wat = 'continue'
        return wat

    def train(self):
        X = []
        y = []
        with open('learning_data.csv', mode = 'r') as csv_file:
            data = list(csv.reader(csv_file))
        for row in data:
            line = []
            for d in row[0:4]:
                line.append(int(d))
            X.append(line)
            y.append([int(row[4])])

        X = np.array(X)
        y = np.array(y)

        nn = NeuralNetwork(X,y)

        for i in range(9000):
            nn.feedforward()
            nn.backprop()

        nn.save()

        with open('output.csv', 'w', newline = '') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(nn.output)
        
    def generate_test_data(self):

        with open('learning_data.csv', mode = 'w') as learning_animal_file:
            employee_writer = csv.writer(learning_animal_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            
            for step in range(1000):
                
                self.position = self.generate_corner_position()
                action = self.generate_action()
                observation = self.generate_observation(action)

                self.move(observation[0])
                
                collision = self.collision_detector()

                output = collision

                observation.append(output)
            
                employee_writer.writerow(observation)



