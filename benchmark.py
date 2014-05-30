from __future__ import print_function

import time

from goless import backends, chan, go, selecting


QUEUE_LEN = 10000
CHANSIZE_AND_NAMES = (
    (0, 'Sync'),
    (-1, 'Async'),
    (1000, 'Buffered(1000)')
)


def bench_channel(chan_size):
    c = chan(chan_size)

    def func():
        for _ in xrange(QUEUE_LEN):
            c.send(0)
        c.close()
    count = 0

    go(func)
    start = time.clock()
    for _ in xrange(QUEUE_LEN):
        c.recv()
        count += 1
    end = time.clock()
    assert count == QUEUE_LEN, '%s != %s' % (count, QUEUE_LEN)
    return end - start


def bench_channels():
    print('Benchmarking channels:')
    for size, name in CHANSIZE_AND_NAMES:
        took = bench_channel(size)
        print ('  %ss: %s' % (took, name))


def bench_select(use_default):
    c = chan(0)
    cases = [
        selecting.scase(c, 1),
        selecting.rcase(c),
        selecting.scase(c, 1),
        selecting.rcase(c),
    ]
    if use_default:
        cases.append(selecting.dcase())

    def sender():
        while True:
            c.send(0)
            c.recv()
    go(sender)

    start = time.clock()
    for i in xrange(QUEUE_LEN):
        selecting.select(cases)
    end = time.clock()
    return end - start


def bench_selects():
    print('Benchmarking select:')
    took_nodefault = bench_select(False)
    print('  %ss: No default case.' % took_nodefault)
    took_withdefault = bench_select(True)
    print('  %ss: With default case.' % took_withdefault)


if __name__ == '__main__':
    print('Using backend %s' % backends.current.__class__.__name__)
    bench_channels()
    bench_selects()
