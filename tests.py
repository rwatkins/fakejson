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


if __name__ == '__main__':
    unittest.main()
