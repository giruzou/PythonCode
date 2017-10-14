"""
implement xorshift with python
https://ja.wikipedia.org/wiki/Xorshift
https://qiita.com/yosgspec/items/e4287262f8dbea2aa815
https://ask.helplib.com/1591921
"""

from numba import jit


def xorshit(generator, seed=None):
    ret = seed
    def inner():
        nonlocal ret
        if ret is None:
            ret = generator()
        else:
            ret = generator(*ret)
        return ret[-1]
    return inner


@jit
def xor32(y=2463534242):
    y = y ^ (y << 13 & 0xFFFFFFFF)
    y = y ^ (y >> 17 & 0xFFFFFFFF)
    y = y ^ (y << 5 & 0xFFFFFFFF)
    return y & 0xFFFFFFFF,


@jit
def xor64(x=88172645463325252):
    x = x ^ (x << 13)
    x = x ^ (x >> 7)
    x = x ^ (x << 17)
    return x & 0xFFFFFFFF,


@jit
def xor96(x=123456789, y=362436069, z=521288629):
    t = (x ^ (x << 3 & 0xFFFFFFFF)) ^ (
        y ^ (y >> 19 & 0xFFFFFFFF)) ^ (
        z ^ (z << 6 & 0xFFFFFFFF))
    x = y
    y = z
    z = t
    return x, y, z


@jit
def xor128(x=123456789, y=362436069, z=521288629, w=88675123):
    t = x ^ (x << 11) & 0xFFFFFFFF
    x = y
    y = z
    z = w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8)) & 0xFFFFFFFF
    return x, y, z, w


def uniform(rand, begin=0, end=1):
    def inner():
        return begin+(rand())/(int(0xFFFFFFFF)/(end-begin))
    return inner


def calc_pi(generator):
    u01 = uniform(generator)
    counter = 0
    N = 100000000
    for i in range(N):
        x = u01()
        y = u01()
        if x*x+y*y < 1.0:
            counter += 1
    print(4.0*counter/N)


def main_():
    random32 = xorshit(xor32, seed=(1,))
    calc_pi(random32)
    random64 = xorshit(xor64, seed=(3,))
    calc_pi(random64)
    random128 = xorshit(xor128, seed=(4, 3, 2, 1))
    calc_pi(random128)


def main():
    random64 = xorshit(xor64)
    for i in range(100):
        r = random64()
        print(r)
if __name__ == '__main__':
    main()
