#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
from argparse import ArgumentParser
from random import sample, randint, choice


def sentence():
    """
    Original source: github.com/TheAbhijeet/lorem_text
    Under the MIT license
    Return a randomly generated sentence of lorem ipsum text.
    The first word is capitalized, and the sentence ends in either a period or
    question mark. Commas are added at random.
    """
    words = (
        'exercitationem', 'perferendis', 'perspiciatis', 'laborum', 'eveniet',
        'sunt', 'iure', 'nam', 'nobis', 'eum', 'cum', 'officiis', 'excepturi',
        'odio', 'consectetur', 'quasi', 'aut', 'quisquam', 'vel', 'eligendi',
        'itaque', 'non', 'odit', 'tempore', 'quaerat', 'dignissimos',
        'facilis', 'neque', 'nihil', 'expedita', 'vitae', 'vero', 'ipsum',
        'nisi', 'animi', 'cumque', 'pariatur', 'velit', 'modi', 'natus',
        'iusto', 'eaque', 'sequi', 'illo', 'sed', 'ex', 'et', 'voluptatibus',
        'tempora', 'veritatis', 'ratione', 'assumenda', 'incidunt', 'nostrum',
        'placeat', 'aliquid', 'fuga', 'provident', 'praesentium', 'rem',
        'necessitatibus', 'suscipit', 'adipisci', 'quidem', 'possimus',
        'voluptas', 'debitis', 'sint', 'accusantium', 'unde', 'sapiente',
        'voluptate', 'qui', 'aspernatur', 'laudantium', 'soluta', 'amet',
        'quo', 'aliquam', 'saepe', 'culpa', 'libero', 'ipsa', 'dicta',
        'reiciendis', 'nesciunt', 'doloribus', 'autem', 'impedit', 'minima',
        'maiores', 'repudiandae', 'ipsam', 'obcaecati', 'ullam', 'enim',
        'totam', 'delectus', 'ducimus', 'quis', 'voluptates', 'dolores',
        'molestiae', 'harum', 'dolorem', 'quia', 'voluptatem', 'molestias',
        'magni', 'distinctio', 'omnis', 'illum', 'dolorum', 'voluptatum', 'ea',
        'quas', 'quam', 'corporis', 'quae', 'blanditiis', 'atque', 'deserunt',
        'laboriosam', 'earum', 'consequuntur', 'hic', 'cupiditate',
        'quibusdam', 'accusamus', 'ut', 'rerum', 'error', 'minus', 'eius',
        'ab', 'ad', 'nemo', 'fugit', 'officia', 'at', 'in', 'id', 'quos',
        'reprehenderit', 'numquam', 'iste', 'fugiat', 'sit', 'inventore',
        'beatae', 'repellendus', 'magnam', 'recusandae', 'quod', 'explicabo',
        'doloremque', 'aperiam', 'consequatur', 'asperiores', 'commodi',
        'optio', 'dolor', 'labore', 'temporibus', 'repellat', 'veniam',
        'architecto', 'est', 'esse', 'mollitia', 'nulla', 'a', 'similique',
        'eos', 'alias', 'dolore', 'tenetur', 'deleniti', 'porro', 'facere',
        'maxime', 'corrupti',
    )

    # Determine the number of comma-separated sections and number of words in
    # each section for this sentence.
    sections = [' '.join(sample(words, randint(1, 12)))
                for _ in range(randint(1, 5))]
    s = ', '.join(sections)
    # Convert to sentence case and add end punctuation.
    return ''.join((s[0].upper(), s[1:], choice('?.')))


parser = ArgumentParser()
parser.add_argument('--sentences', '-s', help='Number of dummy sentences (one sentence per line)', type=int)

args = parser.parse_args()
if any(arg is None for arg in vars(args).values()):
    parser.print_help(sys.stderr)
    exit(2)

for _ in range(args.sentences):
    print(sentence())
