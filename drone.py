import simpy
import random
import math


# This class handles the behaviour of a drone
class Drone(object):

    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())


    def run(self):

        while True:

            print('Start parking and charging at %d' % self.env.now)
            charge_duration = 5
            # We yield the process that process() returns
            # to wait for it to finish
            yield self.env.process(self.charge(charge_duration))
            # The charge process has finished and
            # we can start driving again.
            print('Start driving at %d' % self.env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)


    def charge(self, duration):
        with charging_spot.request() as req:
            yield req
            yield self.env.timeout(duration)



# This class handles the behaviour of a hub
class Hub(object):



    def __init__(self, env):
        self.env = env
        # Start the run process everytime an instance is created.
        self.action = env.process(self.run())


    def run(self):

        while True:
            print('Start parking and charging at %d' % self.env.now)
            charge_duration = 5
            # We yield the process that process() returns
            # to wait for it to finish
            yield self.env.process(self.charge(charge_duration))
            # The charge process has finished and
            # we can start driving again.
            print('Start driving at %d' % self.env.now)


# demand
def store(env, dispatcher):
    while True:
        yield env.timeout(random.expovariate(ARRIVAL_RATE/60))

        # Add origin and detination 
        origin = random.choice(list(LOCATIONS))
        dest = random.choice([l for l in LOCATIONS if l != origin])
        print(f'[{env.now:.1f} min] New parcel request: {origin} → {dest}')
        dispatcher.dispatch((origin, dest))