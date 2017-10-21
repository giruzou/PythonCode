from libc.stdlib cimport rand, RAND_MAX
from cython.parallel import prange
from cython cimport boundscheck, wraparound

cdef int NUM = 1000000000

@boundscheck(False)
@wraparound(False)
def monte():
    cdef :
        int counter = 0
        int i=0
        double x
        double y
    for i in prange(NUM,nogil=True,schedule='static',chunksize=1):
        x = (rand())/(RAND_MAX+1.0)
        y = (rand())/(RAND_MAX+1.0)
        if x*x + y*y < 1.0:
            counter += 1

    pi = 4.0*counter/NUM
    print(pi)