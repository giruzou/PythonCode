import random
import copy
import time
from numba import jit

def shuffle_list(original):
    shuffled=copy.copy(original)
    random.shuffle(shuffled)
    return shuffled

def create_test_set(size,trial):
    original=list(range(size))
    return [(random.choice(original),shuffle_list(original)) for _ in range(trial)]


def main():
    size=100
    trial=10000
    test_set=create_test_set(size,trial)
    original=list(range(size))

    start=time.time()
    for key,arr in test_set:
        for i in arr:
            if i==key:
                break
    end=time.time()

    print(end-start, ['sec'])

    start=time.time()
    for key, arr in test_set:
        if key in arr:
            continue
    end=time.time()

    print(end-start, ['sec'])


if __name__ == '__main__':
    main()