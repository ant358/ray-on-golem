import socket

import ray
from random import random

# Let's start Ray
ray.init()

SAMPLES = 1000000


# By adding the `@ray.remote` decorator, a regular Python function
# becomes a Ray remote function.
@ray.remote
def pi4_sample():
    print(socket.gethostbyname(socket.gethostname()))
    in_count = 0
    for _ in range(SAMPLES):
        x, y = random(), random()
        if x * x + y * y <= 1:
            in_count += 1
    return in_count


if __name__ == '__main__':
    # To invoke this remote function, use the `remote` method.
    # This will immediately return an object ref (a future) and then create
    # a task that will be executed on a worker process. Get retreives the result.
    future = pi4_sample.remote()
    pi = ray.get(future) * 4.0 / SAMPLES
    print(f'{pi} is an approximation of pi')

    # Now let's do this 100,000 times.
    # With regular python this would take 11 hours
    # Ray on a modern laptop, roughly 2 hours
    # On a 10-node Ray cluster, roughly 10 minutes
    BATCHES = 1_000
    results = []
    for _ in range(BATCHES):
        results.append(pi4_sample.remote())
    output = ray.get(results)
    pi = sum(output) * 4.0 / BATCHES / SAMPLES
    print(f'{pi} is a way better approximation of pi')