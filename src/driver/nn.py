from driver.driver import Driver
import math
import random
import copy

class NN(Driver):
    @classmethod
    def random_nn_driver(cls, sensors_size, hidden_layer_size):
        sensor_weights = [[random.random() * 2 - 1 for i in range(0, sensors_size)] for j in range(0, hidden_layer_size)]
        hidden_weights = [[random.random() * 2 - 1 for i in range(0, hidden_layer_size)] for j in range(0, 2)]

        return NN(sensor_weights, hidden_weights)

    @classmethod
    def blank_driver(cls, sensors_size, hidden_layer_size):
        sensor_weights = [[0 for i in range(0, sensors_size)] for j in
                          range(0, hidden_layer_size)]
        hidden_weights = [[0 for i in range(0, hidden_layer_size)] for j in range(0, 2)]

        return NN(sensor_weights, hidden_weights)

    def __init__(self, sensor_weights, hidden_weights):
        assert(len(hidden_weights) == 2)
        assert(len(hidden_weights[0]) == len(hidden_weights[1]))

        assert(len(set([len(w) for w in sensor_weights])) == 1)

        self._sensor_weights = sensor_weights
        self._hidden_weights = hidden_weights


    def steer(self, sensor_readings, speed, direction):
        assert(len(sensor_readings) == len(self._sensor_weights[0]))

        hidden_state = [_activation(sensor_readings, w) for w in self._sensor_weights]
        output_state = [_activation(hidden_state, w) for w in self._hidden_weights]

        return output_state

    def mutate(self, chance=0.2):
        new_sensor_w = copy.deepcopy(self._sensor_weights)
        for i in range(0, len(new_sensor_w)):
            for j in range(0, len(new_sensor_w[i])):
                if random.random() < chance:
                    new_sensor_w[i][j] = random.random() * 2 - 1

        new_hiddden_w = copy.deepcopy(self._hidden_weights)
        for i in range(0, len(new_hiddden_w)):
            for j in range(0, len(new_hiddden_w[i])):
                if random.random() < chance:
                    new_hiddden_w[i][j] = random.random() * 2 - 1

        return NN(new_sensor_w, new_hiddden_w)

def _activation(inputs, weights):
    z = sum([inputs[i] * weights[i] for i in range(0, len(inputs))])
    return math.tanh(z)

__all__ = ["NN"]