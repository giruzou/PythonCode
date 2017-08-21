from functools import wraps
import time 

def get_elapsed_data(function):
    @wraps(function)
    def measure_target(*args,**kwargs):
        start=time.time()
        ret=function(*args,**kwargs)
        end=time.time()
        return function.__name__,ret,end-start
    return measure_target