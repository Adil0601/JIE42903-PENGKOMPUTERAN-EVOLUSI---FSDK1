import streamlit as st
import csv
import random

# Function to read the CSV file and convert it to the desired format
def read_csv_to_dict(file_path):
    program_ratings = {}

    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        # Skip the header
        header = next(reader)

        for row in reader:
            program = row[0]
            ratings = [float(x) for x in row[1:]]  # Convert the ratings to floats
            program_ratings[program] = ratings

    return program_ratings

# Path to the CSV file
file_path = '/content/program_ratings.csv'

# Get the data in the required format
program_ratings_dict = read_csv_to_dict(file_path)

# Parameters
GEN = 100
POP = 50
EL_S = 2
all_programs = list(program_ratings_dict.keys())  # all programs
all_time_slots = list(range(6, 24))  # time slots

# Fitness function
def fitness_function(schedule):
    total_rating = 0
    for time_slot, program in enumerate(schedule):
        total_rating += program_ratings_dict[program][time_slot]
    return total_rating

# Genetic algorithm functions
def crossover(schedule1, schedule2):
    crossover_point = random.randint(1, len(schedule1) - 2)
    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]
    return child1, child2

def mutate(schedule):
    mutation_point = random.randint(0, len(schedule) - 1)
    new_program = random.choice(all_programs)
    schedule[mutation_point] = new_program
    return schedule

def genetic_algorithm(initial_schedule, generations, population_size, crossover_rate, mutation_rate, elitism_size):
    population = [initial_schedule]

    for _ in range(population_size - 1):
        random_schedule = initial_schedule.copy()
        random.shuffle(random_schedule)
        population.append(random_schedule)

    for generation in range(generations):
        new_population = []
        population.sort(key=lambda schedule: fitness_function(schedule), reverse=True)
        new_population.extend(population[:elitism_size])

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = new_population

    return population[0]

# Streamlit interface
st.title("Genetic Algorithm Scheduler")

# Input parameters
st.sidebar.header("Genetic Algorithm Parameters")
crossover_rate = st.sidebar.slider("Crossover Rate (CO_R)", 0.0, 0.95, 0.8, step=0.01)
mutation_rate = st.sidebar.slider("Mutation Rate (MUT_R)", 0.01, 0.05, 0.02, step=0.01)

# Run trials
if st.sidebar.button("Run Trials"):
    results = []

    for trial in range(3):
        initial_schedule = random.sample(all_programs, len(all_programs))
        schedule = genetic_algorithm(
            initial_schedule,
            generations=GEN,
            population_size=POP,
            crossover_rate=crossover_rate,
            mutation_rate=mutation_rate,
            elitism_size=EL_S,
        )

        final_schedule = schedule[:len(all_time_slots)]
        total_ratings = fitness_function(final_schedule)
        results.append((trial + 1, crossover_rate, mutation_rate, final_schedule, total_ratings))

    # Display results
    for trial_result in results:
        trial, co_r, mut_r, schedule, total_ratings = trial_result

        st.write(f"### Trial {trial}")
        st.write(f"**Crossover Rate:** {co_r}, **Mutation Rate:** {mut_r}")
        st.write(f"**Total Ratings:** {total_ratings}")

        table_data = {
            "Time Slot": [f"{time_slot}:00" for time_slot in all_time_slots],
            "Program": schedule
        }
        st.table(table_data)
