import template
import numpy as np

class Car:
    def __init__(self):
        self.mass = 1
        self.position = 0
        self.velocity = 0
        self.acceleration = 0
        self.friction_coefficient = 0.1

    def update(self, in_acceleration, dt):
        self.acceleration = in_acceleration
        if self.velocity > 0:
            self.acceleration -= self.friction_coefficient * self.mass
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt


class Environment(template.Environment):
    def __init__(self):
        self._leader_car = Car()
        self._max_acceleration = 10

        self.l_position = self._leader_car.position
        self.l_velocity = self._leader_car.velocity
        
        self.l_pedal = None

    def reset(self, initial_parameters=None):
        if not initial_parameters:
            self.update([0], 0)
        else:
            pos, vel = initial_parameters
            self.l_position = pos
            self.l_velocity = vel

    def update(self, parameters, dt):
        # the environment updates according to the parameters
        self.l_pedal = parameters[0]
        self._leader_car.update(self.l_pedal * self._max_acceleration, dt)
        self.l_position = self._leader_car.position

class Agent(template.Agent):
    def __init__(self):
        self._car = Car()
        self._max_acceleration = 10

        self.position = self._car.position
        self.velocity = self._car.velocity
        self.distance = None
        
        self.pedal = None

    def reset(self, initial_parameters=None):
        if not initial_parameters:
            self.update([0], 0)
        else:
            pos, vel = initial_parameters
            self.l_position = pos
            self.l_velocity = vel

    def update(self, parameters, dt):
        # the action take place and updates the variables
        self.pedal = parameters[0]
        self._car.update(self.pedal * self._max_acceleration, dt)
        self.position = self._car.position
        
        self.distance = self._environment.l_position - self.position

class Model:
    
    def __init__(self):
        # setting of the initial conditions

        self.agent = Agent()
        self.environment = Environment()

        self.agent.set_environment(self.environment)
        self.environment.set_agent(self.agent)

        self.agent.reset()
        self.environment.reset()

        self._time = 0
        self._records = []

    def step(self, env_input, agent_input, dt):
        # the configuration is generated by the NN

        self.environment.update(env_input, dt)

        # NN should evaluate the moves

        self.agent.update(agent_input, dt)

        # status of the system, env and agent params should be recorded
        self._time += dt
        status = (self._time, self.environment.l_position, \
                self.agent.position, self.agent.distance)
        self._records.append(status)

    def get_records(self):
        return np.array(self._records).T
        
