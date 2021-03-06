import unittest
from unittest import TestCase

import fakejson


class ParseArrayTest(TestCase):
    def test(self):
        self.assertEqual(fakejson.loads('["Hi"]'), ['Hi'])


class ParseObjectTest(TestCase):
    def test(self):
        value = """
        {
            "name": "Riley Watkins",
            "power level": 2.1,
            "aliases": ["Jack the Ripper", "O.G. Nice Guy"]
        }
        """
        self.assertEqual(fakejson.loads(value), {
            'name': 'Riley Watkins',
            'power level': 2.1,
            'aliases': ['Jack the Ripper', 'O.G. Nice Guy'],
        })

    def test_empty_object(self):
        self.assertEqual(fakejson.loads('{}'), {})

    def test_extra_data(self):
        try:
            fakejson.loads("{} ,")
        except Exception as e:
            self.assertEqual(str(e), 'Extra data found in input string')
        else:
            self.fail("Expected to get an error")


class ParseBooleanTest(TestCase):
    def test_true(self):
        self.assertEqual(fakejson.loads('{"is on": true}'), {'is on': True})

    def test_false(self):
        self.assertEqual(fakejson.loads('{"is on": false}'), {'is on': False})


class ParseNullTest(TestCase):
    def test_null(self):
        self.assertEqual(fakejson.loads('{"is null": null}'),
                         {'is null': None})


if __name__ == '__main__':
    unittest.main()
