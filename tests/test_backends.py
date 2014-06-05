from . import BaseTests
from goless import backends

test_backends = dict(
    stackless=lambda: 'be_S',
    gevent=lambda: 'be_G',
)


class CalcBackendTests(BaseTests):
    def calc(self, name, testbackends=test_backends):
        return backends.calculate_backend(name, testbackends)

    def test_envvar_chooses_backend(self):
        be = self.calc('gevent')
        self.assertEqual(be, 'be_G')

    def test_invalid_envvar_raises(self):
        with self.assertRaises(RuntimeError):
            self.calc('invalid')

    def test_stackless_is_cpython_default(self):
        self.assertEqual(self.calc(''), 'be_S')

    def test_no_backends_raises(self):
        with self.assertRaises(RuntimeError):
            self.calc('', {})

    def test_no_valid_backends_raises(self):
        def raiseit():
            raise KeyError()

        with self.assertRaises(RuntimeError):
            self.calc('', {'a': raiseit})
