import simpy


# Trying a bike method
def bike(env):

    while True:

        print('Start pickup at %d' % env.now)

        pickup_duration = 2

        yield env.timeout(pickup_duration)


        print('Start delivering at %d' % env.now)

        trip_duration = 5

        yield env.timeout(trip_duration)


# This class handles the behaviour of a drone
class Drone(object):

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

            trip_duration = 2

            yield self.env.timeout(trip_duration)


    def charge(self, duration):

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

    def charge(self, duration):

        yield self.env.timeout(duration)




# Start of code
env = simpy.Environment()
env.process(bike(env))
env.run(until=20)
