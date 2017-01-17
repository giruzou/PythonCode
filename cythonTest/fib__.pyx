
def calc_fib(n):
    cdef int i
    cdef double a=0.0,b=1.0
    for i in range(n):
        c=a+b
        a=b
        b=c
    return a

def main():
    n=int(input("input fib number:"))
    value=calc_fib(n)
    print(value)
if __name__ == '__main__':
    main()