from measure import get_elapsed_data
from numba import jit
import numpy as np
from array import array
from array_creator import shuffle_list

@get_elapsed_data
def std_max(array):
    max_value=max(array)
    return max_value

@get_elapsed_data
def np_max(array):
    max_value=np.max(array)
    return max_value

@get_elapsed_data
@jit('i8(i8[:])')
def scratch_max_with_annotate(array):
    ret=array[0]
    for value in array:
        ret = value if ret < value else ret
    return ret

@get_elapsed_data
@jit
def scratch_max_jit(array):
    ret=array[0]
    for value in array:
        ret = value if ret < value else ret
    return ret

@get_elapsed_data
def get_shuffled_list(arr):
    return shuffle_list(arr)

def main():
    N=10000000
    arr=np.arange(N)
    #arr=array('L',list(range(N)))
    #arr=list(range(N))
    #_,arr,elapsed=get_shuffled_list(arr)
    #print("elapsed shuffle time",elapsed)
    print(scratch_max_jit(arr))
    print(scratch_max_with_annotate(arr))
    print(np_max(arr))
    #print(std_max(arr))
if __name__ == '__main__':
    main()