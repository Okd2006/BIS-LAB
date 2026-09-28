import random

# Input
n = int(input("Enter number of investments: "))

names = []
returns = []
risk = []

for i in range(n):
    names.append(input(f"Investment {i+1} name: "))
    returns.append(float(input("Expected return (%): ")))
    risk.append(float(input("Risk: ")))

budget = float(input("Enter total budget: "))

POP_SIZE = 20
GENERATIONS = 50
MUTATION_RATE = 0.1


# Fitness function
def fitness(p):
    ret = sum(p[i] * returns[i] / 100 for i in range(n))
    rsk = sum(p[i] * risk[i] / 100 for i in range(n))
    return ret - 0.5 * rsk


# Create portfolio
def create():
    x = [random.random() for _ in range(n)]
    total = sum(x)
    return [v / total * 100 for v in x]


# Mutation
def mutate(p):
    i = random.randrange(n)
    p[i] += random.uniform(-5, 5)
    p = [max(0, x) for x in p]

    total = sum(p)
    return [x / total * 100 for x in p]


# Genetic Algorithm
population = [create() for _ in range(POP_SIZE)]

for generation in range(GENERATIONS):

    # Select best half
    population.sort(key=fitness, reverse=True)
    parents = population[:POP_SIZE // 2]

    new_population = parents[:]

    while len(new_population) < POP_SIZE:

        p1 = random.choice(parents)
        p2 = random.choice(parents)

        # Crossover
        point = random.randint(1, n - 1)

        child = p1[:point] + p2[point:]

        # Normalize
        total = sum(child)
        child = [x / total * 100 for x in child]

        # Mutation
        if random.random() < MUTATION_RATE:
            child = mutate(child)

        new_population.append(child)

    population = new_population


# Best portfolio
best = max(population, key=fitness)

print("\n===== BEST PORTFOLIO =====")

for i in range(n):
    amount = best[i] / 100 * budget
    print(f"{names[i]}: {best[i]:.2f}% = ₹{amount:.2f}")

print(f"\nExpected Return: {sum(best[i] * returns[i] / 100 for i in range(n)):.2f}%")
print(f"Fitness: {fitness(best):.2f}")
