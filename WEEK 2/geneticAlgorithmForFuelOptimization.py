import random
print("Ayush R Kallingal\n1WN24CS057")
# ============================================================
# GENETIC ALGORITHM - FUEL OPTIMIZATION
# ============================================================

POP_SIZE = 60
MAX_GENERATIONS = 100

CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.1


# ============================================================
# 1. USER INPUTS - FIXED CONSTRAINTS
# ============================================================

print("=" * 60)
print("       GENETIC ALGORITHM - FUEL OPTIMIZER")
print("=" * 60)

distance = float(input("Distance to travel (km): "))
road_condition = float(input("Road condition (1-10): "))
traffic_condition = float(input("Traffic condition (1-10): "))
vehicle_load = float(input("Additional load (kg): "))
base_mileage = float(input("Vehicle base mileage (km/L): "))

weather = float(input("Weather severity (1-10): "))
terrain = float(input("Terrain difficulty (1-10): "))

print("\nRunning Genetic Algorithm...\n")


# ============================================================
# 2. INDIVIDUAL
#
# Each individual represents ONE possible driving strategy
#
# [fuel, speed, acceleration, braking, AC, idle_time]
# ============================================================

def create_individual():

    fuel = random.uniform(
        distance / base_mileage * 0.8,
        distance / base_mileage * 2.0
    )

    speed = random.uniform(30, 90)

    acceleration = random.uniform(
        0.2, 3.5
    )

    braking = random.uniform(
        0.2, 3.5
    )

    ac = random.uniform(
        0, 100
    )

    idle_time = random.uniform(
        0, 15
    )

    return [
        fuel,
        speed,
        acceleration,
        braking,
        ac,
        idle_time
    ]


# ============================================================
# 3. FUEL CONSUMPTION MODEL
# ============================================================

def calculate_required_fuel(individual):

    fuel, speed, acceleration, braking, ac, idle_time = individual

    # Base consumption
    base_consumption = 1 / base_mileage

    # --------------------------------------------------------
    # Speed penalty
    # Efficiency is assumed best around 50 km/h
    # --------------------------------------------------------

    speed_penalty = (
        0.00015 * (speed - 50) ** 2
    )

    # --------------------------------------------------------
    # Acceleration penalty
    # Aggressive acceleration consumes more fuel
    # --------------------------------------------------------

    acceleration_penalty = (
        0.025 * acceleration ** 2
    )

    # --------------------------------------------------------
    # Braking penalty
    # Frequent/aggressive braking wastes energy
    # --------------------------------------------------------

    braking_penalty = (
        0.015 * braking ** 2
    )

    # --------------------------------------------------------
    # Traffic penalty
    # --------------------------------------------------------

    traffic_penalty = (
        0.0025 * traffic_condition
    )

    # --------------------------------------------------------
    # Road condition penalty
    # Poor roads increase consumption
    # --------------------------------------------------------

    road_penalty = (
        0.002 * (10 - road_condition)
    )

    # --------------------------------------------------------
    # Vehicle load penalty
    # --------------------------------------------------------

    load_penalty = (
        0.00001 * vehicle_load
    )

    # --------------------------------------------------------
    # Weather penalty
    # --------------------------------------------------------

    weather_penalty = (
        0.0015 * weather
    )

    # --------------------------------------------------------
    # Terrain penalty
    # --------------------------------------------------------

    terrain_penalty = (
        0.003 * terrain
    )

    # --------------------------------------------------------
    # AC penalty
    # --------------------------------------------------------

    ac_penalty = (
        0.0004 * ac
    )

    # --------------------------------------------------------
    # Idling penalty
    # --------------------------------------------------------

    idle_penalty = (
        0.003 * idle_time
    )

    # Total fuel consumed per km
    fuel_per_km = (
        base_consumption
        + speed_penalty
        + acceleration_penalty
        + braking_penalty
        + traffic_penalty
        + road_penalty
        + load_penalty
        + weather_penalty
        + terrain_penalty
        + ac_penalty
        + idle_penalty
    )

    return fuel_per_km * distance


# ============================================================
# 4. FITNESS FUNCTION
# ============================================================

def fitness(individual):

    fuel_gene = individual[0]

    required_fuel = calculate_required_fuel(individual)

    # --------------------------------------------------------
    # Constraint:
    # Fuel selected by GA must be enough for the trip
    # --------------------------------------------------------

    fuel_difference = abs(
        fuel_gene - required_fuel
    )

    # Smaller fuel + smaller constraint violation = better
    score = (
        required_fuel
        + 10 * fuel_difference
    )

    return 1 / (1 + score)


# ============================================================
# 5. SELECTION
# ============================================================

def selection(population):

    tournament = random.sample(
        population,
        3
    )

    return max(
        tournament,
        key=fitness
    )


# ============================================================
# 6. CROSSOVER
# ============================================================

def crossover(parent1, parent2):

    child1 = parent1.copy()
    child2 = parent2.copy()

    for i in range(len(parent1)):

        if random.random() < 0.5:

            child1[i] = parent2[i]
            child2[i] = parent1[i]

    return child1, child2


# ============================================================
# 7. MUTATION
# ============================================================

def mutation(individual):

    # Fuel
    if random.random() < MUTATION_RATE:

        individual[0] += random.uniform(-1, 1)

        individual[0] = max(
            0.1,
            individual[0]
        )

    # Speed
    if random.random() < MUTATION_RATE:

        individual[1] += random.uniform(-5, 5)

        individual[1] = max(
            30,
            min(90, individual[1])
        )

    # Acceleration
    if random.random() < MUTATION_RATE:

        individual[2] += random.uniform(
            -0.5,
            0.5
        )

        individual[2] = max(
            0.1,
            min(3.5, individual[2])
        )

    # Braking
    if random.random() < MUTATION_RATE:

        individual[3] += random.uniform(
            -0.5,
            0.5
        )

        individual[3] = max(
            0.1,
            min(3.5, individual[3])
        )

    # AC usage
    if random.random() < MUTATION_RATE:

        individual[4] += random.uniform(
            -10,
            10
        )

        individual[4] = max(
            0,
            min(100, individual[4])
        )

    # Idle time
    if random.random() < MUTATION_RATE:

        individual[5] += random.uniform(
            -2,
            2
        )

        individual[5] = max(
            0,
            min(15, individual[5])
        )


# ============================================================
# 8. GENETIC ALGORITHM
# ============================================================

def genetic_algorithm():

    population = [
        create_individual()
        for _ in range(POP_SIZE)
    ]

    best_solution = None

    for generation in range(MAX_GENERATIONS):

        # Find best individual
        current_best = max(
            population,
            key=fitness
        )

        if (
            best_solution is None
            or fitness(current_best)
            > fitness(best_solution)
        ):

            best_solution = current_best.copy()

        # Create new population
        new_population = []

        while len(new_population) < POP_SIZE:

            parent1 = selection(population)
            parent2 = selection(population)

            # Crossover
            if random.random() < CROSSOVER_RATE:

                child1, child2 = crossover(
                    parent1,
                    parent2
                )

            else:

                child1 = parent1.copy()
                child2 = parent2.copy()

            # Mutation
            mutation(child1)
            mutation(child2)

            new_population.append(child1)

            if len(new_population) < POP_SIZE:

                new_population.append(child2)

        population = new_population

    return best_solution


# ============================================================
# 9. RUN GA
# ============================================================

best = genetic_algorithm()


# ============================================================
# 10. RESULTS
# ============================================================

fuel_gene = best[0]

speed = best[1]
acceleration = best[2]
braking = best[3]
ac = best[4]
idle_time = best[5]

required_fuel = calculate_required_fuel(best)

# Use the fuel required by the optimized strategy
optimized_fuel = required_fuel

mileage = distance / optimized_fuel


print("\n")
print("=" * 60)
print("             OPTIMIZED FUEL STRATEGY")
print("=" * 60)

print("\nFIXED TRIP CONDITIONS")
print("-" * 60)

print(f"Distance              : {distance:.2f} km")
print(f"Road Condition        : {road_condition:.2f}/10")
print(f"Traffic Condition     : {traffic_condition:.2f}/10")
print(f"Vehicle Load          : {vehicle_load:.2f} kg")
print(f"Weather Severity      : {weather:.2f}/10")
print(f"Terrain Difficulty    : {terrain:.2f}/10")

print("\nOPTIMIZED PARAMETERS")
print("-" * 60)

print(f"Fuel Required         : {optimized_fuel:.2f} L")
print(f"Cost of Fuel          : {optimized_fuel*100:.2f}")
print(f"Speed                 : {speed:.2f} km/h")
print(f"Acceleration          : {acceleration:.2f} m/s²")
print(f"Braking               : {braking:.2f} m/s²")
print(f"AC Usage              : {ac:.2f}%")
print(f"Idle Time             : {idle_time:.2f} minutes")

print("\nRESULT")
print("-" * 60)

print(f"Expected Mileage      : {mileage:.2f} km/L")

print("=" * 60)
