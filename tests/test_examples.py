"""
Idiomatic Go examples converted to use goless.
"""

import time
import unittest

import goless


class Examples(unittest.TestCase):

    def test_select(self):
        # https://gobyexample.com/select
        c1 = goless.chan()
        c2 = goless.chan()

        def func1():
            time.sleep(.1)
            c1.send('one')
        goless.go(func1)

        def func2():
            time.sleep(.2)
            c2.send('two')
        goless.go(func2)

        # We don't print since we run this as a test.
        callbacks = []

        for i in range(2):
            _, val = goless.select([goless.rcase(c1), goless.rcase(c2)])
            callbacks.append(val)

        self.assertEqual(callbacks, ['one', 'two'])

    def test_range_over_channels(self):
        # https://gobyexample.com/range-over-channels
        queue = goless.chan(2)
        queue.send('one')
        queue.send('two')
        queue.close()
        elements = [elem for elem in queue]
        self.assertEqual(elements, ['one', 'two'])

    def test_worker_pool(self):
        # https://gobyexample.com/worker-pools
        jobs_done = []

        # noinspection PyShadowingNames,PyShadowingBuiltins
        def worker(id, jobs, results):
            for j in jobs:
                jobs_done.append('w %s j %s' % (id, j))
                time.sleep(.01)
                results.send(j * 2)

        jobs = goless.chan(100)
        results = goless.chan(100)

        for w in range(1, 4):
            goless.go(lambda: worker(w, jobs, results))

        for j in range(1, 10):
            jobs.send(j)
        jobs.close()

        for a in range(1, 10):
            results.recv()
        self.assertEqual(len(jobs_done), 9)
