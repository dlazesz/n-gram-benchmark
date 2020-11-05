#!/usr/bin/env python3

import argparse

from memory_profiler import profile
from timeit import timeit
from collections import deque
from itertools import islice, tee


def setup_index(it, n):
    it = list(it)
    return range(len(it) - n + 1), it


def ng_index(range_it, it, n):
    for n_gram_start_ind in range_it:
        yield it[n_gram_start_ind:n_gram_start_ind + n]


def setup_iter(it, n):
    return zip(*(islice(it, i, None) for i, it in enumerate(tee(it, n)))), None


def ng_iter(ngram_it, _, __):
    for ngram in ngram_it:
        yield ngram


def setup_frame(it, n):
    it = iter(it)
    frame = deque(maxlen=n)
    for _ in range(1, n):
        frame.append(next(it))
    return frame, it


def ng_frame(frame, it, _):
    for i in it:
        frame.append(i)
        yield frame


def readbybyte(fileobj):
    byte = fileobj.read(1)
    while byte:
        yield byte
        byte = fileobj.read(1)


def general_setup(setup_fun, inp_file, n):
    inp_fh = open(inp_file)
    out_fh = open('/dev/null', 'w')
    extra, it = setup_fun(readbybyte(inp_fh), n)
    return extra, it, out_fh, n


@profile
def mem(extra, inp, out, n, fun):
    tim(extra, inp, out, n, fun)


def tim(extra, inp, out, n, fun):
    for ng in fun(extra, inp, n):
        print(ng, file=out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input-file', '-i',
        help='Input file',
        type=str)
    parser.add_argument(
        '--ngram-length', '-n',
        help='n-gram length',
        type=int)

    args = parser.parse_args()
    in_fh = args.input_file
    ngramlen = args.ngram_length

    print('MEMORY')
    print('index')
    extra_var, iterator, output_fh, ngram_length = general_setup(setup_index, in_fh, ngramlen)
    mem(extra_var, iterator, output_fh, ngram_length, ng_index)
    print('iter')
    extra_var, iterator, output_fh, ngram_length = general_setup(setup_iter, in_fh, ngramlen)
    mem(extra_var, iterator, output_fh, ngram_length, ng_iter)
    print('frame')
    extra_var, iterator, output_fh, ngram_length = general_setup(setup_frame, in_fh, ngramlen)
    mem(extra_var, iterator, output_fh, ngram_length, ng_frame)

    print("INIT TIME")
    print('index:', timeit(stmt='extra, it, out, n = general_setup(setup_index, "{0}", {1})'.format(in_fh, ngramlen),
                           globals=globals(), number=30))
    print('iter:', timeit(stmt='extra, it, out, n = general_setup(setup_iter, "{0}", {1})'.format(in_fh, ngramlen),
                          globals=globals(), number=30))
    print('frame:', timeit(stmt='extra, it, out, n = general_setup(setup_frame, "{0}", {1})'.format(in_fh, ngramlen),
                           globals=globals(), number=30))

    print('TIME')
    print('index:', timeit(setup='extra, it, out, n = general_setup(setup_index, "{0}", {1})'.format(in_fh, ngramlen),
                           stmt='tim(extra, it, out, n, ng_index)', globals=globals(), number=30))
    print('iter:', timeit(setup='extra, it, out, n = general_setup(setup_iter, "{0}", {1})'.format(in_fh, ngramlen),
                          stmt='tim(extra, it, out, n, ng_iter)', globals=globals(), number=30))
    print('frame:', timeit(setup='extra, it, out, n = general_setup(setup_frame, "{0}", {1})'.format(in_fh, ngramlen),
                           stmt='tim(extra, it, out, n, ng_frame)', globals=globals(), number=30))
