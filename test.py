import simpy


def car(env, name, station, driving_time, charge_duration):

    # Simulate driving to the BCS

    yield env.timeout(driving_time)


    # Request one of its charging spots

    print('%s arriving at %d' % (name, env.now))

    with station.request() as request:

        yield request


        # Charge the battery

        print('%s starting to charge at %s' % (name, env.now))

        yield env.timeout(charge_duration)

        print('%s leaving the bcs at %s' % (name, env.now))



# Start of code
environment = simpy.Environment()
station = simpy.Resource(environment, capacity=2)
environment.process(car(environment, "steve", station, 5, 10))
environment.run(until=20)
