import multiprocessing
import random
import time
import matplotlib.pyplot as plt
import numpy as np


class Complex:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Complex(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Complex(self.x - other.x, self.y - other.y)


def merge(left, right):
    result = []
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left or right)
    return result


def parallel_sort(data, num_processes):
    chunk_size = len(data) // num_processes
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    with multiprocessing.Pool(processes=num_processes) as pool:
        sorted_chunks = pool.map(sorted, chunks)

    while len(sorted_chunks) > 1:
        sorted_chunks = [merge(sorted_chunks[i], sorted_chunks[i + 1]) for i in range(0, len(sorted_chunks), 2)]

    return sorted_chunks[0]


def test_parallel_sort():
    data_sizes = [10000, 20000]
    num_processes_options = [1, 2, 3, 4]  # < 5
    times = []

    for data_size in data_sizes:
        data = [random.randint(1, 10000) for _ in range(data_size)]
        row_times = []

        for num_processes in num_processes_options:
            start_time = time.time()
            sorted_data = parallel_sort(data, num_processes)
            elapsed_time = time.time() - start_time
            row_times.append(elapsed_time)

        times.append(row_times)

    return np.array(times), data_sizes, num_processes_options


def plot_results(times, data_sizes, num_processes_options):
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, data_size in enumerate(data_sizes):
        ax.plot(num_processes_options, times[i], label=f'Data size {data_size}', marker='o')

    ax.set_title('Performance of Parallel Sorting with Different Data Sizes and Process Counts')
    ax.set_xlabel('Number of Processes')
    ax.set_ylabel('Time (seconds)')
    ax.legend()
    plt.grid(True)
    plt.show()


class Fibonacci:
    def __init__(self, steps=2):
        self.i = 0
        self.steps = steps

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < self.steps:
            if self.i < 2:
                self.n_2 = 0
                self.n_1 = 0
                self.n_0 = 1
                self.i += 1
                return self.i - 1
            else:
                self.n_2 = self.n_1
                self.n_1 = self.n_0
                self.n_0 = self.n_1 + self.n_2
                self.i += 1
                return self.n_0
        else:
            raise StopIteration


if __name__ == "__main__":

    z1 = Complex(2, 2)
    z2 = Complex(3, 3)
    z3 = z1 + z2
    print([z3.x, z3.y])
    z3 = z1 - z2
    print([z3.x, z3.y])

    data = [38, 27, 43, 3, 9, 82, 10]
    print(data)
    sorted_data = parallel_sort(data, 1)
    print(sorted_data)

    times, data_sizes, num_processes_options = test_parallel_sort()
    plot_results(times, data_sizes, num_processes_options)

    myclass = Fibonacci(6)
    fibo = iter(myclass)
    for x in fibo:
        print(x)
