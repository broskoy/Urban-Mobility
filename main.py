import simpy
from locations import LOCATIONS
import drone  # access drone module directly
from bike import setup as setup_bikes

# Simulated period (8 hours)
SIM_TIME = 8 * 60  # minutes

def setup_drones(env):
    """
    Initialise drone hubs and stores in the shared SimPy environment.
    Replaces the missing setup() helper inside drone.py.
    """
    # reset static server state for repeatable runs
    drone.Server.hubs.clear()
    drone.Server.package_number = 0

    # create one Hub and one Store per location
    for loc in LOCATIONS.keys():
        drone.Server.hubs[loc] = drone.Hub(env, loc)
        drone.Store(env, loc)

    return drone.Server

def run_multimodal_sim():
    env = simpy.Environment()

    # Initialise both transport modes
    bike_dispatcher = setup_bikes(env)
    # drone_server = setup_drones(env)

    env.run(until=SIM_TIME)

    # Optional: end‑of‑day summaries
    print("\n--- Bike finance ---")
    print(f"Revenue: {bike_dispatcher.total_revenue:.2f}")
    print(f"Cost:    {bike_dispatcher.total_cost:.2f}")
    print(f"Profit:  {bike_dispatcher.total_revenue - bike_dispatcher.total_cost:.2f}")

    # if hasattr(drone_server, "stats"):
    #     print("\n--- Drone stats ---")
    #     drone_server.stats.pretty_print()


if __name__ == "__main__":
    run_multimodal_sim()