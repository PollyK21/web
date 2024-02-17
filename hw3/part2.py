import time
import multiprocessing
import multiprocessing.pool


def factorize(*number):
    results = []
    for num in number:
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        results.append(factors)
    return results


def factorize_single(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors


def factorize2(*numbers):
    results = []
    # with ThreadPool(processes=multiprocessing.cpu_count()) as pool:
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(factorize_single, numbers)
    return results


if __name__ == '__main__':
    start_time = time.time()
    result = factorize(128, 255, 99999, 10651060)
    end_time = time.time()

    start_time2 = time.time()
    result2 = factorize2(128, 255, 99999, 10651060)
    end_time2 = time.time()

    print("first", end_time - start_time)
    print("multi", end_time2 - start_time2)
