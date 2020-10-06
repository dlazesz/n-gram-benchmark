#! /usr/bin/env python3

from memory_profiler import profile
from timeit import timeit
from collections import deque
from itertools import islice, tee


TEXT = 'alma barack citrom'


def ng_index(it, n):
    it = list(it)
    for n_gram_start_ind in range(len(it) - n + 1):
        yield it[n_gram_start_ind:n_gram_start_ind + n]


def ng_iter(it, n):
    for ngram in zip(*(islice(iter, i, None) for i, iter in enumerate(tee(it, n)))):
        yield ngram


def ng_frame(it, n):
    frame = deque(maxlen=n)
    it = iter(it)
    c = 1
    while c < n:
        frame.append(next(it))
        c += 1
    for i in it:
        frame.append(i)
        yield frame


def readbybyte(fileobj):
    byte = fileobj.read(1)
    while byte:
        yield byte
        byte = fileobj.read(1)


@profile
def mem(fun):
    with open('input.txt') as inp, open('/dev/null', 'w') as out:
        for ng in fun(readbybyte(inp), 3):
            print(ng, file=out)


def tim(fun, text):
    with open('/dev/null', 'w') as out:
        for ng in fun(text, 3):
            print(ng, file=out)


if __name__ == "__main__":
    print('MEMORY')
    print("index")
    mem(ng_index)
    print("iter ")
    mem(ng_iter)
    print("frame")
    mem(ng_frame)
    print('TIME')
    print("index:", timeit('tim(ng_index, TEXT)', globals=globals(), number=10000))
    print("iter :", timeit('tim(ng_iter, TEXT)', globals=globals(), number=10000))
    print("frame:", timeit('tim(ng_frame, TEXT)', globals=globals(), number=10000))
