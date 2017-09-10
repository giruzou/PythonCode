from numpy import random
import copy

def shuffle_list(original):
    shuffled=copy.copy(original)
    random.shuffle(shuffled)
    return shuffled

def create_test_set(size,trial):
    original=list(range(size))
    return [(random.choice(original),shuffle_list(original)) for _ in range(trial)]
