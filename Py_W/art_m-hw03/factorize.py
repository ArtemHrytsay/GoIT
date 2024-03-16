from multiprocessing import Pool, cpu_count
from time import time


def factors(n:  int) -> list[int]:
    step = 2 if n%2 else 1
    result = sorted([x for l in [[i, n//i] for i in range(1, int(n**0.5) + step) if n % i == 0] for x in l])
    return result

def factorize(*numbers):
    result = [factors(n) for n in numbers]
    return result

def sync_factorize(numbers: list[int]):
    return factorize(*numbers)

def multi_factorize(numbers: list[int]):
    result = []
    with Pool(processes=cpu_count()) as pool:
        result = pool.map(factors, numbers)
    return result

def test():
    a, b, c, d  = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


if __name__ == "__main__":
    test()
    start_s = time()
    list = [i for i in range(1,1000000)]
    r = sync_factorize(list)
    end_s  = time()
    duration_s = end_s - start_s
    print(f"Duration of sync process: [{duration_s}]")

    start_m = time()
    r = multi_factorize(list)
    end_m  = time()
    duration_m = end_m - start_m
    print(f"Duration of multiprocess: [{duration_m}]")
