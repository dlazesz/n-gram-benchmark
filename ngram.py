#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
from os import devnull
from timeit import repeat
from collections import deque
from itertools import islice, tee
from more_itertools import windowed
from argparse import ArgumentParser

from memory_profiler import profile


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


def setup_windowed(it, n):
    return windowed(it, n), None


def ng_windowed(ngram_it, _, __):
    for ngram in ngram_it:
        yield ngram


def setup_frame(it, n):
    it = iter(it)
    frame = deque(maxlen=n)
    for _ in range(n-1):
        frame.append(next(it))
    return frame, it


def ng_frame(frame, it, _):
    for i in it:
        frame.append(i)
        yield frame


def readbycharacters(fileobj, _):
    character = fileobj.read(1)  # Read file by characters
    while character:
        yield character
        character = fileobj.read(1)


def readbywords(fileobj, n):
    for line in fileobj:  # This simulates reading line by line, which is slower than reading the entire file at once
        for word in line.strip().split(' '):
            yield word
        for _ in range(n-1):  # To handle each line separately simulating sentence per line (SPL) format
            yield 'DUMMY WORD'


def general_setup(read_function, setup_function, inp_file, n):
    inp_fh = open(inp_file, encoding='UTF-8')
    out_fh = open(devnull, 'w', encoding='UTF-8')
    extra, it = setup_function(read_function(inp_fh, n), n)
    return extra, it, out_fh, n


@profile
def mem(extra, inp, out, n, fun):
    tim(extra, inp, out, n, fun)


def tim(extra, inp, out, n, fun):
    for ng in fun(extra, inp, n):
        print(ng, file=out)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input-file', '-i', help='Input file', type=str)
    parser.add_argument('--ngram-length', '-n', help='n-gram length', type=int)
    parser.add_argument('--read-unit', '-u', choices=['words', 'characters'], help='Read by words or characters',
                        type=str)

    args = parser.parse_args()
    if any(arg is None for arg in vars(args).values()):
        parser.print_help(sys.stderr)
        exit(2)

    in_file = args.input_file
    ngramlen = args.ngram_length
    if args.read_unit == 'words':
        read_fun = readbywords
    else:
        read_fun = readbycharacters

    alternatvies = (('Index:', setup_index, ng_index),
                    ('Iter.:', setup_iter, ng_iter),
                    ('Windo:', setup_windowed, ng_windowed),
                    ('Frame:', setup_frame, ng_frame))

    print('', 'MEMORY USAGE', '', sep='\n')
    for name, setup_fun, ngram_fun in alternatvies:
        print(name)
        extra_var, iterator, output_fh, ngram_length = general_setup(read_fun, setup_fun, in_file, ngramlen)
        mem(extra_var, iterator, output_fh, ngram_length, ngram_fun)

    print('', 'INIT TIME', '', sep='\n')
    for name, setup_fun, _ in alternatvies:
        res = repeat(stmt='extra, it, out, n = general_setup(read_fun, {0}, "{1}", {2})'.
                     format(setup_fun.__name__, in_file, ngramlen), globals=globals(), number=10, repeat=3)
        print(name, f'{sum(res)/len(res):.10f}', '(' + ', '.join(f'{r:.10f}' for r in res) + ')')

    print('', 'RUNNING TIME', '', sep='\n')
    for name, setup_fun, ngram_fun in alternatvies:
        res = repeat(setup='extra, it, out, n = general_setup(read_fun, {0}, "{1}", {2})'.
                     format(setup_fun.__name__, in_file, ngramlen),
                     stmt='tim(extra, it, out, n, {0})'.format(ngram_fun.__name__), globals=globals(), number=10,
                     repeat=3)
        print(name, f'{sum(res)/len(res):.10f}', '(' + ', '.join(f'{r:.10f}' for r in res) + ')')
    print()
